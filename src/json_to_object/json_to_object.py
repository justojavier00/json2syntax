from dataclasses import dataclass
import json

def create_class(data, name):
    # Create a new class with the dictionary keys as attributes
    data_ = {}
    for key, val in data.items():
        if isinstance(val, dict):
            data_[key] = key
        else:
            data_[key] = type(val).__name__
    print(name)
    # Create the class definition code
    class_def = "@dataclass\nclass " + name + ":\n"
    for key, val in data_.items():
        class_def += "    " + key + ": " + val + "\n"
    
    return class_def

def create_classes(data):
    
    # Iterate over the dictionaries in the JSON file and create a class for each one
    class_defs = ""
    stack = [("MainClass", data)]
    while stack:
        key, value = stack.pop()
        if isinstance(value, dict):
            # If the value is a dictionary, create a class for it and add it to the stack
            class_def = create_class(value, key)
            class_defs += class_def + "\n"
            stack.extend([(f'{k}', v) for k, v in value.items()])
        elif isinstance(value, list):
            # If the value is a list, add each element to the stack
            stack.extend([(f'{key}{i}', v) for i, v in enumerate(value)])
    return class_defs
