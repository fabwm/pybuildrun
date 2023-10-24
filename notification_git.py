import os
import sys
import time
import json


def monitor_commit():

    try:
        git_repo = sys.argv[1]
    except:
        print("script call error...\npass the git repo directory as a arg to run the pipeline")
        exit()
    else:
        git_repo = sys.argv[1]
        commit_file = os.popen(f"./get_git_hooks.sh {git_repo}; echo $?").read()
        get_error = commit_file.split()[-1]
        #print(get_error)
    
    if get_error == '1':
        print(f"{commit_file}^exit code")
    else:
        while True:
            count_loop = 0
            last_commit_file = os.popen(f"./get_git_hooks.sh {git_repo}").read()
            if last_commit_file == commit_file:
                pass
            else:
                if count_loop == 0:
                    pass
                else:   
                    print("diferente")
                count_loop += 1 

def get_json_pipeline():
    
    pipeline = os.popen("cat ci_json.json").read()
    json_pipeline = json.loads(pipeline)
    
    #print(json_pipeline)
    return json_pipeline

def validate_pipeline(json_pipeline):

    for x in json_pipeline:
        if x == "trigger":
            pass
        elif x == "pipeline":
            if "run" in json_pipeline[x]:
                for y in json_pipeline[x]:
                    if y == "run":
                        pass
                    else:
                        print("invalid key value in pipeline, please erase all keys in pipeline that is not 'run'")
                        return False
            else:
                print("No run key in pipeline, please input the run key and its steps")
                return False
        else:
            print("invalid pipeline sintax, please describe trigger and pipeline only")
            return False

def run_pipeline(pipeline):

    commands = pipeline["pipeline"]["run"]
    for key in commands:
        #print(commands[key])
        step_run = os.popen(f"{commands[key]} 2> /dev/null; echo $?").read()
        step_error = step_run.split()[-1]
        if step_error != "0":
            print(f"not work {commands[key]}")
            break
        else:
            print(step_run)

#monitor_commit()
pipeline = get_json_pipeline()
#validate_pipeline(pipeline)
run_pipeline(pipeline)