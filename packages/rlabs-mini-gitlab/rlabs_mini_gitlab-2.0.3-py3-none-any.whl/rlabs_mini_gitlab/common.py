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
    __common.py
'''
from typing import Any
from functools import partial
from rlabs_mini_cache.cache import Cache
from rlabs_mini_api.request import Request
from typing import Optional
from typing import Callable


def __mini_cache_read_fn(exec_fn: Callable, key: str) -> dict | list:
    '''
        Mini Cache Read Fn

        THis is the Read from Source function for Mini Cache.

        'key' is ignored. but is included so it can be used by
        rlabs-mini-cache. Mini Cache will call this function
        as:

        __mini_cache_read_fn(key="some key")

        the 'key' is within the 'request' object, it's
        request.build_url()

        Args:
            - request: request to execute

        Returns:
            - data from the request
    '''
    return exec_fn().python_data

def exec_cached_request(
        request: Request,
        exec_fn: Callable,
        mini_cache: Optional[Cache]
    ) -> dict | list:
    '''
        Execute Cached Request

        Executes a request. If 'mini_cache' is provided, read (execute) the request
        through 'mini_cache'. Else just read from source (execute the request
        directly).

        Args:
            - request: request to execute
    '''

    if mini_cache:
        #  -- Read through mini cache --
        #   mini cache will either read from cache or source

        # set read_fn
        mini_cache.read_fn = partial(
            __mini_cache_read_fn,
            exec_fn=exec_fn # bind request
        )

        # read from cache
        python_data = mini_cache.read(
            key=f"{request._http_method}_{request.build_url()}"
        )

    else:
        # -- Read directly from source --
        python_data = __mini_cache_read_fn(
            exec_fn=exec_fn,
            key=""
        )

    return python_data
