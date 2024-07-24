#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
tiehu parking Class Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_tiehu
=================================================
"""
import hashlib
from datetime import datetime
from typing import Iterable, Callable

from addict import Dict
from guolei_py3_requests import RequestsResponseCallable, requests_request
from requests import Response


class RequestsResponseCallable(RequestsResponseCallable):
    @staticmethod
    def status_code_200_json_addict_status_1(response: Response = None):
        json_addict = RequestsResponseCallable.status_code_200_json_addict(response=response)
        return json_addict.status == 1 or json_addict.status == "1"

    @staticmethod
    def status_code_200_json_addict_status_1_data(response: Response = None):
        if RequestsResponseCallable.status_code_200_json_addict_status_1(response=response):
            return RequestsResponseCallable.status_code_200_json_addict(response=response).Data
        return Dict({})


class Api(object):
    def __init__(
            self,
            base_url: str = "",
            parking_id: str = "",
            app_key: str = "",
    ):
        self._base_url = base_url
        self._parking_id = parking_id
        self._app_key = app_key

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def parking_id(self):
        return self._parking_id

    @parking_id.setter
    def parking_id(self, value):
        self._parking_id = value

    @property
    def app_key(self):
        return self._app_key

    @app_key.setter
    def app_key(self, value):
        self._app_key = value

    def timestamp(self):
        return int(datetime.now().timestamp() * 1000)

    def app_key_md5_upper(self):
        return hashlib.md5(self.app_key.encode('utf-8')).hexdigest().upper()

    def signature(
            self,
            data: dict = {},
    ):
        sign_temp = ""
        data = Dict(data)
        if data.keys():
            data_sorted = sorted(data.keys())
            if isinstance(data_sorted, list):
                sign_temp = "&".join([f"{i}={data[i]}" for i in
                                      data_sorted if
                                      i != "appKey"]) + f"{hashlib.md5(self.app_key.encode('utf-8')).hexdigest().upper()}"
        return hashlib.md5(sign_temp.encode('utf-8')).hexdigest().upper()

    def requests_request_with_json(
            self,
            path: str = "",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_1_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """

        @see https://www.showdoc.com.cn/1735808258920310/9467753400037587
        :param path: example /cxzn/interface/queryPklot
        :param requests_request_kwargs_json: json data
        :param requests_response_callable: guolei_py3_requests.RequestsResponseCallable instance
        :param requests_request_args: guolei_py3_requests.requests_request(*requests_request_args, **requests_request_kwargs)
        :param requests_request_kwargs: guolei_py3_requests.requests_request(*requests_request_args, **requests_request_kwargs)
        :return:
        """
        if not isinstance(path, str):
            raise TypeError(f"path must be type str")
        if not len(path):
            raise ValueError("path must not be empty")
        requests_request_kwargs_json = Dict(requests_request_kwargs_json)
        requests_request_kwargs_json.setdefault("parkingId", self.parking_id)
        requests_request_kwargs_json.setdefault("timestamp", self.timestamp())
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict({
            "url": f"{self.base_url}{path}",
            "method": "POST",
            "json": {
                **requests_request_kwargs_json,
                **requests_request_kwargs.json,
            },
            **requests_request_kwargs,
        })
        requests_request_kwargs.json.sign = self.signature(data=requests_request_kwargs_json)
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )
