# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

from .operators import *


def transform(data, ops=None):
    # Data transformation

    if ops is None:
        ops = []
    for op in ops:
        data = op(data)
        if data is None:
            return None
    return data


def create_operators(op_param_list, global_config=None):
    # Create operators based on the config

    assert isinstance(op_param_list, list), ('Type error')
    ops = []

    for operator in op_param_list:
        assert isinstance(operator, dict) and len(operator) == 1, "Error config"
        
        op_name = list(operator)[0]
        param = {} if operator[op_name] is None else operator[op_name]

        if global_config is not None:
            param.update(global_config)
        op = eval(op_name)(**param)
        ops.append(op)

    return ops
