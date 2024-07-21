'''
    Validate
'''
import logging

from rlabs_mini_cache.types import LoadedCache

def top_level_fields(
        cache_data: LoadedCache,
        cache_id: str,
        top_level_fields: list[str],
        logger: logging.Logger
    ) -> list[str]:
    '''
        Validate top-level fields
    '''
    corrupted_keys: list[str] = []

    for key, value in cache_data.items():

        for field in top_level_fields:

            if field not in value:
                logger.error(
                    f"Corrupted cache entry in '{cache_id}'. "
                    f"Missing field '{field}' for Key={key}. "
                    f"Recovering by deleting the entry. Next read will continue as a cache miss."
                )
                corrupted_keys.append(key)

    return corrupted_keys
