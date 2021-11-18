import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils import *
from datetime import datetime, timedelta

class sheetReader:
    def __init__(self, casino=False):
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.testy = False
        if casino == True:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name("casgino_secret.json", self.scope)
            self.server_name = "Gino's Private"
        else:
            if self.testy == False:
                self.creds = ServiceAccountCredentials.from_json_keyfile_name("ginobot_secret.json", self.scope)
                self.server_name = "Gino's Private"
            else:
                self.creds = ServiceAccountCredentials.from_json_keyfile_name("test_bot_secret.json", self.scope)
                self.server_name = "Bot private"
        self.client = gspread.authorize(self.creds)
        self.sheet1 = self.client.open(self.server_name).sheet1  # Open the spreadhseet


    def add_gold(self, name, server, gold):
        list_names_ally = self.sheet1.col_values(3)
        list_names_horde = self.sheet1.col_values(11)
        list_servers_ally = self.sheet1.col_values(4)
        list_servers_horde = self.sheet1.col_values(12)

        name = name.lower()
        server = server.lower()
        sign = "+"
        if gold < 0:
            sign = "-"
            gold *= -1


        for i in range(0,len(list_names_ally)):
            if list_names_ally[i].lower() == name and list_servers_ally[i].lower() == server:
                formula = self.sheet1.cell(i+1, 5, value_render_option='FORMULA').value
                formula += sign + str(abs(gold))
                self.sheet1.update_cell(i+1, 5, formula)
                return "ok"
        for i in range(0,len(list_names_horde)):
            if list_names_horde[i].lower() == name and list_servers_horde[i].lower() == server:
                formula = self.sheet1.cell(i+1, 13, value_render_option='FORMULA').value
                formula += sign + str(abs(gold))
                self.sheet1.update_cell(i+1, 13, formula)
                return "ok"
        return "Nbalance"

    def get_gold(self, name, server):
        list_names_ally = self.sheet1.col_values(3)
        list_servers_ally = self.sheet1.col_values(4)
        list_gold_ally = self.sheet1.col_values(5)
        name = name.lower()
        server = server.lower()
        for i in range(0,len(list_names_ally)):
            if list_names_ally[i].lower() == name and list_servers_ally[i].lower() == server:
                if i > len(list_gold_ally) - 1 or list_gold_ally[i] == "":
                    return 0
                return list_gold_ally[i]
        list_names_horde = self.sheet1.col_values(11)
        list_servers_horde = self.sheet1.col_values(12)
        list_gold_horde = self.sheet1.col_values(13)
        for i in range(0,len(list_names_horde)):
            if list_names_horde[i].lower() == name and list_servers_horde[i].lower() == server:
                if i > len(list_gold_horde) - 1 or list_gold_horde[i] == "":
                    return 0
                return list_gold_horde[i]
        return "Nbalance"

    def add_balance(self, name, serv, ally_bool):
        list_names_ally = self.sheet1.col_values(3)
        list_servers_ally = self.sheet1.col_values(4)
        list_gold_ally = self.sheet1.col_values(5)
        list_names_horde = self.sheet1.col_values(11)
        list_servers_horde = self.sheet1.col_values(12)
        list_gold_horde = self.sheet1.col_values(13)
        namel = name.lower()
        servl = serv.lower()
        for i in range(0,len(list_names_ally)):
            if list_names_ally[i].lower() == namel and list_servers_ally[i].lower() == servl:
                return "AlreadyIn"
        for j in range(0,len(list_names_horde)):
            if list_names_horde[j].lower() == namel and list_servers_horde[j].lower() == servl:
                return "AlreadyIn"
        if ally_bool:
            i = i +2
            self.sheet1.update_cell(i,3,name)
            self.sheet1.update_cell(i,4,serv)
        else:
            j = j+2
            self.sheet1.update_cell(j,11,name)
            self.sheet1.update_cell(j,12,serv)
        return "ok"

    def post_boost(self, boost):
        ######################## Retreive google sheet info ########################
        sheet2 = self.client.open(self.server_name).worksheet('logs')
        list_logs = sheet2.col_values(1)
        index = len(list_logs)+1
        sheet2.update_cell(index,1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        sheet2.update_cell(index,13, str(boost.notes))
        list_names_ally = self.sheet1.col_values(3)
        list_names_horde = self.sheet1.col_values(11)
        list_servers_ally = self.sheet1.col_values(4)
        list_servers_horde = self.sheet1.col_values(12)
        ######################### Player index for PvP / Torghast ########################
        player_index = 0
        if boost.type == "pvp" or boost.type == 'torghast':
            player_index = boost.nb_boosters
        ######################### Boosters names ########################
        ## TANK - HEAL
        if boost.type == "mm" or boost.type == "tazavesh" or boost.type == "leveling":
            booster_name_tank = sheet_name(boost.tank_in)
            #HEAL
            booster_name_heal = sheet_name(boost.heal_in)
        ## DPS1
        booster_name_dps1 = sheet_name(boost.dps_in[0]) 
        ## DPS2
        if boost.type == "mm" or boost.type == "tazavesh" or player_index > 1 or boost.type == "island":
            booster_name_dps2 = sheet_name(boost.dps_in[1]) 
        ## ADV
        adv_name =  sheet_name(boost.advertiser) 
        user_name_serv = parseName(boost.advertiser.display_name)
        name_adv = user_name_serv[0]
        serv_adv = user_name_serv[1]
        ######################## CUT ########################
        if boost.no_adv_cut:
            sheet2.update_cell(index,16, "NoAdvCut")
        elif  boost.inhouse:
            sheet2.update_cell(index,16, "InHouse")
        elif boost.type == "mm":
            if boost.isValor:
                sheet2.update_cell(index,16, "Valor")
            elif boost.isLeveling:
                sheet2.update_cell(index,16, "Leveling")
            else: 
                sheet2.update_cell(index, 16,"M+")
        elif boost.type == "legacy":
            sheet2.update_cell(index,16,"Legacy")
        elif boost.type == "torghast":
            sheet2.update_cell(index,16,"Torghast")
        elif boost.type == "pvp":
            sheet2.update_cell(index, 16,"PvP")
        elif boost.type == "tazavesh":
            sheet2.update_cell(index, 16,"Tazavesh")
        else: 
            sheet2.update_cell(index, 16,"M+")
        ######################## Armor Stack / Key  info ########################
        if boost.type == "mm":
            if boost.isValor:
                sheet2.update_cell(index,2, "Valor")
            if boost.isLeveling:
                sheet2.update_cell(index,2, "Leveling")
            else:
                sheet2.update_cell(index,2, "+{}".format(boost.key_level))
            if boost.key == "" or boost.key == "random" or boost.key == "/" or boost.key == " " or boost.key == "no":
                sheet2.update_cell(index,3, "No")
            else:
                sheet2.update_cell(index,3, "Yes")
            if boost.armor_stack =="no" or boost.armor_stack == "" or boost.armor_stack == "/" or boost.armor_stack == "noarmorstack" or boost.armor_stack == "noarmorstacks" or boost.armor_stack == "nostack":
                sheet2.update_cell(index,4, "No")
            else:
                sheet2.update_cell(index,4, "Yes")      
        elif boost.type == "legacy":
            sheet2.update_cell(index,2,"Legacy")
            sheet2.update_cell(index,3, "No")
            sheet2.update_cell(index,4, "No")
        elif boost.type == "torghast":
            sheet2.update_cell(index,2,"torghast")
            sheet2.update_cell(index,3, "No")
            sheet2.update_cell(index,4, "No")
        elif boost.type == "pvp":
            sheet2.update_cell(index,2,"PvP")
            sheet2.update_cell(index,3, "No")
            sheet2.update_cell(index,4, "No")
        elif boost.type == "tazavesh":
            sheet2.update_cell(index,2,"Tazavesh")
            sheet2.update_cell(index,3, "No")
            sheet2.update_cell(index,4, "No")
        else:
            sheet2.update_cell(index,2,boost.type.capitalize())
            sheet2.update_cell(index,3, "No")
            if boost.armor_stack =="no" or boost.armor_stack == "" or boost.armor_stack == "/" or boost.armor_stack == "noarmorstack" or boost.armor_stack == "noarmorstacks" or boost.armor_stack == "nostack":
                sheet2.update_cell(index,4, "No")
        ######################## In house flag ########################
        if boost.inhouse == True:
            sheet2.update_cell(index,14, "Yes")
        else:
            sheet2.update_cell(index,14, "No")
        ######################## Helper / GC ########################
        if boost.gold_collector != "" or boost.helper != "":
            try:
                gc_name = boost.gold_collector.display_name
            except:
                gc_name = boost.helper.display_name
            gc_name_serv_adv = parseName(gc_name)
            name_gc = gc_name_serv_adv[0].lower()
            serv_gc = gc_name_serv_adv[1].lower()
            count = 2
            for i in range(0,len(list_names_ally)):
                if count == 0:
                    break
                if list_names_ally[i].lower() == name_gc and list_servers_ally[i].lower() == serv_gc:
                    count -= 1
                    formula = self.sheet1.cell(i+1, 5, value_render_option='FORMULA').value
                    formula += "+" + str(boost.gold * 0.03)
                    self.sheet1.update_cell(i+1, 5, formula)
                if list_names_ally[i].lower() == name_adv and list_servers_ally[i].lower() == serv_adv:
                    count -= 1
                    formula = self.sheet1.cell(i+1, 5, value_render_option='FORMULA').value
                    formula += "-" + str(boost.gold * 0.03)
                    self.sheet1.update_cell(i+1, 5, formula)
            for j in range(0,len(list_names_horde)):
                if count == 0:
                    break
                if list_names_horde[j].lower() == name_gc and list_servers_horde[j].lower() == serv_gc:
                    count -= 1
                    formula = self.sheet1.cell(j+1, 13, value_render_option='FORMULA').value
                    formula += "+" + str(boost.gold * 0.03)
                    self.sheet1.update_cell(j+1, 13, formula)
                if list_names_horde[j].lower() == name_adv and list_servers_horde[j].lower() == serv_adv:
                    count -= 1
                    formula = self.sheet1.cell(j+1, 13, value_render_option='FORMULA').value
                    formula += "-" + str(boost.gold * 0.03)
                    self.sheet1.update_cell(j+1, 13, formula)
        ######################## Boost Info ########################
        sheet2.update_cell(index, 5, boost.gold)
        sheet2.update_cell(index, 6, boost.realm)
        sheet2.update_cell(index, 7, boost.gold_faction.capitalize())
        sheet2.update_cell(index, 8, adv_name)
        try:
            boost_id_str = str(boost.message_annoucement.id)
            if boost_id_str.endswith("000"):
                boost_id_str += "+"
            sheet2.update_cell(index, 15, boost_id_str)
        except:
            if boost.pvp_id == 0:
                a = datetime.now()
                boost.pvp_id = int(a.strftime('%Y%m%d'))
            sheet2.update_cell(index, 15, str(boost.pvp_id))
        if boost.type == "legacy" or player_index == 1:
            sheet2.update_cell(index, 9, booster_name_dps1)
            sheet2.update_cell(index, 10, booster_name_dps1)
            sheet2.update_cell(index, 11, booster_name_dps1)
            sheet2.update_cell(index, 12, booster_name_dps1)
        elif player_index == 2:
            sheet2.update_cell(index, 9, booster_name_dps1)
            sheet2.update_cell(index, 10, booster_name_dps1)
            sheet2.update_cell(index, 11, booster_name_dps2)
            sheet2.update_cell(index, 12, booster_name_dps2)
        else:
            #TANK
            sheet2.update_cell(index, 9, booster_name_tank)
            # HEAL
            sheet2.update_cell(index, 10, booster_name_heal)
            # DPS 1
            sheet2.update_cell(index, 11, booster_name_dps1)
            # DPS 2
            sheet2.update_cell(index, 12, booster_name_dps2)


    def roll(self, winner, losers, gold_w, gold_l):
        gold_balance = int(gold_w*0.05/0.95)
        list_names_ally = self.sheet1.col_values(3)
        list_names_horde = self.sheet1.col_values(11)
        list_servers_ally = self.sheet1.col_values(4)
        list_servers_horde = self.sheet1.col_values(12)
        count = 0
        if winner == "":
            winner_name = "notinbalance"
            winner_serv = "notinbalance"
            count = len(losers) + 1
        else:
            winner_display_name = winner.display_name
            user_name_serv_winner = parseName(winner_display_name)
            winner_name = user_name_serv_winner[0].lower()
            winner_serv = user_name_serv_winner[1].lower()
            count = 1 + len(losers) + 1

        losers_names = []
        losers_serv = []
        for loser in losers:
            loser_display_name = loser.display_name
            user_name_serv_loser = parseName(loser_display_name)
            losers_names.append(user_name_serv_loser[0].lower())
            losers_serv.append(user_name_serv_loser[1].lower())


        for i in range(0,len(list_names_ally)):
            if count == 0:
                break
            if list_names_ally[i].lower() == "casino" and list_servers_ally[i].lower() == "casino":
                formula = self.sheet1.cell(i+1, 5, value_render_option='FORMULA').value
                formula += "+" + str(gold_balance)
                self.sheet1.update_cell(i+1, 5, formula)
                count -= 1
            if list_names_ally[i].lower() == winner_name and list_servers_ally[i].lower() == winner_serv:
                formula = self.sheet1.cell(i+1, 5, value_render_option='FORMULA').value
                formula += "+" + str(gold_w)
                self.sheet1.update_cell(i+1, 5, formula)
                count -= 1
            if list_names_ally[i].lower() in losers_names and list_servers_ally[i].lower() in losers_serv:
                for j in range(len(losers)):
                    if list_names_ally[i].lower() == losers_names[j] and list_servers_ally[i].lower() == losers_serv[j]:
                        formula = self.sheet1.cell(i+1, 5, value_render_option='FORMULA').value
                        formula += "-" + str(gold_l)
                        self.sheet1.update_cell(i+1, 5, formula)
                        count -= 1
                        losers_names.pop(j)
                        losers_serv.pop(j)
                        break
        for i in range(0,len(list_names_horde)):
            if count == 0:
                break
            if list_names_horde[i].lower() == winner_name and list_servers_horde[i].lower() == winner_serv:
                formula = self.sheet1.cell(i+1, 13, value_render_option='FORMULA').value
                formula += "+" + str(gold_w)
                self.sheet1.update_cell(i+1, 13, formula)
                count -= 1
            if list_names_horde[i].lower() in losers_names and list_servers_horde[i].lower() in losers_serv:
                for j in range(len(losers)):
                    if list_names_horde[i].lower() == losers_names[j] and list_servers_horde[i].lower() == losers_serv[j]:
                        formula = self.sheet1.cell(i+1, 13, value_render_option='FORMULA').value
                        formula += "-" + str(gold_l)
                        self.sheet1.update_cell(i+1, 13, formula)
                        count -= 1
                        losers_names.pop(j)
                        losers_serv.pop(j)
                        break

    def close_bet_date(self):
        detailed_logs = self.client.open(self.server_name).worksheet('Detailed Logs')
        date_str = detailed_logs.cell(1, 2).value
        end_cycle = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
        close_bet_date = end_cycle - timedelta(days=3)
        now = datetime.now()
        if now < close_bet_date:
            return True
        else:
            return False

    def close_lottery_date(self):
        detailed_logs = self.client.open(self.server_name).worksheet('Detailed Logs')
        date_str = detailed_logs.cell(1, 2).value
        end_cycle = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
        return end_cycle - timedelta(days=3)



    def close(self):
        self.client.close()
