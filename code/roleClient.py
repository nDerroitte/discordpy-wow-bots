from datetime import datetime
import json
import requests
import traceback
import discord
import os
import asyncio
from sheet import *
from utils import *
from boost import *
from bet import *

class RoleClient(discord.Client):
    ###########################################################################
    #                                       Init                              #
    ###########################################################################
    def __init__(self, guild_name):
        self.guild_name = guild_name
        self.__list_admin_roles = ["EN - Manager", "Developer"]
        self.__list_bot_roles = ["Bot"]
        self.__list_modo_roles = ["EN - Manager", "Developer", "Moderator", "Recruiting", "Management"]
        self.raid_leader_role = ["Legacy Raids Leader", "Raid Leader Alliance", "Raid Leader Horde"]
        self.__day_id = 302188753206771714
        self.testy = False
        if self.testy == False:
            # Gino
            self.__bot_id = 686611501389316108
            self.__ally_mm =628751808512393246
            self.__horde_mm =628751835695677471
            self.__pvp = 676080492998688798
            self.__apply_adv_chan_list_id = 629129518623227914
            self.__boost_annoucement_list_id = [628751808512393246,628751835695677471,676080492998688798]
            self.__apply_chan_list_id = [714816319551176794, 628755009663795210, 697614090650255390, 705477154409939054, 682660687905947688]
            self.__m_apply = 714816319551176794
            self.__bet_chan_list_id = [709019009106051104, 709019069206233199, 709019109257642014]
            self.__strike_chan_id = 654520688870293525
        else:
            # Jmone
            self.__collecting_gold_id = 741569122957262849
            self.__bot_id = 686307367343751317
            self.__ally_mm =691328217721733140
            self.__horde_mm =691771703830773780
            self.__pvp = 691771677390143568
            self.__boost_annoucement_list_id = [691328217721733140,691771703830773780,691771677390143568]
            self.__apply_chan_list_id = [688931455929548812]
            self.__apply_adv_chan_list_id = 2
            self.__bet_chan_list_id = [708975742242914314, 706436097504182292, 708975772072935424]
            self.__strike_chan_id = 654520688870293525

        intents = discord.Intents.all()
        super(RoleClient, self).__init__(intents=intents)

    ###########################################################################
    #                              On ready function                          #
    ###########################################################################
    async def on_ready(self):
        self.__guild = discord.utils.get(self.guilds, name=self.guild_name)
        #me = discord.utils.get(self.__guild.members, id=self.__day_id)
        #await me.create_dm()
        print("OP")
        #print(onlyName("Fabioso"))
        #print(sameName("Fabioso", "fabioso-silvermoon"))
        #print(sameName("fabioso-silvermoon", "Fabioso"))
        self.heal_emo = discord.utils.get(self.__guild.emojis, name ="heal")
        self.tank_emo = discord.utils.get(self.__guild.emojis, name ="tank")
        self.dps_emo = discord.utils.get(self.__guild.emojis, name ="dps")
        self.allowed_emo = discord.utils.get(self.__guild.emojis, name ="allowed")
        self.denied_emo = discord.utils.get(self.__guild.emojis, name ="denied")
        self.chip_emo = discord.utils.get(self.__guild.emojis, name="chip")
        self.inv_emo = discord.utils.get(self.__guild.emojis, name="inv")
        self.mail_emo = discord.utils.get(self.__guild.emojis, name="mail")
        self.coin_emo = discord.utils.get(self.__guild.emojis, name="gold_coin")
        self.mercs_emo = discord.utils.get(self.__guild.emojis, name="mercs")
        self.armor_emo = discord.utils.get(self.__guild.emojis, name="armor")
        self.bronze_key_emo = discord.utils.get(self.__guild.emojis, name="bronze_key")
        self.silver_key_emo = discord.utils.get(self.__guild.emojis, name="silver_key")
        self.gold_key_emo = discord.utils.get(self.__guild.emojis, name="gold_key")
        self.nb_emo = discord.utils.get(self.__guild.emojis, name="tallycounter")

    ###########################################################################
    #                              On message receive                         #
    ###########################################################################
    async def on_message(self, message):
        ######################### Private message ############################
        if message.channel.type == discord.ChannelType.private:
            # Close
            if message.content.lower() == "close":
                user_id = message.author.id
                c_member = discord.utils.get(self.__guild.members, id=user_id)
                for role in c_member.roles:
                    if role.name in self.__list_admin_roles:
                        await message.channel.send("Shutting down the bot. It will become offline in a approx two minutes (its functionalities have already been stopped).\nTo re-activate it, once need launch the run.sh Shell script inside the gino_bot folder of the AWS server.\nContact 7yx#2397 for more information.")
                        await asyncio.sleep(1)
                        os.system('forever stop 0')
                        await self.close()
                        exit(0)
            # Ping
            elif message.content.lower() == "ping":
                user_id = message.author.id
                if user_id == self.__day_id:
                    await message.channel.send("Pong. :smile:")
            elif message.content.lower() == "error_demo":
                user_id = message.author.id
                if user_id == self.__day_id:
                    try:
                        print(demoerreur)
                    except:
                         err = traceback.format_exc()
                         embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
                         embed_error.add_field(name="Error", value = err)
                         embed_error.set_footer(text="Gino's Mercenaries")
                         day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
                         await day_member.create_dm()
                         await day_member.dm_channel.send(embed=embed_error)

            # Casgino set up
            elif message.content.lower() == "casgino set up":

                user_id = message.author.id
                if user_id == self.__day_id:
                    # TAGS
                    celia = discord.utils.get(self.__guild.members, id=self.__celia_id)
                    day = discord.utils.get(self.__guild.members, id=self.__day_id)
                    casgino_info_chan = discord.utils.get(self.__guild.channels, name='casgino-bot-information', type=discord.ChannelType.text)
                    casgino_role_chan = discord.utils.get(self.__guild.channels, name='gambler-role', type=discord.ChannelType.text)
                    gambler_tag = discord.utils.get(self.__guild.roles, name = 'Gambler')
                    # EMBED MESSAGE
                    command_str = "The commands are the same for every game mode.\n```css\n!bet 100000 [@Celia-Dalaran]\n  > Bet against specific gambler. You can tag up to four members.``` ```css\n!betanyone 100000 [4]\n  > Bet against any gamblers. Can be up to four other members.\n```"
                    embed_message = discord.Embed(title="CasGino", description="Welcome, please take a seat while I explain you the rules.", color=0x9acd32)#7FFF00#9ACD32
                    embed_message.add_field(name="How it works", value="Here gamblers roll dice to gain gold. You can play a part of your balance with other boosters. The higher roll wins. **5% of all wins goes to the community!**.\n**Disclaimer:** Although we can't verify it, you probably shouldn't play if you're under 18. Gambling can be very addictive, so be careful.", inline = False)
                    embed_message.add_field(name="Creating a bet", value="Refer to commands to create new bets.", inline = False)
                    embed_message.add_field(name="Joining a bet", value="If you were tagged in a bet or see one with a place available, you can join it by reacting with {}.".format(self.chip_emo), inline = False)
                    embed_message.add_field(name="Regular bet", value="Both players roll between 1 and the entry fee. The highest roll wins the difference between the two rolls.", inline = True)
                    embed_message.add_field(name="Hardcore bet", value="Both players roll between 1 and 100. The highest roll wins everything.", inline = True)
                    embed_message.add_field(name="Deathroll bet", value="In turn, each player rolls between 1 and the previous roll, starting with the entry fee. The first person who reaches 1 loses everything.", inline = True)
                    embed_message.add_field(name="Command", value=command_str, inline = False)
                    embed_message.add_field(name="No credit", value="We don't do credits. You have to have the gold **in your balance** to play in the casino.", inline = True)
                    embed_message.add_field(name="Notifications", value="To receive notifications concerning bets with available spots to gamble, get your {} in {}".format(gambler_tag.mention, casgino_role_chan.mention))
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await casgino_info_chan.send(embed=embed_message)

        ############################ Check balance ############################



        elif message.channel.id == self.__m_apply:
            roles = message.author.roles
            roles_str = [y.name.lower() for y in roles]
            if "customer" in roles_str and "name-realm" not in message.content.lower():
                embed_message = discord.Embed(title="Please follow the format!", description="Hello {}. Thank you for your application but could you please re-apply using our application format.".format(message.author.mention), color=0xffd700)#7FFF00
                embed_message.add_field(name="Format", value = "```Name-realm:\nFaction:\nApplying for:\nVouching for you:\nRaider.io:\nDo you advertise/Boost in other Communities (Name them):```", inline=False)
                embed_message.set_footer(text="Gino's Mercenaries")
                await message.channel.send(embed=embed_message)
                await message.add_reaction(self.denied_emo)


        elif "check-balance" in message.channel.name and message.content == "!b":
            user_id = message.author.id
            #adv = discord.utils.get(self.__guild.members, id=self.user_id)
            name = message.author.display_name
            user_name_serv = parseName(name)
            sr = sheetReader()
            gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
            await message.author.create_dm()
            await message.channel.send("I've sent you your balance by DM {}.".format(message.author.mention))
            embed_message = discord.Embed(title="Your balance", color=0x32cd32)#7FFF00
            if gold == "Nbalance":
                embed_message.add_field(name="The following nickname is not in the balance currently.", value = "{}".format(name), inline=True)
                embed_message.set_footer(text="Gino's Mercenaries")
                await message.author.dm_channel.send(embed=embed_message)
            else:
                embed_message.add_field(name="\u200b", value="Your balance is currently {} gold.".format(gold))
                embed_message.set_footer(text="Gino's Mercenaries")
                await message.author.dm_channel.send(embed=embed_message)

        ######################## Check balance modo ###########################
        elif "check-balance" in message.channel.name and message.content.startswith('!b'):
            print(message.content)
            user_id = message.author.id
            name = message.content[3:]
            serv = "guild"
            sr = sheetReader()
            gold = sr.get_gold(name,serv)
            #print(gold)
            if gold == "Nbalance":
                serv = "guilds"
                gold = sr.get_gold(name,serv)
                if gold == "Nbalance":
                    c_member = discord.utils.get(self.__guild.members, id=user_id)
                    bool_modo = False
                    for role in c_member.roles:
                        if role.name in self.__list_modo_roles:
                            bool_modo = True
                    if bool_modo:
                        user_name_serv = parseName(name)
                        if user_name_serv[0] == "" or user_name_serv[1] == "":
                            embed_message = discord.Embed(title="Oops", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value="The nickname must be in the form Name-Realm except for team.", inline=False)
                            embed_message.set_footer(text="Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        else:
                            gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                            await message.author.create_dm()
                            await message.channel.send("I've sent you the balance by DM {}.".format(message.author.mention))
                            embed_message = discord.Embed(title="The balance", color=0x32cd32)#7FFF00
                            if gold == "Nbalance":
                                embed_message.add_field(name="The following nickname is not in the balance currently.", value = "{}".format(name), inline=True)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.author.dm_channel.send(embed=embed_message)
                            else:
                                embed_message.add_field(name="\u200b", value="The balance is currently {} gold.".format(gold))
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.author.dm_channel.send(embed=embed_message)
                    else:
                        embed_message = discord.Embed(title="Oops", color=0xdc143c)#7FFF00
                        embed_message.add_field(name="\u200b", value="Only moderator can check other people balance.", inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.channel.send(embed=embed_message)

                else:
                    await message.author.create_dm()
                    await message.channel.send("I've sent you the balance by DM {}.".format(message.author.mention))
                    embed_message = discord.Embed(title="Team balance", color=0x32cd32)#7FFF00
                    embed_message.add_field(name="\u200b",value="The team balance is currently {} gold.".format(gold))
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.author.dm_channel.send(embed=embed_message)
            else:
                await message.author.create_dm()
                await message.channel.send("I've sent you the balance by DM {}.".format(message.author.mention))
                embed_message = discord.Embed(title="Team balance", color=0x32cd32)#7FFF00
                embed_message.add_field(name="\u200b",value="The team balance is currently {} gold.".format(gold))
                embed_message.set_footer(text="Gino's Mercenaries")
                await message.author.dm_channel.send(embed=embed_message)

        ######################## Add balance normal ###########################
        elif "add-balance" in message.channel.name and (message.content == "!addally" or message.content == "!addhorde"):
            ally_bool = True
            if message.content == "!addhorde":
                ally_bool = False
            name = message.author.display_name
            user_name_serv = parseName(name)
            if user_name_serv[0] == "" or user_name_serv[1] == "":
                embed_message = discord.Embed(title="Oops", color=0xdc143c)#7FFF00
                embed_message.add_field(name="\u200b", value="Your nickname must be in the form Name-Realm to be added to the balance.", inline=False)
                embed_message.set_footer(text="Gino's Mercenaries")
                await message.channel.send(embed=embed_message)
            else:
                sr = sheetReader()
                ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                check_channel = discord.utils.get(self.__guild.channels, name='📈check-balance', type=discord.ChannelType.text)
                balance_channel = discord.utils.get(self.__guild.channels, name='📂balance-sheets', type=discord.ChannelType.text)

                if ack == "ok":
                    embed_message = discord.Embed(title="Welcome!", color=0xffd700)#7FFF00
                    embed_message.add_field(name="\u200b", value = "{} has been succesfully added to the balance. You can now check your gold by typing !b in the {} or referring to the {}.".format(name, check_channel.mention, balance_channel.mention), inline=False)
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                if ack == "AlreadyIn":
                    embed_message = discord.Embed(title="Oops!", color=0xdc143c)#7FFF00
                    embed_message.add_field(name="\u200b", value = "It seems that {} is already in the balance. You can verify by typing !b in the {} or referring to the {}.".format(name, check_channel.mention, balance_channel.mention), inline=False)
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)

        ######################## Add balance team #############################
        elif "add-balance" in message.channel.name and (message.content.startswith("!addally team") or message.content.startswith("!addhorde team")):
            ally_bool = True
            name = message.content[14:]
            serv = "guild"
            if message.content.startswith("!addhorde"):
                name = message.content[15:]
                ally_bool = False
            user_id = message.author.id
            c_member = discord.utils.get(self.__guild.members, id=user_id)
            for role in c_member.roles:
                if role.name in self.__list_modo_roles:
                    if name == "":
                        embed_message = discord.Embed(title="Oops", color=0xdc143c)#7FFF00
                        embed_message.add_field(name="\u200b", value="You can not enter an empty name team in the balance", inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.channel.send(embed=embed_message)
                    else:
                        sr = sheetReader()
                        ack = sr.add_balance(name, serv, ally_bool)
                        check_channel = discord.utils.get(self.__guild.channels, name='📈check-balance', type=discord.ChannelType.text)
                        balance_channel = discord.utils.get(self.__guild.channels, name='📂balance-sheets', type=discord.ChannelType.text)

                        if ack == "ok":
                            embed_message = discord.Embed(title="Welcome!", color=0xffd700)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The team {} has been succesfully added to the balance. You can now check the team gold by typing !b in the {} or referring to the {}.".format(name, check_channel.mention, balance_channel.mention), inline=False)
                            embed_message.set_footer(text="Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        if ack == "AlreadyIn":
                            embed_message = discord.Embed(title="Oops!", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "It seems that the team {} is already in the balance. You can verify typing !b in the {} or referring to the {}.".format(name, check_channel.mention, balance_channel.mention), inline=False)
                            embed_message.set_footer(text="Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)

        ########################## Add balance modo ###########################
        elif "add-balance" in message.channel.name and (message.content.startswith("!addally ") or message.content.startswith("!addhorde ")):
            ally_bool = True
            name = message.content[9:]
            if message.content.startswith("!addhorde"):
                ally_bool = False
                name = message.content[10:]
            user_id = message.author.id
            c_member = discord.utils.get(self.__guild.members, id=user_id)
            for role in c_member.roles:
                if role.name in self.__list_modo_roles:
                    # PARSER LE NAME
                    user_name_serv = parseName(name)
                    if user_name_serv[0] == "" or user_name_serv[1] == "":
                        embed_message = discord.Embed(title="Oops", color=0xdc143c)#7FFF00
                        embed_message.add_field(name="\u200b", value="The nickname must be in the form Name-Realm to be added to the balance.", inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.channel.send(embed=embed_message)
                    else:
                        sr = sheetReader()
                        ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                        check_channel = discord.utils.get(self.__guild.channels, name='📈check-balance', type=discord.ChannelType.text)
                        balance_channel = discord.utils.get(self.__guild.channels, name='📂balance-sheets', type=discord.ChannelType.text)

                        if ack == "ok":
                            embed_message = discord.Embed(title="Welcome!", color=0xffd700)#7FFF00
                            embed_message.add_field(name="\u200b", value = "{} has been succesfully added to the balance. You can now check your gold by typing !b in the {} or referring to the {}.".format(name, check_channel.mention, balance_channel.mention), inline=False)
                            embed_message.set_footer(text="Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        if ack == "AlreadyIn":
                            embed_message = discord.Embed(title="Oops!", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "It seems that {} is already in the balance. You can check your gold by typing !b in the {} or referring to the {}.".format(name, check_channel.mention, balance_channel.mention), inline=False)
                            embed_message.set_footer(text="Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)

        ########################## Update MM roles ############################
        elif "m-roles" in message.channel.name and message.content.startswith("!update "):
            try:
                name = message.content.split(" ", 1)[1]
                user_name_serv = parseName(name)
                other_role_chan = discord.utils.get(self.__guild.channels, name='🔰other-roles', type=discord.ChannelType.text)
                if user_name_serv[0] == "" or user_name_serv[1] == "":
                    embed_message = discord.Embed(title="Oops", color=0xdc143c)#7FFF00
                    embed_message.add_field(name="\u200b", value="The nickname must be in the form Name-Realm.", inline=False)
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                else:
                    roles = message.author.roles
                    roles_str = [y.name.lower() for y in roles]
                    roles_added = []
                    bool_nick_change = False
                    nickname = message.author.display_name
                    nick_user_name_serv = parseName(nickname)
                    get_url = "https://raider.io/api/v1/characters/profile?region=eu&realm={}&name={}&fields=mythic_plus_scores_by_season%3Acurrent".format(user_name_serv[1].lower(),user_name_serv[0].lower().capitalize())
                    r = requests.get(get_url)
                    if r.status_code == 200:
                        data = r.json()
                        print(data)
                        rio = data["mythic_plus_scores_by_season"][0]['scores']['all']
                        rio_heal = data["mythic_plus_scores_by_season"][0]['scores']['healer']
                        rio_tank = data["mythic_plus_scores_by_season"][0]['scores']['tank']
                        rio_dps = data["mythic_plus_scores_by_season"][0]['scores']['dps']
                        faction = data["faction"]
                        wow_class = data["class"]
                        if rio_tank > 1950 or rio_heal > 1950 or rio_dps > 1950:
                            if wow_class.lower() not in roles_str:
                                roles_added.append(wow_class)
                                wow_class_rank = discord.utils.get(self.__guild.roles, name=wow_class)
                                await message.author.add_roles(wow_class_rank)
                            if faction == "alliance" and "m+ alliance" not in roles_str:
                                roles_added.append("M+ Alliance")
                                fact = discord.utils.get(self.__guild.roles, name='M+ Alliance')
                                await message.author.add_roles(fact)
                            elif faction == "horde" and "m+ horde" not in roles_str:
                                roles_added.append("M+ Horde")
                                fact = discord.utils.get(self.__guild.roles, name='M+ Horde')
                                await message.author.add_roles(fact)
                            if data["class"] in ["Rogue", "Monk", "Demon Hunter","Druid"] and "Leather" not in roles_str:
                                roles_added.append("Leather")
                                Leather = discord.utils.get(self.__guild.roles, name='Leather')
                                await message.author.add_roles(Leather)
                            if data["class"] in ["Paladin", "Warrior", "Death Knight"] and "Plate" not in roles_str:
                                roles_added.append("Plate")
                                Plate = discord.utils.get(self.__guild.roles, name='Plate')
                                await message.author.add_roles(Plate)
                            if data["class"] in ["Hunter", "Shaman"] and "Mail" not in roles_str:
                                roles_added.append("Mail")
                                Mail = discord.utils.get(self.__guild.roles, name='Mail')
                                await message.author.add_roles(Mail)
                            if data["class"] in ["Priest", "Mage", "Warlock"] and "Cloth" not in roles_str:
                                roles_added.append("Cloth")
                                Cloth = discord.utils.get(self.__guild.roles, name='Cloth')
                                await message.author.add_roles(Cloth)
                            if "m+ prestige" not in roles_str:
                                roles_added.append("M+ Prestige")
                                m_prestige = discord.utils.get(self.__guild.roles, name='M+ Prestige')
                                await message.author.add_roles(m_prestige)
                            if rio_heal > 1950 and "healer prestige" not in roles_str:
                                roles_added.append("Healer Prestige")
                                healer_prestige = discord.utils.get(self.__guild.roles, name='Healer Prestige')
                                await message.author.add_roles(healer_prestige)
                            if rio_tank > 1950 and "tank prestige" not in roles_str:
                                roles_added.append("Tank Prestige")
                                tank_prestige = discord.utils.get(self.__guild.roles, name='Tank Prestige')
                                await message.author.add_roles(tank_prestige)
                            if rio_dps > 1950 and "dps prestige" not in roles_str:
                                roles_added.append("DPS Prestige")
                                dps_prestige = discord.utils.get(self.__guild.roles, name='DPS Prestige')
                                await message.author.add_roles(dps_prestige)
                        if rio_tank > 2150 or rio_heal > 2150 or rio_dps > 2150:
                            if "m+ allstars" not in roles_str:
                                roles_added.append("M+ AllStars")
                                m_all_star = discord.utils.get(self.__guild.roles, name='M+ AllStars')
                                await message.author.add_roles(m_all_star)
                            if rio_heal > 2150 and "healer all star" not in roles_str:
                                roles_added.append("Healer All Star")
                                healer_all_star = discord.utils.get(self.__guild.roles, name='Healer All Star')
                                await message.author.add_roles(healer_all_star)
                            if rio_tank > 2150 and "tank all star" not in roles_str:
                                roles_added.append("Tank All Star")
                                tank_all_star = discord.utils.get(self.__guild.roles, name='Tank All Star')
                                await message.author.add_roles(tank_all_star)
                            if rio_dps > 2150 and "dps all star" not in roles_str:
                                roles_added.append("DPS All Star")
                                dps_all_star = discord.utils.get(self.__guild.roles, name='DPS All Star')
                                await message.author.add_roles(dps_all_star)

                        embed_message = discord.Embed(title="Roles updated", color=0xffd700)#7FFF00
                        if len(roles_added) > 0:
                            embed_message.add_field(name="\u200b", value = "You have been succesfully added the following roles: {}.".format(', '.join(roles_added)), inline=False)
                        else:
                            embed_message.add_field(name="\u200b", value = "No new roles have been found.")
                        embed_message.add_field(name="\u200b", value = "If you think that one or more roles may be missing, please contact a moderator or introduce a manual request in {}.".format(other_role_chan.mention), inline=False)
                        if bool_nick_change:
                            balance_channel = discord.utils.get(self.__guild.channels, name='📂balance-sheets', type=discord.ChannelType.text)
                            embed_message.add_field(name="\u200b", value = "If not already done, you should add yourself to the balance sheet! Check {} for more information!".format(balance_channel.mention), inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.author.create_dm()
                        await message.author.dm_channel.send(embed=embed_message)
                        await message.channel.send("I've send you a DM with the result of your request {}.".format(message.author.mention))
                    else:
                        embed_message = discord.Embed(title="Oops", color=0xdc143c)#7FFF00
                        embed_message.add_field(name="\u200b", value="Something went wrong while looking {} in raider.io. Check if the nickname is correct.\n".format(name), inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.channel.send(embed=embed_message)
            except:
                err = traceback.format_exc()
                embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
                embed_error.add_field(name="Error", value = err)
                embed_error.set_footer(text="Gino's Mercenaries")
                day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
                await day_member.create_dm()
                await day_member.dm_channel.send(embed=embed_error)

        ############################## mm - roles #############################
        elif "other-roles" in message.channel.name and "https://raider.io/characters/" in message.content:
            mm_roles = discord.utils.get(self.__guild.channels, name='🔰m-roles', type=discord.ChannelType.text)
            await message.channel.send("Hi {}.\nI saw that you linked a raider.io profile. \nFor any M+ related roles, please consider using {}.\nIf your request is not related to M+, someone will handle it soon! :smile:.".format(message.author.mention, mm_roles.mention))

        ############################## reload #############################
        elif message.channel.name == "private-bot-commands" and message.content.startswith("!rename"):
            reload_dict()
            await message.add_reaction(self.allowed_emo)



    ###########################################################################
    #                              On reaction add                            #
    ###########################################################################
    async def on_raw_reaction_add(self, payload):
        try:
            channel = discord.utils.get(self.__guild.channels, id=payload.channel_id, type=discord.ChannelType.text)
            message = await channel.fetch_message(payload.message_id)
            user = discord.utils.get(self.__guild.members, id=payload.user_id)
            emoji = payload.emoji
            if emoji.is_unicode_emoji():
                emoji = str(emoji)
            if user.id != self.__bot_id:
                # Apply adv
                if message.channel.id == self.__apply_adv_chan_list_id:
                    bool_modo = False
                    for role in user.roles:
                        if role.name in self.__list_modo_roles:
                            bool_modo = True
                    if bool_modo == True and emoji == self.allowed_emo:
                        adv_guid_chan = discord.utils.get(self.__guild.channels, name='📚advertising-guide', type=discord.ChannelType.text)
                        advertising_focus_chan = discord.utils.get(self.__guild.channels, name='❗advertising-focus', type=discord.ChannelType.text)
                        mailing_gold_chan = discord.utils.get(self.__guild.channels, name='📧mailing-gold', type=discord.ChannelType.text)
                        annoucement_chan_a2 = discord.utils.get(self.__guild.channels, id=self.__ally_mm)
                        annoucement_chan_h2 = discord.utils.get(self.__guild.channels, id=self.__horde_mm)
                        role_leather = discord.utils.get(self.__guild.roles, name='Leather')
                        role_plate = discord.utils.get(self.__guild.roles, name='Plate')
                        role_mail = discord.utils.get(self.__guild.roles, name='Mail')
                        role_cloth = discord.utils.get(self.__guild.roles, name='Cloth')
                        role_tank_star = discord.utils.get(self.__guild.roles, name='Tank All Star')
                        role_m_star = discord.utils.get(self.__guild.roles, name='M+ AllStars')
                        embed_message = discord.Embed(title="Congratulations!", color=0x61b3f2, description="You've been succesfully accepted as an advertiser in our community!")#7FFF00
                        embed_message.add_field(name="Here you will find some information:", value="- We will only accept __gold__ as payment for the boosts!\n- Navigate to the {} channel first to check our macros and guides. \n- Check the {} channel to see our current focus.\n\n**__Below you will find a short FAQ__**".format(adv_guid_chan.mention, advertising_focus_chan.mention),inline=False)
                        embed_message.add_field(name="Where do I have to mail the gold?", value="Visit the {} channel, here you will find a list of all the information.".format(mailing_gold_chan.mention), inline=False)
                        embed_message.add_field(name="Where can I find the bot to post a boost?", value="Send us, a mod or one from the management your email-address to grant you access to the bot.",inline=False)
                        embed_message.add_field(name="How do I search for a specific key?", value="Go to the {} channel for Alliance or {} for Horde and ping:\n- If you are looking for a key holder with an armor stack @Plate, @Mail, @Leather or @Cloth (+ @Tank All Star for mail or cloth boost)\n- If you are looking for a key holder with a specific rank, e.g. All Star, you need to use @M+ AllStars.".format(annoucement_chan_a2.mention, annoucement_chan_h2.mention),inline=False)
                        embed_message.add_field(name="How do I book customers for our raids?", value="To book a buyer for a Jaina or Ny'alotha Heroic & Mythic run, you must send all the necessary information to me, or an available trusted advertiser.",inline=False)
                        embed_message.add_field(name="What information do you need to book my customer?", value="Please send us the following information: \nBuyer Name, Battletag, Loot Status (What they are booking for, e.g. 12/12 Personal Loot), Total Price, Deposit Collected, Collected By, Collection Realm.",inline=False)
                        embed_message.add_field(name="What are the advertiser cuts?", value="M+ 18%, (15% for new advertiser), Heroic Raids 15%, Island & Freehold 10%, torghast 18%, PVP 15% \n\nIf you have any questions, feel free to contact me (Dino) or any other available mod/trusted advertiser.", inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.author.create_dm()
                        await message.author.dm_channel.send(embed= embed_message)
                # Apply
                if message.channel.id in self.__apply_chan_list_id:
                    bool_modo = False
                    for role in user.roles:
                        if role.name in self.__list_modo_roles:
                            bool_modo = True
                    if bool_modo == True and emoji == self.allowed_emo:
                        if "mplus" in channel.name:
                            # GET NAME and rename:
                            name_realm = get_name_realm(message.content)
                            user_name_realm = parseName(name_realm)
                            try:
                                val = name_realm.split("-")
                                name = val[0].capitalize()
                                realm = val[1].capitalize()
                                name_realm = name + "-" + realm
                                print(name_realm)
                            except:
                                pass
                            await message.author.edit(nick=name_realm)
                            # roles
                            roles = message.author.roles
                            roles_str = [y.name.lower() for y in roles]
                            if "customer" in roles_str:
                                customer_role = discord.utils.get(self.__guild.roles, name='Customer')
                                await message.author.remove_roles(customer_role)
                            get_url = "https://raider.io/api/v1/characters/profile?region=eu&realm={}&name={}&fields=mythic_plus_scores_by_season%3Acurrent".format(user_name_realm[1].lower(),user_name_realm[0].lower().capitalize())
                            r = requests.get(get_url)
                            if r.status_code == 200:
                                data = r.json()
                                rio = data["mythic_plus_scores_by_season"][0]['scores']['all']
                                rio_heal = data["mythic_plus_scores_by_season"][0]['scores']['healer']
                                rio_tank = data["mythic_plus_scores_by_season"][0]['scores']['tank']
                                rio_dps = data["mythic_plus_scores_by_season"][0]['scores']['dps']
                                faction = data["faction"]
                                wow_class = data["class"]
                                if rio_tank > 1950 or rio_heal > 1950 or rio_dps > 1950:
                                    if wow_class.lower() not in roles_str:
                                        wow_class_rank = discord.utils.get(self.__guild.roles, name=wow_class)
                                        await message.author.add_roles(wow_class_rank)
                                    if faction == "alliance" and "m+ alliance" not in roles_str:
                                        fact = discord.utils.get(self.__guild.roles, name='M+ Alliance')
                                        await message.author.add_roles(fact)
                                    elif faction == "horde" and "m+ horde" not in roles_str:
                                        fact = discord.utils.get(self.__guild.roles, name='M+ Horde')
                                        await message.author.add_roles(fact)
                                    if data["class"] in ["Rogue", "Monk", "Demon Hunter","Druid"] and "Leather" not in roles_str:
                                        Leather = discord.utils.get(self.__guild.roles, name='Leather')
                                        await message.author.add_roles(Leather)
                                    if data["class"] in ["Paladin", "Warrior", "Death Knight"] and "Plate" not in roles_str:
                                        Plate = discord.utils.get(self.__guild.roles, name='Plate')
                                        await message.author.add_roles(Plate)
                                    if data["class"] in ["Hunter", "Shaman"] and "Mail" not in roles_str:
                                        Mail = discord.utils.get(self.__guild.roles, name='Mail')
                                        await message.author.add_roles(Mail)
                                    if data["class"] in ["Priest", "Mage", "Warlock"] and "Cloth" not in roles_str:
                                        Cloth = discord.utils.get(self.__guild.roles, name='Cloth')
                                        await message.author.add_roles(Cloth)
                                    m_prestige = discord.utils.get(self.__guild.roles, name='M+ Prestige')
                                    await message.author.add_roles(m_prestige)
                                    if rio_heal > 1950:
                                        healer_prestige = discord.utils.get(self.__guild.roles, name='Healer Prestige')
                                        await message.author.add_roles(healer_prestige)
                                    if rio_tank > 1950:
                                        tank_prestige = discord.utils.get(self.__guild.roles, name='Tank Prestige')
                                        await message.author.add_roles(tank_prestige)
                                    if rio_dps > 1950:
                                        dps_prestige = discord.utils.get(self.__guild.roles, name='DPS Prestige')
                                        await message.author.add_roles(dps_prestige)
                                if rio_tank > 2150 or rio_heal > 2150 or rio_dps > 2150:
                                    m_all_star = discord.utils.get(self.__guild.roles, name='M+ AllStars')
                                    await message.author.add_roles(m_all_star)
                                    if rio_heal > 2150:
                                        healer_all_star = discord.utils.get(self.__guild.roles, name='Healer All Star')
                                        await message.author.add_roles(healer_all_star)
                                    if rio_tank > 2150:
                                        tank_all_star = discord.utils.get(self.__guild.roles, name='Tank All Star')
                                        await message.author.add_roles(tank_all_star)
                                    if rio_dps > 2150:
                                        dps_all_star = discord.utils.get(self.__guild.roles, name='DPS All Star')
                                        await message.author.add_roles(dps_all_star)
                        # MESSAGE:
                        mm_roles_chan = discord.utils.get(self.__guild.channels, name='🔰m-roles', type=discord.ChannelType.text)
                        other_role_chan = discord.utils.get(self.__guild.channels, name='🔰other-roles', type=discord.ChannelType.text)
                        add_balance_chan = discord.utils.get(self.__guild.channels, name='📬add-balance', type=discord.ChannelType.text)
                        check_balance_chan = discord.utils.get(self.__guild.channels, name='📈check-balance', type=discord.ChannelType.text)
                        howpaid_chan = discord.utils.get(self.__guild.channels, name='💰how-do-i-get-paid', type=discord.ChannelType.text)
                        embed_message = discord.Embed(title="Welcome!", color=0x61b3f2, description="You've been succesfully accepted as a booster in our community!")#7FFF00
                        embed_message.add_field(name="Verification", value="You’ve been renamed in the community Discord. Please check if the name corresponds to your character. You will be paid based on said nickname.\nYou’ve also had roles added corresponding to what you can boost. If you think you are missing some or want to apply for more roles, please check {} for M+ roles and {} for other roles.".format(mm_roles_chan.mention, other_role_chan.mention),inline=False)
                        embed_message.add_field(name="Adding yourself to the balance", value="The first thing you should do, is to add yourself to the balance sheet. Please use the command **!addally** or **!addhorde** (depending on your faction) in {}. **You only need to do this once!**".format(add_balance_chan.mention), inline=False)
                        embed_message.add_field(name="Applying for a boost", value="The boosts will be posted boost-announcement channel. In most cases, you simply have to react with the emoji of your role to apply ({} {} {}). **If you don't see your roles under the boost message, you arrived too late.**\nFor some specific boosts (PVP for example), you may have to send a DM to the advertiser. This will be stated in the announcement.".format(self.dps_emo,self.tank_emo,self.heal_emo),inline=False)
                        embed_message.add_field(name="Getting your gold", value="Having boosters all over Europe, you will get paid every 3-4 weeks, at the end of the cycle. You can find more information on payment on {} which also contains the next payment date.\nTo check the gold you currently own in the community, please refer to {} once you've added yourself to the balance.".format(howpaid_chan.mention, check_balance_chan.mention), inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.author.create_dm()
                        await message.author.dm_channel.send(embed= embed_message)

        except:
                err = traceback.format_exc()
                embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
                embed_error.add_field(name="Error", value = err)
                embed_error.set_footer(text="Gino's Mercenaries")
                day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
                await day_member.create_dm()
                await day_member.dm_channel.send(embed=embed_error)
