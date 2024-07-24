# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

import onnxruntime as ort
import os
import copy

from .engine import CTCLabelDecode
from .utility import resize_image


__all__ = ['build_post_process', 'create_predictor', 'resize_image']


def build_post_process(config, global_config=None):
    # Post-processing for recognition model

    support_dict = [
        'CTCLabelDecode'
    ]
    config = copy.deepcopy(config)
    module_name = config.pop('name')

    if global_config is not None:
        config.update(global_config)
    assert module_name in support_dict, Exception(
        'Post process only support {}'.format(support_dict))
    module_class = eval(module_name)(**config)

    return module_class


def prepare_inference_session(device='cpu'):
    # Create session options

    so = ort.SessionOptions()
    so.intra_op_num_threads = 4
    so.inter_op_num_threads = 2
    so.execution_mode = ort.ExecutionMode.ORT_PARALLEL
    
    if device == 'gpu':
        # configure GPU settings
        providers = [
            'CUDAExecutionProvider', 'CPUExecutionProvider'
        ]
    else:
        # configure CPU settings
        so.enable_cpu_mem_arena = True
        providers = ['CPUExecutionProvider']

    return so, providers


def create_predictor(model_path=None, device='cpu'):
    # Create a predictor for ONNX model inference.

    so, providers = prepare_inference_session(device)

    # use default model path if none provided or if the provided path does not exist
    if not model_path or not os.path.exists(model_path):
        work_dir = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(work_dir, "../../data/model.onnx")

    # create the ONNX Runtime inference session
    sess = ort.InferenceSession(model_path, sess_options=so, providers=providers)

    return sess, sess.get_inputs()[0], None
