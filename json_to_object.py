import json

def create_class(data,name):
    # Create a new class with the dictionary keys as attributes
    data_ = {}
    for key,val in data.items():
        if type(val) == dict:
            data_[key] = create_class(val,key)
        else:
            data_[key] = type(val)
            
    cls = type(name, (object,), data_)
    return cls

def create_classes(json_file):
    # Load the JSON file
    with open(json_file) as f:
        data = json.load(f)
    
    # Iterate over the dictionaries in the JSON file and create a class for each one
    classes = []
    stack = [("c",data)]
    while stack:
        key, value = stack.pop()
        if isinstance(value, dict):
            # If the value is a dictionary, create a class for it and add it to the stack
            cls = create_class(value,key)
            #setattr(cls, '__name__', key)
            classes.append(cls)
            stack.extend([(f'{key}.{k}', v) for k, v in value.items()])
        elif isinstance(value, list):
            # If the value is a list, add each element to the stack
            stack.extend([(f'{key}[{i}]', v) for i, v in enumerate(value)])

    return classes
