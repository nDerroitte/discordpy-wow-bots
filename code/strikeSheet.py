from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils import *
from datetime import datetime, timedelta
import time

class sheetStrike:
    def __init__(self):
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("gino_strike_secret.json", self.scope)
        self.server_name = "Gino Strikes"
        self.client = gspread.authorize(self.creds)
        self.sheet1 = self.client.open(self.server_name).sheet1  # Open the spreadhseet

    def invite_current_uses(self, dicto):
        sheet2 = self.client.open(self.server_name).worksheet('Invite')
        list_invite_creator = sheet2.col_values(2)
        list_invite_nb = sheet2.col_values(3)
        for creator in list(dicto.keys()):
            if creator.name in list_invite_creator:
                i = list_invite_creator.index(creator.display_name)
                dicto[creator] -= int(list_invite_nb[i])
            if dicto[creator] <= 0:
                dicto.pop(creator, None)
        dicto = {k: v for k, v in dicto.items() if v}
        dicto = dict(sorted(dicto.items(), key=lambda item: item[1], reverse = True))
        return dicto

    def invite_reset(self):
        sheet2 = self.client.open(self.server_name).worksheet('Invite')
        list_invite_nb = sheet2.col_values(3)
        nb = len(list_invite_nb)
        for i in range(1, nb + 1):
            sheet2.update_cell(i, 3, 0)
            if i % 90 == 0:
                time.sleep(100)
        print("done")

    def invite_start(self, dict):
        sheet2 = self.client.open(self.server_name).worksheet('Invite')
        list_invite_creator = sheet2.col_values(2)
        list_invite_nb = sheet2.col_values(3)
        nb_creators = len(list_invite_creator)
        j = 1
        for creator in list(dict.keys()):
            print(creator.display_name)
            if j % 45 == 0:
                print('98')
                time.sleep(100)
            if creator.display_name in list_invite_creator:
                i = list_invite_creator.index(creator.display_name)
                sheet2.update_cell(i + 1, 3, dict[creator])
            else:
                sheet2.update_cell(nb_creators + 1, 2, creator.name)
                sheet2.update_cell(nb_creators + 1, 3, dict[creator])
                nb_creators += 1
            j += 1
        print("done")



    def strike(self, name):
        list_names = self.sheet1.col_values(2)
        name = name.lower()
        for i in range(0,len(list_names)):
            if sameName(list_names[i].lower(), name):
                formula = str(self.sheet1.cell(i+1, 3, value_render_option='FORMULA').value)
                formula += "+1"
                self.sheet1.update_cell(i+1, 3, formula)
                self.sheet1.update_cell(i+1, 4, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                return self.sheet1.cell(i+1, 3).value
        self.sheet1.update_cell(i+2,2,name)
        self.sheet1.update_cell(i+2,3,"=1")
        self.sheet1.update_cell(i+2, 4, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        return self.sheet1.cell(i+2, 3).value

    def reset(self, name):
        list_names = self.sheet1.col_values(2)
        name = name.lower()
        for i in range(0,len(list_names)):
            if sameName(list_names[i].lower(), name):
                formula = "=0"
                self.sheet1.update_cell(i+1, 3, formula)
                return str(self.sheet1.cell(i+1, 3).value)
        return "who"

    def unstrike(self, name):
        list_names = self.sheet1.col_values(2)
        name = name.lower()
        for i in range(0,len(list_names)):
            if sameName(list_names[i].lower(), name):
                formula = str(self.sheet1.cell(i+1, 3, value_render_option='FORMULA').value)
                formula += "-1"
                self.sheet1.update_cell(i+1, 3, formula)
                return str(self.sheet1.cell(i+1, 3).value)
        return "who"

    def see(self, name):
        list_names = self.sheet1.col_values(2)
        name = name.lower()
        for i in range(0,len(list_names)):
            if sameName(list_names[i].lower(), name):
                return [str(self.sheet1.cell(i+1, 3).value), str(self.sheet1.cell(i+1, 4).value)]
        return []

    def update(self):
        list_names = self.sheet1.col_values(2)
        list_strikes = self.sheet1.col_values(3)
        list_time = self.sheet1.col_values(4)
        now = datetime.now()
        name_l = []
        strike_l = []
        time_l = []
        ret_list = [name_l, strike_l, time_l]
        for i in range(0,len(list_names)):
            try:
                date_time_obj = datetime.strptime(list_time[i], "%m/%d/%Y, %H:%M:%S")
            except:
                continue
            delta_t = (now - date_time_obj).days
            if delta_t >= 42 and (list_strikes[i] != "0" and list_strikes[i] != "=0"):
                formula = str(self.sheet1.cell(i+1, 3, value_render_option='FORMULA').value)
                formula = "=0"
                self.sheet1.update_cell(i+1, 3, formula)
                ret_list[0].append(list_names[i])
                ret_list[1].append(list_strikes[i])
                re_worked_date = datetime.strftime(date_time_obj, "%m/%d/%Y")
                ret_list[2].append(str(re_worked_date) + " (" + str(delta_t) + " days)")
        return ret_list
