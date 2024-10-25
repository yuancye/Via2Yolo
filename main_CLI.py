
import os
from via2yolo import extract_dimension, extract_bbox, normalize_bbox
from utils import create_dir

def convert_via_to_yolo(image_dir, image_format, via_project_path, label_dir):

    dimensions = extract_dimension(image_dir, image_format)
    image_bboxs_dict = extract_bbox(via_project_path)
    normalize_bbox(image_bboxs_dict, dimensions, label_dir)

if __name__ == "__main__":
    
    image_format = ['.jpg', '.png']
    via_project_name = 'sheep (3).json'

    image_folder_name = 'images'   
    via_folder_name = 'via_projects'


    label_folder_name = 'labels'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir= create_dir(base_dir, image_folder_name)
    label_dir = create_dir(base_dir, label_folder_name)
    via_dir = create_dir(base_dir, via_folder_name)

    via_project_path = os.path.join(via_dir, via_project_name)

    convert_via_to_yolo(image_dir, image_format, via_project_path, label_dir)