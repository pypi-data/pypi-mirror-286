# coding=utf-8
import os
import copy
import unittest
import torch
from unittest.mock import patch, DEFAULT
from msprobe.pytorch.api_accuracy_checker.run_ut.run_ut import *
from msprobe.pytorch.api_accuracy_checker.common.utils import get_json_contents

base_dir = os.path.dirname(os.path.realpath(__file__))
forward_file = os.path.join(base_dir, "forward.json")
forward_content = get_json_contents(forward_file)
for api_full_name, api_info_dict in forward_content.items():
    api_full_name = api_full_name
    api_info_dict = api_info_dict


class TestRunUtMethods(unittest.TestCase):
    def test_exec_api(self):
        api_info = copy.deepcopy(api_info_dict)

        [api_type, api_name, _, _] = api_full_name.split(".")
        args, kwargs, need_grad = get_api_info(api_info, api_name, None)
        cpu_args, cpu_kwargs = generate_cpu_params(args, kwargs, True, '')
        out = exec_api(api_type, api_name, cpu_args, cpu_kwargs)
        self.assertEqual(out[0].dtype, torch.float32)
        self.assertTrue(out[0].requires_grad)
        self.assertEqual(out[0].shape, torch.Size([2048, 2, 1, 128]))

    def test_generate_device_params(self):
        mock_tensor = torch.rand([2, 2560, 24, 24], dtype=torch.float32, requires_grad=True)

        with patch.multiple('torch.Tensor',
                            to=DEFAULT,
                            clone=DEFAULT,
                            detach=DEFAULT,
                            requires_grad_=DEFAULT,
                            type_as=DEFAULT,
                            retain_grad=DEFAULT) as mocks:
            mocks['clone'].return_value = mock_tensor
            mocks['detach'].return_value = mock_tensor
            mocks['requires_grad_'].return_value = mock_tensor
            mocks['type_as'].return_value = mock_tensor
            mocks['retain_grad'].return_value = None
            mocks['to'].return_value = mock_tensor

            device_args, device_kwargs = generate_device_params([mock_tensor], {'inplace': False}, True, '')
            self.assertEqual(len(device_args), 1)
            self.assertEqual(device_args[0].dtype, torch.float32)
            self.assertTrue(device_args[0].requires_grad)
            self.assertEqual(device_args[0].shape, torch.Size([2, 2560, 24, 24]))
            self.assertEqual(device_kwargs, {'inplace': False})

    def test_generate_cpu_params(self):
        api_info = copy.deepcopy(api_info_dict)
        [api_type, api_name, _, _] = api_full_name.split(".")
        args, kwargs, need_grad = get_api_info(api_info, api_name, None)
        cpu_args, cpu_kwargs = generate_cpu_params(args, kwargs, True, '')
        self.assertEqual(len(cpu_args), 2)
        self.assertEqual(cpu_args[0].dtype, torch.float32)
        self.assertTrue(cpu_args[0].requires_grad)
        self.assertEqual(cpu_args[0].shape, torch.Size([2048, 2, 1, 256]))
        self.assertEqual(cpu_kwargs, {'dim': -1})

    def test_UtDataInfo(self):
        data_info = UtDataInfo(None, None, None, None, None, None, None)
        self.assertIsNone(data_info.bench_grad)
        self.assertIsNone(data_info.device_grad)
        self.assertIsNone(data_info.device_output)
        self.assertIsNone(data_info.bench_output)
        self.assertIsNone(data_info.grad_in)
        self.assertIsNone(data_info.in_fwd_data_list)
