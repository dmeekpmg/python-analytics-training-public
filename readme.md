# Advanced python

## References for setting up the project

https://docs.python-guide.org/writing/structure/
https://choosealicense.com/

## Creating the environment

It is strongly recommended that you use an environment. 

Environments can be created in VSCode or Conda. A quick way to start is to open
a terminal and run:

```
conda create --name your_environment_name python ipykernel
conda activate your_environment_name
pip install -r requirements.txt
```

In VSCode, open the command palette, search for "Select Interpreter" and choose the
environment you just created.

## Data souce

Download static data from the following links

https://opendata.transport.nsw.gov.au/dataset/temporary-andor-sample-gtfs-data/resource/8bbb51f1-b4aa-49e9-be47-db4bd4688152
from page: https://opendata.transport.nsw.gov.au/dataset/temporary-andor-sample-gtfs-data

Create a file called .env in the root of your repository and create variables like the 
following:
```
DATA_PATH="C:/Temp/advanced_python/sample_full_greater_sydney"
```

Paths need to have either forward slashes or double-backslashes.

## Reloading modules while developing and prototyping

As you develop and prototype, it can be helpful to automatically reload modules that 
you're working on. You can set this up by doing either of the following

Add magic commands to your notebook
```
%load_ext autoreload
%autoreload 2
```

Add magic commands in a way that doesn't trigger linting errors
```
from IPython import get_ipython
ip = get_ipython()
ip.run_line_magic("load_ext", "autoreload")
ip.run_line_magic("autoreload", "2")
```

Set this up for any notebook you work on by adding the following to your VSCode
settings:
```
"jupyter.runStartupCommands": [
    "%load_ext autoreload", "%autoreload 2"
],
```

Note that only one level of modules will be reloaded. If there are multiple nested
levels of modules, you will need to reload deeper levels with a command such as the
following:
```
from importlib import reload
from multiple.levels.down import mymodule
reload(mymodule)
```