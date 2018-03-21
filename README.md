# HTTP Server and Web Socket for CPEN 391

## INSTALLATION INSTRUCTIONS

Dependencies are managed through [pipenv](https://github.com/pypa/pipenv).


For Raspberry Pi:

We are using `python` = `3.4.4`
with:

    `tensorflow` = `1.1.0`
    `numpy` = `1.11.0`

This is due to the available pre-compiled Tensorflow wheel for Pi being `1.1.0`
which only supports `python 3.4.4`.
Unfortunately `numpy-extensions > 1.11.0` does not work properly on `python 3.4.4`
so we are locked to `numpy 1.11.0` for the time being as well.

1. Download the Tensorflow 1.1.0 wheel from [here](https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.1.0/tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl) and place it in the project root directory.
1. Edit the Pipfile:
    1. Comment out `tensorflow = "==1.1.0"`
    1. Comment out `opencv-python = "*"`
    1. Uncomment `"c0a73bc" = {path = "./tensorflow...whl"}`
1. run `pipenv install --skip-lock` 

For Linux:
1. Edit the Pipfile:
    1. Comment out `"c0a73bc" = {path = "./tensorflow...whl"}`
    1. Uncommment any other line
1. run `pipenv install --skip-lock` 

For Windows:
1. Check if your Python version is running on 64-bit arch, re-install if it isn't
    1. Run the following in a Python shell to check
        ```
        >>> import platform
        >>> platform.architecture()
        ```
1. Edit the Pipfile:
    1. Comment out `tensorflow = "==1.1.0"`
    1. Comment out `"c0a73bc" = {path = "./tensorflow...whl"}`
    1. Run `pipenv install`. Terminate if the last one hangs
        1. Run `pip install --upgrade tensorflow` if it hung
    1. Install the version of [Tensorflow](https://pypi.python.org/pypi/tensorflow) which corresponds to your environment. With `pipenv install <wheel_file_name>.whl`. 
        + `tensorflow-1.5.1-cp35-cp35m-win_amd64.whl (md5)`
            + `tensorflow-1.5.1`: Tensorflow version 1.5
            + `cp35`: for Python3.5
            + `win_amd64`: for Windows 64-bit. 

## RUNNING INSTRUCTIONS

1. Make sure the current shell is a virtualenv shell by running `pipenv shell` in the project root directory.
1. Run `python app.py -db` to set up database
1. Run `python app.py` to start server



