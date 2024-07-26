import inspect
import hashlib
import json

def remove_decorators(source):    
    # Split the source code into lines
    lines = source.splitlines()
    
    # Identify the lines corresponding to decorators
    # Decorators start with @ and appear before the function definition
    func_line_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('@'):
            continue
        else:
            func_line_index = i
            break
    
    # Remove the decorator lines
    stripped_lines = lines[func_line_index:]
    
    # Reconstruct the function's source code
    stripped_source = '\n'.join(stripped_lines)
    
    # Return the reconstructed source code without decorators
    return stripped_source

def get_source_code_hash(func):
    source_code = remove_decorators(inspect.getsource(func))
    hasher = hashlib.sha256()
    hasher.update(source_code.encode('utf-8'))
    hash_digest = hasher.hexdigest()
    return source_code, hash_digest, func.__name__


def get_json_obj_hash(obj):
    serialized_obj = json.dumps(obj).encode('utf-8')
    hasher = hashlib.sha256()
    hasher.update(serialized_obj)
    hash_digest = hasher.hexdigest()
    return hash_digest