#! /bin/python 

## Released under the GPL3 license. Please give credit when making your own version / derivitive
## Copyright 2024 Thomas Kocourek
## Version 1.0, 06Nov2024
##
## Changelog 
##
## 06Nov2024
## Modified listing method. Older method could not differenciate between alternative versions of a stored model
## Example: a 3b version vs a 7b version of a model
##
## 07nov2024
## Added more error trapping. Touched up error reporting messages to make more sense.
## Added the ability to override the default model via the launcher command
##
## 04Feb2025
## Added the ability to save the default model in a hidden text file in the home directory
##
## 15Jun2025
## Added a check for the latest version of a model before running the model.
## Changed default to use the first model listed. ollama sorts list per latest pulled model
##
## 11jul2025
## added script to check for Internet access before attempting a manifest pull
##

import os
import sys
import argparse

## Change this next line to reflect your default llama model supported by ollama
## see the get_default() function
##ollama_default = "mistral"
command = ""
# ollama_path = "/usr/share/ollama/.ollama/models/manifests/registry.ollama.ai/library"
ollama_model = ""
home_dir = os.path.expanduser('~')
default_file = home_dir + "/.ollama_pick.txt"

def extract_list():
    try: ## in case ollama is not installed properly
        command = "ollama list > temp.txt"
        os.system(command)
    except Exception as es:
        print(f"Has ollama been properly installed? Error code is =-> {es}")
        x = input("Press ENTER to terminate.")
        sys.exit()

    with open("temp.txt") as fd:
        result = fd.readlines()
    os.remove("temp.txt")

    index = 0
    name_list = []
    for element in result:
        if index == 0:
            index += 1
            continue
        temp_list = element.split(' ')
        name_list.append(temp_list[0])

    return name_list

def sel_model(listing):
    index = 0
    ## check for a match
    for model in listing:
        if model == ollama_default:
            print("*"+str(index)+" "+model)
            sel_default = str(index)
        else:
            print(" "+str(index)+" "+model)
        index += 1
        
    print("Current default is indicated by a '*'. Press ENTER to use the default model.")
    selection = input("Select model and press ENTER: ")
    ## Automatically default to first model in list
    if selection == "":
        selection = "0"
    
    return int(selection)

def get_default(input_filename):
    ## The idea is to check for a 'default' model via a text file
    ## If the file exist, assign the default model
    ## If the file is empty or missing, create a new one.
    default_val = ""
    try:
        with open(input_filename,"r") as f:
            default_val = f.read()
    except Exception:
        default_val = "mistral:latest"
        with open(input_filename, 'w') as f:
            f.write(default_val)
    return default_val

## start of main program
ollama_default = get_default(default_file)

parser = argparse.ArgumentParser()

parser.add_argument("--override", help="Your override for path to ollama models")
parser.add_argument("--default", help="Override default model (include the model modifiers, example: codegemma:7b)")

args = parser.parse_args()

if args.override:
    if os.path.exists(args.override):
        ollama_path = args.override
    else:
        x = input("Bad Path for override. Press ENTER to terminate.")
        sys.exit()
        
if args.default:
    ollama_default = args.default
    with open(default_file, 'w') as f:
            f.write(ollama_default)

## read in list of installed models for ollama
dir_list = extract_list()

## if the ollama_default only specifies the model name, append "latest"
default_list = ollama_default.split(':')
if len(default_list) == 1:
    default_list.append("latest")
    ollama_default = default_list[0]+':'+default_list[1]

try:
    selection = sel_model(dir_list)
    print(selection)
    if selection < 0:
        #print("Negative index. Using default selection.")
        selection = ""
    
    else: ## choose the selected model
        ollama_model = dir_list[int(selection)]
    
except Exception as es:
    print(f"Bad selection. Error code is =-> {es}")
    x = input("Press ENTER to terminate.")
    sys.exit()
    
try:
    ## Check for Internet access and if good, pull model
    command = "if ping -q -c 1 google.com >/dev/null 2>&1; then gnome-terminal -e 'bash -c \"ollama pull "+ollama_model+"\"' "
    os.system(command)
    command = "gnome-terminal -e 'bash -c \"ollama run "+ollama_model+"\"' 2>/dev/null "
    os.system(command)
except Exception as es:
    print(f"gnome-terminal needs to be checked. Error code is =-> {es}")
    x = input("Press ENTER to terminate.")
    sys.exit()