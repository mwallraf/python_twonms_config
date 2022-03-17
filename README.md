# Python 2NMS config manager

<p align="center">
<a href="https://pypi.python.org/pypi/python_twonms_config">
    <img src="https://img.shields.io/pypi/v/python_twonms_config.svg"
        alt = "Release Status">
</a>

<a href="https://github.com/mwallraf/python_twonms_config/actions">
    <img src="https://github.com/mwallraf/python_twonms_config/actions/workflows/release.yml/badge.svg?branch=release" alt="CI Status">
</a>

<a href="https://mwallraf.github.io/python_twonms_config/">
    <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" alt="Documentation Status">
</a>

</p>

Python package to manage application configurations. This is a wrapper around the OmegaConf create function.

This package makes it easy to define parameters for your application. It's possible to define parameters in different ways (in order of precedence):

-   programmatically defined default values
-   environment variables/dotenv files
-   configuration files in YAML format
-   cli arguments

## Documentation

Check out the [Github Docs](https://mwallraf.github.io/python_twonms_config/)

## Features

-   generates an [OmegaConf](https://omegaconf.readthedocs.io) dictionary object
-   supports environment variables
-   supports dotenv
-   reads yaml config files
-   supports cli parameters
-   allows programmatic initialization of parameters

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.
