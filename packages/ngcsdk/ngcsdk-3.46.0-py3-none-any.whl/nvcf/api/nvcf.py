#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Nvidia Corporation and its affiliates
# (the "Company") and all right, title, and interest in and to the software
# product, including all associated intellectual property rights, are and
# shall remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.
#

from nvcf.api.asset import AssetAPI
from nvcf.api.deploy import DeployAPI
from nvcf.api.function import FunctionAPI

from ngcbpc.api.connection import Connection


class CloudFunctionAPI:  # noqa: D101
    def __init__(self, connection: Connection = None, api_client=None):
        self.connection = connection or Connection()
        self.api_client = api_client

    @property
    def deployments(self):  # noqa: D102
        return DeployAPI(connection=self.connection, api_client=self.api_client)

    @property
    def functions(self):  # noqa: D102
        return FunctionAPI(connection=self.connection, api_client=self.api_client)

    @property
    def assets(self):  # noqa: D102
        return AssetAPI()
