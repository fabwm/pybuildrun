import os
import sys
import time
import json


script_init_msg ="\
██████╗░██╗░░░██╗██████╗░██╗░░░██╗██╗██╗░░░░░██████╗░██████╗░██╗░░░██╗███╗░░██╗\n\
██╔══██╗╚██╗░██╔╝██╔══██╗██║░░░██║██║██║░░░░░██╔══██╗██╔══██╗██║░░░██║████╗░██║\n\
██████╔╝░╚████╔╝░██████╦╝██║░░░██║██║██║░░░░░██║░░██║██████╔╝██║░░░██║██╔██╗██║\n\
██╔═══╝░░░╚██╔╝░░██╔══██╗██║░░░██║██║██║░░░░░██║░░██║██╔══██╗██║░░░██║██║╚████║\n\
██║░░░░░░░░██║░░░██████╦╝╚██████╔╝██║███████╗██████╔╝██║░░██║╚██████╔╝██║░╚███║"


# def git_trigger(json_pipeline):

#     try:
#         git_repo = sys.argv[2]
#     except:
#         print("Script call error...\nPass the git repo directory as a arg to run the pipeline")
#         exit()
#     else:
#         git_repo = sys.argv[2]
#         commit_file = os.popen(f"./get_git_hooks.sh {git_repo}; echo $?").read()
#         get_error = commit_file.split()[-1]
    
#     if get_error == '1':
#         print(f"{commit_file}^Exit code\nCheck log file to see the error...")
#     else:
#         print("*******************************************************************************\n\n")
#         print(script_init)
#         print("\n\n*******************************************************************************")
#         print("\n\nStarting pybuildrun....\nWaiting for commits\n\n")
#         while True:
            
#             last_commit_file = os.popen(f"./get_git_hooks.sh {git_repo}; echo $?").read()
#             if last_commit_file == commit_file:
#                 pass
#             else:
#                 print("Commit received...\nStarting pipeline...")
#                 pipeline_run_status = run_pipeline(json_pipeline)
#                 commit_file = last_commit_file
#                 if pipeline_run_status == False:
#                     print("Pipeline error, one or more commands within key 'run:{}' are not working")
#                     exit()
#                 else:
#                     print("Pipeline succesfull run\n")
#                     var_for_validation_inloop = 0
#                     user_decision_to_continue_run_pipeline = input("Would you like to continue listening to git commits? (y/n)\n")
#                     while(var_for_validation_inloop == 0):
#                         if user_decision_to_continue_run_pipeline == 'y':
#                             var_for_validation_inloop = 1
#                             print("\nRestarting pybuildrun...\nWaiting for commits\n")
#                             pass
#                         elif user_decision_to_continue_run_pipeline == 'n':
#                             print("\nExiting pybuildrun...")
#                             exit()
#                         else:
#                             print("Not readable answer, please input 'y' or 'n' to continue pybuildrun.\n")
#                             pass

def get_json_pipeline():
    
    try:
        pipeline_path = sys.argv[1]
    except:
        print("pybuildrun pipeline error: no pipeline file passed...\nPlease select a valid pipeline file as a arg")
        exit()
    else:
        pipeline = os.popen(f"cat {pipeline_path}").read()
        try:
            json.loads(pipeline)
        except:
            print("pybuildrun pipeline error: invalid file type passed...\nPlease select a valid pipeline file as a arg")
            exit()
        else:
            json_pipeline = json.loads(pipeline)    
            return json_pipeline

def validate_pipeline(json_pipeline):

    for x in json_pipeline:
        
        if x == "pipeline":
            if "run" in json_pipeline[x]:
                for y in json_pipeline[x]:
                    if y == "run":
                        pass
                    else:
                        print("Invalid key value in pipeline, please erase all keys in pipeline that is not 'run'")
                        exit()
            else:
                print("No run key in pipeline, please input the run key and its steps")
                exit()
        else:
            print("Invalid pipeline sintax, please describe trigger and pipeline only")
            exit()
    
    return json_pipeline

def run_pipeline(pipeline):

    commands = pipeline["pipeline"]["run"]
    for key in commands:
    
        step_run = os.popen(f"{commands[key]} 2>> log_pybuildrun.txt; echo $?").read()
        step_error = step_run.split()[-1]
        
        if step_error != "0":
            print(f"Command {commands[key]} error with exit {step_error}\ncheck logfile to see the error\n")
            os.popen(f'echo $(date)" >> log_pybuildrun.txt')
            return False
            break
        else:
            pass
    
    return True

# def get_trigger():
    
#     json_pipeline = get_json_pipeline()
#     pipeline = validate_pipeline(json_pipeline)

#     trigger = pipeline["trigger"]

#     return trigger, pipeline

def app_run():

    json_pipeline = get_json_pipeline()
    pipeline = validate_pipeline(json_pipeline)

    try:

        sys.argv[2]
    
    except:
        print("Directory to start pipeline not defined.\nPlease input the directory that you want \
the pipeline to run from\nGive it as a second argument.")
    else:
        dir_to_run_pipeline = sys.argv[2]
        
        if os.path.exists(dir_to_run_pipeline):

            os.chdir(dir_to_run_pipeline)
            print("*******************************************************************************\n\n")
            print(script_init_msg)
            print("\n\n*******************************************************************************")
            print("\n\nStarting pybuildrun....\nrunning pipeline\n\n")
            time.sleep(1)
            run_pipeline(pipeline)
            print("Done")

        else:

            print("Error on directory selection...\nInvalid directory to run pipeline, please input a valid directory as an argument..")

# def app_run():

    # trigger = get_trigger()
    # pipeline = trigger[1]

    # if trigger[0] == 'git':
    #     git_trigger(pipeline)
    # elif trigger[0] == 'manual':
    # manual_trigger()
    # else:
    #     print("Pipeline error: select trigger in pipeline between 'manual' or 'git'")


if __name__ == '__main__':
    app_run()
    