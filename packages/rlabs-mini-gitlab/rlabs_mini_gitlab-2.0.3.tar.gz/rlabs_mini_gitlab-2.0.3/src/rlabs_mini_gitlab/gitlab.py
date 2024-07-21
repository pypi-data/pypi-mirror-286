#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini Gitlab.
#
# RLabs Mini Gitlab is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs Mini Gitlab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs Mini Gitlab. If not, see <http://www.gnu.org/licenses/>.
#
'''
    Gitlab
'''
from typing import Optional
from typing import cast
from typing import ClassVar
from pathlib import Path
from typing import Type
from typing import Any
from typing import Dict
from typing import override
from rlabs_mini_api.response import Response
from rlabs_mini_api.request import Request
from rlabs_mini_cache.cache import Cache
from rlabs_mini_box.data import Box
import logging

from rlabs_mini_gitlab import logger
from rlabs_mini_gitlab.error import ConfigError
from rlabs_mini_gitlab import common

class GitlabRequest(Request):
    '''
        Gitlab Request

        Custom methods to add functionality
        (fetch all pages, etc.) to the original
        from Mini API's Request class
    '''
    @override
    def exec(self, fetch_all: bool = False) -> Box:

        match fetch_all:
            case True:
                return fetch_all_pages(
                    self
                )
            case False:
                return Box(
                        common.exec_cached_request(
                        self,
                        super().exec,
                        Gitlab.mini_cache
                    )
                )


class GitlabRequestMeta(type):
    '''
        Gitlab Request Meta

        (custom Request, different from Mini API's Reques)
    '''
    def __getattr__(cls, path_part: str) -> 'Request':
        return GitlabRequest(cls._http_method).__append_path(path_part) # type: ignore

    def __call__(cls, *args: Any, **kwargs: Any) -> 'Request':
        return GitlabRequest(cls._http_method, *args, **kwargs) # type: ignore

class GITLAB_GET(metaclass=GitlabRequestMeta):
    '''
        GET
        (custom Metaclass, different from Mini API's RequestMeta)
    '''
    _http_method: str = 'GET'

class GITLAB_DELETE(metaclass=GitlabRequestMeta):
    '''
        DELETE
        (custom Metaclass, different from Mini API's RequestMeta)
    '''
    _http_method: str = 'DELETE'

class GITLAB_POST(metaclass=GitlabRequestMeta):
    '''
        POST
        (custom Metaclass, different from Mini API's RequestMeta)
    '''
    _http_method: str = 'POST'

    def __call__(
        cls,
        data: Optional[Dict[str, Any]] = None,
        *args: Any,
        **kwargs: Any
    ) -> Request:

        return Request(
            cls._http_method,
            data
        )

class GITLAB_PUT(metaclass=GitlabRequestMeta):
    '''
        PUT
        (custom Metaclass, different from Mini API's RequestMeta)
    '''
    _http_method: str = 'PUT'

    def __call__(
        cls,
        data: Optional[Dict[str, Any]] = None,
        content: Optional[bytes] = None,
        *args: Any,
        **kwargs: Any
    ) -> Request:

        return Request(
            cls._http_method,
            data
        )

class Gitlab:
    '''
        Gitlab
    '''
    mini_cache: ClassVar[Optional[Cache]] = None
    log_level: ClassVar[Optional[int]] = None
    logger: ClassVar[logging.Logger]
    response_log_dir: ClassVar[Optional[Path]] = None

    #
    # make all methods available to the user
    #
    GET: ClassVar[Type[GITLAB_GET]] = GITLAB_GET            # type: ignore
    POST: ClassVar[Type[GITLAB_POST]] = GITLAB_POST         # type: ignore
    PUT: ClassVar[Type[GITLAB_PUT]] = GITLAB_PUT            # type: ignore
    DELETE: ClassVar[Type[GITLAB_DELETE]] = GITLAB_DELETE   # type: ignore

    def __init__(self) -> None:
        '''
            __init__
        '''
        pass

    @staticmethod
    def config(
        gitlab_url: str,
        gitlab_token: str,
        requests_general_timeout: Optional[float] = 7.0,
        mini_cache: Optional[Cache] = None,
        log_level: Optional[int] = None,
        logger_override: Optional[logging.Logger] = None,
        response_log_dir: Optional[Path] = None
    ) -> None:
        '''
            config

            Configures the Gitlab class.
        '''
        Gitlab.mini_cache = mini_cache
        Gitlab.log_level = log_level
        Gitlab.response_log_dir = response_log_dir

        if response_log_dir is not None and not isinstance(response_log_dir, Path):
            raise ConfigError(
                "'response_log_dir' must be of type Path"
            )

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
            Gitlab.logger = logger_override
            Gitlab.log_level = logger_override.getEffectiveLevel()
        else:
            Gitlab.logger = logger.stdout(
                __name__,
                cast(
                    int,
                    log_level
                )
            )
            Gitlab.log_level = log_level

        logger.enable_pretty_tracebacks()

        Request.config(
            base_url=gitlab_url,
            headers={
                "PRIVATE-TOKEN": gitlab_token
            },
            retries=3,
            retry_base_delay=0.5,
            general_timeout=requests_general_timeout,
            logger_override=Gitlab.logger,
            response_log_dir=Gitlab.response_log_dir
        )

def fetch_all_pages(
    request: GitlabRequest
) -> Box:
    '''
        Fetch All Pages

        Asks Gitlabs for all pages of data

        Args:
            - exec_fn: function to execute the request
            - per_page: size of the page to ask in every request

        Returns:
            - Box of all the aggreageted data from all pages
    '''
    collected: list = []
    page = 1

    while True:

        #
        # edit query param
        # to include 'page'
        #
        # (override whatever the user had in there, if any)
        #
        # this is how they look:
        #
        #   [{"key1": "value1"}, {"key2": "value2"}]
        #
        page_edited = False

        for param_dict in request._params:
            for key, _ in param_dict.items():
                if key == 'page':
                    param_dict[key] = page
                    page_edited = True
                    break

        if not page_edited:
            request._params.append(
                {
                    'page': page
                }
            )

        python_data = request.exec().data()

        if not python_data:
            break

        collected += python_data
        page += 1

    return Box(collected)
