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

## First-time setup of VSCode

### Extensions

While VSCode is fairly powerful on its own, it will be helpful to install several 
extensions. The following are recommended:

- gitgraph (similar to SourceTree or the git desktop tool with a visual commit history)
- gitlens (powerful git tool with an optional paid upgrade)
- MSSQL (a lightweight version of SQL Server Management Studio)
- github pull requests and issues (to create, review and approve github pull requests)
- Pylint (to show linting of python files)

The core Python extension should already be installed, but if not, you will need to
install that too.

Other extensions that may be useful if you develop more widely:

- SQLite (work with SQLite databases)
- SAS (run SAS from VSCode)
- R and R debugger (https://code.visualstudio.com/docs/languages/r)
- Open (Open files in the default application)
- Markdown All in One (preview markdown files and convert to HTML)
- Live SASS compiler (for working with CSS and SASS)
- autoDocstring (automatically create templates for docstrings)

### Rulers

Best practice code has a maximum line width. You can set and adjust this in VSCode by
adding a setting such as the following to your user settings:

```
    "editor.rulers": [
        {
            "column": 72,
            "color": "#1eff0015"
        },
        {
            "column": 88,
            "color": "#888888bb"
        }
    ]
```

## Project-specific setup of VSCode

### Select the interpreter

In VSCode, open the command palette, search for "Select Interpreter" and choose the
environment you just created.

### Configure the root folder for notebooks

When testing code and working with prototypes, it is ideal if you can store your rough
code outside of the core codebase. Typically, one might change the working directory
using something like `os.chdir(os.getcwd().split("\")) ... etc`

In VSCode, it is much easier. Just set up the default notebookfileroot setting for the 
workspace. This repository already includes the settings file in .vscode/settings.json.

Any folder-related settings can either be edited directly in this file (if you know
the parameters) or editing through the UI. Open the command palette (Ctrl+Shift+P),
search for "Open Settings (UI)" and then navigate to "User", "Workspace" or "Folder".

https://code.visualstudio.com/docs/editor/variables-reference

## Data souce

Download static data from the following links. This requires an account with TfNSW.
https://opendata.transport.nsw.gov.au/dataset/temporary-andor-sample-gtfs-data/resource/8bbb51f1-b4aa-49e9-be47-db4bd4688152
from page: https://opendata.transport.nsw.gov.au/dataset/temporary-andor-sample-gtfs-data

Create a file called .env in the root of your repository and create variables like the 
following:
```
DATA_PATH="C:/Temp/advanced_python"
CERT="C:/Users/abcusername/OneDrive - KPMG/Setup/Certificates/caadmin.netskope.com.pem"
API_KEY=abcdefmyapikey
APP_NAME=python_training_my_app
SQLDRIVER="sqlite:///C:\\Temp\\advanced_python\\db.db"
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

## Potential use cases

- map of bus routes
- density of bus routes
- map of frequency of service
- which days are less congested on my route to the office?
- how many busses on the road at each time? What proportion?
- on-time performance by agency
- predictive model for factors that affect on-time performance
- map of frequency by stop