# for testing/demonstrating printerInterface
# see https://stackoverflow.com/a/15752645/3210158

from printerInterface import wait_for_print_job_info, job_status_string

if __name__ == '__main__':
  import time
  print('Type Ctrl+C to exit')
  try:
    while True:
      info = wait_for_print_job_info(timeout=0.25)
      if not info:
        continue
      for nd in info:
        job_id, key, value = nd
        if key == 'job_status':
          status_string = job_status_string(value)
          value = '%#010x (%s)' % (value, status_string)
        print('[%08x] %s: %s' % (job_id, key, value))
        time.sleep(.05)
      print('')
      time.sleep(.05)
  except KeyboardInterrupt:
    pass
