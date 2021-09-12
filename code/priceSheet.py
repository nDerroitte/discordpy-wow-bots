import discord
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils import *
from datetime import datetime, timedelta

class priceSheet():
    def __init__(self):
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("gino_strike_secret.json", self.scope)
        self.server_name = "Gino's Pricelist"
        self.client = gspread.authorize(self.creds)

    def price_sheet(self, name, id):
        sheet = self.client.open(self.server_name).worksheet(name.upper())
        list_title = sheet.col_values(2)
        list_value = sheet.col_values(3)
        list_price = sheet.col_values(4)
        return_list = []
        title = ""
        image = ""
        top_image = ""
        emojis = ""
        description = ""
        for i in range(3, len(list_title)):
            if list_title[i].lower() == "id" and str(list_value[i]) == id:
                current_field = {"name" : "\u200b", "value" : "", "price" : ""}
                fields = []
                no_price_bool = False
                while True:
                    if list_title[i].lower() == "end":
                        fields.append(current_field)
                        break
                    if list_title[i].lower() == "image above":
                        image = list_value[i]
                    if list_title[i].lower() == "main title":
                        title = list_value[i]
                    if list_title[i].lower() == "top image":
                        top_image = list_value[i]
                    if list_title[i].lower() == "description":
                        description = str(list_value[i])
                    if list_title[i].lower() == "emojis":
                        emojis = str(list_value[i])
                    if list_title[i].lower() == "" and list_value[i] != "" and  list_price[i] != "":
                        current_field["value"] += str(list_value[i]) + "\n"
                        current_field["price"] += str(list_price[i]) + "\n"
                    if list_title[i].lower() == "" and list_value[i] == "" and list_price[i] == "":
                        current_field["value"] += "\u200b \n"
                        if not no_price_bool:
                            current_field["price"] += "\u200b \n"
                    if list_title[i].lower() == "" and list_value[i] != "" and list_price[i] == "":
                        current_field["value"] += str(list_value[i]) + "\u200b \n"
                        if not no_price_bool:
                            current_field["price"] += "\u200b \n"
                    if list_title[i].lower() == "subtitle":
                        no_price_bool = False
                        if current_field["value"] != "":
                            fields.append(current_field)
                        current_field = {"name" : str(list_value[i]), "value" : "", "price" : ""}
                    if list_title[i].lower() == "subtitle no price":
                        no_price_bool = True
                        if current_field["value"] != "":
                            fields.append(current_field)
                        current_field = {"name" : str(list_value[i]), "value" : ""}
                    i += 1
                    if i == 200:
                        return ["break"]
                return_list.append(int(sheet.cell(2, 3).value))
                return_list.append(image)
                return_list.append(title)
                return_list.append(description)
                return_list.append(fields)
                return_list.append(emojis)
                return_list.append(top_image)
                break
        if title == "":
            return ["error"]
        return return_list

    def price_sheet_name(self, name, title_input):
        if name == "mercs":
            return self.price_sheet_name_mercs(title_input)
        sheet = self.client.open(self.server_name).worksheet(name.upper())
        list_title = sheet.col_values(2)
        list_value = sheet.col_values(3)
        list_price = sheet.col_values(4)
        return_list = []
        title = ""
        image = ""
        top_image = ""
        description = ""
        emojis = ""
        for i in range(3, len(list_title)):
            if list_title[i].lower() == "main title" and str(list_value[i]) == title_input:
                current_field = {"name" : "\u200b", "value" : "", "price" : ""}
                fields = []
                no_price_bool = False
                while True:
                    if list_title[i].lower() == "end":
                        fields.append(current_field)
                        break
                    if list_title[i].lower() == "image above":
                        image = list_value[i]
                    if list_title[i].lower() == "main title":
                        title = list_value[i]
                    if list_title[i].lower() == "emojis":
                        emojis = str(list_value[i])
                    if list_title[i].lower() == "top image":
                        top_image = list_value[i]
                    if list_title[i].lower() == "description":
                        description = str(list_value[i])
                    if list_title[i].lower() == "" and list_value[i] != "" and  list_price[i] != "":
                        current_field["value"] += str(list_value[i]) + "\n"
                        current_field["price"] += str(list_price[i]) + "\n"
                    if list_title[i].lower() == "" and list_value[i] == "" and list_price[i] == "":
                        current_field["value"] += "\u200b \n"
                        if not no_price_bool:
                            current_field["price"] += "\u200b \n"
                    if list_title[i].lower() == "" and list_value[i] != "" and list_price[i] == "":
                        current_field["value"] += str(list_value[i]) + "\u200b \n"
                        if not no_price_bool:
                            current_field["price"] += "\u200b \n"
                    if list_title[i].lower() == "subtitle":
                        no_price_bool = False
                        if current_field["value"] != "":
                            fields.append(current_field)
                        current_field = {"name" : str(list_value[i]), "value" : "", "price" : ""}
                    if list_title[i].lower() == "subtitle no price":
                        no_price_bool = True
                        if current_field["value"] != "":
                            fields.append(current_field)
                        current_field = {"name" : str(list_value[i]), "value" : ""}
                    i += 1
                    if i == 200:
                        return ["break"]
                return_list.append(int(sheet.cell(2, 3).value))
                return_list.append(image)
                return_list.append(title)
                return_list.append(description)
                return_list.append(fields)
                return_list.append(emojis)
                return_list.append(top_image)
                break
        if title == "":
            return ["error"]
        return return_list

    def price_sheet_name_mercs(self, title_input):
        possibilites = ["pveally", "pvehorde", "pvp", "legacy", "mount"]
        for pos in possibilites:
            ack = self.price_sheet_name(pos, title_input)
            if ack != ["error"]:
                return ack
        return ["error"]
