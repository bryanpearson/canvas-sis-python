#!/usr/bin/python
import sys
import requests
import json
import logging
import time

LOGDIR =  '<WRITABLE_LOG_DIRECTORY>' # Example: /var/log/canvas/
LOGFILENAME =  '<LOG_FILE_NAME>' # Example: canvas_sis.log
TIMESTAMP = time.strftime("%Y%m%d")
logging.basicConfig(format='%(asctime)s cron canvas/sis: %(levelname)s %(message)s', datefmt='%b %d %H:%M:%S', filename=LOGDIR + LOGFILENAME + TIMESTAMP, level=logging.DEBUG)


# 1. Define standard variables
base_url = '<MY_BASE_URL>' # Example: https://mysubdomain.test.instructure.com/api/v1/accounts/'
account_id = '<MY_ACCOUNT_ID>' # Example: 12
header = {'Authorization' : 'Bearer <MY_ACCESS_TOKEN>'}
sleep_timeout = 60 # Amount of time to wait between checking API for task progress
job_watch_max_counter = 60 # Maximum times to check API for job progress before quitting


def main(argv):
  if len(argv) == 3 and argv[1] in ['csv', 'zip'] and argv[2] in ['true', 'false']:
    try:
      logging.info("### CANVAS API SCRIPT STARTED ###")
      logging.info("File argument: %s, file type: %s, watch job: %s" % (argv[0], argv[1], argv[2]))
      payload = {'import_type' : 'instructure_csv', 'extension' : argv[1]}
      
      # 2. Read file provided by first argument in list
      data = open(argv[0], 'rb').read()

      # 3. Submit file to Canvas API, pull job_id from json response
      initial_request = requests.post(base_url + account_id + "/sis_imports/", headers=header, params=payload, data=data)
      initial_json = json.loads(initial_request.text)
      logging.info(initial_json)
      job_id = str(initial_json['id'])

      # 4. Use API to check job_id progress, if third agument = 'true'
      if argv[2] == 'true':
        counter = 0
        while True:
          time.sleep(sleep_timeout)
          counter = counter + 1
          logging.info("Slept %s minutes. Checking job %s progress now." % (counter, job_id))

          # 5. Make API request, pull parameters from json response
          progress_request = requests.get(base_url + account_id + "/sis_imports/" + job_id, headers=header)
          progress_json = json.loads(progress_request.text)
          ended_at = progress_json['ended_at']
          workflow_state = progress_json['workflow_state']
          logging.info("Workflow_state state is: '%s'" % workflow_state)

          # 6. Stop while loop if job has ended, or max number of checks reached
          if ended_at:
            logging.info("Canvas API SIS import complete. Logging json from canvas")
            logging.info(progress_json)
            break
          if counter > job_watch_max_counter:
            logging.info("Counter reached 60 minutes, manually quitting job monitoring")
            break

      logging.info("### CANVAS API SCRIPT FINISHED ###")
    except Exception, e:
      logging.exception(e)
      sys.exit()
  else:
    print "\nusage: import_csv.py <PATH_TO_CSV_OR_ZIP> <FILE_TYPE (zip/csv)> <LOG_JOB_PROGRESS (true/false)>\n"

if __name__ == "__main__":
  main(sys.argv[1:])
