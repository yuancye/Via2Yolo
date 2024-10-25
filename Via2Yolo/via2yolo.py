
import os
import cv2
from utils import save_2darray_to_txt, save_to_json, load_json
from typing import Dict, List
from pathlib import Path


def extract_dimension(image_folder_path: Path, image_format: List[str]) ->Dict:
    dimensions = dict()
    for root, folder, images in os.walk(image_folder_path):
        for image in images:
            ext = os.path.splitext(image)[1]
            print(ext)
            if ext in image_format:
                image_path = os.path.join(root, image)
                img = cv2.imread(image_path)
                h, w, c = img.shape
                dimensions.update({image: {'width' : w, 'height' : h}})
    return dimensions

def extract_bbox(via_project_path: Path) ->Dict:
    via_data = load_json(via_project_path)
    via_img_metadata = via_data['_via_img_metadata']
    image_bboxs_dict = dict()
    for key, value in via_img_metadata.items():
        filename = value['filename']
        regions = value['regions']
        bboxs = []
        for region in regions:
            shape_attributes = region['shape_attributes']   
            if 'width' in shape_attributes:        
                w = shape_attributes['width']
                h = shape_attributes['height']
                x_c = (shape_attributes['x']) + w/2
                y_c = (shape_attributes['y']) + h/2
                bbox = [x_c, y_c, w, h]
                bboxs.append(bbox)

        if bboxs:
            image_bboxs_dict.update({filename : bboxs})
    # directory = os.path.dirname(via_project_path)
    # output_name = os.path.join(directory, 'bboxs.json')
    # save_to_json(output_name, image_bboxs_dict)
    return image_bboxs_dict

def normalize_bbox(image_bboxs_dict: Dict, dimensions: Dict, output_txt_folder_path: Path) ->None:
    for key, bboxs in image_bboxs_dict.items():
        if key in dimensions:
            output_txt_name = os.path.splitext(key)[0] + '.txt'
            output_txt_path = os.path.join(output_txt_folder_path, output_txt_name)
            
            bboxs_norm = []
            for bbox in bboxs:                   
                x_center = round(bbox[0] / dimensions[key]['width'], 3)
                x_center = '{:.3f}'.format(x_center) if x_center > 0 else str(0.000)
                y_center = round(bbox[1] / dimensions[key]['height'], 3)
                y_center = '{:.3f}'.format(y_center) if y_center > 0 else str(0.000)
                width = round(bbox[2] / dimensions[key]['width'], 3)
                if  width > 0:
                    width = '{:.3f}'.format(width)
                else:
                    break
                height = round(bbox[3] / dimensions[key]['height'], 3)
                if  height > 0:
                    height = '{:.3f}'.format(height)
                else:
                    break
                bbox_norm = [str(0), x_center, y_center, width, height]
                bboxs_norm.append(bbox_norm)
            save_2darray_to_txt(output_txt_path, bboxs_norm)


