import discord
from utils import *
from datetime import datetime, timedelta
class boostOb:
    def __init__(self, adv, unpost_channel,tank, heal, dps, allowed, denied, coin, mercs, armor, k1, k2, k3, nb_emo):
        self.preseason = False
        self.pvp_id = 0
        self.type = "/"
        self.ongoing_message = ""
        self.faction = "/"
        self.helper = ""
        self.advertiser = adv
        self.notes = "/"
        self.key = "/"
        self.gold_faction = "/"
        self.auto_post = True
        self.no_ping = False
        self.armor_stack = "/"
        self.gold = "/"
        self.realm = "/"
        self.buyer_name = ""
        self.who_to_w = "/"
        self.buyer_spec = "/"
        self.dps_in = ["", "", "", ""]
        self.dps_torghast = []
        self.heal_in = ""
        self.tank_in = ""
        self.nb_runs = 0
        self.real_realm = ""
        self.message_annoucement = "/"
        self.message_collecting = "/"
        self.tmp_collecting_msg = "/"
        self.unpost_chan = unpost_channel
        self.annoucement_chan = ""
        self.heal_emo = heal
        self.armor_emo = armor
        self.tank_emo = tank
        self.dps_emo = dps
        self.allowed_emo = allowed
        self.denied_emo = denied
        self.coin_emo = coin
        self.mercs_emo = mercs
        self.bronze_key_emo = k1
        self.silver_key_emo = k2
        self.gold_key_emo = k3
        self.nb_emo = nb_emo
        self.nb_boosters = 0
        self.booster_place = 0
        self.key_level = 0
        self.real_gold = 0
        self.role_dps = []
        self.role_heal = []
        self.role_tank = []
        self.role_tag = []
        self.tank_waiting = []
        self.heal_waiting = []
        self.dps_waiting = []
        self.tag_message = ""
        self.nb_dps = 0
        self.previous_booster = []
        self.inhouse = False
        self.no_adv_cut = False
        self.gold_collector = ""
        self.pvp_type = ""
        self.isValor = False
        self.isLeveling = False

    def completeInfo(self):
        if self.helper != "":
            self.notes += "\nHelper: {}".format(self.helper.display_name)
        if self.type == "torghast":
            #self.auto_post = False
            self.booster_place = self.nb_boosters
            print(self.nb_boosters)
            self.nb_dps = self.nb_boosters
            if self.dps_in[0] != "":
                self.booster_place -= 1
            if self.dps_in[1] != "":
                self.booster_place -= 1
            print(self.booster_place)
        elif self.type == "legacy":
            #self.auto_post = True
            self.nb_boosters = 1
            self.booster_place = 1
            self.nb_dps = 1
            if self.dps_in[0] != "":
                self.booster_place -= 1
        elif self.type == "island":
            #self.auto_post = False
            self.nb_boosters = 2
            self.nb_dps = 2
            self.booster_place = 2
            if self.dps_in[0] != "":
                self.booster_place -=1
            if self.dps_in[1] != "":
                self.booster_place -=1
        elif self.type == "pvp":
            #self.auto_post = False
            self.booster_place = self.nb_boosters
            self.nb_dps = self.nb_boosters
            if self.dps_in[0] != "":
                self.booster_place -= 1
            if self.dps_in[1] != "":
                self.booster_place -= 1
        elif self.type == "tazavesh":
            self.nb_boosters = 4
            self.nb_dps = 2
            self.booster_place = self.nb_boosters
            if self.dps_in[0] != "":
                self.booster_place -= 1
            if self.dps_in[1] != "":
                self.booster_place -= 1
            if self.heal_in != "":
                self.booster_place -=1
            if self.tank_in != "":
                self.booster_place -=1
        elif self.type == "mm":
            self.nb_boosters = 4
            self.nb_dps = 2
            self.booster_place = self.nb_boosters
            if self.dps_in[0] != "":
                self.booster_place -= 1
            if self.dps_in[1] != "":
                self.booster_place -= 1
            if self.heal_in != "":
                self.booster_place -=1
            if self.tank_in != "":
                self.booster_place -=1

    def print(self):
        print("type: {}".format(self.type))
        print("fact: {}".format(self.faction))
        print("adve: {}".format(self.advertiser))
        print("note: {}".format(self.notes))
        print("key : {}".format(self.key))
        print("key_: {}".format(self.key_level))
        print("armo: {}".format(self.armor_stack))
        print("gold: {}".format(self.gold))
        print("real: {}".format(self.realm))
        print("who_: {}".format(self.who_to_w))
        print("buye: {}".format(self.buyer_name))
        print("buye: {}".format(self.buyer_spec))
        print("dps_: {}".format(self.dps_in))
        print("heal: {}".format(self.heal_in))
        print("tank: {}".format(self.tank_in))
        print("nb_r: {}".format(self.nb_runs))
        print("inho: {}".format(self.inhouse))
        print("auto: {}".format(self.auto_post))
        print("advc: {}".format(self.no_adv_cut))
        print("ping: {}".format(self.no_ping))
        print("help: {}".format(self.helper))


    def getStr(self):
        str = "type: {}\n".format(self.type)+"fact: {}\n".format(self.faction)+"adve: {}\n".format(self.advertiser)+"note: {}\n".format(self.notes)+"key : {}\n".format(self.key)+"key_: {}\n".format(self.key_level)+"armo: {}\n".format(self.armor_stack)+"gold: {}\n".format(self.gold)+"real: {}\n".format(self.realm)+"who_: {}\n".format(self.who_to_w)+"buye: {}\n".format(self.buyer_name)+"buye: {}\n".format(self.buyer_spec)+"dps_: {}\n".format(self.dps_in)+"heal: {}\n".format(self.heal_in)+"tank: {}\n".format(self.tank_in)+"nb_r: {}\n".format(self.nb_runs) +"inho: {}\n".format(self.inhouse)+"auto: {}\n".format(self.auto_post)+"advc: {}\n".format(self.no_adv_cut)+"ping: {}\n".format(self.no_ping)+"help: {}\n".format(self.helper)
        return str



    def post(self, pb = False):
        if self.type == "torghast":
            return self.__create_em_torghast()
        elif self.type == "legacy":
            return self.__create_em_legacy()
        elif self.type == "island":
            return self.__create_em_island()
        elif self.type == "pvp_old":
            return self.__create_em_pvp_old()
        elif self.type == "tazavesh":
            return self.__create_em_tazavesh()
        elif self.type == "pvp":
            return self.__create_em_pvp_request()
        elif self.type == "mm":
            if self.isValor:
                return self.__create_em_valor()
            if self.isLeveling:
                return self.__create_em_leveling()
            else:
                return self.__create_em_mm(pb)

    def end_post(self):
        embed_message = discord.Embed(title="Boost to add", color=0xffd700)#7FFF00
        embed_message.add_field(name="Boost type:", value = self.type.capitalize(), inline=True)
        embed_message.add_field(name="Boost faction:", value = self.faction, inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="Gold", value = self.gold, inline=True)
        embed_message.add_field(name="Collection Realm", value = self.realm, inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        str_out = ""
        if self.tank_in != "":
            str_out += "{}".format(self.tank_emo) + " " + mention_or_nada(self.tank_in) + "\n"
        if self.heal_in != "":
            str_out += "{}".format(self.heal_emo) + " " + mention_or_nada(self.heal_in) + "\n"
        if self.dps_in[0] !="":
            str_out += "{}".format(self.dps_emo)+ " " +  mention_or_nada(self.dps_in[0]) + "\n"
        if self.dps_in[1] !="":
            str_out += "{}".format(self.dps_emo)+ " " +  mention_or_nada(self.dps_in[1]) + "\n"
        if self.dps_in[2] !="":
            str_out += "{}".format(self.dps_emo)+ " " +  mention_or_nada(self.dps_in[2]) + "\n"
        if self.dps_in[3] !="":
            str_out += "{}".format(self.dps_emo)+ " " +  mention_or_nada(self.dps_in[3]) + "\n"
        for i in range(len(self.previous_booster)):
            if self.previous_booster[i][0] == "tank":
                emo = "{}".format(self.tank_emo)
            elif self.previous_booster[i][0] == "heal":
                emo = "{}".format(self.heal_emo)
            else:
                emo = "{}".format(self.dps_emo)
            str_out += emo+ " " + mention_or_nada(self.previous_booster[i][1]) + "\n"
        embed_message.add_field(name="Booster(s) : ", value =str_out, inline=False)
        return embed_message

    def __create_em_leveling(self):
        embed_message = discord.Embed(title="Leveling Boost".format(self.key_level), color=0x228b22)#7FFF00 #228B22
        embed_message.add_field(name="Total gold", value = "{:,} {}".format(int(self.gold), self.coin_emo), inline=True)
        embed_message.add_field(name="Booster cut", value = "{:,} {}".format(int(self.cut()), self.coin_emo), inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="Boosters", value="{} {}\n{} {}\n{} {}\n{} {}\n".format(self.tank_emo,mention_or_nada(self.tank_in),self.heal_emo, mention_or_nada(self.heal_in),self.dps_emo,mention_or_nada(self.dps_in[0]),self.dps_emo,mention_or_nada(self.dps_in[1])),inline=False)

        if self.notes != "" and self.notes != "/":
            embed_message.add_field(name="Boost notes", value = "```{}```".format(self.notes), inline=False)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        if self.gold_collector != "":
            embed_message.add_field(name="Gold Collector", value = self.gold_collector.mention, inline=True)

        dt_wanted = datetime.now() + timedelta(hours=2)
        embed_message.set_footer(text="Gino's Mercenaries - {}".format(dt_wanted.isoformat(' ', 'seconds')))
        return embed_message
    def __create_em_torghast(self):
        embed_message = discord.Embed(title="Torghast Boost", color=0x228b22)#7FFF00
        embed_message.add_field(name="Boost", value ="```{}```".format(self.notes), inline=False)
        embed_message.add_field(name="Gold", value = "{:,} {}".format(int(self.gold), self.coin_emo), inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        if self.nb_boosters == 1:
            embed_message.add_field(name="Booster", value="{} {}".format(self.dps_emo, mention_or_nada(self.dps_in[0])),inline=False)
        if self.nb_boosters == 2:
            embed_message.add_field(name="Booster", value="{} {}\n {} {}".format(self.dps_emo, mention_or_nada(self.dps_in[0]),self.dps_emo, mention_or_nada(self.dps_in[1])),inline=False)
        if self.nb_boosters == 3:
            embed_message.add_field(name="Booster", value="{} {}\n {} {}\n {} {}".format(self.dps_emo, mention_or_nada(self.dps_in[0]),self.dps_emo, mention_or_nada(self.dps_in[1]),self.dps_emo, mention_or_nada(self.dps_in[2])),inline=False)
        if self.nb_boosters >= 4:
            embed_message.add_field(name="Booster", value="{} {}\n {} {}\n {} {}\n {} {}".format(self.dps_emo, mention_or_nada(self.dps_in[0]),self.dps_emo, mention_or_nada(self.dps_in[1]),self.dps_emo, mention_or_nada(self.dps_in[2]),self.dps_emo, mention_or_nada(self.dps_in[3])),inline=False)
        return embed_message
    def __create_em_legacy(self):
        embed_message = discord.Embed(title="Legacy Boost",  color=0x228b22)#7FFF00
        embed_message.add_field(name="Boost", value = "```{}```".format(self.notes), inline=False)
        embed_message.add_field(name="Gold", value = "{:,} {}".format(int(self.gold), self.coin_emo), inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        embed_message.add_field(name="Booster", value="{} {}".format(self.dps_emo, mention_or_nada(self.dps_in[0])),inline=False)
        embed_message.set_footer(text="Gino's Mercenaries - {}".format(datetime.now().isoformat(' ', 'seconds')))
        return embed_message
    def __create_em_island(self):
        embed_message = discord.Embed(title="Island Boost", color=0xffd700)#7FFF00
        embed_message.add_field(name="Boost", value = "```{}```".format(self.notes), inline=True)
        embed_message.add_field(name="Gold", value = "{}k".format(self.gold/1000), inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        embed_message.add_field(name="Booster", value="{} {}\n{} {}".format(self.dps_emo, mention_or_nada(self.dps_in[0]),self.dps_emo, mention_or_nada(self.dps_in[1])),inline=False)
        embed_message.set_footer(text="Gino's Mercenaries - {}".format(datetime.now().isoformat(' ', 'seconds')))
        return embed_message
    def __create_em_pvp_old(self):
        embed_message = discord.Embed(title="PVP Boost", color=0x228b22)#7FFF00
        embed_message.add_field(name="Boost", value = "```{}```".format(self.notes), inline=False)
        embed_message.add_field(name="Gold", value = "{:,} {}".format(int(self.gold), self.coin_emo), inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="Buyer Spec", value = self.buyer_spec, inline=True)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        if self.nb_boosters == 1:
            embed_message.add_field(name="Booster", value="{} {}".format(self.dps_emo, mention_or_nada(self.dps_in[0])),inline=False)
        elif self.nb_boosters >= 2:
            embed_message.add_field(name="Boosters", value="{} {}\n{} {}".format(self.dps_emo, mention_or_nada(self.dps_in[0]),self.dps_emo, mention_or_nada(self.dps_in[1])),inline=False)
        embed_message.set_footer(text="Gino's Mercenaries - {}".format(datetime.now().isoformat(' ', 'seconds')))
        return embed_message
    def __create_em_pvp_request(self):
        embed_message = discord.Embed(title="PVP Boost", color=0x228b22)#7FFF00
        embed_message.add_field(name="Boost", value = "```{}```".format(self.notes), inline=False)
        embed_message.add_field(name="Gold", value = "{:,} {}".format(int(self.gold), self.coin_emo), inline=True)
        embed_message.add_field(name="Buyer's PvP experience", value = "{}".format(self.buyer_name), inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="How to apply?", value="Press {}. We'll inform the advertiser that you applied.".format(self.dps_emo),inline=False)
        embed_message.set_footer(text="Gino's Mercenaries - {}".format(datetime.now().isoformat(' ', 'seconds')))
        return embed_message

    def __create_em_tazavesh(self):
        embed_message = discord.Embed(title="Tazavesh Boost", color=0x228b22)
        embed_message.add_field(name="Total gold", value = "{:,} {}".format(int(self.gold), self.coin_emo), inline=True)
        embed_message.add_field(name="Booster cut", value = "{:,} {}".format(int(self.cut()), self.coin_emo), inline=True)
        embed_message.add_field(name="{} Armor stack".format(self.armor_emo), value = self.armor_stack.capitalize(), inline=True)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        embed_message.add_field(name="Boosters", value="{} {}\n{} {}\n{} {}\n{} {}\n".format(self.tank_emo,mention_or_nada(self.tank_in),self.heal_emo, mention_or_nada(self.heal_in),self.dps_emo,mention_or_nada(self.dps_in[0]),self.dps_emo, mention_or_nada(self.dps_in[1])),inline=False)
        if self.notes != "" and self.notes != "/":
            embed_message.add_field(name="Boost notes", value = "```{}```".format(self.notes), inline=False)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        if self.gold_collector != "":
            embed_message.add_field(name="Gold Collector", value = self.gold_collector.mention, inline=True)

        dt_wanted = datetime.now() + timedelta(hours=2)
        embed_message.set_footer(text="Gino's Mercenaries - {}".format(dt_wanted.isoformat(' ', 'seconds')))
        return embed_message


    def __create_em_valor(self):
        embed_message = discord.Embed(title="Valor Boost".format(self.key_level), color=0x228b22)#7FFF00 #228B22
        embed_message.add_field(name="Total gold", value = "{:,} {}".format(int(self.gold), self.coin_emo), inline=True)
        embed_message.add_field(name="Booster cut", value = "{:,} {}".format(int(self.cut()), self.coin_emo), inline=True)
        embed_message.add_field(name="{} Number of runs".format(self.nb_emo), value = self.nb_runs, inline=True)
        embed_message.add_field(name="Boosters", value="{} {}\n{} {}\n{} {}\n{} {}\n".format(self.tank_emo,mention_or_nada(self.tank_in),self.heal_emo, mention_or_nada(self.heal_in),self.dps_emo,mention_or_nada(self.dps_in[0]),self.dps_emo,mention_or_nada(self.dps_in[1])),inline=False)

        if self.notes != "" and self.notes != "/":
            embed_message.add_field(name="Boost notes", value = "```{}```".format(self.notes), inline=False)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        if self.gold_collector != "":
            embed_message.add_field(name="Gold Collector", value = self.gold_collector.mention, inline=True)

        dt_wanted = datetime.now() + timedelta(hours=2)
        embed_message.set_footer(text="Gino's Mercenaries - {}".format(dt_wanted.isoformat(' ', 'seconds')))
        return embed_message
    def __create_em_mm(self, pb = False):
        embed_message = discord.Embed(title="+{} Mythic+ Boost".format(self.key_level), color=0x228b22)#7FFF00 #228B22
        embed_message.add_field(name="Total gold", value = "{:,} {}".format(int(self.gold), self.coin_emo), inline=True)
        embed_message.add_field(name="Booster cut", value = "{:,} {}".format(int(self.cut()), self.coin_emo), inline=True)
        embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
        if int(self.key_level) < 10:
            embed_message.add_field(name="{} Specific keys".format(self.bronze_key_emo), value = self.key, inline=True)
        elif int(self.key_level) <15:
            embed_message.add_field(name="{} Specific keys".format(self.silver_key_emo), value = self.key, inline=True)
        else:
            embed_message.add_field(name="{} Specific keys".format(self.gold_key_emo), value = self.key, inline=True)
        embed_message.add_field(name="{} Number of runs".format(self.nb_emo), value = self.nb_runs, inline=True)
        embed_message.add_field(name="{} Armor stack".format(self.armor_emo), value = self.armor_stack.capitalize(), inline=True)
        embed_message.add_field(name="Boosters", value="{} {}\n{} {}\n{} {}\n{} {}\n".format(self.tank_emo,mention_or_nada(self.tank_in),self.heal_emo, mention_or_nada(self.heal_in),self.dps_emo,mention_or_nada(self.dps_in[0]),self.dps_emo,mention_or_nada(self.dps_in[1])),inline=False)

        if self.notes != "" and self.notes != "/":
            embed_message.add_field(name="Boost notes", value = "```{}```".format(self.notes), inline=False)
        embed_message.add_field(name="Advertiser", value = self.advertiser.mention, inline=True)
        if self.gold_collector != "":
            embed_message.add_field(name="Gold Collector", value = self.gold_collector.mention, inline=True)


        if pb:
            str_out = ""
            for list_booster in self.previous_booster:
                if list_booster[0] == "tank":
                    emo = self.tank_emo
                elif list_booster[0] == "heal":
                    emo = self.heal_emo
                elif list_booster[0] == "dps":
                    emo = self.dps_emo
                str_out += "{} {} {}/{}".format(emo, mention_or_nada(list_booster[1]), list_booster[2],self.nb_runs)
            embed_message.add_field(name="Previous boosters", value=str_out,inline=False)
        dt_wanted = datetime.now() + timedelta(hours=2)
        embed_message.set_footer(text="Gino's Mercenaries - {}".format(dt_wanted.isoformat(' ', 'seconds')))
        return embed_message

    def notIn(self, user):
        if self.heal_in == user or self.tank_in == user or user in self.dps_in:
            return False
        return True

    def tags(self):
        if self.type == "torghast":
            if self.faction == "alliance":
                self.role_dps = ["Torghast Runner Ally"]
                self.role_tag = ["Torghast Runner Ally"]
            elif self.faction == "horde":
                self.role_dps = ["Torghast Runner Horde"]
                self.role_tag = ["Torghast Runner Horde"]
        elif self.type == "legacy":
            self.role_dps = ["Legacy Booster"]
            self.role_tag = ["Legacy Booster"]
        elif self.type == "island":
            self.role_dps = ["Island Expert"]
            self.role_tag = ["Island Expert"]
        elif self.type == "pvp_old":
            if self.faction == "alliance":
                self.role_dps = ["PvP Alliance"]
                self.role_tag = ["PvP Alliance"]
            else:
                self.role_dps = ["PvP Horde"]
                self.role_tag = ["PvP Horde"]
        elif self.type == "pvp":
            if self.pvp_type == "arena":
                if self.faction == "alliance":
                    self.role_dps = ["PvP Alliance"]
                    self.role_tag = ["PvP Alliance"]
                else:
                    self.role_dps = ["PvP Horde"]
                    self.role_tag = ["PvP Horde"]
            elif self.pvp_type == "rbg":
                self.role_dps = ["RL RBG"]
                self.role_tag = ["RL RBG"]
            elif self.pvp_type == "coaching":
                self.role_dps = ["PvP Coaching"]
                self.role_tag = ["PvP Coaching"]
        elif self.type == "tazavesh":
            self.role_dps = ["DPS Prestige"]
            self.role_heal = ["Healer Prestige"]
            self.role_tank = ["Tank Prestige"]
            self.role_tag = ["M+ Prestige"]
            if self.armor_stack != "/":
                if self.armor_stack != "cloth" and self.armor_stack != "Cloth" and self.armor_stack != "mail" and self.armor_stack != "Mail":
                    self.role_tank.append(self.armor_stack.capitalize())
                    self.role_tag = [self.armor_stack.capitalize()]
                else:
                    self.role_tag = [self.role_tank[0], self.armor_stack.capitalize()]
                self.role_heal.append(self.armor_stack.capitalize())
                self.role_dps.append(self.armor_stack.capitalize())
        elif self.type == "mm":
            if self.isValor:
                self.role_dps = ["Valor"]
                self.role_heal = ["Valor"]
                self.role_tank = ["Valor"]
                self.role_tag = ["Valor"]
            elif self.isLeveling:
                self.role_dps = ["Leveling"]
                self.role_heal = ["Leveling"]
                self.role_tank = ["Leveling"]
                self.role_tag = ["Leveling"]
            elif self.preseason == False:
                if self.key_level == 0:
                    if self.faction == "alliance":
                        self.role_dps = ["M+ Alliance"]
                        self.role_heal = ["M+ Alliance"]
                        self.role_tank = ["M+ Alliance"]
                        self.role_tag = ["M+ Alliance"]
                    else:
                        self.role_dps = ["M+ Horde"]
                        self.role_heal = ["M+ Horde"]
                        self.role_tank = ["M+ Horde"]
                        self.role_tag = ["M+ Horde"]
                elif self.key_level < 14:
                    self.role_dps = ["DPS Prestige"]
                    self.role_heal = ["Healer Prestige"]
                    self.role_tank = ["Tank Prestige"]
                    self.role_tag = ["M+ Prestige"]
                else:
                    self.role_dps = ["DPS All Star"]
                    self.role_heal = ["Healer All Star"]
                    self.role_tank = ["Tank All Star"]
                    self.role_tag = ["M+ AllStars"]
            else:
                self.role_dps = ["3800+ r.io"]
                self.role_heal = ["3800+ r.io"]
                self.role_tank = ["3800+ r.io"]
                self.role_tag = ["3800+ r.io"]
            if self.armor_stack != "/":
                if self.armor_stack != "cloth" and self.armor_stack != "Cloth" and self.armor_stack != "mail" and self.armor_stack != "Mail":
                    self.role_tank.append(self.armor_stack.capitalize())
                    self.role_tag = [self.armor_stack.capitalize()]# + role_ping_tmp]
                else:
                    self.role_tag = [self.role_tank[0], self.armor_stack.capitalize()]# + role_ping_tmp]
                self.role_heal.append(self.armor_stack.capitalize())
                self.role_dps.append(self.armor_stack.capitalize())

    def cut(self):
        if self.no_adv_cut:
            cut = int(self.gold*0.225)
        elif self.inhouse:
            cut = int(self.gold*0.2118)
        else:
            cut = int(self.gold*0.18)
        return cut
