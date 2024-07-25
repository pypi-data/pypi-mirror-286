import numpy as np
from PIL import Image
from typing import List

from dingo.model.model import Model
from dingo.model.rule.base import ResModel, BaseRule
from dingo.model.rule.util import *

try:
    import torch
except ModuleNotFoundError as e:
    raise ModuleNotFoundError("You need to install `torch`, try `pip install torch`")
try:
    import pyiqa
except ModuleNotFoundError as e:
    raise ModuleNotFoundError("You need to install `pyiqa`, try `pip install pyiqa`")

@Model.rule_register('QUALITY_SIGNAL_EFFECTIVENESS', [])
class ImageValid(BaseRule):
    """check whether image is not all white or black"""
    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        res = ResModel()
        img = Image.open(input_data[0])
        img_new = img.convert("RGB")
        img_np = np.asarray(img_new)
        if np.all(img_np == (255, 255, 255)) or np.all(img_np == (0, 0, 0)):
            res.error_status = True
            res.error_reason = 'Image is not valid: all white or black'
        img.close()
        img_new.close()
        return res

@Model.rule_register('QUALITY_SIGNAL_EFFECTIVENESS', [])
class ImageSizeValid(BaseRule):
    """check whether image ratio of width to height is valid"""
    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        res = ResModel()
        img = Image.open(input_data[0])
        width, height = img.size
        aspect_ratio = width / height
        if aspect_ratio > 4 or aspect_ratio < 0.25:
            res.error_status = True
            res.error_reason = 'Image size is not valid, the ratio of width to height: ' + str(aspect_ratio)
        img.close()
        return res

@Model.rule_register('QUALITY_SIGNAL_EFFECTIVENESS', [])
class ImageQuality(BaseRule):
    """check whether image quality is good."""
    threshold = 5.5

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        res = ResModel()
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        iqa_metric = pyiqa.create_metric('nima', device=device)
        score_fr = iqa_metric(input_data[0])
        score = score_fr.item()
        print(score)
        if score < cls.threshold:
            res.error_status = True
            res.error_reason = 'Image quality is not satisfied, ratio: ' + str(score)
        return res

# @Model.rule_register('QUALITY_SIGNAL_SECURITY', [])
# class ImageQRCode(BaseRule):
#     """check whether image contains QR code."""
#     @classmethod
#     def eval(cls, input_data: List[str]) -> ResModel:
#         res = ResModel()
#         img = cv2.imread(input_data[0])
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         scanner = zbar.Scanner()
#         tmp = scanner.scan(gray)
#         if len(tmp) != 0:
#             if tmp[0].type == 'QR-Code':
#                 res.error_status = True
#                 res.error_reason = tmp[0].data
#         return res
