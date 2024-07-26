## envOS

Create a system variable with the name `envOS`, the value will be the path of the main configuration file

Within the main file are the paths to the specific configuration files for each project in Python.

The variable `ENV` refers to the general configuration of the entire environment, the other variables.
For example: `pyvert_settings` refer to the specific configurations of the project.
```
from envOS import ENV
print(ENV.SERVER_SETTINGS)
```
