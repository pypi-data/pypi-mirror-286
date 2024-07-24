"""
Rate limit public interface.

This module includes the decorator used to rate limit function invocations.
Additionally this module includes a naive retry strategy to be used in
conjunction with the rate limit decorator.
"""

import logging
import sys
import threading
import time
from functools import wraps
from math import floor
import traceback
from typing import Any, Callable

from ratelimit.exception import RateLimitException
from ratelimit.utils import now

from .types import ClockCallable

logger = logging.getLogger(__name__)


class RateLimitDecorator(object):
    """
    Rate limit decorator class.
    """

    def __init__(
        self,
        calls: int = 15,
        period: int = 900,
        clock: ClockCallable = now(),
        raise_on_limit: bool = False,
        log_on_limit: bool = True,
        log_message: str | None = None,
        log_trace_depth: int = 3,
        log_trace_pad: int = 0,
    ) -> None:
        """
        Instantiate a RateLimitDecorator with some sensible defaults. By
        default the Twitter rate limiting window is respected (15 calls every
        15 minutes).

        :param int calls: Maximum function invocations allowed within a time period.
        :param float period: An upper bound time period (in seconds) before the rate limit resets.
        :param function clock: An optional function retuning the current time.
        :param bool raise_on_limit: A boolean allowing the caller to avoiding rasing an exception.
        """  # noqa: E501
        self.clamped_calls = max(1, min(sys.maxsize, floor(calls)))
        self.period = period
        self.clock = clock
        self.raise_on_limit = raise_on_limit
        self.log_on_limit = log_on_limit
        self.log_message = log_message
        self.log_trace_depth = log_trace_depth
        self.log_trace_pad = log_trace_pad

        # Initialise the decorator state.
        self.last_reset = clock()
        self.num_calls = 0

        # Add thread safety.
        self.lock = threading.RLock()

    def __call__(self, func: Callable) -> Callable:
        """
        Return a wrapped function that prevents further function invocations if
        previously called within a specified period of time.

        :param function func: The function to decorate.
        :return: Decorated function.
        :rtype: function
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Extend the behaviour of the decorated function, forwarding function
            invocations previously called no sooner than a specified period of
            time. The decorator will raise an exception if the function cannot
            be called so the caller may implement a retry strategy such as an
            exponential backoff.

            :param args: non-keyword variable length argument list to the decorated function.
            :param kargs: keyworded variable length argument list to the decorated function.
            :raises: RateLimitException
            """  # noqa: E501
            with self.lock:
                period_remaining = self.__period_remaining()

                # If the time window has elapsed then reset.
                if period_remaining <= 0:
                    self.num_calls = 0
                    self.last_reset = self.clock()

                # Increase the number of attempts to call the function.
                self.num_calls += 1

                # If the number of attempts to call the function exceeds the
                # maximum then raise an exception.
                if self.num_calls > self.clamped_calls:
                    if self.raise_on_limit:
                        raise RateLimitException("too many calls", period_remaining)

                    elif self.log_on_limit:
                        message = (
                            self.log_message or f"Rate limit exceeded: {func.__name__}"
                        )
                        stack_message = self.__get_stack_message()
                        logger.warning(f"{message}\n{stack_message}")
                    else:
                        return

            return func(*args, **kwargs)

        return wrapper

    def __period_remaining(self) -> float:
        """
        Return the period remaining for the current rate limit window.

        :return: The remaing period.
        :rtype: float
        """
        elapsed = self.clock() - self.last_reset
        return self.period - elapsed

    def __get_stack_message(self) -> str:
        """
        Return the name of the calling function.

        :return: The name of the calling function.
        :rtype: str
        """
        stack = traceback.format_stack()
        return "\n".join(
            stack[
                -(self.log_trace_depth + 2 + self.log_trace_pad) : -2
                - self.log_trace_pad
            ]
        )


def sleep_and_retry(func: Callable) -> Callable:
    """
    Return a wrapped function that rescues rate limit exceptions, sleeping the
    current thread until rate limit resets.

    :param function func: The function to decorate.
    :return: Decorated function.
    :rtype: function
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Call the rate limited function. If the function raises a rate limit
        exception sleep for the remaing time period and retry the function.

        :param args: non-keyword variable length argument list to the decorated function.
        :param kargs: keyworded variable length argument list to the decorated function.
        """  # noqa: E501
        while True:
            try:
                return func(*args, **kwargs)
            except RateLimitException as exception:
                time.sleep(exception.period_remaining)

    return wrapper
