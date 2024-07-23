import os
import stat
import numpy as np

class Const:
    """
    Class for const
    """
    SEP = "."
    REGEX_PREFIX_MAX_LENGTH = 20
    REGEX_PREFIX_PATTERN = r"^[a-zA-Z0-9_-]+$"
    FILE_PATTERN = r'^[a-zA-Z0-9_./-]+$'
    COMMA = ","
    FLOAT_EPSILON = np.finfo(float).eps
    OFF = 'OFF'
    BACKWARD = 'backward'
    FORWARD = 'forward'

    # dump mode
    ALL = "all"
    LIST = "list"
    RANGE = "range"
    STACK = "stack"
    ACL = "acl"
    API_LIST = "api_list"
    API_STACK = "api_stack"
    DUMP_MODE = [ALL, LIST, RANGE, STACK, ACL, API_LIST, API_STACK]
    SUMMARY = "summary"
    MD5 = "md5"
    SUMMARY_MODE = [ALL, SUMMARY, MD5]

    WRITE_FLAGS = os.O_WRONLY | os.O_CREAT
    WRITE_MODES = stat.S_IWUSR | stat.S_IRUSR
    OVERWRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC

    PKL_SUFFIX = ".pkl"
    NUMPY_SUFFIX = ".npy"
    ONE_GB = 1073741824  # 1 * 1024 * 1024 * 1024
    TEN_GB = 10737418240  # 10 * 1024 * 1024 * 1024
    FILE_PATTERN = r'^[a-zA-Z0-9_./-]+$'
    DISTRIBUTED_PREFIX_LENGTH = 60
    # env dump path
    KWARGS = 'kwargs'
    INPUT = 'input'
    OUTPUT = 'output'
    INPUT_ARGS = 'input_args'
    INPUT_KWARGS = 'input_kwargs'
    GRAD_INPUT = 'grad_input'
    GRAD_OUTPUT = 'grad_output'
    START = "start"
    STOP = "stop"
    ENV_ENABLE = "1"
    ENV_DISABLE = "0"
    MAX_SEED_VALUE = 4294967295  # 2**32 - 1
    TASK_LIST = ["tensor", "statistics", "overflow_check", "free_benchmark"]
    LEVEL_LIST = ["L0", "L1", "L2", "mix"]
    STATISTICS = "statistics"
    TENSOR = "tensor"
    OVERFLOW_CHECK = "overflow_check"
    FREE_BENCHMARK = "free_benchmark"
    ATTR_NAME_PREFIX = "wrap_"
    KERNEL_DUMP = "kernel_dump"
    DATA = "data"
    PT_FRAMEWORK = "pytorch"
    MS_FRAMEWORK = "mindspore"
    DIRECTORY_LENGTH = 4096
    FILE_NAME_LENGTH = 255
    FLOAT_TYPE = [np.half, np.single, float, np.double, np.float64, np.longdouble, np.float32, np.float16]
    BOOL_TYPE = [bool, np.uint8]
    INT_TYPE = [np.int32, np.int64]
    NPU = 'NPU'
    DISTRIBUTED = 'Distributed'
    
    INPLACE_LIST = [
        "broadcast", "all_reduce", "reduce", "all_gather", "gather", "scatter", "reduce_scatter",
        "_reduce_scatter_base", "_all_gather_base", "send", "recv", "irecv", "isend", "all_to_all_single"
    ]
    
    CONVERT = {
        "int32_to_int64": ["torch.int32", "torch.int64"],
    }

    CONVERT_API = {
        "int32_to_int64": ["cross_entropy"]
    }

class CompareConst:
    """
    Class for compare module const
    """
    SPACE = " "
    # compare result column name
    NPU_NAME = "NPU Name"
    BENCH_NAME = "Bench Name"
    NPU_DTYPE = "NPU Dtype"
    BENCH_DTYPE = "Bench Dtype"
    NPU_SHAPE = "NPU Tensor Shape"
    BENCH_SHAPE = "Bench Tensor Shape"
    NPU_MAX = "NPU max"
    NPU_MIN = "NPU min"
    NPU_MEAN = "NPU mean"
    NPU_NORM = "NPU l2norm"
    BENCH_MAX = "Bench max"
    BENCH_MIN = "Bench min"
    BENCH_MEAN = "Bench mean"
    BENCH_NORM = "Bench l2norm"
    MAX_DIFF = "Max diff"
    MIN_DIFF = "Min diff"
    MEAN_DIFF = "Mean diff"
    NORM_DIFF = "L2norm diff"
    COSINE = "Cosine"
    MAX_ABS_ERR = "MaxAbsErr"
    MAX_RELATIVE_ERR = "MaxRelativeErr"
    MIN_RELATIVE_ERR = "MinRelativeErr"
    MEAN_RELATIVE_ERR = "MeanRelativeErr"
    NORM_RELATIVE_ERR = "NormRelativeErr"
    ACCURACY = "Accuracy Reached or Not"
    STACK = "NPU_Stack_Info"
    DATA_NAME = "Data_name"
    ERROR_MESSAGE = "Err_message"
    ONE_THOUSANDTH_ERR_RATIO = "One Thousandth Err Ratio"
    FIVE_THOUSANDTHS_ERR_RATIO = "Five Thousandths Err Ratio"
    NPU_MD5 = "NPU MD5"
    BENCH_MD5 = "BENCH MD5"
    RESULT = "Result"

    COMPARE_RESULT_HEADER = [
        NPU_NAME, BENCH_NAME, NPU_DTYPE, BENCH_DTYPE, NPU_SHAPE, BENCH_SHAPE, COSINE, MAX_ABS_ERR, MAX_RELATIVE_ERR,
        ONE_THOUSANDTH_ERR_RATIO, FIVE_THOUSANDTHS_ERR_RATIO,
        NPU_MAX, NPU_MIN, NPU_MEAN, NPU_NORM, BENCH_MAX, BENCH_MIN, BENCH_MEAN, BENCH_NORM, ACCURACY, ERROR_MESSAGE
    ]

    SUMMARY_COMPARE_RESULT_HEADER = [
        NPU_NAME, BENCH_NAME, NPU_DTYPE, BENCH_DTYPE, NPU_SHAPE, BENCH_SHAPE, MAX_DIFF, MIN_DIFF, MEAN_DIFF, NORM_DIFF,
        MAX_RELATIVE_ERR, MIN_RELATIVE_ERR, MEAN_RELATIVE_ERR, NORM_RELATIVE_ERR,
        NPU_MAX, NPU_MIN, NPU_MEAN, NPU_NORM, BENCH_MAX, BENCH_MIN, BENCH_MEAN, BENCH_NORM, RESULT, ERROR_MESSAGE
    ]

    MD5_COMPARE_RESULT_HEADER = [
        NPU_NAME, BENCH_NAME, NPU_DTYPE, BENCH_DTYPE, NPU_SHAPE, BENCH_SHAPE, NPU_MD5, BENCH_MD5, RESULT
    ]

    # compare standard
    HUNDRED_RATIO_THRESHOLD = 0.01
    THOUSAND_RATIO_THRESHOLD = 0.001
    FIVE_THOUSAND_RATIO_THRESHOLD = 0.005
    TEN_THOUSAND_RATIO_THRESHOLD = 0.0001
    COSINE_THRESHOLD = 0.9999
    ULP_FLOAT32_THRESHOLD = 32
    ULP_FLOAT16_THRESHOLD = 1

    # compare result data
    READ_NONE = 'No data'
    NONE = 'None'
    SHAPE_UNMATCH = 'shape unmatched'
    DIFF = 'Different'
    UNSUPPORTED = 'unsupported'
    NAN = 'Nan'
    PASS = 'pass'
    WARNING = 'Warning'
    ERROR = 'error'
    SKIP = 'SKIP'
    BFLOAT16_MIN = -3.3895313892515355e+38
    BFLOAT16_MAX = 3.3895313892515355e+38
    BFLOAT16_EPS = 3.90625e-3  # 2 ** -8

    # accuracy standards
    COS_THRESHOLD = 0.99
    MAX_ABS_ERR_THRESHOLD = 0.001
    COS_MAX_THRESHOLD = 0.9
    MAX_ABS_ERR_MAX_THRESHOLD = 1
    ACCURACY_CHECK_YES = "Yes"
    ACCURACY_CHECK_NO = "No"
    ACCURACY_CHECK_UNMATCH = "Unmatched"

    # error message
    NO_BENCH = "No bench data matched."

    # compare const
    FLOAT_TYPE = [np.half, np.single, float, np.double, np.float64, np.longdouble]

    # highlight xlsx color const
    RED = "FFFF0000"
    YELLOW = "FFFF00"
    BLUE = "0000FF"

    # highlight rules const
    OVERFLOW_LIST = ['nan\t', 'inf\t', '-inf\t', 'nan', 'inf', '-inf']
    MAX_DIFF_RED = 1e+10
    ORDER_MAGNITUDE_DIFF_YELLOW = 1
    ONE_THOUSAND_ERROR_IN_RED = 0.9
    ONE_THOUSAND_ERROR_OUT_RED = 0.6
    ONE_THOUSAND_ERROR_DIFF_YELLOW = 0.1
    COSINE_DIFF_YELLOW = 0.1
    MAX_RELATIVE_OUT_RED = 0.5
    MAX_RELATIVE_OUT_YELLOW = 0.1
    MAX_RELATIVE_IN_YELLOW = 0.01

class FileCheckConst:
    """
    Class for file check const
    """
    READ_ABLE = "read"
    WRITE_ABLE = "write"
    READ_WRITE_ABLE = "read and write"
    DIRECTORY_LENGTH = 4096
    FILE_NAME_LENGTH = 255
    FILE_VALID_PATTERN = r"^[a-zA-Z0-9_.:/-]+$"
    FILE_PATTERN = r'^[a-zA-Z0-9_./-]+$'
    PKL_SUFFIX = ".pkl"
    NUMPY_SUFFIX = ".npy"
    JSON_SUFFIX = ".json"
    PT_SUFFIX = ".pt"
    CSV_SUFFIX = ".csv"
    YAML_SUFFIX = ".yaml"
    MAX_PKL_SIZE = 1073741824  # 1 * 1024 * 1024 * 1024
    MAX_NUMPY_SIZE = 10737418240  # 10 * 1024 * 1024 * 1024
    MAX_JSON_SIZE = 1073741824  # 1 * 1024 * 1024 * 1024
    MAX_PT_SIZE = 10737418240  # 10 * 1024 * 1024 * 1024
    MAX_CSV_SIZE = 1073741824  # 1 * 1024 * 1024 * 1024
    MAX_YAML_SIZE = 1048576  # 10 * 1024 * 1024
    DIR = "dir"
    FILE = "file"
    DATA_DIR_AUTHORITY = 0o750
    DATA_FILE_AUTHORITY = 0o640
    FILE_SIZE_DICT = {
        PKL_SUFFIX: MAX_PKL_SIZE,
        NUMPY_SUFFIX: MAX_NUMPY_SIZE,
        JSON_SUFFIX: MAX_JSON_SIZE,
        PT_SUFFIX: MAX_PT_SIZE,
        CSV_SUFFIX: MAX_CSV_SIZE,
        YAML_SUFFIX: MAX_YAML_SIZE
    }

class OverflowConst:
    """
    Class for Overflow
    """
    OVERFLOW_DEBUG_MODE_ENABLE = "OVERFLOW_DEBUG_MODE_ENABLE"
    OVERFLOW_ORIGINAL_MODE = 0
    OVERFLOW_DEBUG_MODE = 1
