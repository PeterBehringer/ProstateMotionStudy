import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('/Users/peterbehringer/Desktop/My_Project-439dfbf5191c.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gc = gspread.authorize(credentials)

wks = gc.open("https://docs.google.com/spreadsheets/d/1um9MhzkpQoY3MfO15vgRI5YevvE2hz1KYiwumBAQXIM/edit#gid=968190622").sheet1

