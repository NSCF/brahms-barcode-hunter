# brahms-barcode-hunter

A web app utility for quickly looking up specimen records from BRAHMS. 

### Requirements
You will need to have [git](https://git-scm.com/downloads) and [Python](https://www.python.org/downloads/) installed on your computer first. 

When installing Python make sure to select 'Add to PATH' on the first installation window. 

After installing, open a command window and test each program installed properly using the following commands:

`python --version`
`git --version`

If installation was successful, each will show the version installed in the command window. 

If you're unfamiliar with the command line take [10mins to watch this tutorial video](https://youtu.be/MBBWVgE0ewk).

You will also need `pip`, the Python package installer to be included on your PATH. [Follow these instructions](https://www.alphr.com/pip-is-not-recognized-as-an-internal-or-external-command/) if you don't have it already.

### Installation
After installing the programs above, create a folder in your C drive called `devprojects`. Open that folder, and in the address bar type `cmd`. This opens a command window in that folder. Run each of the following commands to install the utility:

`git clone https://github.com/NSCF/brahms-barcode-hunter.git`

`cd brahms-barcode-hunter`

`pip install -r requirements.txt`

You only have to run all these steps the first time you install the tool. 

### Updating
To update the tool run the following command in the brahms-barcode-hunter folder:

`git pull`

Then run start the server again. 

### Database
This utility needs a sqlite file containing the BRAHMS records to search. The records need to be extracted from BRAHMS first and added to a sqlite database file called brahms.sqlite. The fields required from BRAHMS8 are Accession, Barcode, Collector, FieldNumber, CollectionDay, CollectionMonth, CollectionYear, FamilyName, FullName, AcceptedName, Country, MajorAdmin, LocalityNotes

If using BRAHMS7 make sure to rename the extracted fields to be exactly as above before importing into sqlite (they are case sensitive). 

Extract these fields and save as a .csv file in the brahms-barcode-hunter folder. Open the file makedb.py in a text editor like Notepad and change the datafile parameter to the name of your csv file (just replace what's in the quotes), and save makedb.py. Then on the command line run:

`python makedb.py`

This will import the data into sqlite. It takes around an hour to transfer 1M records. 

If several people will be using the utility with the same database, you can copy the .sqlite file to each of their computers, you don't have to run makedb.py for each one.

### Using the barcode-hunter tool
After following all the above steps you are ready to run the tool. It runs locally on your machine, in a web browser. No data is transferred over the internet. To start it run the following command in a command window opened in the brahms-barcode-hunter folder:

`python server.py`

This will start a local server and open a browser tab and with a set of fields you can use to search the database. It's best to search on the accession number if you have one, followed by the collector name and collector number, followed by other fields. You have to search for a combinations of fields. Searching on a single field other than accession won't work.

Note that for the taxon name you can use the first three letters of the genus and species name, you don't have to type out the full name, e.g. 'Aca scu' = 'Acanthopsis scullyi'.

To shutdown open the command window where you ran the command above and press `Ctrl + C`. This will shutdown the server, and you can close the browser tab. Next time you want to run the tool you only need to run `python server.py` again. 

## Taxon names

The newer versions of this tool also allow for taxon names to be found quickly, using the 'Name Search' link at the top right of the barcode hunter page. That takes you to a new page with a single search box and a dropdown for searching the SANBI checklist or WFO for names. To use the SANBI checklist, you need an extract from the SANBI taxon backbone (the SA National Plants Checklist) with fields 'fullname', 'guid', 'status', and 'acceptedname' (case is important, rename fields if necessary). Update the file path and name in addtaxatodb.py and run that file to create the taxa.sqlite database file. Then the SANBI option can be used in the Name Search. 