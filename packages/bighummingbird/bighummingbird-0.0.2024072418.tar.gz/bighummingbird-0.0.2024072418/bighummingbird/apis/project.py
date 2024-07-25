import requests
import json
from ..utils.constants import WORKSPACE_BASE_URL, PROJECT_BASE_URL, BASE_CLIENT_URL
from ..utils.display_util import orange, reset_color, blue_underline, gray, green_check, bold, reset_font
from ..utils.error_handling import UNEXPECTED_ERROR, BHBCustomException

def get_project_uid(project_name):
    formatted_name = project_name.strip()
    formatted_name = formatted_name.lower().replace(' ', '-')
    return formatted_name


def create_project(workspace_id, api_key):
    while True:
        print(f"{gray()}Enter a project name: {reset_color()}")
        project_name = input()
        project_response = requests.post(PROJECT_BASE_URL + "/create-via-api", json={'displayName': project_name, 'projectUID': get_project_uid(project_name), 'workspaceId': workspace_id}, headers={'Authorization': f'Bearer {api_key}'})
        project_body = json.loads(project_response.text)
        if project_response.status_code == 201:
            return project_body["project"]["id"]
        else:
            error_code = project_body["code"]
            if error_code == 'project_name_already_exist':
                print(f'🚧 {orange()}Project name already exists.{reset_color()} Please enter a unique project name')
            elif error_code == 'exceed_project_creation_limit':
                print(f'🚧 {orange()}You\'ve reached your project limit!{reset_color()} Upgrade to Pro to unlock unlimited projects. {blue_underline(f"{BASE_CLIENT_URL}/pricing")}')
                raise BHBCustomException("exceed_project_creation_limit")
            else:
                raise BHBCustomException()

def select_project(workspace_id, api_key):
    response = requests.get(WORKSPACE_BASE_URL + "/" + workspace_id +"/editable-project-list", headers={'Authorization': f'Bearer {api_key}'})    
    body = json.loads(response.text)
    print(f"\n{reset_color()}Projects")
    print("--------")
    if response.status_code == 200:
        print(f"[0] Create a new project")
        i = 1
        for project in body["projects"]:
            print(f"[{i}] {project['name']}")
            i += 1
        
        while True:
            try:
                print(f"{gray()}Select a project: {reset_color()}")
                option = int(input())
                if option == "" or option < 0 or option > len(body["projects"]):
                    raise ValueError()
                if option == 0:
                    return create_project(workspace_id, api_key)
                else:
                    return body["projects"][option - 1]["id"]
            except ValueError as e:
                print(f"{orange()}Invalid selection. Please try again.{reset_color()}")

def initialize_project(workspace_id, project_name, api_key):
    response = requests.get(PROJECT_BASE_URL + "/name/" + project_name + "/workspace/" + workspace_id, headers={'Authorization': f'Bearer {api_key}'})
    body = json.loads(response.text)
    if response.status_code == 200:
        print(f"{green_check()} Project selected: {bold()}{body['project']['displayName']}{reset_font()}{reset_color()}")
    elif body["code"]:
        print(f"🚧 {orange()}Project {project_name} not found.{reset_color()} Please make sure there is no typo.")
    else:
        raise BHBCustomException(body["error"])
    return body["project"]["id"]