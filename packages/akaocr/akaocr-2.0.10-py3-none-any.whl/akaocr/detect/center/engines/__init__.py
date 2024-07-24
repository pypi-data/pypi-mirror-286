# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

import copy
import os
import onnxruntime as ort

from .engine import DetPostProcess

__all__ = ['build_post_process', 'create_predictor']


def build_post_process(config, global_config=None):
    # Build post processing
    
    support_dict = [
        'DetPostProcess'
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

    if device == 'gpu':
        # configure GPU settings
        providers = [
            'CUDAExecutionProvider', 'CPUExecutionProvider'
        ]
    else:
        # configure CPU settings
        providers = ['CPUExecutionProvider']

    return providers


def create_predictor(model_path=None, device='cpu'):
    # Create a predictor for ONNX model inference.

    providers = prepare_inference_session(device)

    # use default model path if none provided or if the provided path does not exist
    if not model_path or not os.path.exists(model_path):
        work_dir = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(work_dir, "../../data/model.onnx")

    # create the ONNX Runtime inference session
    sess = ort.InferenceSession(model_path, providers=providers)

    return sess, sess.get_inputs()[0]
