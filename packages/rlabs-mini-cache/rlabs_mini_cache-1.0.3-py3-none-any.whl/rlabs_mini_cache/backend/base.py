'''
    Base class for all cache backends.
'''
import logging
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Type
from logging import getLogger
from typing import ClassVar
from datetime import timedelta
from datetime import datetime
from typing import cast
from enum import Enum
from typing import Optional

from rlabs_mini_cache.error import CacheMissNotFound
from rlabs_mini_cache.error import CacheMissMaxAgeExceeded
from rlabs_mini_cache.error import CacheMissGracefulDegradation
from rlabs_mini_cache.error import SourceReadError
from rlabs_mini_cache import checks
from rlabs_mini_cache.types import ParsedJsonData
from rlabs_mini_cache.types import CacheEntry
from rlabs_mini_cache.types import LoadedCache

class LoadedFrom(Enum):
    '''
        Loaded From Enum
    '''
    LOCAL_MEMORY = 'Local Memory'
    REMOTE_MONGODB = 'Remote MongoDB'

class Backend(ABC):
    '''
        Backend

        Cache file format:

            {
                "data": {
                    # Parsed JSON data
                    ...
                },
                "timestamp": "2021-09-01T12:00:00" # ISO 8601 string
            }
    '''
    logger: ClassVar[logging.Logger] = getLogger("dummy")   # dummy logger to avoid type errors
                                                            # will never be used
    _configured: ClassVar[bool] = False

    @classmethod
    def config(
        cls,
        logger: logging.Logger
    ) -> None:
        '''
            config

            Configures the class logger
        '''
        cls.logger = logger
        cls._configured = True

    def __init__(
            self,
            max_age: timedelta,
            subclass: Type["Backend"],
            read_fn: Optional[Callable[..., ParsedJsonData]] = None,
        ) -> None:
        '''
            Init
        '''
        self.max_age: timedelta = max_age
        self.read_fn: Optional[Callable[..., ParsedJsonData]] = read_fn # None value is permitted during init
                                                                        # but will be checked later


        checks.class_is_configured(
            self.__class__
        )

        self.__class__.logger.debug(
            f"Initializing Cache [{subclass.__name__}]"
        )
        self._cache_init()

    def invalidate(
            self,
        ) -> None:
        '''
            Invalidate cache

            Invalidates the cache
        '''
        self.__check_read_fn()

        self.__class__.logger.debug(
            f"Invalidating Cache"
        )
        self._cache_invalidate()

    def read(
            self,
            key: str
        ) -> ParsedJsonData:
        '''
            Read from backend

            Attempts to read data from cache, if not found reads from source
            and writes to cache.

            Args:
                key: The key to read

            Returns:
                The data read
        '''
        self.__check_read_fn()

        try:
            #
            #  -- Read from cache --
            #
            self.__class__.logger.debug(
                f"Reading from Cache. Key='{key}'"
            )

            timestamp, loaded_from = self._cache_read_timestamp(
                key
            )

            if datetime.now() - timestamp > self.max_age:
                raise CacheMissMaxAgeExceeded(loaded_from.value)

            self.__class__.logger.debug(
                #
                # cache hit is correct to be here because
                # it always reads the timestamp before the data
                # (which means there was no CacheMissNotFound)
                # AND it only get here after checking gto data age
                # (which means there was no CacheMissMaxAgeExceeded)
                #
                f"<< Cache Hit [{loaded_from.value}] >>"
            )

            return self._cache_read_data(
                key
            )
        except (CacheMissNotFound, CacheMissMaxAgeExceeded, CacheMissGracefulDegradation) as e:
            #
            # -- Handle Cache Miss --
            #
            if isinstance(e, CacheMissNotFound):
                self.__class__.logger.debug(
                    "<< Cache Miss: Not Found >>"
                )
            elif isinstance(e, CacheMissMaxAgeExceeded):
                self.__class__.logger.debug(
                    f"<< Cache Miss: Max Age Exceeded [{e.loaded_from}] >>"
                )
            elif isinstance(e, CacheMissGracefulDegradation):
                self.__class__.logger.debug(
                    "<< Cache Miss: Graceful Degradation >>"
                )
                self.__class__.logger.warning(
                    f"Encountered an ERROR while reading from cache: {str(e)}. "
                    f"Carrying on reading from source, but THIS IS NOT NORMAL."
                )
            #
            # Read from source
            #
            try:
                self.__class__.logger.debug(
                    f"Reading from Source"
                )
                self.read_fn = cast(
                    Callable[..., ParsedJsonData],
                    self.read_fn
                )
                data: ParsedJsonData = self.read_fn(
                    key=key
                )
            except Exception as e:

                self.__class__.logger.error(
                    f"Source Read Error: {str(e)}"
                )
                raise SourceReadError(
                    key,
                    str(e)
                ) from e

            #
            # Write to cache
            #
            self.__class__.logger.debug(
                f"Writing to Remote Cache"
            )
            self._cache_write_data(
                key,
                data
            )

            return data

    def write(
            self,
            key: str,
            data: ParsedJsonData
        ) -> None:
        '''
            Write to backend

            Writes data to cache

            Args:
                key: The key to write
                data: The data to write
        '''
        self.__check_read_fn()

        self.__class__.logger.debug(
            f"Writing to Cache. Key='{key}'"
        )

        self._cache_write_data(
            key,
            data
        )

    @abstractmethod
    def _cache_init(
            self
        ) -> None:
        '''
            Cache init

            Backend Base class calls this when the cache is
            initialized.
        '''
        pass

    @abstractmethod
    def _cache_invalidate(
            self
        ) -> None:
        '''
            Cache invalidate

            Backend Base class calls this when the cache is
            invalidated.
        '''
        pass

    @abstractmethod
    def _cache_read_timestamp(
            self,
            key: str
        ) -> tuple[datetime, LoadedFrom]:
        '''
            Cache read timestamp

            Backend Base class calls this when the timestamp
            of the data is requested.

            Args:
                key: The key to read from cache.

            Returns:
                A tuple of:
                    - The timestamp for key 'key' in the cache
                    - How it was loaded (from local or remote)

            Raises:
                - CacheMissNotFound: If the data is not in the cache.
                - CacheMissGracefulDegradation: If there was an error reading the timestamp.
        '''
        pass

    @abstractmethod
    def _cache_read_data(
            self,
            key: str
        ) -> ParsedJsonData:
        '''
            Cache read data

            Backend Base class calls this when data
            is requested.

            Args:
                key: The key to read from cache.
                data: The data to read from cache.

            Returns:
                The data for key 'key' in the cache.

            Raises:
                - CacheMissNotFound: If the data is not in the cache.
                - CacheMissGracefulDegradation: If there was an error reading the data.
        '''
        pass

    @abstractmethod
    def _cache_write_data(
            self,
            key: str,
            data: ParsedJsonData
        ) -> None:
        '''
            Cache write data

            Backend Base class calls to write data to cache after
            reading from source (after a cache miss).

            Args:
                key: The key to write to cache.
                data: The data to write to cache.
        '''
        pass

    def __check_read_fn(
            self
        ) -> None:
        '''
            Check teh param self.read_fn is set

            Raises:
                - ValueError: If self.read_fn is not set.
        '''
        if self.read_fn is None:
            raise ValueError(
                "'read_fn' is not set. Parameter 'read_fn' is permitted to be None during obejct creation, "
                "but must be set before calling 'read', 'write' or 'invalidate' methods."
            )
