import os
import sys
import time
import json


def monitor_commit():

    json_pipeline = get_json_pipeline()
    validate_pipeline(json_pipeline)

    try:
        git_repo = sys.argv[1]
    except:
        print("script call error...\npass the git repo directory as a arg to run the pipeline")
        exit()
    else:
        git_repo = sys.argv[1]
        commit_file = os.popen(f"./get_git_hooks.sh {git_repo}; echo $?").read()
        get_error = commit_file.split()[-1]
    
    if get_error == '1':
        print(f"{commit_file}^exit code\ncheck log file to see the error...")
    else:
        while True:
            #count_loop = 0
            last_commit_file = os.popen(f"./get_git_hooks.sh {git_repo}; echo $?").read()
            if last_commit_file == commit_file:
                # print("commits iguais")
                # time.sleep(2)
                pass
            else:
                # print(last_commit_file)
                # print("diferente")
                pipeline_run_status = run_pipeline(json_pipeline)
                commit_file = last_commit_file
                #print(pipeline_run_status)
                if pipeline_run_status == None:
                    print("pipeline error, one or more commands within key 'run:{}' are not working")
                    exit()
                else:
                    pass

def get_json_pipeline():
    
    pipeline = os.popen("cat pipeline_config.json").read()
    json_pipeline = json.loads(pipeline)
    
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
                        break
            else:
                print("No run key in pipeline, please input the run key and its steps")
                break
        else:
            print("invalid pipeline sintax, please describe trigger and pipeline only")
            break

def run_pipeline(pipeline):

    commands = pipeline["pipeline"]["run"]
    for key in commands:
    
        step_run = os.popen(f"{commands[key]} 2> log.txt; echo $?").read()
        step_error = step_run.split()[-1]
        
        if step_error != "0":
            print(f"command {commands[key]} error with exit {step_error}\ncheck logfile to see the error")
            os.popen(f'echo "command {commands[key]} error with exit {step_error} - $(date)" >> log.txt')
            break
            return False
        else:
            return True
            pass

if __name__ == '__main__':
    monitor_commit()