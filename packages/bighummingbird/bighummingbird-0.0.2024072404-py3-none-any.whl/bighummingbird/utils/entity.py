import time
import requests
import json
import inspect
from .constants import MODEL_BASE_URL
from .file import upload_data, get_data_size
from .source_code import get_source_code_hash
from .error_handling import BHBCustomException
from .display_util import green_check, red_check, reset_color

def _get_model_tag(name, hash, project_id, api_key):
    model_tag_response = requests.post(MODEL_BASE_URL + "/tag", json={
        'name': name,
        'hash': hash,
        'projectId': project_id,
    }, headers={'Authorization': f'Bearer {api_key}'})

    if model_tag_response.status_code != 200:
        raise ValueError("Failed to get model tag")

    model_tag_response_body = json.loads(model_tag_response.text)
    model_tag = model_tag_response_body["tag"]
    model_version = model_tag_response_body["version"]
    model_exists_previously = model_tag_response_body["exists"]
    return model_tag, model_version, model_exists_previously

def _upload_model_code(api_key, hash, name, project_id, source_code):
    model_tag, model_version, model_exists_previously = _get_model_tag(name, hash, project_id, api_key)
    model_filename = project_id + "_" + model_tag + ".txt"
    if not model_exists_previously:
        upload_data(model_filename, source_code, api_key)
    return model_tag, model_version, model_filename

def create_model(name, source_code, inputs, outputs, project_id, api_key):
    code, hash_digest, model_name = get_source_code_hash(source_code)
    
    model_tag, model_version, model_filename = _upload_model_code(
        api_key=api_key,
        hash=hash_digest,
        name=name,
        project_id=project_id,
        source_code=code,
    )

    data_size = get_data_size(code)
    model_response = requests.post(MODEL_BASE_URL, json={
        'codeFilename': model_filename,
        'dataSize': data_size,
        'hash': hash_digest,
        'inputs': inputs,
        'modelTag': model_tag,
        "name": model_name,
        'outputs': outputs,
        'projectId': project_id,
        'version': model_version,
    }, headers={'Authorization': f'Bearer {api_key}'})

    if model_response.status_code != 201:
        raise ValueError("Failed to create or fetch model with model tag: " + model_tag)

    return model_tag

def get_input_types(func):
    signature = inspect.signature(func)
    param_types = []
    
    for (param_name, param) in signature.parameters.items():
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
        param_types.append({'name': param_name, 'type': param_type.__name__.lower()})
    
    return param_types
 

def get_type(input):
    if isinstance(input, dict):
        return {key: get_type(value) for key, value in input.items()}
    elif isinstance(input, list):
        return [get_type(item) for item in input]
    else:
        return type(input).__name__

def evaluate_run(func, args, kwargs, scoring_rubric, passing_criteria):
    # run function and get latency
    start = time.perf_counter()
    result = func(*args, **kwargs)
    latency = time.perf_counter() - start

    # evaluate result with judge
    score = scoring_rubric(result)
    if not isinstance(score, (int, float)):
        raise BHBCustomException("scoring_func_invalid_return_type")

    passed = None
    if passing_criteria == None:
        print(f"\r score: {score}", end="", flush=True)
    else:
        passed = passing_criteria(score)
        if not isinstance(passed, bool):
            raise BHBCustomException("passing_func_invalid_return_type")
        if passed:
            print(f"\r{green_check()} score: {score} {reset_color()}", end="", flush=True)
        else:
            print(f"\r{red_check()} score: {score} {reset_color()}", end="", flush=True)

    return (result, latency, score, passed)

def evaluate_dataset_with_no_passing_function(func, dataset, scoring_rubric):
    scores = []
    output_type = None
    for i, row in enumerate(dataset["data"]):
        message = f"Evaluating {dataset['name']} {i}/{len(dataset['data'])}..."
        print(f"\n{message}", end="", flush=True)
        outputs = func(row)
        output_type = get_type(outputs)
        score = scoring_rubric(outputs)
    
        if not isinstance(score, (int, float)):
            raise BHBCustomException("scoring_func_invalid_return_type")
        
        clear_length = len(message)
        score_message = f"\r{dataset['name']}[{i}] score: {score}"
        print(f"\r{score_message}{' ' * (clear_length - len(score_message) + 10)}", end="", flush=True)

        scores.append({
            "output": outputs,
            "score": score,
        })
    return (output_type, scores)

def evaluate_dataset(func, dataset, scoring_rubric, passing_criteria):
    scores = []
    passed_cases = 0
    failed_cases = 0
    output_type = None
    for i, row in enumerate(dataset["data"]):
        message = f"Evaluating {dataset['name']} {i}/{len(dataset['data'])}..."
        clear_length = len(message)
        print(f"\n{message}", end="", flush=True)
        outputs = func(row)
        output_type = get_type(outputs)
        score = scoring_rubric(outputs)

        if not isinstance(score, (int, float)):
            raise BHBCustomException("scoring_func_invalid_return_type")
        
        passed = passing_criteria(score)
        if not isinstance(passed, bool):
            raise BHBCustomException("passing_func_invalid_return_type")
        
        if passed:
            passed_cases += 1
            score_message = f"\r{green_check()} {dataset['name']}[{i}] score: {score} {reset_color()}"
        else:
            failed_cases += 1
            score_message = f"\r{red_check()} {dataset['name']}[{i}] score: {score} {reset_color()}"
        print(f"\r{score_message}{' ' * (clear_length - len(message) + 10)}", end="", flush=True)
        
        scores.append({
            "output": outputs,
            "passed": passed,
            "score": score,
        })
    
    if failed_cases == 0:
        print(f"\n{green_check()} All cases in dataset passed.{reset_color()}")
    else:
        print(f"\n\n{red_check()} {failed_cases} out of {len(dataset['data'])} failed. {reset_color()}")
    return (output_type, scores)