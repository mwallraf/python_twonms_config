"""twonms.config module to manage application configuration

The module uses OmegaConf to combine and read configuration items.

Configuration parameters can be provided in different ways and will
be processessed in a certain order where each step may override the
parameters of the previous step. In the end all parameters of all
steps will be combined and accessible in the Configure() class

  1. no parameters provided - use application default parameters if
     configured (via REQUIRED_CONFIG_PARAMETERS parameter)
  2. from envvars (system env vars or .env file)
  3. from *.yml config files
  4. from cli


  Typical usage example:

    from twonms.config import Config

    config = Config.create()

    debug = config.debug
    my_other_param = config.my_other_param
"""


import os
import sys
from typing import Dict, List, Optional, Set, Union

from dotenv import load_dotenv
from loguru import logger
from omegaconf import OmegaConf


class Config:
    """Main class of the module

    Manages application configuration parameters and this actually
    overrides from OmegaConf so the same rules apply, check the
    OmegaConf docs for more details.

    This class implements some default inheritance to take parameters
    from different sources (envvars, cli, conf files)


    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.

    Raises:
        NotImplementedError
    """

    # Does a mapping of pre-defined environments to their
    # corresponding yaml configuration files
    # This is only used in case there was no config file specified.
    # This requires the application to have the correct files
    # initialized  (ex. development.yaml)
    ENVIRONMENT_MAPPING = {
        "DEV": "development.yaml",
        "PROD": "production.yaml",
        "DEBUG": "debug.yaml",
        "TEST": "test.yaml",
    }

    # These are the environment variables that are allowed by default
    # These parameters could be defined as envvar, dotenv or cli
    # All other paremeters are ignored
    DEFAULT_ALLOWED_ENVVARS = [
        "environment",
        "debug",
    ]

    def __init__(
        self,
        path: str,
        conf: str,
        env: str,
        required_config,
        allowed_envvars,
    ) -> None:
        self._path = path
        self._conf = conf
        self._env = env
        self._required_config = required_config
        self.allowed_envvars = allowed_envvars or []

    @property
    def path(self):
        """Property for path variable

        Returns the path if the folder exists,
        otherwise returns None
        """
        if os.path.isdir(self._path):
            return self._path
        return None

    @property
    def conf(self):
        """Property to return the yaml config filename

        If the config file is defined then return it
        Otherwise check if the file for the environment exists
        If not then return None
        """
        if self._conf:
            return self._conf

        env = self.env
        if env and env in self.ENVIRONMENT_MAPPING:
            return self.ENVIRONMENT_MAPPING[env]

        return None

    @property
    def env(self):
        """Property for the environment variable

        Returns either a predefined environment (DEV, PROD, DEBUG, TEST) or
        None
        """
        env = self._env.upper()
        if env in self.ENVIRONMENT_MAPPING.keys():
            return env
        return None

    @property
    def required_config(self) -> OmegaConf:
        """Property for the required config

        Returns the OmegaConf
        """
        try:
            obj = OmegaConf.create(self._required_config)
            return obj
        except Exception as e:
            logger.debug(e)
            pass
        return OmegaConf.create()

    @property
    def environment_config(self) -> OmegaConf:
        """Property for the environment variables config

        Returns the OmegaConf object
        """
        # load environment variables
        load_dotenv()
        conf = OmegaConf.create(
            {x: os.environ.get(x) for x in self.allowed_envvars if os.environ.get(x)}
        )
        return conf

    @property
    def cli_config(self) -> OmegaConf:
        """Property for the CLI variables config

        Returns the OmegaConf object
        """
        # load cli variables
        conf = OmegaConf.create({x: y for x, y in OmegaConf.from_cli().items()})
        return conf

    @property
    def file_config(self) -> OmegaConf:
        """Property that returs the OmegaConf based on the yaml configuration file"""
        if self.path and self.conf:
            config_file = os.path.join(self.path, self.conf)
            if os.path.isfile(config_file):
                return OmegaConf.load(config_file)
        return OmegaConf.create()

    def __create(self) -> OmegaConf:
        """Class method to create an OmegaConf object"""

        # loads config parameters, in order of precedence (later configs overrides earlier ones)
        required_config = self.required_config
        env_config = self.environment_config
        cli_config = self.cli_config
        file_config = self.file_config

        merged_config = OmegaConf.merge(
            required_config, env_config, file_config, cli_config
        )

        return merged_config

    @staticmethod
    def create(
        path: str = "./conf",
        conf: str = None,
        env: str = "PROD",
        required_config: Union[str, dict] = {},
        allowed_envvars=DEFAULT_ALLOWED_ENVVARS,
    ) -> OmegaConf:
        """Creates the Config object

        This method should be used as the constructor

        Attributes:

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

        Example usage:

            REQUIRED_CONFIG_PARAMETERS = \"\"\"
            environment: PRODUCTION
            debug: false
            \"\"\"

            Config.create()
                creates a Config object with default settings, if "./conf/production.yaml"
                exists then this will be loaded

            Config.create(path="./configs",
                          conf="myconfig.yaml",
            )
                creates a Config object and load "./configs/myconfig.yaml"

            Config.create(path="./configs",
                          env="DEV",
            )
                creates a Config object and load "./configs/development.yaml"

            Config.create(required_config=REQUIRED_CONFIG_PARAMETERS,
            )
                creates a Config object loads a set of predefined required config parameters

        """
        obj = Config(path, conf, env, required_config, allowed_envvars)
        conf = obj.__create()
        return conf
