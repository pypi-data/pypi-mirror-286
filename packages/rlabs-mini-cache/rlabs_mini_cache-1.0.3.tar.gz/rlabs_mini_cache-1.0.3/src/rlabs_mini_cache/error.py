#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini Cache.
#
# RLabs Mini Cache is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs Mini Cache is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs Mini Cache. If not, see <http://www.gnu.org/licenses/>.
#
'''
    error.py
'''
class PrettyError(Exception):
    '''
        Custom Base Error

        This is the base class for all custom errors

        Pretty Logs error to stdout and exits with -1
    '''
    def __init__(self, msg: str):
        super().__init__(msg)

class ConfigError(PrettyError):
    '''
        ConfigError
    '''
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class MustCallConfigFirstError(PrettyError):
    '''
        MustCallConfigFirstError.
    '''
    def __init__(self, class_name: str) -> None:
        super().__init__(
            f"class '{class_name}' must be configured before use. "
            f"This error occurs when the class 'Cache' is not configured, "
            f"since Cache's config configures {class_name}. \n\n"
            f"Please Call 'Cache.config(...)' first."
        )

class CacheMissNotFound(ValueError):
    '''
        Cache Miss Not Found.
    '''
    pass

class CacheMissMaxAgeExceeded(ValueError):
    '''
        Cache Miss Max Age Exceeded
    '''
    loaded_from: str

    def __init__(self, loaded_from: str) -> None:
        self.loaded_from = loaded_from
        super().__init__()

class CacheFileNotFound(ValueError):
    '''
        Cache File Not Found
    '''
    pass

class CacheMissGracefulDegradation(ValueError):
    '''
        Cache Miss Graceful Degradation
    '''
    pass

class SourceReadError(PrettyError):
    '''
        SourceReadError
    '''
    def __init__(self, key: str, e: str) -> None:
        super().__init__(
            f"Error reading data from source for key '{key}'. Error: {e}"
        )

class FailedToConnectToBackendError(PrettyError):
    '''
        FailedToConnectToBackend
    '''
    def __init__(self, backend: str, e: str) -> None:
        super().__init__(
            f"Failed to connect to backend '{backend}'. Error: {e}"
        )

class MongoDBEntryNotFoundError(ValueError):
    '''
        MongoDBEntryNotFoundError
    '''
    pass

class FailedToDeleteCorruptedKeyError(PrettyError):
    '''
        FailedToDeleteCorruptedKeyError
    '''
    def __init__(self, key: str) -> None:
        super().__init(
            f"Failed to delete corrupted key '{key}'"
        )
