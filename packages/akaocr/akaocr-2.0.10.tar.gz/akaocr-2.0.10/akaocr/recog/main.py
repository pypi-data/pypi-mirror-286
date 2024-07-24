# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

import os, traceback
import numpy as np
os.environ["FLAGS_allocator_strategy"] = 'auto_growth'

from akaocr.recog.center.engines import create_predictor
from akaocr.recog.center.engines import build_post_process
from akaocr.recog.center.engines import resize_image

SUPPORTED_LANG = ['eng']


class Recognizor(object):
    def __init__(self, model_path=None, vocab_path=None, 
                use_space_char=True, model_shape=None, 
                max_wh_ratio=None, device='cpu'):

        # init parameters
        self.rec_image_shape = model_shape
        self.max_wh_ratio = max_wh_ratio
        self.model_path = model_path
        self.vocab_path = vocab_path
        self.use_space_char = use_space_char
        self.rec_batch_num = 32
        self.predictor, self.input_tensor, self.output_tensors = create_predictor(model_path, device)

        # for post-processing
        postprocess_params = {
            'name': 'CTCLabelDecode',
            "character_dict_path": self.vocab_path,
            "use_space_char": self.use_space_char
        }
        self.postprocess_op = build_post_process(postprocess_params)


    def __call__(self, img_list):
        """Text recognition pipeline (supported for English)
        Args:
            org_img_list (list): list of images
        Returns:
            list(tuple): (text, text confidence)
        """
        # calculate the aspect ratio of all text bars
        img_num = len(img_list)
        width_list = []
        for img in img_list:
            width_list.append(img.shape[1] / float(img.shape[0]))

        # sorting can speed up the recognition process
        indices = np.argsort(np.array(width_list))
        rec_res = [['', 0.0]] * img_num
        batch_num = self.rec_batch_num
        _, img_h, img_w = self.rec_image_shape[:3]

        for beg_img_no in range(0, img_num, batch_num):
            end_img_no = min(img_num, beg_img_no + batch_num)
            norm_img_batch = []
            max_wh_ratio = img_w / img_h

            # calculate max_wh_ratio of batch
            for ino in range(beg_img_no, end_img_no):
                h, w = img_list[indices[ino]].shape[0:2]
                wh_ratio = w * 1.0 / h
                max_wh_ratio = max(max_wh_ratio, wh_ratio)

            # update max_ratio
            if self.max_wh_ratio != None:
                max_wh_ratio = min(10, self.max_wh_ratio)

            # create a batch of images
            for ino in range(beg_img_no, end_img_no):
                norm_img = resize_image(img_list[indices[ino]],
                                        self.rec_image_shape,
                                        max_wh_ratio)
                norm_img = norm_img[np.newaxis, :]
                norm_img_batch.append(norm_img)
               
            norm_img_batch = np.concatenate(norm_img_batch)
            norm_img_batch = norm_img_batch.copy()

            # infder with batch
            input_dict = {}
            input_dict[self.input_tensor.name] = norm_img_batch
            outputs = self.predictor.run(self.output_tensors, input_dict)
            preds = outputs[0]
                
            rec_result = self.postprocess_op(preds)
            for rno in range(len(rec_result)):
                rec_res[indices[beg_img_no + rno]] = rec_result[rno]

        return rec_res


class TextEngine():
    def __init__(self, model_path=None,
                vocab_path=None, 
                use_space_char=True,
                model_shape=[3, 48, 320],
                max_wh_ratio=None,
                device='cpu') -> None:
        
        self.text_recognizer = Recognizor(
            model_path, vocab_path, use_space_char, model_shape, max_wh_ratio, device)


    def __call__(self, image):
        # Text recogntion pipeline

        rec_res = None
        try:
            if isinstance(image, list):
                rec_res = self.text_recognizer(image)
            else:    
                rec_res = self.text_recognizer([image])
        except Exception:
            print(traceback.format_exc())

        return rec_res