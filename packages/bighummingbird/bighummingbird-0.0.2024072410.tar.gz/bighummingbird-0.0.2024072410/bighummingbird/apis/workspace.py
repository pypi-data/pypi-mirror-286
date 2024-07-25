import requests
import json
from ..utils.constants import API_BASE_URL, WORKSPACE_BASE_URL
from ..utils.display_util import orange, gray, reset_color, bold, reset_font, green_check
from ..utils.error_handling import BHBCustomException

def select_workspace(api_key):
    print("select_workspace api_key: ", api_key)
    response = requests.get(API_BASE_URL + "/workspace-list", headers={'Authorization': f'Bearer {api_key}'})
    body = json.loads(response.text)    
    if response.status_code == 200:
        # if there is only 1 workspace, then select it by default
        workspaceNameList = body["workspaceNameList"]
        if len(workspaceNameList) == 1:
            print(f"Workspace selected: {bold()}{workspaceNameList[0]['name']}{reset_font()} (default)")
            return workspaceNameList[0]["id"]

        # title
        print(f"\n{reset_color()}Workspaces")
        print("----------")
    
        # print all workspace name options
        i = 0
        for workspaceName in workspaceNameList:
            print(f"[{i}] {workspaceName['name']}")
            i += 1

        # prompt to select workspace        
        while True:
            try:
                option = int(input(f"{gray()}Select a workspace: {reset_color()}"))
                if option == "" or option < 0 or option > len(workspaceNameList) - 1:
                    raise ValueError()
                else:
                    return workspaceNameList[option]["id"]
            except ValueError as e:
                print(f"{orange()}Invalid selection. Please try again.{reset_color()}")
    else:
        raise BHBCustomException(body["error"])


def initialize_workspace(api_key, workspace_name):
    response = requests.get(WORKSPACE_BASE_URL + "/name/" + workspace_name, headers={'Authorization': f'Bearer {api_key}'})
    body = json.loads(response.text)
    if response.status_code == 200:
        print(f"{green_check()} Workspace selected: {bold()}{body['workspace']['name']}{reset_font()}")
    elif body["errorCode"]:
        raise BHBCustomException(body["errorCode"])
    else:
        print(f"{orange()}Workspace {bold()}{workspace_name}{reset_font()} not found. Please make sure there is no typo.{reset_color()}")
    return body["workspace"]["id"]