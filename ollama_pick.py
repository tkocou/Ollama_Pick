#! /bin/python 
import os
import sys
import argparse

## Change this next line to reflect your default llama model supported by ollama
ollama_default = "codellama"
command = "ollama run"
ollama_path = "/usr/share/ollama/.ollama/models/manifests/registry.ollama.ai/library"
ollama_model = ""

def sel_model(listing):
    index = 0
    sel_default = ""
    for model in listing:
        if model == ollama_default:
            print("*"+str(index)+" "+model)
            sel_default = str(index)
        else:
            print(" "+str(index)+" "+model)
        index += 1
        
    print("Current default is indicated by a '*'. Press ENTER to use the default model.")
    selection = input("Select model and press ENTER: ")
    if selection == "":
        selection = sel_default
    
    return int(selection)


parser = argparse.ArgumentParser()

parser.add_argument("--override", help="Your override for path to ollama models")

args = parser.parse_args()

if args.override:
    if os.path.exists(args.override):
        ollama_path = args.override
    else:
        x = input("Bad Path")
        sys.exit()

dir_list = os.listdir(ollama_path)

try:
    selection = sel_model(dir_list)
    if selection < 0:
        print("Negative index. Using default selection.")
        selection = ""
    if selection == "":
        ollama_model = ollama_default
    else:
        ollama_model = dir_list[int(selection)]
    
except Exception as es:
    print(f"Bad selection. Error code is =-> {es}")
    sys.exit()

command = "gnome-terminal -e 'bash -c \"ollama run "+ollama_model+"\"' 2>/dev/null "
os.system(command)