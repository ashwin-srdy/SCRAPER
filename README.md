This repositorty contains the following models.

--> MODEL 1:
---------
* To split large excel sheets into smaller files, each file having 100 entries.

#### Things to remember:
--------------------
* INPUT: excel file (.XLSX)
* OUTPUT: Multiple excel files in the folder 'SPLIT_DATASETS' present in the same location of model.
* The Excel file must and should contain only the names of the companies in the first column without any column name. (Image pasted below for reference)
![image](https://user-images.githubusercontent.com/66512139/197240348-345e1404-c575-4322-afab-b38c0b6bc3a2.png)
* python must be installed.


--> MODEL 2:
--------
This model scrapes the following data for each entry of the input excel file.
* Company Name
* Company Status
* Date of Incorporation
* Activity
* Email

#### Things to remember:
--------------------
* INPUT: excel file (.XLSX) having 100 entries. Model won't consider entries from the same file after 100 entries are scraped at a time.
* OUTPUT: Multiple excel files in the folder 'SPLIT_DATASETS' present in the same location of model. (Image below for reference)
![image](https://user-images.githubusercontent.com/66512139/197241688-682a0edb-a95e-4cf6-9d04-dd623ed92437.png)
* There will be three output files (EXCEL SHEETS) one containing above mentioned data and other two files containing names of companies for which emails, no data was found. (Image below for reference)
![image](https://user-images.githubusercontent.com/66512139/197242261-028c940c-e4e0-4d48-bde1-a60282603ce7.png)
* Expected time to scrape for 100 entries is 1 - 2 hrs depending on internet speed.
* python must be installed.

--> HOW TO DOWNLOAD & RUN MODELS:
------------------------------
* Click on 'Code' option and 'download as ZIP' as shown in below image.
![image](https://user-images.githubusercontent.com/66512139/197242817-19479d2e-e8cc-4e89-822f-b6b5d1bde49b.png)
* Extract the ZIP file to any location.

## RUNNING MODEL 1:
================
* Open the folder 'MODEL 1 (EXCEL SPLITTER)' and in the address bar type 'cmd' to open command prompt.
![image](https://user-images.githubusercontent.com/66512139/197246546-48e56fcc-4afd-43ee-b48b-866c7e3b4887.png)
##### Type in following commands
* pip install -r requirements.txt
* python script.py
![image](https://user-images.githubusercontent.com/66512139/197246853-f60a26cd-600a-4731-acca-3bc4b8c7602a.png)
* Now copy the link provided i.e. 'http://127.0.0.1:8000' and paste in the browser to open the UI.
![image](https://user-images.githubusercontent.com/66512139/197247121-ac6f3302-7be0-4034-ae0b-32cc92d190d8.png)
* Now upload an excel sheet using 'Choose File' button and click on 'Upload'
* The saved files will be available in the same folder 'MODEL 1 (EXCEL SPLITTER)\SPLIT_DATASETS' 
![image](https://user-images.githubusercontent.com/66512139/197247532-45c7e0c1-0ddc-483c-bb9a-0b69f675db70.png)

## RUNNING MODEL 2:
================
* Open the folder 'MODEL 2 (SCRAPER)' and in the address bar type 'cmd' to open command prompt.
##### Type in following commands
* pip install -r requirements.txt
* python script.py
* Now copy the link provided i.e. 'http://127.0.0.1:8000' and paste in the browser to open the UI.
* Now upload an excel sheet using 'Choose File' button and click on 'Upload'
* The progress will be shown in the cmd.
![image](https://user-images.githubusercontent.com/66512139/197250028-328c08eb-465b-4d61-804f-22df128b2591.png)
* The saved files will be available in the same folder 'MODEL 2 (SCRAPER)\output'
![image](https://user-images.githubusercontent.com/66512139/197248527-5907b9b1-6d94-42f7-add7-dd6f088df496.png)
* You'll hear 3 beeps once the scraping process is done.
