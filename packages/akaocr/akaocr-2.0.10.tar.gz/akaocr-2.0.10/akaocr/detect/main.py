# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

import numpy as np
import traceback

from akaocr.detect.center.engines import create_predictor
from akaocr.detect.center.engines import build_post_process
from akaocr.detect.center.data import create_operators
from akaocr.detect.center.data import transform
from scipy.spatial import distance as dist
from concurrent.futures import ThreadPoolExecutor


class Detector(object):
    def __init__(self, model_path=None, 
                 side_len=960, 
                 conf_thres=0.5, 
                 mask_thes=0.4,
                 unclip_ratio=2.0,
                 max_candidates=1000,
                 device='cpu'):
        # Initialize parameters
        self.conf_thres = conf_thres
        self.output_tensors = None

        # Build pre-processing operations
        pre_process_list = [
            {'DetResize': {'limit_side_len': side_len, 'limit_type': 'min'}}, 
            {'NormalizeImage': {'std': [0.229, 0.224, 0.225], 
                                'mean': [0.485, 0.456, 0.406], 
                                'scale': '1./255.', 'order': 'hwc'}},
            {'ToCHWImage': None}, 
            {'KeepKeys': {'keep_keys': ['image', 'shape']}}
        ]
        self.preprocess_op = create_operators(pre_process_list)

        # Build post-processing operations
        postprocess_params = {
            'name': 'DetPostProcess',
            'thresh': mask_thes,
            'box_thresh': conf_thres,
            'max_candidates': max_candidates,
            'unclip_ratio': unclip_ratio,
            'use_dilation': False
        }
        self.postprocess_op = build_post_process(postprocess_params)

        # Create predictor
        self.predictor, self.input_tensor = create_predictor(model_path, device)


    def order_points_clockwise(self, pts):
        # Order points (4 points) clockwise

        x_sorted = pts[np.argsort(pts[:, 0]), :]
        left_most = x_sorted[:2, :]
        right_most = x_sorted[2:, :]
        
        # get top-left & bottom-left points
        left_most = left_most[np.argsort(left_most[:, 1]), :]
        (tl, bl) = left_most
        
        # get bottom-right & top-right points
        D = dist.cdist(tl[np.newaxis], right_most, "euclidean")[0]
        (br, tr) = right_most[np.argsort(D)[::-1], :]
        
        return np.array([tl, tr, br, bl], dtype="float32")


    def clip_det_res(self, points, img_height, img_width):
        # Clip detection results

        for pno in range(points.shape[0]):
            points[pno, 0] = int(min(max(points[pno, 0], 0), img_width - 1))
            points[pno, 1] = int(min(max(points[pno, 1], 0), img_height - 1))

        return points


    def filter_det_res(self, dt_boxes, image_shape):
        # Filter tag detection results

        img_height, img_width = image_shape[0:2]

        def process_box(box):
            box = self.order_points_clockwise(box)
            box = self.clip_det_res(box, img_height, img_width)
            
            rect_width = int(np.linalg.norm(box[0] - box[1]))
            rect_height = int(np.linalg.norm(box[0] - box[3]))
            if rect_width <= 3 or rect_height <= 3:
                return None
            return box

        dt_boxes_new = []
        
        with ThreadPoolExecutor() as executor:
            results = executor.map(process_box, dt_boxes)
        
        for result in results:
            if result is not None:
                dt_boxes_new.append(result)
        
        return dt_boxes_new


    def __call__(self, ori_image):
        # Inference for text detection

        image = ori_image.copy()
        data = {'image': image}

        # transform image
        image, shape_list = transform(data, self.preprocess_op)
        image = np.expand_dims(image, axis=0)
        shape_list = np.expand_dims(shape_list, axis=0)

        # inference model
        input_dict = {}
        input_dict[self.input_tensor.name] = image
        outputs = self.predictor.run(self.output_tensors, input_dict)
       
        # post-processing
        preds = dict()
        preds['maps'] = outputs[0]
        dt_boxes = self.postprocess_op(preds, shape_list)
        dt_boxes = self.filter_det_res(dt_boxes, ori_image.shape)
      
        return dt_boxes


class BoxEngine():
    def __init__(self, model_path=None, 
                 side_len=960, 
                 conf_thres=0.5, 
                 mask_thes=0.4,
                 unclip_ratio=2.0,
                 max_candidates=1000,
                 device='cpu'):
        # Init some parameters

        self.text_detector = Detector(
            model_path, side_len, 
            conf_thres, mask_thes, 
            unclip_ratio, 
            max_candidates, device)

    def __call__(self, image):
        # Text Detection Pipeline
        
        det_res = None
        try:
            det_res = self.text_detector(image)
        except Exception:
            print(traceback.format_exc())

        return det_res