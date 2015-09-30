#!/usr/bin/python
import sys
import requests
import json
import logging
import time

logdir =  '<WRITABLE_LOG_DIRECTORY>' # Example: /var/log/canvas_sis/
logfilename =  '<LOG_FILE_NAME>' # Example: 'canvas_sis.log.'
timestamp = time.strftime("%Y%m%d")
logging.basicConfig(format='%(asctime)s cron canvas/sis: %(levelname)s %(message)s', datefmt='%b %d %H:%M:%S', filename=logdir + logfilename + timestamp, level=logging.DEBUG)


# 1. Define standard variables
base_url = '<MY_BASE_URL>' # Example: https://mysubdomain.test.instructure.com/api/v1/accounts/'
account_id = '<MY_ACCOUNT_ID>' # Example: 1
header = {'Authorization' : 'Bearer <MY_ACCESS_TOKEN>'}

watch_job = True # Watch progress of Canvas SIS import
sleep_timeout = 60 # In seconds. Amount of time to wait between checking API for task progress
job_watch_max_counter = 60 # Maximum times to check API for job progress before quitting

params = {} # dict of options sent in POST request
params['import_type'] = 'instructure_csv' # String: instructure_csv is only option
params['extension'] = 'zip' # String: zip, xml or csv
# params['batch_mode'] = '' # Boolean
# params['batch_mode_term_id'] = '' # String
# params['diffing_data_set_identifier'] = '' # String, ex: 'campus_daily_import'
# params['diffing_remaster_data_set'] = '' # Boolean



def main(argv):
  if len(argv) == 1:
    try:
      logging.info("### CANVAS API SCRIPT STARTED ###")
      logging.info("File argument: %s, Post Params: %s" % (argv[0], params))
      
      # 2. Read file provided by first argument in list
      data = open(argv[0], 'rb').read()

      # 3. Submit file to Canvas API, pull job_id from json response
      initial_request = requests.post(base_url + account_id + "/sis_imports/", headers=header, params=params, data=data)
      initial_json = json.loads(initial_request.text)
      logging.info(initial_json)
      job_id = str(initial_json['id'])

      # 4. Use API to check job_id progress, if third agument = 'true'
      if watch_job:
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
    print "\nusage: canvas_sis_import.py <PATH_TO_CSV_OR_ZIP>\n"

if __name__ == "__main__":
  main(sys.argv[1:])
