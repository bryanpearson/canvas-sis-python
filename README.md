# canvas-sis-python
Canvas SIS API integration using Python Requests Library

## General Information

Documentation on the SIS import API itself: <https://canvas.instructure.com/doc/api/sis_imports.html>

Documentation on the required format for the files you import: <https://canvas.instructure.com/doc/api/sis_csv.html>

## Requests Library

This example makes use of the [Requests](http://docs.python-requests.org/) library, a Python HTTP library "written for human beings". As of this writing, Requests is supported in Python versions 2.6 to 3.3. 

Instructions for installing Requests can be found [here](http://docs.python-requests.org/en/latest/user/install/). If you'd like to learn more about how to use the library itself, take a look at the [Quickstart Guide](http://docs.python-requests.org/en/latest/user/quickstart/).

## Using the Script

### Set static variables
This script allows you to both submit an SIS import and check the status of imports that you've already run. Before you can submit an initial request you'll need to replace the code enclosed in angle brackets with your own data, and adjust sleep timeout and job watch maximums.

    logdir =  '<WRITABLE_LOG_DIRECTORY>' # Example: /var/log/canvas/
    logfilename =  '<LOG_FILE_NAME>' # Example: canvas_sis.log
    
    # 1. Define standard variables
    base_url = '<MY_BASE_URL>' # Example: https://bleh.test.instructure.com/api/v1/accounts/'
    account_id = '<MY_ACCOUNT_ID>' # Example: 12
    header = {'Authorization' : 'Bearer <MY_ACCESS_TOKEN>'}
    sleep_timeout = 60 # Amount of time to wait between checking API for task progress
    job_watch_max_counter = 60 # Maximum times to check API for job progress before quitting

* `<WRITABLE_LOG_DIRECTORY>`: Directory where log files should be created/stored
* `<LOG_FILE_NAME>`: Name of log file to create and update. Example: canvas_sis.log
* `<MY_BASE_URL>`: From the example, replace "mysubdomain" with the subdomain for your Canvas instance.
* `<MY_ACCOUNT_ID>`: The account ID for your Canvas instance. This number is visible in the URL address when accessing Canvas, immediately following "accounts/".
* `<MY_ACCESS_TOKEN>`: If you're unsure of how to generate this, review [this](https://canvas.instructure.com/doc/api/file.oauth.html) page of the Canvas API, under "Manual Token Generation".
* `sleep_timeout`: If argument 3 is true, this sets the amount of time to wait between checking API for job progress. Default: 60 seconds.
* `job_watch_max_counter`: If argument 3 is true, this sets the maximum number of times the script will check the API for job progress. Once `job_watch_max_counter` is reached, script will log event and quit. Default: 60.

### Script arguments
The script requires 3 arguments. 

1. Full or relative path to file containing Canvas data. `csv` or `zip` files allowed.
2. Type of file passed in argument 1. `csv` or `zip` files allowed.
3. Continue to monior `true` or `false` allowed. 

### Running the script (submit a file to the Canvas API)
Run the script with the three required arguments. Script output will be logged to log file.

**Example: submit CSV, log job progress**

`python canvas_sis_import.py /my/directory/canvasdata.csv csv true`

**Example: submit ZIP file, do not log job progress**

`python canvas_sis_import.py /my/directory/canvasdata.zip zip false`

### Logged information









