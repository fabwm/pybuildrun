#!/bin/bash
REPO_GIT=$1


function check_dir()
{
    if [[ ! -z $1 ]]; then
        
        if [ -d $1 ]; then
            cd $1 && git log 2> /dev/null 1> /dev/null
            if [ $? != 0 ]; then
                echo "Not a git repository - please input a git repo dir as a arg  - $(date)" # >> log.txt
                exit 1
            else
                get_commit_logs $1
            fi
            #echo $1
        else
            echo "diretorio $1 invalido - $(date)" >> log.txt
            #echo "diretorio $1 invalido - $(date)"
        fi
    
    else
    
        echo "no args - $(date)" >> log.txt
        #echo "no args - $(date)"
    
    fi
}

function get_commit_logs()
{
    cd $1
    COMMIT_DONE=$(git log | grep commit | cut -d " " -f 2)
    ARRAY_COMMIT_HASH=($COMMIT_DONE)
    for (( i=0; i<=${#ARRAY_COMMIT_HASH[@]}; i++ )); do
        GIT_SHOW=$(git show ${ARRAY_COMMIT_HASH[$i]}) # | grep diff ) | cut -d "/" -f 3)
        #GIT_SHOW=$(git show ${ARRAY_COMMIT_HASH[$i]} | grep file )
    done
}

check_dir $REPO_GIT
echo $GIT_SHOW