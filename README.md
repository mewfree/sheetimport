# SheetImport

Allows to import local CSV files into Google Spreadsheet, returning a new Google Sheet URL.

[Create a new Google Cloud project](https://console.cloud.google.com/projectcreate) with the Google Sheets API activated.
Place the generated `credentials.json` in the same directory as `sheetimport.py`.

Import CSV by either referencing the file as a parameters:
`python3 sheetimport.py example.csv`

Or by piping the file to the script:
`cat example.csv | python3 sheetimport.py`
