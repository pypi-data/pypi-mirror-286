import time
import json
import requests
from .utils.display_util import clear_line, green_check, red_check, reset_color, bold, reset_font, right_angle, orange
import time
from urllib.parse import quote
from .apis.workspace import initialize_workspace, select_workspace
from .apis.project import initialize_project, select_project

from .utils.source_code import get_source_code_hash, get_json_obj_hash
from .utils.constants import BASE_CLIENT_URL, PROJECT_BASE_URL, RUN_BASE_URL, DATASET_BASE_URL, JUDGE_BASE_URL, EVALUATION_BASE_URL
from .utils.file import upload_data, download_data, read_source_code_as_func, get_data_size
from .utils.entity import create_model, get_type, get_input_types, evaluate_run, evaluate_dataset, evaluate_dataset_with_no_passing_function
from .utils.error_handling import BHBCustomException

class BigHummingbird:
    def __init__(self, API_KEY, config=None):
        print("in init API_KEY: ", API_KEY)
        if API_KEY == "":
            raise BHBCustomException("invalid_api_key")
        self.api_key = API_KEY

        workspace_name = None
        project_name = None

        if config is not None:
            workspace_name = config.get("workspace_name")
            project_name = config.get("project_name")
            if project_name is not None and workspace_name is None:
                raise BHBCustomException("config_error")

        if workspace_name is None:
            # If workspace_name is None, show a list of available workspaces
            self.workspace_id = select_workspace(self.api_key)
        else:
            # verify workspace_id is valid and set it
            self.workspace_id = initialize_workspace(self.api_key, workspace_name)
        
        # If project_name is None, show a list of available projects or create a new one        
        if project_name is None:
            self.project_id = select_project(self.workspace_id, self.api_key)
        else:
            self.project_id = initialize_project(self.workspace_id, project_name, self.api_key)


    def _download_dataset(self, dataset_tag):
        try:
            response = requests.get(DATASET_BASE_URL + "/" + dataset_tag + "?projectId=" + self.project_id, headers={'Authorization': f'Bearer {self.api_key}'})
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            raise BHBCustomException("failed_download_dataset", dataset_tag)
        except requests.exceptions.RequestException as err:
            raise BHBCustomException("unexpected_error", err)

        dataset = json.loads(response.text)["data"]
        response = json.loads(download_data(dataset["filename"], self.api_key))
        return {
            "name": dataset["name"],
            "data": response["data"],
        }
    

    def upload_dataset(self, dataset):
        print(f"Uploading dataset {dataset.name}...", end="", flush=True)
        dataset_hash = get_json_obj_hash(dataset.to_json())

        tag_response = requests.post(DATASET_BASE_URL + "/tag", json={
            'description': dataset.description,
            'hash': dataset_hash,
            'name': dataset.name,
            'projectId': self.project_id,
        }, headers={'Authorization': f'Bearer {self.api_key}'})

        if tag_response.status_code != 200:
            raise BHBCustomException("invalid_dataset_tag")

        tag = json.loads(tag_response.text)["tag"]
        version = json.loads(tag_response.text)["version"]
        existed = json.loads(tag_response.text)["existed"]

        dataset_filename = self.project_id + "_" + tag + ".txt"
        upload_data(dataset_filename, dataset.to_json(), self.api_key)

        try:
            dataset_response = requests.post(DATASET_BASE_URL, json={
                'dataSize': get_data_size(dataset.to_json()),
                'description': dataset.description,
                'filename': dataset_filename,
                'hash': dataset_hash,
                'name': dataset.name,
                'projectId': self.project_id,
                'tag': tag,
                'version': version,
            }, headers={'Authorization': f'Bearer {self.api_key}'})
            dataset_response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            print(f"\r{red_check()} Failed to upload dataset {bold()}{dataset.name}{reset_font()} {reset_color()}\n{right_angle()} ", end="")
            raise BHBCustomException(json.loads(http_error.response.content)["code"])
        except requests.exceptions.RequestException as err:
            raise BHBCustomException("unexpected_error", err)

        if existed:
            print(f"\r{green_check()} Dataset set to: {bold()}{tag}{reset_font()}{reset_color()}")
        else:
            print(f"\r{green_check()} Dataset {bold()}{tag}{reset_font()} created.{reset_color()}")
        
        return tag


    def add_judge(self, judge):
        print(f"Adding judge {judge.name}...", end="", flush=True)
        scoring_source_code, judge_scoring_hash, judge_scoring_func_name = get_source_code_hash(judge.scoring_rubric)

        passing_criteria_source_code = None
        judge_passing_hash = None
        judge_passing_func_name = None
        if judge.passing_criteria:
            passing_criteria_source_code, judge_passing_hash, judge_passing_func_name = get_source_code_hash(judge.passing_criteria)
        
        try:
            judge_tag_response = requests.post(JUDGE_BASE_URL + "/tag", json={
                'name': judge.name,
                'passingCodeHash': judge_passing_hash,
                'projectId': self.project_id,
                'scoringCodeHash': judge_scoring_hash,
            }, headers={'Authorization': f'Bearer {self.api_key}'})
            judge_tag_response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            raise BHBCustomException("failed_create_judge", judge.name);
        except requests.exceptions.RequestException as err:
            raise BHBCustomException("unexpected_error", err)        


        judge_tag_body = json.loads(judge_tag_response.text)
        judge_tag = judge_tag_body["tag"]
        judge_version = judge_tag_body["version"]
        judge_existed = judge_tag_body["existed"]

        scoring_filename = self.project_id + "_" + judge_tag + "_scoring.txt"
        upload_data(scoring_filename, scoring_source_code, self.api_key)

        passing_filename = None
        if judge.passing_criteria:
            passing_filename = self.project_id + "_" + judge_tag + "_passing.txt"
            upload_data(passing_filename, passing_criteria_source_code, self.api_key)

        dataSize = get_data_size(scoring_source_code)
        if passing_criteria_source_code:
            dataSize += get_data_size(passing_criteria_source_code)
        response = requests.post(JUDGE_BASE_URL, json={
            'dataSize': dataSize,
            'description': judge.description,
            'name': judge.name,
            'passingCodeFilename': passing_filename,
            'passingCodeHash': judge_passing_hash,
            'passingCodeFuncName': judge_passing_func_name,
            'projectId': self.project_id,
            'scoringCodeFilename': scoring_filename,
            'scoringCodeHash': judge_scoring_hash,
            'scoringCodeFuncName': judge_scoring_func_name,
            'tag': judge_tag,
            "version": judge_version,
        }, headers={'Authorization': f'Bearer {self.api_key}'})

        if response.status_code == 201:
            if not judge_existed:
                print(f"\r{green_check()} Judge {bold()}{judge_tag}{reset_font()} created.{reset_color()}")
            else:
                print(f"\r{green_check()} Judge set to: {bold()}{judge_tag}{reset_font()}{reset_color()}")
        return judge_tag
        
    def _get_judge_from_judge_tag(self, judge_tag):
        encoded_judge_tag = quote(judge_tag)
        judge_response = requests.get(JUDGE_BASE_URL + "/" + encoded_judge_tag + "?projectId=" + self.project_id, headers={'Authorization': f'Bearer {self.api_key}'})
        if judge_response.status_code == 404:
            print(f"\r{red_check()} Judge {bold()}{judge_tag}{reset_font()} not found. Please make sure there are no typos. {reset_color()}")
        
        judge = json.loads(judge_response.text)["data"]
        return judge


    def _get_scoring_rubric_func_from_judge(self, judge):
        scoring_source_code = download_data(judge["scoringCodeFilename"], self.api_key)
        return read_source_code_as_func(scoring_source_code, judge["scoringCodeFuncName"])


    def _get_passing_criteria_func_from_judge(self, judge):
        if 'passingCodeFilename' not in judge:
            return None
        passing_source_code = download_data(judge["passingCodeFilename"], self.api_key)
        return read_source_code_as_func(passing_source_code, judge["passingCodeFuncName"])


    def assess(self, judge_tag, dataset_tag=None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                judge = self._get_judge_from_judge_tag(judge_tag)
                scoring_rubric = self._get_scoring_rubric_func_from_judge(judge)
                passing_criteria = self._get_passing_criteria_func_from_judge(judge)

                if dataset_tag is None: 
                    print("\n=== Start of Run ===")
                    (result, latency, score, passed) = evaluate_run(func, args, kwargs, scoring_rubric, passing_criteria)
                    model_tag = create_model(
                        name=func.__name__,
                        source_code=func,
                        inputs=get_input_types(func),
                        outputs=get_type(result),
                        project_id=self.project_id,
                        api_key=self.api_key
                    )
                    print("\n=== End of Run ===")
                    print(f"\nRecording run...", end="", flush=True)
                    run_creation_response = requests.post(RUN_BASE_URL, json={
                        'inputs': args,
                        'judgeTag': judge_tag,
                        'latency': latency,
                        'modelTag': model_tag,
                        'outputs': result,
                        'passed': passed,
                        'projectId': self.project_id,
                        'score': score,
                    }, headers={'Authorization': f'Bearer {self.api_key}'})

                    
                    body = json.loads(run_creation_response.text)
                    if run_creation_response.status_code == 201:
                        print("\r✨ View run " + body["run"]["id"] + " at " + BASE_CLIENT_URL + "/workspace/" + body["workspaceId"] + "/project/" + self.project_id + "#run=" + body["run"]["id"])
                        return result
                    else:
                        raise BHBCustomException(body["code"])
                else:
                    dataset = self._download_dataset(dataset_tag)
                    print("\n=== Start of Evaluation ===")
                    if passing_criteria:
                        (output_type, scores) = evaluate_dataset(func, dataset, scoring_rubric, passing_criteria)
                    else:
                        (output_type, scores) = evaluate_dataset_with_no_passing_function(func, dataset, scoring_rubric)
                    print("\n=== End of Evaluation ===")
                    print(f"\nRecording model...", end="", flush=True)
                    model_tag = create_model(
                        name=func.__name__,
                        source_code=func,
                        inputs=get_input_types(func),
                        outputs=output_type,
                        projectId=self.project_id,
                        api_key=self.api_key,
                    )

                    print(f"\r{green_check()} Model {model_tag} uploaded. {reset_color()}")
                    print(f"Recording evaluation...", end="", flush=True)
                    response = requests.post(EVALUATION_BASE_URL, json={
                        'datasetTag': dataset_tag,
                        'judgeTag': judge["tag"],
                        'modelTag': model_tag,
                        'projectId': self.project_id,
                        'scores': scores,
                    }, headers={'Authorization': f'Bearer {self.api_key}'})
                    
                    evaluation_body = json.loads(response.text)
                    if response.status_code != 201:
                        raise BHBCustomException("failed_to_create_evaluation")
                    print("\r✨ View evaluation " + evaluation_body["id"] + " at " + evaluation_body["url"])
                return func(*args, **kwargs)
            return wrapper
        return decorator


    def trace(self, func):
        def wrapper(*args, **kwargs):
            print(f"Tracing function: {func.__name__}")
            # run function and get latency
            start = time.perf_counter()
            result = func(*args, **kwargs)
            latency = time.perf_counter() - start

            # create a model if one doesn't exist yet
            model_tag = create_model(
                name=func.__name__,
                source_code=func,
                inputs=get_input_types(func),
                outputs=get_type(result),
                project_id=self.project_id,
                api_key=self.api_key
            )

            run_creation_response = requests.post(RUN_BASE_URL, json={
                'inputs': args,
                'latency': latency,
                'modelTag': model_tag,
                'outputs': result,
                'projectId': self.project_id,
            }, headers={'Authorization': f'Bearer {self.api_key}'})

            body = json.loads(run_creation_response.text)
            if run_creation_response.status_code == 201:
                print("\r✨ View run " + body["run"]["id"] + " at " + BASE_CLIENT_URL + "/workspace/" + body["workspaceId"] + "/project/" + self.project_id + "#run=" + body["run"]["id"])
                return result
            else:
                raise BHBCustomException(body["code"])

        return wrapper