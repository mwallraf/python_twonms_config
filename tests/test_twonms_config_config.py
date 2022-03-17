#!/usr/bin/env python
"""Tests for `python_twonms_config` package."""
# pylint: disable=redefined-outer-name

from unittest import TestCase

import pytest
from omegaconf import DictConfig, OmegaConf
from twonms.config import Config


class TestCreateConfig:
    """Tests for creating a twonms.config.config.Config object"""

    def test_create_without_parameters_and_config_file(self):
        """Creates an empty object without parameters or any
        config files present

        should return an OmegaConf object type
        """
        config = Config.create()
        assert (
            type(config) == DictConfig
        ), "an OmegaConfg DictConfig object was expected"

    def test_create_without_parameters_and_default_config_file(self):
        """Creates an empty object without parameters or any
        config files present

        should return an OmegaConf object type
        """
        config = Config.create()
        assert (
            type(config) == DictConfig
        ), "an OmegaConfg DictConfig object was expected"
