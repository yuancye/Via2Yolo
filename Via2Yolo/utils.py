import os, json
from pathlib import Path
from typing import List

def create_dir(base_dir: Path, dir_name: str) -> Path:
    path = os.path.join(base_dir, dir_name)
    os.makedirs(path, exist_ok=True)
    return path

def save_to_json(output_path: Path, data: any) -> None:
    with open(output_path, 'w') as output:
        json.dump(data, output)

def save_2darray_to_txt(ouput_path: Path, array_2d: List[List[float]]):
    with open(ouput_path, 'w') as output:
        for row in array_2d:
            list1 =[(str(item) + " ") for item in row]
            output.writelines(list1)
            output.write('\n')
        # output.write('\n'.join([' '.join(i) for i in array_2d]))

def load_json(json_path: Path) -> dict:
    if Path(json_path).is_file(): 
        with open(json_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    return data