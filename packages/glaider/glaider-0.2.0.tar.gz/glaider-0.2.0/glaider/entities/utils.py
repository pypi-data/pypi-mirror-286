import traceback
from functools import wraps
from typing import Any, Callable, Iterator, List

from glaider.entities.logger import get_logger

logger = get_logger(__name__)


def max_retries(times: int, exceptions: tuple = (Exception,)):
    """
    Max Retry Decorator
    Retries the wrapped function/method `times` times
    :param times: The max number of times to repeat the wrapped function/method
    :type times: int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: List of Exceptions
    """

    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.error(
                        f"Exception '{e}' thrown when running '{func}'"
                        + f"(attempt {attempt} of {times} times)"
                    )
                    attempt += 1
            return func(*args, **kwargs)

        return newfn

    return decorator


class StreamProcessor:
    def __init__(self, stream_processor: Callable) -> None:
        self.stream_processor = stream_processor
        self.cached_streamed_response = []

    def process_stream(self, response: Iterator) -> Iterator:
        for item in self.stream_processor(response):
            self.cached_streamed_response.append(item)
            yield item

    def get_cached_streamed_response(self) -> List[str]:
        return self.cached_streamed_response


def reraise_500(func: Callable) -> Callable:
    """
    Decorator to ensure routes return informative error messages
    when encountering an internal error. Provides a sensible default,
    but will be overwritten if the route provides a specific HTTP exception.

    Always put this decorator as the bottom decorator. Otherwise, the fastapi
    router decorator will overpower it.

    :param func: Callable to be decorated
    :type func: Callable
    :raises HTTPException: If there is any error raise HTTP 500 and log to DataDog
    :return: Decorated callable
    :rtype: Callable
    """

    # stops function signature from being overwritten
    @wraps(func)
    def wrapper(*args: Any, **kwargs: dict) -> None:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # If the route is already raising a specific HTTPException,
            # use it instead of overriding with our 500 code
            if isinstance(e, Exception):
                raise e
            else:
                logger.error(traceback.format_exc())
                raise Exception(f"Internal error due to: {str(e)}")

    return wrapper
