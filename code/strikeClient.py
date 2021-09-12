import random
import json
import requests
import discord
import os
import asyncio
from utils import *
from strikeSheet import *
import name_dict_lib
from importlib import reload
from priceSheet import *
from giveaway import *
from sheet import *
from datetime import datetime


class strikeClient(discord.Client):
    ###########################################################################
    #                                       Init                              #
    ###########################################################################
    def __init__(self, guild_name):
        self.guild_name = guild_name
        self.__list_admin_roles = ["EN - Manager", "Developer"]
        self.__list_bot_roles = ["Bot"]
        self.__list_modo_roles = ["EN - Manager", "Developer", "Moderator"]
        self.event_leader_role = ["Support"]
        self.__events = []
        self.__day_id = 302188753206771714
        self.testy = False
        self.to_update_members = []
        self.booking_id = 1693 + 1
        self.ticket_id = 1397 + 1
        self.help_id = 100 + 1
        self.giveaway_list = []
        self.real_list_nitro = []
        self.list_nitro_str = ""
        if self.testy == False:
            # Gino
            self.__bot_id = 733080115306561636
            self.__strike_chan_id = 654520688870293525
            self.__booking_chan_id = 757163555815686144
            self.price_dict = {683130342651068426 : "pveally", 880528230803722270 : "pvehorde", 633334207334055948 :"pvp", 676097936584867850 : "legacy", 886031845190402048 : "mount",  677127738993279010 : "mercs"}
            self.__mercs_chan_id = 677127738993279010
            self.__mercs_ticket_id = 794724553661480960
            self.__mercs_help_id = 818614702003191848
            self.__public_strike_chan_id = 815530788761108480
        else:
            # Jmone
            self.__bot_id = 733080115306561636
            self.__strike_chan_id = 733066222417215588
            self.__booking_chan_id = 756863106218459158
            self.price_dict = {761682393693945896 : "pve"}
            self.__mercs_chan_id = 677127738993279010
            self.__mercs_ticket_id = 794724553661480960
        intents = discord.Intents.all()
        super(strikeClient, self).__init__(intents=intents)

    ###########################################################################
    #                              On ready function                          #
    ###########################################################################
    async def on_ready(self):
        self.__guild = discord.utils.get(self.guilds, name=self.guild_name)
        #me = discord.utils.get(self.__guild.members, id=self.__day_id)
        #await me.create_dm()

        print("OP")
        self.allowed_emo = discord.utils.get(self.__guild.emojis, name ="allowed")
        self.denied_emo = discord.utils.get(self.__guild.emojis, name ="denied")
        self.chip_emo = discord.utils.get(self.__guild.emojis, name="chip")
        self.allseer_emo = discord.utils.get(self.__guild.emojis, name ="allseer")
        self.peperage_emo = discord.utils.get(self.__guild.emojis, name ="peperage")
        self.inv_emo = discord.utils.get(self.__guild.emojis, name="inv")
        self.mail_emo = discord.utils.get(self.__guild.emojis, name="mail")

    ###########################################################################
    #                              On message receive                         #
    ###########################################################################
    async def on_message(self, message):
        try:
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

                elif message.content.lower() == "mayu":
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        adv_chan  = discord.utils.get(self.__guild.channels, id=674212223945670667, type=discord.ChannelType.text)
                        mayu = discord.utils.get(self.__guild.members, id=227039513384452096)
                        await adv_chan.send("{} stop pinging me please {} Oh and happy birthday btw.".format(mayu.mention, self.peperage_emo))

                elif message.content.lower() == "c":
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        await message.channel.send(f"Bookings:{self.booking_id}\nTickets:{self.ticket_id}\nHelps:{self.help_id}")

                elif message.content.lower() == "ping":
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        await message.channel.send(self.giveaway_list)

                # Giveaway
                elif message.content.lower().startswith("giveaway"):
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        values = message.content.split("_")
                        role = values[1]
                        prize = values[2]
                        nb_winners = values[3]
                        end_date = values[4]
                        channel_id = values[5]
                        if RepresentsInt(channel_id):
                            channel_id = int(channel_id)
                        ga = giveaway(role, prize, end_date, channel_id, nb_winners= nb_winners)
                        ga.create_participants_list(self.__guild)
                        embed_msg = ga.giveaway_embed()
                        print(embed_msg)
                        giveaway_channel = discord.utils.get(self.__guild.channels, id=channel_id, type=discord.ChannelType.text)
                        msg = await giveaway_channel.send(embed=embed_msg)
                        ga.message = msg
                        self.giveaway_list.append(ga)
                        await msg.add_reaction(self.allowed_emo)
                        await msg.add_reaction("🎉")
                        await msg.add_reaction("🔧")

                elif message.content.lower().startswith("!editgiveaway"):
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        values = message.content.split("_")
                        for ga in self.giveaway_list:
                            if ga.message.id == int(values[1]):
                                member_to_add = discord.utils.get(self.__guild.members, id=int(values[2]))
                                ga.add_participant(member_to_add)
                                embed_message = ga.giveaway_embed()
                                await ga.message.edit(embed=embed_message)
                                break
                elif message.content.lower() == "request":
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        booking_channel = discord.utils.get(self.__guild.channels, id=self.__booking_chan_id, type=discord.ChannelType.text)
                        embed_message = discord.Embed(title="Booking Request", color=0x9acd32)#7FFF00#9ACD32
                        embed_message.add_field(name="Welcome :clap:", value="Hey! Got a question, or looking for Mercenaries to help you out? \nPress 🇬🇧\n \u200b", inline = False)
                        embed_message.add_field(name="Bienvenue :wave:", value="Salut! Tu as une question ou cherches des Mercenaires?\nRéagis avec 🇫🇷\n \u200b", inline = False)
                        embed_message.add_field(name="Willkommen :ok_hand:", value="Hi! Suchst du nach Söldnern zur Unterstützung oder du hast eine Frage?\n Reagiere mit 🇩🇪 \n \u200b", inline = False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        tmp = await booking_channel.send(embed=embed_message)
                        await tmp.add_reaction("🇬🇧")
                        await tmp.add_reaction("🇫🇷")
                        await tmp.add_reaction("🇩🇪")

                elif message.content.lower() == "request_mercs":
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        booking_channel = discord.utils.get(self.__guild.channels, id=self.__mercs_ticket_id, type=discord.ChannelType.text)
                        embed_message = discord.Embed(title="Help ticket", description="Hey! Got a question or looking for a information you don't find on discord? Create a ticket here by pressing the :mailbox:. ", color=0x9acd32)#7FFF00#9ACD32
                        embed_message.add_field(name="Avoid DM", value="Please, always consider using this ticket tool instead of sending a DM to a member of the staff.", inline = False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        tmp = await booking_channel.send(embed=embed_message)
                        await tmp.add_reaction("📫")

                elif message.content.lower() == "request_help":
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        help_channel = discord.utils.get(self.__guild.channels, id=self.__mercs_help_id, type=discord.ChannelType.text)
                        embed_message = discord.Embed(title="Help ticket", description="Hey! Got a question or looking for a information you don't find on discord? Create a ticket here by pressing the :mailbox:. ", color=0x9acd32)#7FFF00#9ACD32
                        embed_message.set_footer(text="Gino's Mercenaries")
                        tmp = await help_channel.send(embed=embed_message)
                        await tmp.add_reaction("📫")


            ############################## Strike $$ #############################
            elif message.channel.id == self.__public_strike_chan_id and message.content == "!s":
                name = message.author.display_name
                error = ""
                try:
                    stricky = self.get_stricky(name)
                    ss = sheetStrike()
                    ack = ss.see(stricky.display_name)
                    if ack == []:
                        error = "not in"
                    else:
                        str_message = "**{}**'s strike information:\nNumber of strike: **{}**\nLast strike: **{}**".format(stricky.display_name, int(ack[0]), ack[1])
                except:
                    error = "who"
                if error == "not in" or error == "who":
                    str_message = "There is no strike encoded in the database for {}".format(name)
                await message.author.create_dm()
                await message.author.dm_channel.send(str_message)
                await message.add_reaction("📬")
            elif message.channel.id == self.__strike_chan_id:
                error = ""
                if message.content.startswith("!see "):
                    try:
                        name = message.content.split(" ", 1)[1]
                    except:
                        error = "who"
                    if error == "":
                        try:
                            stricky = self.get_stricky(name)
                            ss = sheetStrike()
                            ack = ss.see(stricky.display_name)
                            if ack == []:
                                error = "not in"
                            else:
                                await message.channel.send("**{}**'s strike information:\nNumber of strike: **{}**\nLast strike: **{}**".format(stricky.display_name, int(ack[0]), ack[1]))
                        except:
                            error = "who"
                if message.content.startswith("!strike "):
                    try:
                        name = message.content.split(" ", 1)[1]
                    except:
                        error = "who"
                    if error == "":
                        try:
                            stricky = self.get_stricky(name)
                            ss = sheetStrike()
                            nb_strikes = ss.strike(stricky.display_name)
                            await message.channel.send("Succesfully added a strike to **{}** who now has {} strike(s).".format(stricky.display_name, nb_strikes))
                        except:
                            error = "who"
                elif message.content.startswith("!reset "):
                    try:
                        name = message.content.split(" ", 1)[1]
                    except:
                        error = "who"
                    if error == "":
                        try:
                            stricky = self.get_stricky(name)
                            ss = sheetStrike()
                            ack = ss.reset(stricky.display_name)
                            if ack == "who":
                                error = "not in"
                            else:
                                await message.channel.send("Succesfully reseted **{}**'s strike(s).".format(stricky.display_name, int(ack)))
                        except:
                            error = "who"
                elif message.content.startswith("!unstrike "):
                    try:
                        name = message.content.split(" ", 1)[1]
                    except:
                        error = "who"
                    if error == "":
                        try:
                            stricky = self.get_stricky(name)
                            ss = sheetStrike()
                            ack = ss.unstrike(stricky.display_name)
                            if ack == "who":
                                error = "not in"
                            else:
                                await message.channel.send("Succesfully unstriked **{}** who now have {} strike(s).".format(stricky.display_name, int(ack)))
                        except:
                            error = "who"
                elif message.content.startswith("!remove_balance "):
                    try:
                        val = message.content.split(" ")
                        name = val[1]
                        gold = val[2]
                        print(name)
                        print(gold)
                    except:
                        error = "who"
                    try:
                        gold = int(gold)
                        gold *= -1
                    except:
                        error = "gold"
                    if error == "":
                        user_name_serv = parseName(name)
                        sr = sheetReader()
                        ack = sr.add_gold(user_name_serv[0],user_name_serv[1], gold)
                        if ack == "ok":
                            await message.channel.send("Done!")
                        else:
                            error = "who_balance"
                if error == "who":
                    embed_message = discord.Embed(title="Unknown booster", description="Couldn't find **{}** in discord.".format(name), color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                if error == "who_balance":
                    embed_message = discord.Embed(title="Unknown booster", description="Couldn't find **{}** in the balance.".format(name), color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                if error == "gold":
                    embed_message = discord.Embed(title="Gold as a number", description="Please, introduce a number of gold in full digit.".format(name), color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                if error == "not in":
                    embed_message = discord.Embed(title="Couldn't find booster", description="Couldn't find **{}** in the strike sheet.".format(stricky.display_name), color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
            ############################## Update all $$ #############################
            elif message.channel.name == "private-bot-commands" and message.content == "!resetseason":
                all_members = message.guild.members#list(self.get_all_members())
                for member in all_members:
                    roles_str = [y.name.lower() for y in member.roles]
                    if "m+ prestige" in roles_str:
                        allstar_role = discord.utils.get(self.__guild.roles, name='M+ Prestige')
                        await member.remove_roles(allstar_role)
                        if "healer prestige" in roles_str:
                            healer_all_star = discord.utils.get(self.__guild.roles, name='Healer Prestige')
                            await member.remove_roles(healer_all_star)
                        if "tank prestige" in roles_str:
                            tank_all_star = discord.utils.get(self.__guild.roles, name='Tank Prestige')
                            await member.remove_roles(tank_all_star)
                        if "dps prestige" in roles_str:
                            dps_all_star = discord.utils.get(self.__guild.roles, name='DPS Prestige')
                            await member.remove_roles(dps_all_star)
                    if "m+ allstars" in roles_str:
                        allstar_role = discord.utils.get(self.__guild.roles, name='M+ AllStars')
                        await member.remove_roles(allstar_role)
                        if "healer all star" in roles_str:
                            healer_all_star = discord.utils.get(self.__guild.roles, name='Healer All Star')
                            await member.remove_roles(healer_all_star)
                        if "tank all star" in roles_str:
                            tank_all_star = discord.utils.get(self.__guild.roles, name='Tank All Star')
                            await member.remove_roles(tank_all_star)
                        if "dps all star" in roles_str:
                            dps_all_star = discord.utils.get(self.__guild.roles, name='DPS All Star')
                            await member.remove_roles(dps_all_star)
                await message.channel.send("All done! :tada:")
            elif message.channel.name == "private-bot-commands" and message.content == "!prepatchreset":
                boosters = []
                all_members = message.guild.members#list(self.get_all_members())
                if len(self.to_update_members) == 0:
                    for i in range(len(all_members)):
                        roles_str = [o.name for o in all_members[i].roles]
                        if "3800+ r.io" in roles_str:
                            boosters.append(all_members[i])
                count = 1
                print(len(boosters))
                len_to_update_members = len(boosters)
                for i in range(len_to_update_members):
                    try:
                        booster = boosters.pop()
                        if count % 100 == 0:
                            await asyncio.sleep(70)
                        roles_str = [y.name.lower() for y in booster.roles]
                        name_realm = parseName(booster.display_name)
                        realm = name_realm[1].replace("'","")
                        realm = realm.replace(" ","")
                        get_url = "https://raider.io/api/v1/characters/profile?region=eu&realm={}&name={}&fields=mythic_plus_scores_by_season%3Aseason-bfa-4".format(realm.lower(),name_realm[0].lower().capitalize())
                        r = requests.get(get_url)
                        if r.status_code == 200:
                            data = r.json()
                            rio = data["mythic_plus_scores_by_season"][0]['scores']['all']
                            if rio < 3800:
                                high_rio_rank = discord.utils.get(self.__guild.roles, name='3800+ r.io')
                                await booster.remove_roles(high_rio_rank)
                                print(booster.display_name)
                    except:
                        pass
                print("all done")
            elif message.channel.name == "private-bot-commands" and message.content == "!mraider":
                downgraded_boosters = []
                all_members = message.guild.members#list(self.get_all_members())
                for member in all_members:
                    roles_str = [o.name for o in member.roles]
                    if "Raider Alliance" in roles_str:
                        m_alliance = discord.utils.get(self.__guild.roles, name='Raider Alliance')
                        await member.remove_roles(m_alliance)
                        if 'M+ Alliance' not in roles_str:
                            m_alliance = discord.utils.get(self.__guild.roles, name='M+ Alliance')
                            await member.add_roles(m_alliance)
                    if "Raider Horde" in roles_str:
                        m_alliance = discord.utils.get(self.__guild.roles, name='Raider Horde')
                        await member.remove_roles(m_alliance)
                        if 'M+ Horde' not in roles_str:
                            m_alliance = discord.utils.get(self.__guild.roles, name='M+ Horde')
                            await member.add_roles(m_alliance)
                print('all donee')
            ############################## Nickname $$ #############################
            elif message.channel.name == "private-bot-commands" and message.content.startswith("!rename"):
                reload(name_dict_lib)
                error = ""
                try:
                    new_name = message.content.split(" ")[2].lower()
                    old_name = message.content.split(" ")[1].lower()
                    if "]" in new_name or '[' in new_name:
                        error = "no name"
                except:
                    error = "no name"
                if new_name in name_dict_lib.name_dict:
                    error = "name taken"
                if error == "":
                    if old_name in name_dict_lib.name_dict:
                        change_nick(old_name, new_name)
                    else:
                        append_dict(new_name, old_name)
                    await message.channel.send("Hi {}! I renamed {} as {} in the code. Please don't forget to rename him on discord.".format(message.author.mention, old_name.capitalize(), new_name.capitalize()))
                elif error == 'no name':
                    await message.channel.send("Sorry {}. New name not found..".format(message.author.mention))
                elif error == 'name taken':
                    await message.channel.send("Sorry {}. Name already taken".format(message.author.mention))
                await message.channel.send("!reload")
                reload(name_dict_lib)
            elif message.channel.name == "private-bot-commands" and message.content.startswith("!who"):
                reload(name_dict_lib)
                error = ""
                try:
                    name = message.content[5:].lower()
                except:
                    error = "no name"
                if error == "":
                    to_print = ""
                    for nick, fullname in name_dict_lib.name_dict.items():
                        if nick == name:
                            to_print = fullname
                        if fullname == name:
                            to_print = nick
                    if to_print != "":
                        await message.channel.send("Other name : {}".format(to_print))
                    else:
                        await message.channel.send("No one linked to this name")
            ############################## price list #############################
            elif message.channel.name == "private-bot-commands" and message.content.startswith("!price"):
                if message.content.startswith("!pricepveally"):
                    id = message.content.split("!pricepveally",1)[1]
                    pc = priceSheet()
                    return_dict = pc.price_sheet("pveally", id)
                if message.content.startswith("!pricepvehorde"):
                    id = message.content.split("!pricepvehorde",1)[1]
                    pc = priceSheet()
                    return_dict = pc.price_sheet("pvehorde", id)
                if message.content.startswith("!pricepvp"):
                    id = message.content.split("!pricepvp",1)[1]
                    pc = priceSheet()
                    return_dict = pc.price_sheet("pvp", id)
                if message.content.startswith("!pricelegacy"):
                    id = message.content.split("!pricelegacy",1)[1]
                    pc = priceSheet()
                    return_dict = pc.price_sheet("legacy", id)
                if message.content.startswith("!pricemount"):
                    id = message.content.split("!pricemount",1)[1]
                    pc = priceSheet()
                    return_dict = pc.price_sheet("mount", id)
                if message.content.startswith("!pricehotdeals"):
                    id = message.content.split("!pricehotdeals",1)[1]
                    pc = priceSheet()
                    return_dict = pc.price_sheet("hotdeals", id)
                if len(return_dict) == 0 or return_dict[0] == "error" or return_dict[0] == "break":
                        embed_error = discord.Embed(title="Oops" ,color=0x61b3f2)#7FFF0
                        embed_error.add_field(name="Error", value = "That didn't work. No data were found")
                        embed_error.set_footer(text="Gino's Mercenaries")
                else:
                    price_channel = discord.utils.get(self.__guild.channels, id=return_dict[0], type=discord.ChannelType.text)
                    mercs_channel = discord.utils.get(self.__guild.channels, id= self.__mercs_chan_id, type=discord.ChannelType.text)
                    emo = []
                    try:
                        for emo_str in return_dict[5].split(" "):
                            emo.append(discord.utils.get(self.__guild.emojis, name =f"{emo_str}"))
                    except:
                        pass
                    embed_message = discord.Embed(title=return_dict[2].format(*emo), description=return_dict[3].format(*emo), color=0x9acd32)#7FFF00#9ACD32
                    for field in return_dict[4]:
                        embed_message.add_field(name=field["name"].format(*emo), value=field["value"].format(*emo), inline = True)
                        embed_message.add_field(name="\u200b", value="\u200b", inline = True)
                        if "price" in field:
                            embed_message.add_field(name="Price", value=field["price"].format(*emo), inline = True)
                        else:
                            embed_message.add_field(name="\u200b", value="\u200b", inline = True)
                    print(return_dict)
                    if return_dict[6] != "":
                        try:
                            embed_message.set_image(url=return_dict[6])
                        except:
                            pass
                    embed_message.set_footer(text="Gino's Mercenaries")
                    if return_dict[1] != "":
                        embed_image = discord.Embed(color=0x9acd32)
                        embed_image.set_image(url=return_dict[1])
                    try:
                        await price_channel.send(embed= embed_image)
                    except:
                        pass
                    await price_channel.send(embed=embed_message)
                    if not message.content.startswith("!pricehotdeals"):
                        await mercs_channel.send(embed=embed_message)
                    await message.add_reaction(self.allowed_emo)
            elif message.content.lower().startswith("arena registration:"):
                    await message.add_reaction(self.mail_emo)
                    await message.add_reaction(self.inv_emo)
        except:
                err = traceback.format_exc()
                embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
                embed_error.add_field(name="Error", value = err)
                embed_error.set_footer(text="Gino's Mercenaries")
                day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
                await day_member.create_dm()
                await day_member.dm_channel.send(embed=embed_error)


    ###########################################################################
    #                              On reaction add                            #
    ###########################################################################
    async def on_raw_reaction_add(self, payload):
        try:
            channel = discord.utils.get(self.__guild.channels, id=payload.channel_id, type=discord.ChannelType.text)
            message = await channel.fetch_message(payload.message_id)
            user = discord.utils.get(self.__guild.members, id=payload.user_id)
            emoji = payload.emoji
            # Event accepted
            if emoji == self.mail_emo and user.id != self.__bot_id:
                support = False
                user_role = [o.name for o in user.roles]
                for role in user_role:
                    if role in self.event_leader_role:
                        support = True
                        break
                if support is True:
                    resp = get_list_tag(message.content)
                    list_tag = resp[0]
                    embed_rooster = discord.Embed(title="Event application", description="Thank you for your apply in our arena event, we’ll send you a message when we  are ready to start" ,color=0x61b3f2)#7FFF0
                    alreadyin = False
                    iter_raid = 0
                    for raid in self.__events:
                        if raid[0] == message.id:
                            alreadyin = True
                            break
                        iter_raid += 1
                    if alreadyin is False:
                        iter_raid = len(self.__events)
                        self.__events.append([message.id, []])
                    for tag in list_tag:
                        member = discord.utils.get(self.__guild.members, id=int(tag))
                        if member not in self.__events[iter_raid][1]:
                            self.__events[iter_raid][1].append(member)
                            await member.create_dm()
                            await member.dm_channel.send(embed = embed_rooster)

            # Event finish
            if emoji == self.inv_emo and user.id != self.__bot_id:
                support = False
                user_role = [o.name for o in user.roles]
                for role in user_role:
                    if role in self.event_leader_role:
                        support = True
                        break
                if support is True:
                    rep = get_list_tag(message.content)
                    list_tag = rep[0]
                    inv_message = rep[1]
                    embed_rooster = discord.Embed(title="Event is ready" ,color=0x61b3f2)#7FFF0
                    iter_raid = 0
                    for raid in self.__events:
                        if raid[0] == message.id:
                            self.__events.pop(iter_raid)
                            break
                        iter_raid += 1
                    if inv_message != "":
                        inv = "```css\n" + inv_message + "```Copy paste that, it auto invites!"
                        embed_rooster.add_field(name="\u200b", value="The event in {} will start shortly! Please log on your character and whisper the following char:".format(channel.mention) +inv, inline = False)
                        embed_rooster.add_field(name="\u200b", value="Good luck, have fun! :smile:", inline = False)
                    else:
                        embed_rooster.add_field(name="\u200b", value="The event in {} will start shortly! Please log on your character and whisper the according char.".format(channel.mention), inline = False)
                        embed_rooster.add_field(name="\u200b", value="Good luck, have fun! :smile:", inline = False)

                    for tag in list_tag:
                        embed_rooster.set_footer(text="Gino's Mercenaries")
                        member = discord.utils.get(self.__guild.members, id=int(tag))
                        await member.create_dm()
                        await member.dm_channel.send(embed = embed_rooster)
            
            # giveway
            if len(self.giveaway_list) > 0 and channel.id == self.giveaway_list[0].channel_id and user.id != self.__bot_id:
                for ga in self.giveaway_list:
                    if message.id == ga.message.id:
                        if emoji.name == "🔧":
                            print("aaa")
                            await user.create_dm()
                            await user.dm_channel.send(ga.message.id)
                            await message.remove_reaction(emoji, user)
                        if emoji.name == "🎉":
                            user_role = [o.name for o in user.roles]
                            if user in ga.get_participants_list():
                                embed_message = discord.Embed(title="Already In", description="You are already register in the giveaway!", color=0x32cd32)#7FFF00
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await user.create_dm()
                                await user.dm_channel.send(embed=embed_message)
                                await message.remove_reaction(emoji, user)
                            elif ga.role in user_role:
                                ga.add_participant(user)
                                embed_message = ga.giveaway_embed()
                                await ga.message.edit(embed=embed_message)
                            else:
                                embed_message = discord.Embed(title="Missing role", description="You need to have the {} role to join the giveaway".format(ga.role), color=0x32cd32)#7FFF00
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await user.create_dm()
                                await user.dm_channel.send(embed=embed_message)
                                await message.remove_reaction(emoji, user)
                        if emoji == self.allowed_emo:
                            if user.id == self.__day_id:
                                winners = ga.select_winners()
                                winner_str = ""
                                for winner in winners:
                                    winner_str += "{} ".format(winner.mention)
                                await channel.send("Congratulations, you won {}! :tada:".format(winner_str))
                                self.giveaway_list.remove(ga)
                                await message.clear_reactions()
                            else:
                                await message.remove_reaction(emoji, user)
                        break

            # tickets
            if channel.id == self.__mercs_ticket_id and user.id != self.__bot_id:
                mod_role = discord.utils.get(self.__guild.roles, name='Moderator')
                supp_role = discord.utils.get(self.__guild.roles, name='Support')
                category = channel.category #discord.utils.get(self.__guild.categories, name='🤼Mercenaries Corner')
                pos = len(category.channels)
                print(pos)
                overwrites = {
                    self.__guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    mod_role : discord.PermissionOverwrite(read_messages=True),
                    supp_role : discord.PermissionOverwrite(read_messages=True),
                    user: discord.PermissionOverwrite(read_messages=True)
                }
                chan_name = "ticket-{}".format(self.ticket_id)
                chan_created = await self.__guild.create_text_channel(chan_name, category=category, overwrites=overwrites)
                embed_eng = discord.Embed(title="Hello!", color=0x9acd32)#7FFF00#9ACD32
                embed_eng.add_field(name="How to close this ticket?", value="Simply react to this message with {}.".format(self.allowed_emo), inline = False)
                embed_eng.set_footer(text="Gino's Mercenaries")
                tmp_message = await chan_created.send(embed = embed_eng)
                support_role = discord.utils.get(self.__guild.roles, name='Support')
                await tmp_message.add_reaction(self.allowed_emo)
                await chan_created.send("Hello {}!\nI've created this channel with the {} team. How can we help you?\n**Please always start the conversation in English**.".format(user.mention, support_role.mention))
                self.ticket_id += 1
                await message.remove_reaction(emoji,user)

            # help
            if channel.id == self.__mercs_help_id and user.id != self.__bot_id:
                mod_role = discord.utils.get(self.__guild.roles, name='Support')
                category = channel.category #discord.utils.get(self.__guild.categories, id=834900314057998366)
                overwrites = {
                    self.__guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    mod_role : discord.PermissionOverwrite(read_messages=True),
                    user: discord.PermissionOverwrite(read_messages=True)
                }
                chan_name = "help-{}".format(self.help_id)
                pos = len(category.channels)
                print(pos)
                chan_created = await self.__guild.create_text_channel(chan_name, category=category, overwrites=overwrites)
                embed_eng = discord.Embed(title="Hello!", color=0x9acd32)#7FFF00#9ACD32
                embed_eng.add_field(name="How to close this ticket?", value="Simply react to this message with {}.".format(self.allowed_emo), inline = False)
                embed_eng.set_footer(text="Gino's Mercenaries")
                tmp_message = await chan_created.send(embed = embed_eng)
                await tmp_message.add_reaction(self.allowed_emo)
                support_role = discord.utils.get(self.__guild.roles, name='Support')
                await chan_created.send("Hello {}!\nI've created this channel with the {} team. How can we help you?".format(user.mention, support_role.mention))
                self.help_id += 1
                await message.remove_reaction(emoji,user)


            # bookings
            if channel.id == self.__booking_chan_id and user.id != self.__bot_id:
                trusted_role = discord.utils.get(self.__guild.roles, name='Trusted Advertiser')
                category = channel.category
                overwrites = {
                    self.__guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    trusted_role : discord.PermissionOverwrite(read_messages=True),
                    user: discord.PermissionOverwrite(read_messages=True)
                }
                chan_name = "Booking-{}".format(self.booking_id)
                pos = len(category.channels)
                chan_created = await self.__guild.create_text_channel(chan_name, category=category, overwrites=overwrites)
                if emoji.name == "🇫🇷":
                    trusted_role = discord.utils.get(self.__guild.roles, name='FR')
                    embed_fr = discord.Embed(title="Bienvenue 🇫🇷", color=0x9acd32)#7FFF00#9ACD32
                    embed_fr.add_field(name="Comment clore ce ticket?", value="Appuie simplement sur {}.".format(self.allowed_emo), inline = False)
                    embed_fr.set_footer(text="Gino's Mercenaries")
                    tmp_message = await chan_created.send(embed = embed_fr)
                    await tmp_message.add_reaction(self.allowed_emo)
                    await chan_created.send("Hello {}!\nJ'ai crée ce channel avec nos advertisers {}. Comment peut-on t'aider? Si tu as déjà un advertiser préféré, n'hésite pas à le mentionner!".format(user.mention, trusted_role.mention))
                elif emoji.name == "🇩🇪":
                    trusted_role = discord.utils.get(self.__guild.roles, name='DE')
                    embed_ge = discord.Embed(title="Willkommen 🇩🇪", color=0x9acd32)#7FFF00#9ACD32
                    embed_ge.add_field(name="Wie kannst du das Ticket schließen?", value="Reagiere einfach auf diese Nachricht mit {}.".format(self.allowed_emo), inline = False)
                    embed_ge.set_footer(text="Gino's Mercenaries")
                    tmp_message = await chan_created.send(embed = embed_ge)
                    await tmp_message.add_reaction(self.allowed_emo)
                    await chan_created.send("Hallo {}!\nIch habe dir einen Channel eröffnet mit unseren {} Verkäufern. Wie können wir dir weiterhelfen? Wenn du bereits einen Verkäufer in der Community kennst, kannst du den Namen gern im Channel reinschreiben!".format(user.mention, trusted_role.mention))
                else:
                    trusted_role = discord.utils.get(self.__guild.roles, name='ENG')
                    embed_eng = discord.Embed(title="Hello 🇬🇧", color=0x9acd32)#7FFF00#9ACD32
                    embed_eng.add_field(name="How to close this ticket?", value="Simply react to this message with {}.".format(self.allowed_emo), inline = False)
                    embed_eng.set_footer(text="Gino's Mercenaries")
                    tmp_message = await chan_created.send(embed = embed_eng)
                    await tmp_message.add_reaction(self.allowed_emo)
                    await chan_created.send("Hello {}!\nI've created this channel with our {} advertisers. How can we help you? If you already have a favorite advertiser in the community, please consider mentioning it!".format(user.mention, trusted_role.mention))
                self.booking_id += 1
                await message.remove_reaction(emoji,user)

            # delete help
            if channel.name.startswith("help-") and user.id != self.__bot_id:
                if emoji == self.allowed_emo and len(message.embeds)> 0:
                    mod_role = discord.utils.get(self.__guild.roles, name='Support')
                    overwrites = {
                        self.__guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        mod_role : discord.PermissionOverwrite(read_messages=True),
                    }
                    await channel.edit(overwrites = overwrites)
                    embed_msg = discord.Embed(title="End of conversation", description="{} closed the chat. Please react with {} to delete this channel.".format(user.mention, self.denied_emo) ,color=0x9acd32)#7FFF00#9ACD32
                    embed_msg.set_footer(text="Gino's Mercenaries")
                    tmp_message = await channel.send(embed = embed_msg)
                    await tmp_message.add_reaction(self.denied_emo)
                if emoji == self.denied_emo and len(message.embeds)> 0:
                    await channel.delete()

            # delete ticket
            if channel.name.startswith("ticket") and user.id != self.__bot_id:
                if emoji == self.allowed_emo and len(message.embeds)> 0:
                    mod_role = discord.utils.get(self.__guild.roles, name='Moderator')
                    supp_role = discord.utils.get(self.__guild.roles, name='Support')
                    overwrites = {
                        self.__guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        supp_role : discord.PermissionOverwrite(read_messages=True),
                        mod_role : discord.PermissionOverwrite(read_messages=True),
                    }
                    await channel.edit(overwrites = overwrites)
                    embed_msg = discord.Embed(title="End of conversation", description="{} closed the chat. Please react with {} to delete this channel.".format(user.mention, self.denied_emo) ,color=0x9acd32)#7FFF00#9ACD32
                    embed_msg.set_footer(text="Gino's Mercenaries")
                    tmp_message = await channel.send(embed = embed_msg)
                    await tmp_message.add_reaction(self.denied_emo)
                if emoji == self.denied_emo and len(message.embeds)> 0:
                    await channel.delete()
            
            # delete bookings
            if channel.name.startswith("booking") and user.id != self.__bot_id:
                if emoji == self.allowed_emo and len(message.embeds)> 0:
                    trusted_role = discord.utils.get(self.__guild.roles, name='Trusted Advertiser')
                    overwrites = {
                        self.__guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        trusted_role : discord.PermissionOverwrite(read_messages=True),
                    }
                    await channel.edit(overwrites = overwrites)
                    embed_msg = discord.Embed(title="End of conversation", description="{} closed the chat. Please react with {} to delete this channel.".format(user.mention, self.denied_emo) ,color=0x9acd32)#7FFF00#9ACD32
                    embed_msg.set_footer(text="Gino's Mercenaries")
                    tmp_message = await channel.send(embed = embed_msg)
                    await tmp_message.add_reaction(self.denied_emo)
                if emoji == self.denied_emo and len(message.embeds)> 0:
                    await channel.delete()
            
            # price wrench
            if (channel.id in self.price_dict or channel.id == self.__mercs_chan_id) and user.id != self.__bot_id:
                try:
                    chan_name  = self.price_dict[channel.id]
                except:
                    chan_name  = "mercs"
                user_role = [o.name for o in user.roles]
                if "Moderator" in user_role:
                    if emoji.name == "🔧":
                        if len(message.embeds)> 0:
                            title = message.embeds[0].title
                            pc = priceSheet()
                            return_dict = pc.price_sheet_name(chan_name, title)
                            emo = []
                            try:
                                for emo_str in return_dict[5].split(" "):
                                    emo.append(discord.utils.get(self.__guild.emojis, name =f"{emo_str}"))
                            except:
                                pass
                            embed_message = discord.Embed(title=return_dict[2].format(*emo), description=return_dict[3].format(*emo), color=0x9acd32)#7FFF00#9ACD32
                            for field in return_dict[4]:
                                if "price" in field:
                                    embed_message.add_field(name=field["name"].format(*emo), value=field["value"].format(*emo), inline = True)
                                    embed_message.add_field(name="\u200b", value="\u200b", inline = True)
                                    embed_message.add_field(name="Price", value=field["price"].format(*emo), inline = True)
                                else:
                                    embed_message.add_field(name=field["name"].format(*emo), value=field["value"].format(*emo), inline = True)
                                    embed_message.add_field(name="\u200b", value="\u200b", inline = True)
                                    embed_message.add_field(name="\u200b", value="\u200b", inline = True)
                            print(return_dict)
                            if return_dict[6] != "":
                                embed_message.set_image(url=return_dict[6])

                            embed_message.set_footer(text="Gino's Mercenaries")
                            try:
                                await message.edit(embed=embed_message)
                            except discord.errors.HTTPException:
                                 await user.create_dm()
                                 await user.dm_channel.send("The post you are trying to make is too long! (Discord limit is 1024 characters). Try reducing it or spliting it into two posts! :smile:")
                            await message.remove_reaction(emoji, user)

        except:
                err = traceback.format_exc()
                embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
                embed_error.add_field(name="Error", value = err)
                embed_error.set_footer(text="Gino's Mercenaries")
                day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
                await day_member.create_dm()
                await day_member.dm_channel.send(embed=embed_error)

    def get_embed_updateall(self, downgraded_boosters, sleep=False, current_members = 0, max_members = 0, finish= False):
        embed_message = discord.Embed(title="Updating every boosters.",description="Hi, I will check if all the *All Star* meet the 2.8k requierement.\n This process will take serveral minutes.", color=0x32cd32)#7FFF00
        if finish:
            embed_message.add_field(name="Status",value="All checked! :tada:".format(current_members, max_members))
        elif sleep:
            embed_message.add_field(name="Status",value=":sleeping: for 1 minute. Already checked {}/{} boosters.".format(current_members, max_members))
        else:
            embed_message.add_field(name="Status",value="Working :woman_office_worker:")
        if len(downgraded_boosters) > 0:
            value_string = ""
            for booster in downgraded_boosters:
                value_string += "{} - {}\n".format(booster.mention, booster.display_name)
            embed_message.add_field(name="List of downgraded boosters:",value=value_string)
        embed_message.set_footer(text="Gino's Mercenaries")
        return embed_message

    def get_stricky(self, name):
        for i in range(len(name)):
            current_tag = ""
            stricky = ""
            if (name[i] == '<' and name[i+1] == '@' and name[i+2] == '!'):
                j = 0
                while name[i+3+j] != '>':
                    current_tag += name[i+3+j]
                    j += 1
                    if current_tag != "":
                        stricky = discord.utils.get(self.__guild.members, id=int(current_tag))
                        break
                        i += (j+2)
        if stricky == "":
            name = name.replace(" ","")
            name = onlyName(name)
            p = self.get_all_members()
            stricky = list(filter(lambda m: sameName(m.display_name.lower(), name.lower()), p))[0]
        return stricky
