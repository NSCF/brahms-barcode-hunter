# for testing/demonstrating printerInterface
# see https://stackoverflow.com/a/15752645/3210158

from printerInterface import wait_for_print_job

if __name__ == '__main__':
  print('Type Ctrl+C to exit')
  counter = 0
  try:
    while True:
      info = wait_for_print_job()
      if not info:
        continue
      counter +=1 
      print(counter)
  except KeyboardInterrupt:
    pass
