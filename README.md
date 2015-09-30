# canvas-sis-python
Canvas SIS API integration using Python Requests Library


## General Information
Relied heavily on the following project for initial structure and assistance: <a href="https://github.com/kajigga/canvas-contrib/tree/master/SIS%20Integration/python_requestlib" target="_blank">kajigga/canvas-contrib</a>

Documentation on the SIS import API itself: <https://canvas.instructure.com/doc/api/sis_imports.html>

Documentation on the required format for the files you import: <https://canvas.instructure.com/doc/api/sis_csv.html>


## Requests Library
This example makes use of the [Requests](http://docs.python-requests.org/) library, a Python HTTP library "written for human beings". As of this writing, Requests is supported in Python versions 2.6 to 3.3. 

Instructions for installing Requests can be found [here](http://docs.python-requests.org/en/latest/user/install/). If you'd like to learn more about how to use the library itself, take a look at the [Quickstart Guide](http://docs.python-requests.org/en/latest/user/quickstart/).


## Using the Script
### Set static variables
This script allows you to both submit an SIS import and check the status of imports that you've already run. Before you can submit an initial request you'll need to replace the code enclosed in angle brackets with your own data, adjust sleep timeout and job watch maximums, and set any parameters for your particular setup.

* `<WRITABLE_LOG_DIRECTORY>`: Directory where log files should be created/stored
* `<LOG_FILE_NAME>`: Name of log file to create and update. Example: canvas_sis.log
* `<MY_BASE_URL>`: From the example, replace "mysubdomain" with the subdomain for your Canvas instance.
* `<MY_ACCOUNT_ID>`: The account ID for your Canvas instance. This number is visible in the URL address when accessing Canvas, immediately following "accounts/".
* `<MY_ACCESS_TOKEN>`: If you're unsure of how to generate this, review [this](https://canvas.instructure.com/doc/api/file.oauth.html) page of the Canvas API, under "Manual Token Generation".
* `watch_job`: If `True`, the script will call the API and log the status of the import, using `sleep_timeout` and `job_watch_max_counter` values. If `False`, the script stops after it's submitted the files to the Canvas API endpoint.
* `sleep_timeout`: If `watch_job` `True`, this sets the amount of time to wait between checking API for job progress. Default: 60 seconds.
* `job_watch_max_counter`: If argument 3 is true, this sets the maximum number of times the script will check the API for job progress. Once `job_watch_max_counter` is reached, script will log event and quit. Default: 60.
* `params['import_type']`: See instructure documentation for the following properties and definitions.
* `params['extension']`
* `params['batch_mode']`
* `params['batch_mode_term_id']`
* `params['batch_mode_term_id']`
* `params['batch_mode_term_id']`


### Script arguments
The script requires 1 argument, a full or relative path to file containing Canvas data. `csv`, `xml` or `zip` files allowed.


### Running the script (submit a file to the Canvas API)
Run the script with the required file argument. Script output will be logged to log file. Example (after updating `watch_job` and `params` as needed):
`python canvas_sis_import.py /my/directory/canvasdata.csv`


### Logging example
    Apr 18 06:25:04 cron canvas/sis: INFO ### CANVAS API SCRIPT STARTED ###
    Apr 18 06:25:04 cron canvas/sis: INFO File argument: /var/canvas_dumps/lms_daily.zip, file type: zip, watch job: true
    Apr 18 06:25:04 cron canvas/sis: INFO Starting new HTTPS connection (1): mydomain.instructure.com
    Apr 18 06:25:06 cron canvas/sis: DEBUG "POST /api/v1/accounts/1/sis_imports/?import_type=instructure_csv&extension=zip HTTP/1.1" 200 144
    Apr 18 06:25:06 cron canvas/sis: INFO {u'ended_at': None, u'workflow_state': u'created', u'created_at': u'2014-04-18T13:25:05Z', u'updated_at': u'2014-04-18T13:25:06Z', u'progress': 0, u'data': {u'import_type': u'instructure_csv'}, u'id': 141}
    Apr 18 06:26:06 cron canvas/sis: INFO Slept 1 minutes. Checking job 141 progress now.
    Apr 18 06:26:06 cron canvas/sis: INFO Starting new HTTPS connection (1): mydomain.instructure.com
    Apr 18 06:26:07 cron canvas/sis: DEBUG "GET /api/v1/accounts/1/sis_imports/141 HTTP/1.1" 200 188
    Apr 18 06:26:07 cron canvas/sis: INFO Workflow_state state is: 'importing'
    Apr 18 06:27:07 cron canvas/sis: INFO Slept 2 minutes. Checking job 141 progress now.
    Apr 18 06:27:07 cron canvas/sis: INFO Starting new HTTPS connection (1): mydomain.instructure.com
    Apr 18 06:27:10 cron canvas/sis: DEBUG "GET /api/v1/accounts/1/sis_imports/141 HTTP/1.1" 200 189
    Apr 18 06:27:10 cron canvas/sis: INFO Workflow_state state is: 'importing'
    Apr 18 06:28:14 cron canvas/sis: INFO Slept 3 minutes. Checking job 141 progress now.
    Apr 18 06:28:14 cron canvas/sis: INFO Starting new HTTPS connection (1): mydomain.instructure.com
    Apr 18 06:28:15 cron canvas/sis: DEBUG "GET /api/v1/accounts/1/sis_imports/141 HTTP/1.1" 200 321
    Apr 18 06:28:15 cron canvas/sis: INFO Workflow_state state is: 'imported_with_messages'
    Apr 18 06:28:15 cron canvas/sis: INFO Canvas API SIS import complete. Logging json from canvas
    Apr 18 06:28:15 cron canvas/sis: INFO {u'ended_at': u'2014-04-18T13:27:29Z', u'workflow_state': u'imported_with_messages', u'created_at': u'2014-04-18T13:25:05Z', u'updated_at': u'2014-04-18T13:31:29Z', u'processing_warnings': [[u'users.csv', u'Improper status for user 9C4544']], u'progress': 100, u'data': {u'import_type': u'instructure_csv', u'counts': {u'terms': 0, u'users': 3839, u'grade_publishing_results': 0, u'abstract_courses': 0, u'group_memberships': 0, u'courses': 4145, u'accounts': 0, u'xlists': 10, u'groups': 0, u'enrollments': 50, u'sections': 4145}, u'supplied_batches': [u'course', u'section', u'xlist', u'user', u'enrollment']}, u'id': 141}
    Apr 18 06:28:15 cron canvas/sis: INFO ### CANVAS API SCRIPT FINISHED ###
