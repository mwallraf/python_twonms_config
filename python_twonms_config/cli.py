"""Console script for python_twonms_config."""

import fire


def help():
    print("python_twonms_config")
    print("=" * len("python_twonms_config"))
    print("Python package to manage configs based on OmegaConf")


def main():
    fire.Fire({"help": help})


if __name__ == "__main__":
    main()  # pragma: no cover
