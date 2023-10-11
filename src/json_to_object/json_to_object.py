from dataclasses import dataclass
import json
import os

def generate_python_class(data, name):
    """
    Generate a single class from a dictionary of data
    and a name for the class.
    """
    data_ = {}
    for key, val in data.items():
        data_[key] = type(val).__name__
    
    # Create the class definition code
    class_def = "\nclass " + name + "(BaseModel):\n"
    for key, val in data_.items():
        class_def += "    " + key + ": " + val + "\n"
    
    return class_def

def generate_python_classes(data, root_name="Root"):
    """
    Generate a class definition for each object in the JSON string.
    """
    class_defs = ""
    stack = [(root_name, data)]
    while stack:
        key, value = stack.pop()
        if isinstance(value, dict):
            class_def = generate_python_class(value, key)
            class_defs += class_def + "\n"
            stack.extend([(f'{key}_{k}', v) for k, v in value.items()])
        elif isinstance(value, list):
            stack.extend([(f'{key}_{i}', v) for i, v in enumerate(value)])
    return class_defs


def generate_python_file(json_file_path, root_name="Root", output_file_path=None):
    file_imports = "from __future__ import annotations \n"+\
                   "from pydantic import BaseModel \n"+\
                   "from typing import Optional \n\n"
                      
    output_file_path = output_file_path or os.path.splitext(json_file_path)[0] + ".py"
    with open(json_file_path) as f:
        json_string = f.read()
    class_defs = generate_python_classes(json.loads(json_string), root_name=root_name)
    with open(output_file_path, "w") as f:
        f.write(file_imports)
        f.write(class_defs)
