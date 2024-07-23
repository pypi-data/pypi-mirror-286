#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Copyright (C) 2024-2024. Huawei Technologies Co., Ltd. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
from unittest import TestCase
from unittest.mock import patch, mock_open

from msprobe.core.common.const import Const
from msprobe.mindspore.ms_config import (parse_json_config, parse_task_config,
                                      TensorConfig, StatisticsConfig, OverflowCheck)


class TestMsConfig(TestCase):
    def test_parse_json_config(self):
        mock_json_data = {
            "dump_path": "./dump/",
            "rank": [],
            "step": [],
            "level": "L1",
            "seed": 1234,
            "statistics": {
                "scope": [],
                "list": [],
                "data_mode": ["all"],
                "summary_mode": "statistics"
            }
        }
        with patch("msprobe.mindspore.ms_config.FileOpen", mock_open(read_data='')), \
             patch("msprobe.mindspore.ms_config.json.load", return_value=mock_json_data):
            common_config, task_config = parse_json_config("./config.json")
        self.assertEqual(common_config.task, Const.STATISTICS)
        self.assertEqual(task_config.data_mode, ["all"])

        with self.assertRaises(Exception) as context:
            parse_json_config(None)
        self.assertEqual(str(context.exception), "json file path is None")

    def test_parse_task_config(self):
        mock_json_config = {
            "tensor": None,
            "statistics": None,
            "overflow_check": None,
            "free_benchmark": None
        }

        task_config = parse_task_config("tensor", mock_json_config)
        self.assertTrue(isinstance(task_config, TensorConfig))

        task_config = parse_task_config("statistics", mock_json_config)
        self.assertTrue(isinstance(task_config, StatisticsConfig))

        task_config = parse_task_config("overflow_check", mock_json_config)
        self.assertTrue(isinstance(task_config, OverflowCheck))

        with self.assertRaises(Exception) as context:
            parse_task_config("free_benchmark", mock_json_config)
        self.assertEqual(str(context.exception), "task is invalid.")
