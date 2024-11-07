## ollama_pick
an app to augment the ability of the native Linux desktop launcher for selecting a locally stored ollama models before launching ollama.

## Prerequisite:

ollama has been installed and one or many models have been created locally using the **ollama run (or pull)** *model* command.

gnome terminal is installed

python 3 is installed

ollama will run in a normal terminal window when ran by hand.

## How To Install:

The 'ollama_pick' module was compiled for a Linux system where *gnome terminal* is available.

Download the *ollama pick* module and place it into the bin directory found in your Linux Home directory (i.e. ~/bin directory) and insure the executable attribute has been set.

Create a desktop launcher and use the **\/home/<home directory\>/bin/ollama_pick** as the executable.

To override the built-in model, use the **--default=<model>** option

For those who store their ollama models in a different location than the default, add the **--override=<path>** option and the absolute path in the launcher.

## Ollama_Pick has been upgraded. Read the Changelog in the source code.
