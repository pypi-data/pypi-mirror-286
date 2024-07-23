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
from unittest.mock import patch

from msprobe.core.common_config import CommonConfig, BaseConfig
from msprobe.mindspore.debugger.debugger_config import DebuggerConfig
from msprobe.mindspore.dump.kernel_graph_dump import KernelGraphDump
from msprobe.mindspore.task_handler_factory import TaskHandlerFactory


class TestTaskHandlerFactory(TestCase):

    def test_create(self):
        class HandlerFactory:
            def create(self):
                return None

        tasks = {"statistics": HandlerFactory}

        json_config = {
            "task": "statistics",
            "dump_path": "/absolute_path",
            "rank": [],
            "step": [],
            "level": "L2"
        }

        common_config = CommonConfig(json_config)
        task_config = BaseConfig(json_config)
        config = DebuggerConfig(common_config, task_config)

        handler = TaskHandlerFactory.create(config)
        self.assertTrue(isinstance(handler, KernelGraphDump))

        with patch("msprobe.mindspore.task_handler_factory.TaskHandlerFactory.tasks", new=tasks):
            with self.assertRaises(Exception) as context:
                TaskHandlerFactory.create(config)
            self.assertEqual(str(context.exception), "Can not find task handler")

        config.task = "free_benchmark"
        with self.assertRaises(Exception) as context:
            TaskHandlerFactory.create(config)
        self.assertEqual(str(context.exception), "valid task is needed.")
