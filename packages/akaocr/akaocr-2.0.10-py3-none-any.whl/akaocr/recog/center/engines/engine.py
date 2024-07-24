# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

import numpy as np
import os


class CTCLabelDecode(object):
    def __init__(self, character_dict_path=None, use_space_char=False):
        # Init vocab & some parameters
        
        self.beg_str = "sos"
        self.end_str = "eos"
        self.reverse = False
        self.character_str = []

        # get vocab path
        work_dir = os.path.dirname(os.path.realpath(__file__))
        if not character_dict_path:
            character_dict_path = os.path.join(work_dir, '../../', "data/vocab.txt")

        # read vocab path
        with open(character_dict_path, "rb") as fin:
            lines = fin.readlines()
            for line in lines:
                line = line.decode('utf-8').strip("\n").strip("\r\n")
                self.character_str.append(line)
    
        # create character dictionary
        if use_space_char:
            self.character_str.append(" ")
        dict_character = list(self.character_str)

        dict_character = self.add_special_char(dict_character)
        self.dict = {}
        for i, char in enumerate(dict_character):
            self.dict[char] = i
        self.character = dict_character


    def add_special_char(self, dict_character):
        # Add blank for CTC decode
        
        dict_character = ['blank'] + dict_character
        return dict_character
    

    def decode(self, text_index, text_prob=None, is_remove_duplicate=False):
        # CTC label decode
        
        result_list = []
        ignored_tokens = [0]
        batch_size = len(text_index)

        for batch_idx in range(batch_size):
            selection = np.ones(len(text_index[batch_idx]), dtype=bool)
            if is_remove_duplicate:
                selection[1:] = text_index[batch_idx][1:] != text_index[
                    batch_idx][:-1]
            for ignored_token in ignored_tokens:
                selection &= text_index[batch_idx] != ignored_token

            char_list = [
                self.character[text_id]
                for text_id in text_index[batch_idx][selection]
            ]
            if text_prob is not None:
                conf_list = text_prob[batch_idx][selection]
            else:
                conf_list = [1] * len(selection)
            if len(conf_list) == 0:
                conf_list = [0]
            text = ''.join(char_list)
            result_list.append((text, np.mean(conf_list).tolist()))

        return result_list


    def __call__(self, preds, label=None, *args, **kwargs):
        # Convert between text-label and text-index

        if isinstance(preds, tuple) or isinstance(preds, list):
            preds = preds[-1]
        preds_idx = preds.argmax(axis=2)
        preds_prob = preds.max(axis=2)
        text = self.decode(preds_idx, preds_prob, is_remove_duplicate=True)
        if label is None:
            return text
        label = self.decode(label)
        
        return text, label