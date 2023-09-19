#get the list of barcodes from the imaging spreadsheets
# note that only spreadsheets that conform to the naming standard are read (ie date string)
# also note that the code for getting unique barcodes needs to be edited per herbarium

from __future__ import print_function

import os.path
import re
import csv
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DRIVE_FOLDER_ID = '1o3MmDQcb1IC5VUKPORo2yEdxL_8-a-89'

# If modifying these scopes, delete the file token.json.
SCOPES = [
  'https://www.googleapis.com/auth/spreadsheets.readonly',
  'https://www.googleapis.com/auth/drive.metadata.readonly'
]

def main():

  print('authenticating...')
  #authenticate
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open('token.json', 'w') as token:
        token.write(creds.to_json())

  try:
    drive = build('drive', 'v3', credentials=creds)
    sheets = build('sheets', 'v4', credentials=creds)

    # Warm up the Sheets API
    sheetService = sheets.spreadsheets()

    folderMimeType = 'application/vnd.google-apps.folder'
    q = f"mimeType = '{folderMimeType}' and trashed = false and parents in '{DRIVE_FOLDER_ID}'"
    folders = drive.files().list(q=q, fields='files(id, name)').execute()

    barcodesSet = set()
    recordCounter = { 'count': 0 }
    barcodeSheetsIndex = {}
    zeros = []
    errors = {}
    for folder in folders['files']:
      processFolder(drive, sheetService, folder['name'], folder['id'], barcodesSet, recordCounter, barcodeSheetsIndex, zeros, errors)

    if len(zeros) > 0:
      print('the following files have no unique barcodes:')
      print('; '.join(zeros))

    if len(errors) > 0:
      print('there were the following errors reading files:')
      for key, value in errors.items():
        print(key + ': ' + str(value))
    else:
      print('all folders and sheets successfully processed')


    print(len(barcodesSet), 'unique barcodes were found, saving to file...')
    barcodesSet = list(barcodesSet)
    barcodesSet.sort()
    with open('uniqueBarcodes.csv', 'w', encoding='UTF8', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(['barcode'])
      for barcode in barcodesSet:
        writer.writerow([barcode])
    
    
    with open('barcodesIndex.csv', 'w', encoding='UTF8', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(['barcode', 'files'])
      for key, value in barcodeSheetsIndex.items():
        writer.writerow([key, '|'.join(value)])
    
    print('all done, see uniqueBarcodes.csv and barcodesIndex.csv')
      
  except HttpError as err:
    print(err)


def processFolder(drive, sheetService, folderPath, folderID, barcodesList, recordCounter, barcodeSheetsIndex, zeros, errors):
  print('processing contents of', folderPath)
  
  folderMimeType = 'application/vnd.google-apps.folder'
  sheetMymeType = "application/vnd.google-apps.spreadsheet"
 
  #first get all the contents of the folder
  try:
    result = drive.files().list(q=f"parents in '{folderID}'", fields='files(id, name, mimeType)').execute()
  except Exception as ex:
    errors[folderPath] = ex
    return

  for item in result['files']:
    if item['mimeType'] == folderMimeType:
      newFolderPath = folderPath + '/' + item['name']
      processFolder(drive, sheetService, newFolderPath, item['id'], barcodesList, recordCounter, barcodeSheetsIndex, zeros, errors)
    elif item['mimeType'] == sheetMymeType and re.match('[0-9]{8}', item['name']): #we only read spreadsheets here that conform to the naming standard
      time.sleep(1) #we can't overload the sheets api
      processSheet(sheetService, item['id'], item['name'], folderPath, barcodesList, recordCounter, barcodeSheetsIndex, zeros, errors)
    
  return

def processSheet(sheetService, sheetID, sheetName, folderPath, barcodesList, recordCounter, barcodeSheetsIndex, zeros, errors):
  
  RANGE = 'barcodes' #barcodes spreadsheet, all cells
  try:
    result = sheetService.values().get(spreadsheetId=sheetID, range=RANGE).execute()
  except Exception as ex:
    print('could not read', folderPath + '/' + sheetName)
    errors[folderPath + '/' + sheetName] = ex
    return
  
  rows = result.get('values', [])

  if not rows:
    print('No data found.')
    return

  barcodeFieldIndex = None
  counter = 0
  for row in rows:
    if barcodeFieldIndex == None:
      try:
        barcodeFieldIndex = row.index('barcode')
        continue
      except ValueError as ex:
        print('no barcode field found, please check the file')
        return
    
    if len(row) <= barcodeFieldIndex:
      continue
    barcode = row[barcodeFieldIndex]
    if barcode is not None and barcode.strip() != '':
      barcode = re.split('[_-]', barcode.strip())[0] #NB this has to change depending on the barcoding formatting rules of the herbarium...
      recordCounter['count'] += 1

      #update the index
      if barcode in barcodeSheetsIndex:
        barcodeSheetsIndex[barcode].add(folderPath + '/' + sheetName)
      else:
        barcodeSheetsIndex[barcode] = set()
        barcodeSheetsIndex[barcode].add(folderPath + '/' + sheetName)

      if barcode not in barcodesList:
        counter += 1
        barcodesList.add(barcode)

  if counter > 0:  
    print(counter, 'barcodes added from', sheetName)
  else:
    zeros.append(folderPath + '/' + sheetName)

  return

if __name__ == '__main__':
  main()