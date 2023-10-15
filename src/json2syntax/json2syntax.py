import json
import os

def consistent_class_name(data, *, optional, data_id=None, names=None, dict_ids=None):
    data_id = data_id or id(data)
    if isinstance(data, dict):
        if data_id in dict_ids:
            class_names = list(set(consistent_class_name(d, optional=optional, names={}) for d in data.values()))
            if len(class_names) == 0:
                inner_class = "Dict"
            elif len(class_names) == 1:
                inner_class = "Dict[str, " + class_names[0] + "]"
            else:
                inner_class = "Dict[str, Union[" + ", ".join(class_names) + "]]"
        elif names and data_id in names:
            inner_class = names[data_id]
        else:
            inner_class = f"C{id(data)}"
    elif isinstance(data, list):
        class_names = list(set(consistent_class_name(d, optional=optional, names={}) for d in data))
        if len(class_names) == 0:
            inner_class = "List"
        elif len(class_names) == 1:
            inner_class = "List[" + class_names[0] + "]"
        else:
            inner_class = "List[Union[" + ", ".join(class_names) + "]]"
    else:
        inner_class = type(data).__name__
    return "Optional[" + inner_class + "]" if (optional and inner_class != 'NoneType') else inner_class

class ClassDef:
    def __init__(self, data):
        self.data = data
        self.data_id = id(data)

    def merge(self, other):
        if other is None: return self
        for k, v in other.data.items():
            if k in self.data and v is None: continue
            self.data[k] = v
        return self

    def code(self, names=None, dict_ids=None):
        code = "\nclass " + consistent_class_name(self.data, optional=False, data_id=self.data_id, names=names, dict_ids=dict_ids) + "(BaseModel):\n"
        for key, val in self.data.items():
            code += "    " + key + ": " + consistent_class_name(val, optional=True, names=names, dict_ids=dict_ids) + " = None\n"
        return code

def generate_python_classes(data, path_to_name=lambda _: None, path_is_dict=lambda _: False):
    """
    Generate a class definition for each object in the JSON string.
    """
    code = "from pydantic import BaseModel \n"+\
           "from typing import Optional \n"+\
           "from __future__ import annotations \n"
    class_defs = {}
    class_names = {}
    dict_ids = set()
    stack = [([], data)]
    while stack:
        path, value = stack.pop()
        if isinstance(value, dict):
            if path and path_is_dict(path):
                dict_ids.add(id(value))
                stack.extend([(path + [k], v) for k, v in value.items()])
            else:
                class_def = ClassDef(value)
                name = path_to_name(path) or consistent_class_name(value, optional=False, data_id=class_def.data_id, names=class_names, dict_ids=dict_ids)
                class_names[class_def.data_id] = name
                class_defs[name] = class_def.merge(class_defs.get(name))
                stack.extend([(path + [k], v) for k, v in value.items()])
        elif isinstance(value, list):
            stack.extend([(path + [i], v) for i, v in enumerate(value)])
    code += "\n".join(class_def.code(names=class_names, dict_ids=dict_ids) for class_def in class_defs.values())
    return code

def generate_python_file(json_file_path, output_file_path=None):
    output_file_path = output_file_path or os.path.splitext(json_file_path)[0] + ".py"
    with open(json_file_path) as f:
        json_string = f.read()
    class_defs = generate_python_classes(json.loads(json_string))
    with open(output_file_path, "w") as f:
        f.write(class_defs)

