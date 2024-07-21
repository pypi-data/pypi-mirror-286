'''
    Cache
'''
import logging
from pathlib import Path
from typing import ClassVar, Optional, Type, cast

from rlabs_mini_cache import logger
from rlabs_mini_cache.backend.memory import Memory
from rlabs_mini_cache.backend.base import Backend
from rlabs_mini_cache.backend.file import File
from rlabs_mini_cache.backend.mongodb import MongoDB

class Cache:
    '''
        Cache
    '''
    log_level: ClassVar[Optional[int]]
    logger: ClassVar[logging.Logger]

    Memory: ClassVar[Type[Backend]] = Memory
    File: ClassVar[Type[Backend]] = File
    MongoDB: ClassVar[Type[Backend]] = MongoDB

    def __init__(self) -> None:
        '''
            __init__
        '''
        pass

    @classmethod
    def config(
        cls,
        log_level: Optional[int] = None,
        logger_override: Optional[logging.Logger] = None
    ) -> None:
        '''
            config

            Configures the Cache class.
        '''
        # Set up logging
        if log_level and logger_override:
            raise ValueError(
                "log_level and logger_override are mutually exclusive. "
                "Please provide one or the other."
            )

        if not log_level and not logger_override:
            raise ValueError(
                "log_level or logger_override must be provided."
            )

        if logger_override:
            cls.logger = logger_override
            cls.log_level = logger_override.getEffectiveLevel()
        else:
            cls.logger = logger.stdout(
                __name__,
                cast(
                    int,
                    log_level
                )
            )
            cls.log_level = log_level

        logger.enable_pretty_tracebacks()

        #
        # configure all Backends
        #
        Backend.config(
            logger=cls.logger
        )
