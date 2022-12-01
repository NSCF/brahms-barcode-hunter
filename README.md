# brahms-barcode-hunter

A web app utility for quickly looking up specimen records from BRAHMS. The records need to be extracted from BRAHMS first and added to a sqlite database file called brahms.sqlite (use makedb.py). The fields required from BRAHMS are Accession, Barcode, Sheets, Collector, AdditionalCollectors, FieldNumber, CalcShortCollectionDate, CollectionDay, CollectionMonth, CollectionYear, FamilyName, FullName, AcceptedName, Country, MajorAdmin, LocalityNotes.

To run the utility, pull the repo, get a build a copy of brahms.sqlite, and run `python server.py` in the command line.