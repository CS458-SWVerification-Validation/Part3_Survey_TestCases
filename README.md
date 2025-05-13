# Part3_Survey_TestCases

This is the Selenium Tester for CS458 Project.

# Getting Started

> [!WARNING]
> (For Windows) If Visual Studio Code is the used\
> IDE, it is advised to use CMD instead of PowerShell\
> since if the required permissions are not given\
> to PowerShell it will not run the scripts that are \
> needed for the next steps.

## Cloning Repository

This step clones the project repository onto your\
local machine.

```bash
git clone https://github.com/CS458-SWVerification-Validation/Part3_Survey_TestCases.git
```

## Python Virtual Environment Setup

Python virtual environment used to both install\
dependencies and run the tester on, which\
provides a clean and isolated development environment for Python\
projects easing the management process.

For Windows:
```bash
cd Part3_Survey_TestCases
python -m venv env
.\env\Scripts\activate
```

For Linux/MacOS:
```bash
cd Part3_Survey_TestCases
python -m venv env
source env/bin/activate
```

If '(env)' is seen at the start of the command line\
the first part of the setup is complete.

## Dependency Installation

This command installs all the necessary dependencies\
for the project to run. After the installation only\
database setup remains.

```bash
pip install -r requirements.txt
```

## Running the Selenium Tester

This command is used to run the code on the development environment.\
Just make sure that Flask application also runs on the background\
before executing this command.

```bash
python sel_login_test.py
```

Now the Selenium Tester would be able to run the webdriver\
to execute the automated tests on Flask application that runs\
on https://validsoftware458.com.tr:8443/
