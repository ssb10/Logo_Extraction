# Logo Extraction

This program extracts url of website logo given a website's url.

# Getting started

This program will work for Python 3 and above. Download the logo extraction folder on your local machine.

## Prerequistes

This program requires you to install [selenium](https://pypi.org/project/selenium/) package.
Installation instructions can be found [here](https://selenium-python.readthedocs.io/installation.html). 
*(Note:There are specific instructions for Windows users.)*

In general, running the following command in commandline should install selenium successfully. *(Assuming pip is already installed.)*

```console
pip install selenium
```

A headless browser is used to fetch webpage content. The program uses firefox driver (It comes by default with the Selenium package)
The headless browser needs geckodriver which can be found [here](https://github.com/mozilla/geckodriver/releases).
Based on the machine that you are using download the driver.

## Config file

Mention the location of geckodriver.


# Running the script

## logo_extraction.py

This file performs the logo extraction task. It accepts the input file from command line.

To the run the file:
1. Open command prompt (The application is tested on anaconda command prompt) and cd to the logo extraction directory.
2. Use the command:

```console
python logo_extraction.py /path/to/your/input file/your_input_file.txt
```

The output would be written to a file in the same directory. The name of the output file will be *****.
The output format is website url, logo_url.
For some websites the logo might be just stylized text. In such cases, the logo url will be blank.


# Running tests

## logo_extraction_test.py
1. Open command prompt (The application is tested on anaconda command prompt) and cd to the logo extraction directory.
2. Use the command:

```console
python -m unittest logo_extraction_test.py
```

# Interpreting logs

The log is present in logo_extraction.log file. The log file will be stored in the same directory.
The log shows information about number of urls processed, logo url sources by tags and errors like invalid urls.

Apart from the log generated by the script, geckodriver has its own log named geckodriver.log, which will be in the same directory.
This log can be referred to for additional information.


