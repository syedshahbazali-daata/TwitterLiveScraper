import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds_sheet = ServiceAccountCredentials.from_json_keyfile_name(
    r"GoogleSheetsApi.json", scope)
client = gspread.authorize(creds_sheet)
sheet_url = "https://docs.google.com/spreadsheets/d/1yG75p7o31NLTdZByLhXZBQyU9LrIS2Nzps5iUU6mAWU/edit?usp=sharing"
sheet = client.open_by_url(sheet_url).sheet1

def add_row(row_data: list):
  sheet.insert_row(row_data, 2)
