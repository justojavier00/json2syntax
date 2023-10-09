from dataclasses import dataclass
import json
import ast


# This function reduces redundant classs
def contract_classes(s):
    module = ast.parse(s)
    classes = {}
    for cls in module.body:
        if isinstance(cls, ast.ClassDef):
            fields = []
            for dec in cls.decorator_list:
                if isinstance(dec, ast.Name) and dec.id == 'dataclass':
                    for f in cls.body:
                        if isinstance(f, ast.AnnAssign):
                            fields.append((f.target.id, ast.unparse(f.annotation)))
            fields = tuple(fields)
            if fields in classes:
                classes[fields].append(cls.name)
            else:
                classes[fields] = [cls.name]

    res = []
    for fields, names in classes.items():
        res.append('@dataclass')
        res.append(f'class {names[0]}:')
        for name, typ in fields:
            res.append(f'    {name}: {typ}')
        res.append('')

    return '\n'.join(res)

# This function defines a class once a dictionary is found
def create_class(data, name):
    # Create a new class with the dictionary keys as attributes
    data_ = {}
    for key, val in data.items():
        if isinstance(val, dict):
            data_[key] = key
        else:
            data_[key] = type(val).__name__
    
    # Create the class definition code
    class_def = "@dataclass\nclass " + name + ":\n"
    for key, val in data_.items():
        class_def += "    " + key + ": " + val + "\n"
    
    return class_def

# This funtion creates a file json_file_name.py from every json_file_name.json
def create_classes(json_file):
    # Load the JSON file
    with open(json_file) as f:
        data = json.load(f)
    # Iterate over the dictionaries in the JSON file and create a class for each one
    class_defs = ""
    stack = [(json_file[:json_file.index(".json")], data)]
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
    
    class_defs = contract_classes(class_defs)
    f = open(json_file[:json_file.index(".json")]+".py",'w')
    f.write("from dataclasses import dataclass"+"\n\n")
    f.write(class_defs)
    return class_defs

