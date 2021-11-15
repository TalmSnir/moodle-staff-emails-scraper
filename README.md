
# Staff emails scraper

scrape all of the staff's emails and names from your available courses and write them into a csv file.

(there is an option in the script to write to a google drive sheet- enabling google drive api and sheets api is needed)



## Resources

* [selenium with python docs](https://selenium-python.readthedocs.io/)  
* [Google sheets API](https://developers.google.com/sheets/api)  


## Tech Stack

**Client:** Python, Selenium



## Run Locally

Clone the project

```bash
  git clone git@github.com:TalmSnir/moodle-staff-emails-scraper.git
```

Go to the project directory

```bash
  cd moodle-staff-emails-scraper
```
install selenium using pip

```bash
pip install selenium
```

[Download selenium web driver](https://sites.google.com/chromium.org/driver/) and add the exe file to the project directory

Enter your Moodle login data in the scraper.py file 

```python
   username = 'your_Moodle_username' 
   user_id = 'your_Moodle_id'
   user_password = 'your_Moodle_password'
```

To enable writing the data to Google sheet you must have a Google Sheet API token-
[get a Google sheet token](https://developers.google.com/sheets/api/quickstart/python)
read the quickstart and do as it says to enable the API

uncomment the next lines in scarper.py to enable the functionallity of the sheet.py file
```python
  import sheet

  sheet.write_to_sheet(teacher_name, teacher_email_address[0])
```

Run the script 

```bash
  python -m scraper
```

