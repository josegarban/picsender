#picsender2

### Before doing anything:
1. Make sure pictures have been saved to folder Fotos.
2. Save personal data to datos.xlsx.
3. Review emailtemplate.html.
4. Set up application key in Google.

### Set up virtual environment
>> py -3.8 -m venv picenv
### Activate virtual environment
>> picenv\Scripts\Activate
### Install requirements
>> pip install -r requirements.txt
### Set up database
>> python createdb.py
### Send emails
>> python picsender.py

### After having sent emails
5. Wait a few days for feedback from customers.
6. Correct any wrong data in datos.xlsx.
7. Delete all files from your computer.