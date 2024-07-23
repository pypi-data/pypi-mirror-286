import csv
import os
import shutil
import time
import unittest

import numpy as np
import torch.nn.functional

from msprobe.pytorch.api_accuracy_checker.compare.compare import Comparator
from msprobe.pytorch.api_accuracy_checker.compare.compare_column import CompareColumn
from msprobe.pytorch.api_accuracy_checker.run_ut.run_ut import UtDataInfo

current_time = time.strftime("%Y%m%d%H%M%S")
RESULT_FILE_NAME = "accuracy_checking_result_" + current_time + ".csv"
DETAILS_FILE_NAME = "accuracy_checking_details_" + current_time + '.csv'
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCompare(unittest.TestCase):
    def setUp(self):
        self.output_path = os.path.join(base_dir, "../compare_result")
        os.mkdir(self.output_path, mode=0o750)
        self.result_csv_path = os.path.join(self.output_path, RESULT_FILE_NAME)
        self.details_csv_path = os.path.join(self.output_path, DETAILS_FILE_NAME)
        self.is_continue_run_ut = False
        self.compare = Comparator(self.result_csv_path, self.details_csv_path, self.is_continue_run_ut)

    def tearDown(self) -> None:
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

    def test_compare_dropout(self):
        dummy_input = torch.randn(100, 100)
        bench_out = torch.nn.functional.dropout2d(dummy_input, 0.3)
        npu_out = torch.nn.functional.dropout2d(dummy_input, 0.3)
        self.assertTrue(self.compare._compare_dropout(bench_out, npu_out))

    def test_compare_core_wrapper(self):
        dummy_input = torch.randn(100, 100)
        bench_out, npu_out = dummy_input, dummy_input
        test_final_success, detailed_result_total = self.compare._compare_core_wrapper("api", bench_out, npu_out)
        actual_cosine_similarity = detailed_result_total[0][3]
        # 设置一个小的公差值
        tolerance = 1e-4
        # 判断实际的余弦相似度值是否在预期值的公差范围内
        self.assertTrue(np.isclose(actual_cosine_similarity, 1.0, atol=tolerance))
        # 对其他值进行比较，确保它们符合预期
        detailed_result_total[0][3] = 1.0
        self.assertEqual(detailed_result_total, [['torch.float32', 'torch.float32', (100, 100), 1.0, 0.0, ' ', ' ', ' ',
                                                ' ', 0.0, 0.0, 0, 0.0, 0.0, ' ', ' ', ' ', ' ', ' ', ' ', 'pass', 
                                                '\nMax abs error is less than 0.001, consider as pass, skip other check and set to SPACE.\n']])
        self.assertTrue(test_final_success)

        bench_out, npu_out = [dummy_input, dummy_input], [dummy_input, dummy_input]
        test_final_success, detailed_result_total = self.compare._compare_core_wrapper("api", bench_out, npu_out)
        actual_cosine_similarity = detailed_result_total[0][3]
        self.assertTrue(np.isclose(actual_cosine_similarity, 1.0, atol=tolerance))
        actual_cosine_similarity = detailed_result_total[1][3]
        self.assertTrue(np.isclose(actual_cosine_similarity, 1.0, atol=tolerance))
        detailed_result_total[0][3] = 1.0
        detailed_result_total[1][3] = 1.0
        self.assertTrue(test_final_success)
        self.assertEqual(detailed_result_total, [['torch.float32', 'torch.float32', (100, 100), 1.0, 0.0, ' ', ' ', ' ',
                                                ' ', 0.0, 0.0, 0, 0.0, 0.0, ' ', ' ', ' ', ' ', ' ', ' ', 'pass', 
                                                '\nMax abs error is less than 0.001, consider as pass, skip other check and set to SPACE.\n'], 
                                                 ['torch.float32', 'torch.float32', (100, 100), 1.0, 0.0, ' ', ' ', ' ', 
                                                ' ', 0.0, 0.0, 0, 0.0, 0.0, ' ', ' ', ' ', ' ', ' ', ' ', 'pass', 
                                                '\nMax abs error is less than 0.001, consider as pass, skip other check and set to SPACE.\n']])

    def test_compare_output(self):
        bench_out, npu_out = torch.randn(100, 100), torch.randn(100, 100)
        bench_grad, npu_grad = [torch.randn(100, 100)], [torch.randn(100, 100)]
        api_name = 'Functional.conv2d.0'
        data_info = UtDataInfo(bench_grad, npu_grad, bench_out, npu_out, None, None, None)
        is_fwd_success, is_bwd_success = self.compare.compare_output(api_name, data_info)
        self.assertFalse(is_fwd_success)
        # is_bwd_success should be checked

        dummy_input = torch.randn(100, 100)
        bench_out, npu_out = dummy_input, dummy_input
        data_info = UtDataInfo(None, None, bench_out, npu_out, None, None, None)
        is_fwd_success, is_bwd_success = self.compare.compare_output(api_name, data_info)
        self.assertTrue(is_fwd_success)
        self.assertTrue(is_bwd_success)

    def test_record_results(self):
        args = ('Functional.conv2d.0', False, 'N/A', [['torch.float64', 'torch.float32', (32, 64, 112, 112), 1.0,
                                                       0.012798667686, 'N/A', 0.81631212311, 0.159979121213, 'N/A',
                                                       'error', '\n']], None, 0)
        self.compare.record_results(args)
        with open(self.details_csv_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            api_name_list = [row[0] for row in csv_reader]
        self.assertEqual(api_name_list[0], 'Functional.conv2d.0.forward.output.0')

    def test_compare_torch_tensor(self):
        cpu_output = torch.Tensor([1.0, 2.0, 3.0])
        npu_output = torch.Tensor([1.0, 2.0, 3.0])
        compare_column = CompareColumn()
        status, compare_column, message = self.compare._compare_torch_tensor("api", cpu_output, npu_output,
                                                                             compare_column)
        self.assertEqual(status, "pass")

    def test_compare_bool_tensor(self):
        cpu_output = np.array([True, False, True])
        npu_output = np.array([True, False, True])
        self.assertEqual(self.compare._compare_bool_tensor(cpu_output, npu_output), (0.0, 'pass', ''))

    def test_compare_builtin_type(self):
        compare_column = CompareColumn()
        bench_out = 1
        npu_out = 1
        status, compare_result, message = self.compare._compare_builtin_type(bench_out, npu_out, compare_column)
        self.assertEqual((status, compare_result.error_rate, message), ('pass', 0, ''))

    def test_compare_float_tensor(self):
        cpu_output = torch.Tensor([1.0, 2.0, 3.0])
        npu_output = torch.Tensor([1.0, 2.0, 3.0])
        compare_column = CompareColumn()
        status, compare_column, message = self.compare._compare_float_tensor("api", cpu_output.numpy(),
                                                                             npu_output.numpy(),
                                                                             compare_column, npu_output.dtype)
        self.assertEqual(status, "pass")
