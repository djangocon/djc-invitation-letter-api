# djc invitation letter generator

To run locally, do the usual:
1. Create a Python 3.8 or greater virtualenv
2. Install dependencies:

```
pip install -r requirements.txt
```
3. Create a Google Cloud project [here](https://console.cloud.google.com/)
4. Enable Google Docs and Google Sheets APIs
5. Create a service account [direct link](https://console.cloud.google.com/iam-admin/serviceaccounts/create)
6. Create a new key (json) for the service account you created and download the json file.

:memo: **Note:** Add this to .gitignore should you add it to the project directory.

```bash
export GOOGLE_APPLICATION_CREDENTIALS="<PATH_TO_KEY>" 
```
### Google Drive
1. create a directory<br> 
eg. ```DJC_2025_Letters\templates\```
2. Upload your docs & sheets templates or create a template(refer to placeholders for both docs & sheets)
3. Get the respective ids and set them as environment variable


### Set Environment variable
`FOLDER_ID` = [Google Drive project parent folder id] <br>
`FILE_ID` = [ Google Docs file id ]<br>
`SPREADSHEET_ID` = [Google Sheets file id]

:memo: **Note:** Add the service account email to the google drive folder with ```Editor``` permission. eg. ```djc@xxxx.iam.gserviceaccount.com```

#### Placeholder in Google Docs
1. fullname
2. address
3. letterdate
4. passportno
5. dateofbirth
6. letter-content

#### Columns in Google Sheets
1. Timestamp
2. Fullname
3. Email
4. Download Link


### Run API
```bash
uvicorn main:app --reload        
```




**Attendee Payload**
``` json

{
    "fullname": "Django Conference",
    "address": "125 32nd Street, San Diego, California, USA",
    "dob": "May 25, 1950",
    "email": "djc@django.com",
    "passport_no": "DJC6003434",
}
```


**Opportunity Grant Recipient Payload**
``` json

{
    "fullname": "Django Conference",
    "address": "125 32nd Street, San Diego, California, USA",
    "dob": "May 25, 1950",
    "email": "djc@django.com",
    "passport_no": "DJC6003434",
     "letteropt":{
        "key":"og",
        "value": "1234.00"
    }
}
```
**Speaker Payload**
``` json

{
    "fullname": "Django Conference",
    "address": "125 32nd Street, San Diego, California, USA",
    "dob": "May 25, 1950",
    "email": "djc@django.com",
    "passport_no": "DJC6003434",
     "letteropt":{
        "key":"speaker",
        "value": "Django is the best framework!"
    }
}
```
