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
from unittest.mock import patch, MagicMock

from msprobe.core.common.log import BaseLogger, logger


class TestLog(TestCase):
    @patch("msprobe.core.common.log.print")
    def test__print_log(self, mock_print):
        logger._print_log("level", "msg")
        self.assertIn("[level] msg", mock_print.call_args[0][0])
        self.assertEqual("\n", mock_print.call_args[1].get("end"))

        logger._print_log("level", "msg", end="end")
        self.assertIn("[level] msg", mock_print.call_args[0][0])
        self.assertEqual("end", mock_print.call_args[1].get("end"))

    @patch.object(BaseLogger, "_print_log")
    def test_print_info_log(self, mock__print_log):
        logger.info("info_msg")
        mock__print_log.assert_called_with("INFO", "info_msg")

    @patch.object(BaseLogger, "_print_log")
    def test_print_warn_log(self, mock__print_log):
        logger.warning("warn_msg")
        mock__print_log.assert_called_with("WARNING", "warn_msg")

    @patch.object(BaseLogger, "_print_log")
    def test_print_error_log(self, mock__print_log):
        logger.error("error_msg")
        mock__print_log.assert_called_with("ERROR", "error_msg")

    @patch.object(BaseLogger, "error")
    def test_error_log_with_exp(self, mock_error):
        with self.assertRaises(Exception) as context:
            logger.error_log_with_exp("msg", Exception("Exception"))
        self.assertEqual(str(context.exception), "Exception")
        mock_error.assert_called_with("msg")

    @patch.object(BaseLogger, "get_rank")
    def test_on_rank_0(self, mock_get_rank):
        mock_func = MagicMock()
        func_rank_0 = logger.on_rank_0(mock_func)

        mock_get_rank.return_value = 1
        func_rank_0()
        mock_func.assert_not_called()

        mock_get_rank.return_value = 0
        func_rank_0()
        mock_func.assert_called()

        mock_func = MagicMock()
        func_rank_0 = logger.on_rank_0(mock_func)
        mock_get_rank.return_value = None
        func_rank_0()
        mock_func.assert_called()

    @patch.object(BaseLogger, "get_rank")
    def test_info_on_rank_0(self, mock_get_rank):
        mock_print = MagicMock()
        with patch("msprobe.core.common.log.print", new=mock_print):
            mock_get_rank.return_value = 0
            logger.info_on_rank_0("msg")
            self.assertIn("[INFO] msg", mock_print.call_args[0][0])

            mock_get_rank.return_value = 1
            logger.info_on_rank_0("msg")
            mock_print.assert_called_once()

    @patch.object(BaseLogger, "get_rank")
    def test_error_on_rank_0(self, mock_get_rank):
        mock_print = MagicMock()
        with patch("msprobe.core.common.log.print", new=mock_print):
            mock_get_rank.return_value = 0
            logger.error_on_rank_0("msg")
            self.assertIn("[ERROR] msg", mock_print.call_args[0][0])

            mock_get_rank.return_value = 1
            logger.error_on_rank_0("msg")
            mock_print.assert_called_once()

    @patch.object(BaseLogger, "get_rank")
    def test_warning_on_rank_0(self, mock_get_rank):
        mock_print = MagicMock()
        with patch("msprobe.core.common.log.print", new=mock_print):
            mock_get_rank.return_value = 0
            logger.warning_on_rank_0("msg")
            self.assertIn("[WARNING] msg", mock_print.call_args[0][0])

            mock_get_rank.return_value = 1
            logger.warning_on_rank_0("msg")
            mock_print.assert_called_once()
