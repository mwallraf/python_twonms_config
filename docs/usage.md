# Usage

To use Python 2NMS config manager in a project

```python
from twonms.config import Config

config = Config.create()

print(config.env)

print (config)
```

## Config.create() object

A configuration object is created by calling the `Config.create()` method. This actually a wrapper around the `OmegaConf.create()`method.

The method takes the following parameters:

    path: (optional) the path name where yaml config files can be found,
            default=./conf

    conf: (optional) the filename including extension that should be loaded
            if blank then the environmont default config file will be loaded
            if the "env" variable is given and the file exists
            default=None

    env: (optional) if the application is using the standard config file
            naming conventions then the env variable can be specified and the
            correct config file is automatically loaded
            default=PROD

    allowed_envvars: (optional) a list of allowed environment variables that can be loaded
                        via system env vars

    required_config: (optional) dictionary or string with all the required parameters,
                        meaning that these parameters will always be present in
                        the Config object
                        If this is a string then it should be in yaml format

## Defining parameters

Parameters can be defined in different ways and in a predefined order. Multiple ways can be used at the same time, for example a yaml config file exists together with environment variables and cli arguments.

In the end a single OmegaConf object will be created combining all parameters.

Import order:

-   programmatically defined default values
-   environment variables
-   dotenv files
-   configuration files in YAML format
-   cli arguments

### programatically defined parameters

It's easy to define defaults for your application by defining a dictionary or list or yaml string. Check the OmegaConf documentation for more details.

```python
from twonms.config import Config

DEFAULT_CONFIG = """
name: maarten
debug: true
"""

config = Config.create(required_config=DEFAULT_CONFIG)

print(config.name)
```

### configuration files defined in yaml format

It is possible to store all your application parameters in yaml files. You can specifically refer to a file or you can use the default filenames and then the `environment` parameter will define which config file will be loaded (if it exists).

If no filename is specified and no `environment` parameter is defined then the filename `./conf/producation.yaml` will be loaded automatically if it exists.

Default config folder = `./conf`

Default config filenames and matching environment variable:

| environment | config file      |
| ----------- | ---------------- |
| PROD        |  production.yaml |
| DEV         | development.yaml |
| TEST        | test.yaml        |
| DEBUG       | debug.yaml       |

#### Example:

```yaml
---
name: maarten
description: production configuration file
script: test.py
  usage: test.py --help
```

Usage:

```python

from twonms.config import Config

# create a config object with default parameters
# this will search for the file ./conf/production.yaml
config_default = Config.create()
print(config_default.script.usage)

# create a config object by specifying the debug environment
# this will search for the file ./conf/debug.yaml
config_debug = Config.create(required_config={"env": "DEBUG"})
print(config_debug.script.usage)

# create a config object with custom config folder and file
config_custom = Config.create(path="./customfolder", conf="mycustomconfig.yaml")
print(config_custom.name)
```

### environment variables

Environment variables can be defined via system environment variables or via `.env` files which will be loaded automatically if it exists.

To prevent all existing environment variables to be loaded into your configuration object, you'll have to specify which variables are allowed by specifying the `allowed_envvars`parameter in the `create()` method.

#### Example:

```python
import os

# simulate system environment variable
os.environ("name", "maarten)

from twonms.config import Config

config = Config.create(allowed_envvars=["name"])

print(config.name)
```

### dotenv variables

Similar as with system environment variables you can also define envvars in a `.env` file, locally to the main script. The difference with system environment variables is that there is no need to define the allowed parameters, all parameters defined in the .env file will be loaded.

#### Example:

**.env file**

```console
name=maarten
DEBUG=true
```

```python

from twonms.config import Config

config = Config.create()

print(config.name, config.DEBUG)

```

### cli arguments

The last method to load parameters is to use cli script arguments. All arguments will be loaded.

#### Example:

** myscript.py **

```python

from twonms.config import Config

config = Config.create()

print(config.env)
```

```console
# start the script with extra arguments

python myscript.py env=DEBUG
```
