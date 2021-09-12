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

class MainClient(discord.Client):
    ###########################################################################
    #                                       Init                              #
    ###########################################################################
    def __init__(self, guild_name):
        self.guild_name = guild_name
        self.__list_admin_roles = ["EN - Manager", "Developer"]
        self.__list_bot_roles = ["Bot"]
        self.__list_modo_roles = ["EN - Manager", "Developer", "Moderator", "Recruiting", "Management"]
        self.raid_leader_role = ["Legacy Raids Leader", "Raid Leader Alliance", "Raid Leader Horde"]
        self.__boost_being_fill = []
        self.__boost_being_done = []
        self.__boost_being_collected = []
        self.__raids = []
        self.__bets = []
        self.__dr_bet = []
        self.__last_webhook = []
        self.__day_id = 302188753206771714
        self.testy = False
        if self.testy == False:
            # Gino
            self.__collecting_gold_id = 741953895604944946
            self.__bot_id = 686611501389316108
            self.__ally_mm =628751808512393246
            self.__horde_mm =628751835695677471
            self.__pvp = 676080492998688798
            self.__legacy = 703392478283431936
            self.__apply_adv_chan_list_id = 629129518623227914
            self.__boost_annoucement_list_id = [628751808512393246,628751835695677471,676080492998688798, 676080492998688798, 703392478283431936]
            self.__apply_chan_list_id = [714816319551176794, 628755009663795210, 697614090650255390, 705477154409939054, 682660687905947688]
            self.__bet_chan_list_id = [709019009106051104, 709019069206233199, 709019109257642014]
            self.__strike_chan_id = 654520688870293525
        else:
            # Jmone
            self.__collecting_gold_id = 741569122957262849
            self.__bot_id = 686307367343751317
            self.__ally_mm =691328217721733140
            self.__horde_mm =691771703830773780
            self.__pvp = 691771677390143568
            self.__legacy = 825329060694458368
            self.__boost_annoucement_list_id = [691328217721733140,691771703830773780,691771677390143568, 825329060694458368]
            self.__apply_chan_list_id = [688931455929548812]
            self.__apply_adv_chan_list_id = 2
            self.__bet_chan_list_id = [708975742242914314, 706436097504182292, 708975772072935424]
            self.__strike_chan_id = 654520688870293525

        intents = discord.Intents.all()
        super(MainClient, self).__init__(intents=intents)

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
                # Last Webhook
                elif message.content.lower() == "last_webhook":
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        await message.channel.send("Last Webhook:\n{}".format(self.__last_webhook))
                # List status
                elif message.content.lower() == "list_status":
                    try:
                        user_id = message.author.id
                        if user_id == self.__day_id:
                            await message.channel.send("Here is the boost list : \n1) {}\n2){}\n".format(self.__boost_being_fill, self.__boost_being_done))
                            await message.channel.send("Here is the raid list : \n {}".format(self.__raids))
                    except:
                        err = traceback.format_exc()
                        embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
                        embed_error.add_field(name="Error", value = err)
                        embed_error.set_footer(text="Gino's Mercenaries")
                        day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
                        await day_member.create_dm()
                        await day_member.dm_channel.send(embed=embed_error)

                elif message.content.lower() == "c":
                    try:
                        user_id = message.author.id
                        if user_id == self.__day_id:
                            await message.channel.send("{}\n".format(len(self.__boost_being_done)))
                    except:
                        err = traceback.format_exc()
                        embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
                        embed_error.add_field(name="Error", value = err)
                        embed_error.set_footer(text="Gino's Mercenaries")
                        day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
                        await day_member.create_dm()
                        await day_member.dm_channel.send(embed=embed_error)

                # List status complete
                elif message.content.lower() == "list_status_complete":
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        await message.channel.send("Here is the complete list:\nFill:")
                        for boost in self.__boost_being_fill:
                            await message.channel.send(boost.getStr())
                            await message.channel.send("------------")
                        await message.channel.send("Done:")
                        for boost in self.__boost_being_done:
                            await message.channel.send(boost.getStr())
                            await message.channel.send("------------")
                # Set ip : information role
                elif message.content.lower() == "information role set up":
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        information_role_channel = discord.utils.get(self.__guild.channels, id=689148262837518378, type=discord.ChannelType.text)
                        other_role_chan = discord.utils.get(self.__guild.channels, id=720306861013729351, type=discord.ChannelType.text)
                        mm_roles_channel = discord.utils.get(self.__guild.channels, id=689148468777713708, type=discord.ChannelType.text)
                        embed_message = discord.Embed(title="Roles", color=0x61b3f2)#7FFF00
                        embed_message.add_field(name="M+ roles", value="You currently need 1950 to be a prestige booster (up to +13) and 2150 to be an allstar booster (14 and higher).", inline=False)
                        embed_message.add_field(name="\u200b",value="**If you want to update your roles** after leveling a new alt or gaining some r.io points, you can use !update name-realm in {}. (where name and realm must be replaced with the ones of your character)\nThis command also works to get the roles of your alts by using the name and realm of your alts!\n".format(mm_roles_channel.mention), inline=False)
                        embed_message.add_field(name="Other roles and change name", value="In order to change name or request other roles (For example: torghast runner), please introduce a manual request in {}. ".format(other_role_chan.mention))
                        embed_message.add_field(name="Removes roles", value="In order to remove roles, please introduce a manual request in {}. ".format(other_role_chan.mention))
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await information_role_channel.send(embed=embed_message)
                # Edit boost set up
                elif message.content.lower() == "edit boost set up":
                    user_id = message.author.id
                    if user_id == self.__day_id:
                        information_role_channel = discord.utils.get(self.__guild.channels, name='edit-boost-info', type=discord.ChannelType.text)
                        embed_message = discord.Embed(title="!edit command", color=0x61b3f2)#7FFF00
                        embed_message.add_field(name="Usage:", value="**The boost id can be found by reacting with :wrench: on the boost.**\nEdit the information of the boost. \n**Exmple of utilisation**: removing an armor stack, changing the number or runs, etc..",inline=False)
                        embed_message.add_field(name="Form:", value="**!edit** *boost_id*\n*Field: value*\n...", inline=False)
                        embed_message.add_field(name="List of fields editable:", value="Armor stack: \nBoost note:\nAuto post:\nGold:\nGold realm:\nCharacter to whisp:\nBuyer name: *(PVP boost)*\nBuyer spec: *(PVP boost)*\nKey level:\nKey:\nNumber of run(s):", inline=False)
                        embed_message.add_field(name="Example One: Adding another run to a boost", value="!edit 692145493958066226\nGold: 600000\nNumber of run(s): 2",inline=True)
                        embed_message.add_field(name="Example Two: Removing an armor stack", value="!edit 692145493958066226\nArmor stack: ",inline=True)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await information_role_channel.send(embed=embed_message)
                        embed_message = discord.Embed(title="!addtank/ !addheal/ !adddps1 / ... command", color=0x61b3f2)#7FFF00
                        embed_message.add_field(name="Usage:", value="**The boost id can be found by reacting with :wrench: on the boost.**\nAdd someone to the boost.\n**Exmple of utilisation**: Adding a booster who can't tag because he hasn't the armor stack.",inline=False)
                        embed_message.add_field(name="Form:", value="**!addtank** *boost_id*\n**Booster name**:\n", inline=False)
                        embed_message.add_field(name="Example:", value="!adddps2 692145493958066226\nBooster name: daygrim-hyjal",inline=True)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await information_role_channel.send(embed=embed_message)
                        embed_message = discord.Embed(title="!removetank / !removeheal / !removedps1 / ... command", color=0x61b3f2)#7FFF00
                        embed_message.add_field(name="Usage:", value="**The boost id can be found by reacting with :wrench: on the boost.**\nRemove someone from the boost.\n**Exmple of utilisation**: Removing a booster that has to go before the boost started.",inline=False)
                        embed_message.add_field(name="Form:", value="**!removetank** *boost_id*\n**!removeheal** *boost_id*\n**!removedps1** *boost_id*\n**!removedps2** *boost_id*\n**!removedps3** *boost_id*\n**!removedps4** *boost_id*", inline=False)
                        embed_message.add_field(name="Example:", value="!removetank 692145493958066226",inline=True)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await information_role_channel.send(embed=embed_message)
                        embed_message = discord.Embed(title="!replacetank/ !replaceheal/ !replacedps1 / !replacedps2 command", color=0x61b3f2)#7FFF00
                        embed_message.add_field(name="Usage:", value="**The boost id can be found by reacting with :wrench: on the boost.**\nIn case of a multiple MM+ run, replace a booster that has to go. The boost will be set as **auto post off**.",inline=False)
                        embed_message.add_field(name="Form:", value="**!replacetank** *boost_id*\n**Number of runs already done**:\n**Booster name**:", inline=False)
                        embed_message.add_field(name="Example:", value="!replacetank *boost_id*\nNumber of runs already done: 2\nBooster name: daygrim-hyjal",inline=True)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await information_role_channel.send(embed=embed_message)


            ################################# Form ################################
            elif message.channel.name == "form" and message.author.id != self.__bot_id:
                to_handle = True
                if len(message.embeds)> 0:
                    em = message.embeds[0]
                    for field in em.fields:
                        if field.name =="Type of boost:":
                            if field.value.lower() == "pvp":
                                to_handle = False
                else:
                    to_handle = False
                if to_handle:
                    error = ""
                    em = message.embeds[0]
                    p = self.get_all_members()
                    adv_field = list(filter(lambda m: m.name=="Advertiser:", em.fields))[0]
                    adv_name = onlyName(adv_field.value.replace(" ",""))
                    good_bool = False
                    try:
                        adv = list(filter(lambda m: sameName(m.display_name.lower(), adv_name.lower()), p))[0]
                        good_bool = True
                    except:
                        error += "adv"
                    if good_bool == True:
                        adv_role = [o.name for o in adv.roles]
                        if "On Strike" in adv_role:
                            error = "adv"
                            embed_message = discord.Embed(title="Advertiser on Strike", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value="The advertiser is currently on Strike. Contact Ayyia for more information.", inline=False)
                            embed_message.set_footer(text="Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                    # Utiliser un contains
                    # Si Gino tout seul, mettre un alias
                    if error == "adv":
                        embed_message = discord.Embed(title="Advertiser not found", color=0xdc143c)#7FFF00
                        embed_message.add_field(name="\u200b", value="The advertiser from the Google form ({}) can not be found.".format(adv_field.value), inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.channel.send(embed=embed_message)
                    else:
                        unpost_channel = discord.utils.get(self.__guild.channels, name='boost-unposted', type=discord.ChannelType.text)
                        boost = boostOb(adv, unpost_channel, self.tank_emo, self.heal_emo, self.dps_emo, self.allowed_emo, self.denied_emo, self.coin_emo, self.mercs_emo, self.armor_emo, self.bronze_key_emo, self.silver_key_emo, self.gold_key_emo, self.nb_emo)
                        for field in em.fields:
                            if field.name =="Type of boost:":
                                if field.value == "M+":
                                    boost.type = "mm"
                                elif field.value == "Valor":
                                    boost.type = "mm"
                                    boost.isValor = True
                                elif field.value == "Leveling":
                                    boost.type = "mm"
                                    boost.isLeveling = True
                                elif field.value == "Legacy":
                                    boost.type = "legacy"
                                else:
                                    boost.type = field.value.lower()
                            if field.name == "Faction:":
                                boost.faction = field.value.lower()
                            if field.name == "Boost description:":
                                boost.notes = field.value
                            if field.name == "Gold:":
                                boost.gold = int(field.value)
                            if field.name == "Gold faction:":
                                boost.gold_faction  = field.value
                            if field.name == "Collection Realm:":
                                boost.realm = main_connected_realm(field.value.lower())
                                boost.real_realm = field.value.lower()
                            if field.name == "Character to whisp:":
                                boost.who_to_w = field.value
                            if field.name == "Character to whisper:":
                                boost.who_to_w = field.value
                            if field.name == "Number of booster(s):":
                                boost.nb_boosters = int(field.value)
                            if field.name == "Buyer name:":
                                boost.buyer_name = field.value
                            if field.name == "Buyer spec:":
                                boost.buyer_spec = field.value
                            if field.name == "Key level:":
                                boost.key_level = int(field.value)
                            if field.name == "Number of run(s):":
                                boost.nb_runs = int(field.value)
                            if field.name == "Specific key:":
                                boost.key = field.value
                            if field.name.startswith("Other options?"):
                                if field.value == "No advertiser cut":
                                    boost.no_adv_cut = True
                                elif field.value == "No pings":
                                    boost.no_ping = True
                                elif field.value == "Don't post in balance automatically":
                                    boost.auto_post = False
                                elif field.value == "In house boost":
                                    boost.inhouse = True
                                else:
                                    p = self.get_all_members()
                                    helper_name = onlyName(field.value.lower().replace(" ",""))
                                    try:
                                        boost.helper = list(filter(lambda m: sameName(m.display_name.lower(), helper_name.lower()), p))[0]
                                    except:
                                        error = "helper"
                            if field.name == "Boost note:":
                                boost.notes = field.value
                            if field.name == "Armor Stack:":
                                if field.value != "No":
                                    boost.armor_stack = field.value.lower()
                            if field.name == "Already in Tank:":
                                if field.value != "No":
                                    tank_name = onlyName(field.value.replace(" ",""))
                                    try:
                                        p = self.get_all_members()
                                        tank = list(filter(lambda m: sameName(m.display_name, tank_name), p))[0]
                                        boost.tank_in = tank
                                    except:
                                        error = "Tank"
                            if field.name == "Already in Heal:":
                                if field.value != "No":
                                    heal_name = onlyName(field.value.replace(" ",""))
                                    try:
                                        p = self.get_all_members()
                                        heal = list(filter(lambda m: sameName(m.display_name, heal_name), p))[0]
                                        boost.heal_in = heal
                                    except:
                                        error = "Heal"
                            if field.name == "Already in DPS:":
                                if field.value != "No":
                                    try:
                                        dps_list = field.value.split(" ")
                                        i = 0
                                        for dps in dps_list:
                                            dps = onlyName(dps)
                                            p = self.get_all_members()
                                            dps_member = list(filter(lambda m: sameName(m.display_name.lower(), dps.lower()), p))[0]
                                            boost.dps_in[i] = dps_member
                                            i += 1
                                    except:
                                        error = "DPS"

                        if self.__last_webhook != []:
                            if self.__last_webhook[1] == boost.advertiser.display_name:
                                now = datetime.now()
                                delta_t = (now - self.__last_webhook[0]).total_seconds()
                                if delta_t < 60:
                                    error = "double"
                                    self.__last_webhook = [now, boost.advertiser.display_name]
                        if error == "":
                            now = datetime.now()
                            self.__last_webhook = [now, boost.advertiser.display_name]
                            boost.completeInfo()
                            boost.tags()
                            if boost.type in ["torghast", "mm","tazavesh","island", "leveling"]:
                                if boost.faction == "alliance":
                                    boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.__ally_mm)
                                elif boost.faction == "horde":
                                    boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.__horde_mm)
                            if boost.type == "pvp":
                                boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.__pvp)
                            if boost.type == "legacy":
                                boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.__legacy)
                            roles = adv.roles
                            role_str = [y.name.lower() for y in roles]
                            new_adv = True
                            if "advertiser alliance" in role_str or "advertiser horde" in role_str or "trusted advertiser" in role_str or "gold collector" in role_str:
                                new_adv = False
                            if new_adv:
                                # DM the new adv
                                gold_collecting_chan = discord.utils.get(self.__guild.channels, id=self.__collecting_gold_id)
                                embed_message = discord.Embed(title="Gold Collection", color=0x61b3f2, description="Thank you for your boost!\nAs you are not register as a regular advertiser, a Gold Collector will collect the gold before the boost is posted on discord.\nPlease check {} where you'll be able to see who you have to invite to collect the gold.".format(gold_collecting_chan.mention))#7FFF00
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await adv.create_dm()
                                await adv.dm_channel.send(embed= embed_message)
                                # Post in collection (add message in boost)
                                embed_message = discord.Embed(title="Gold Collection: {} - {}".format(boost.realm.capitalize(), boost.faction.capitalize()), color=0x61b3f2)#7FFF00
                                embed_message.add_field(name="Advertiser", value = "{} - {}".format(boost.advertiser.mention, boost.advertiser.display_name))
                                embed_message.add_field(name="Character to whisp", value = boost.who_to_w, inline=False)
                                if boost.inhouse:
                                    embed_message.add_field(name="Gold", value = "{}k".format(boost.gold * 0.85/1000), inline=False)
                                else:
                                    embed_message.add_field(name="Gold", value = "{}k".format(boost.gold/1000), inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                boost.message_collecting = await gold_collecting_chan.send(embed = embed_message)
                                await boost.message_collecting.add_reaction(self.allowed_emo)
                                await boost.message_collecting.add_reaction(self.denied_emo)
                                gold_collector_role = discord.utils.get(self.__guild.roles, name='Gold Collector')
                                boost.tmp_collecting_msg = await gold_collecting_chan.send("{} Can one of you collect the gold?\nPlease warn the others by writing in this chan that you will take care of it.\nPress {} only when collected please!".format(gold_collector_role.mention, self.allowed_emo))
                                # add boost in list
                                self.__boost_being_collected.append(boost)
                                # add reaction
                                await message.add_reaction("💸")
                            else:
                                em = boost.post()
                                boost.message_annoucement = await boost.annoucement_chan.send(embed=em)
                                role_tag = discord.utils.get(self.__guild.roles, name = boost.role_tag[0])
                                if len(boost.role_tag) == 2:
                                    role_tag_2 = discord.utils.get(self.__guild.roles, name = boost.role_tag[1])
                                    if boost.no_ping == False:
                                        boost.tag_message = await boost.message_annoucement.channel.send("{} {} Let's go! Boost will open in 5s.".format(role_tag.mention,role_tag_2.mention))
                                else:
                                    if boost.no_ping == False:
                                        boost.tag_message = await boost.message_annoucement.channel.send("{} Let's go! Boost will open in 5s.".format(role_tag.mention))
                                await asyncio.sleep(5)
                                self.__boost_being_fill.append(boost)
                                if boost.type in ["mm", "tazavesh"]:
                                    await boost.message_annoucement.add_reaction(self.tank_emo)
                                    await boost.message_annoucement.add_reaction(self.heal_emo)
                                await boost.message_annoucement.add_reaction(self.dps_emo)
                                await boost.message_annoucement.add_reaction(self.allowed_emo)
                                await boost.message_annoucement.add_reaction(self.denied_emo)
                                await boost.message_annoucement.add_reaction("🔧")
                                if boost.no_ping == False:
                                    try:
                                        if len(boost.role_tag) == 2:
                                            role_tag_2 = discord.utils.get(self.__guild.roles, name = boost.role_tag[1])
                                            await boost.tag_message.edit(content="{} {} Let's go!".format(role_tag.mention,role_tag_2.mention))
                                        else:
                                            await boost.tag_message.edit(content="{} Let's go!".format(role_tag.mention))
                                    except:
                                        pass
                                await message.add_reaction(self.allowed_emo)
                        elif error == "double":
                            embed_message = discord.Embed(title="Double post detected.", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value="Google form seems to have sent the answer twice. Second will be ingore.\n If it was two different boosts, you posted them with less then 30 secs, impressive! In that case, simply repost the second one.", inline=False)
                            embed_message.set_footer(text="Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        else:
                            embed_message = discord.Embed(title="Booster not found", color=0xdc143c)#7FFF00
                            if error == "Tank":
                                strstr = tank_name
                            elif error == "Heal":
                                strstr = heal_name
                            elif error == 'helper':
                                strstr = "Helper advertiser in Other option."
                            else:
                                print(error)
                                strstr = "DPS"
                            embed_message.add_field(name="\u200b", value="One of the already in booster you entered is unknown : {}.".format(strstr), inline=False)
                            embed_message.set_footer(text="Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
            ############################## reload #############################
            elif message.channel.name == "private-bot-commands" and message.content.startswith("!rename"):
                reload_dict()
                await message.add_reaction(self.allowed_emo)

            ############################## Edit boost #############################
            elif message.channel.name == "edit-boost" and message.content.startswith("!"):
                tmp1 = message.content.split(" ", 1)
                if len(tmp1) < 2:
                    edit_boost_chan = discord.utils.get(self.__guild.channels, name='edit-boost-info', type=discord.ChannelType.text)
                    embed_message = discord.Embed(title="Incorrect form", color=0xdc143c)#7FFF00
                    embed_message.add_field(name="\u200b", value = "The command is not valid. Please refer to {} to edit boost.".format(edit_boost_chan.mention), inline=False)
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                boost_id = tmp1[1].split("\n",1)[0]
                if not RepresentsInt(boost_id):
                    form_channel = discord.utils.get(self.__guild.channels, name='post-boost-form', type=discord.ChannelType.text)
                    embed_message = discord.Embed(title="Incorrect boost id", color=0xdc143c)#7FFF00
                    embed_message.add_field(name="\u200b", value = "The boost id enter does not correspond to a valid number.\n ", inline=False)
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                else:
                    boost_id= int(boost_id)
                    boost = ""
                    boost_type = "none"
                    for iter_boost in self.__boost_being_fill:
                        if iter_boost != "" and iter_boost.message_annoucement.id == boost_id:
                            boost_type = "fill"
                            boost = iter_boost

                    for iter_boost in self.__boost_being_done:
                        if iter_boost != "" and iter_boost.message_annoucement.id == boost_id:
                            boost_type = "done"
                            boost = iter_boost

                    if boost == "":
                        form_channel = discord.utils.get(self.__guild.channels, name='post-boost-form', type=discord.ChannelType.text)
                        embed_message = discord.Embed(title="Incorrect boost id", color=0xdc143c)#7FFF00
                        embed_message.add_field(name="\u200b", value = "The boost id enter does not correspond to any boost currently.", inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.channel.send(embed=embed_message)
                    else:
                        str_message = message.content.lower()
                        #data = [line.strip().split(':') for line in str.split('\n') if line.strip()]
                        #data = [x for x in data if not len(x)<2]
                        if message.content.startswith("!add"):
                            new_booster = False
                            booster_id_field = False
                            good_id = False
                            nb_dps_good = False
                            data = [line.strip().split(':') for line in str_message.split('\n') if line.strip()]
                            data = [x for x in data if not len(x)<2]
                            for info in data:
                                if info[0] == "booster name":
                                    info[1] = info[1].replace(" ","")
                                    booster_id_field = True
                                    p = self.get_all_members()
                                    booster_l = list(filter(lambda m: sameName(m.display_name.lower(), info[1].lower()), p))
                                    if len(booster_l) != 0:
                                        booster = booster_l[0]
                                        good_id = True
                            if booster_id_field is False:
                                embed_message = discord.Embed(title="Missing booster name field", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "Couldn't find the booster's name field in the edit message.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif good_id is False:
                                embed_message = discord.Embed(title="Couldn't find booster", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The booster's name entered doesn't not correspond to anyone in the Gino server.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            else:
                                if message.content.startswith("!addtank"):
                                    if boost.tank_in == "":
                                        boost.booster_place -= 1
                                    boost.tank_in = booster
                                    nb_dps_good = True
                                if message.content.startswith("!addheal"):
                                    if boost.heal_in == "":
                                        boost.booster_place -= 1
                                    boost.heal_in = booster
                                    nb_dps_good = True
                                if message.content.startswith("!adddps1"):
                                    if boost.dps_in[0] == "":
                                        boost.booster_place -= 1
                                    boost.dps_in[0] = booster
                                    nb_dps_good = True
                                if message.content.startswith("!adddps2"):
                                    if boost.nb_dps < 2:
                                        nb_dps_good = False
                                        embed_message = discord.Embed(title="Only one dps in boost", color=0xdc143c)#7FFF00
                                        embed_message.add_field(name="\u200b", value = "You tried to add a second DPS on a boost that only contains one booster.", inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                    else:
                                        nb_dps_good = True
                                        if boost.dps_in[1] == "":
                                            boost.booster_place -= 1
                                        boost.dps_in[1] = booster
                                if message.content.startswith("!adddps3"):
                                    if boost.nb_dps < 3:
                                        nb_dps_good = False
                                        embed_message = discord.Embed(title="Only two dps in boost", color=0xdc143c)#7FFF00
                                        embed_message.add_field(name="\u200b", value = "You tried to add a 3rd DPS on a boost that only contains two boosters.", inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                    else:
                                        nb_dps_good = True
                                        if boost.dps_in[2] == "":
                                            boost.booster_place -= 1
                                        boost.dps_in[2] = booster
                                if message.content.startswith("!adddps4"):
                                    if boost.nb_dps < 4:
                                        nb_dps_good = False
                                        embed_message = discord.Embed(title="Only 3 dps in boost", color=0xdc143c)#7FFF00
                                        embed_message.add_field(name="\u200b", value = "You tried to add a 4th DPS on a boost that only contains three boosters.", inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                    else:
                                        nb_dps_good = True
                                        if boost.dps_in[3] == "":
                                            boost.booster_place -= 1
                                        boost.dps_in[3] = booster
                                else:
                                    embed_message = discord.Embed(title="Command not found", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The command you entered is unknown.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                if nb_dps_good:
                                    em = boost.post()
                                    await boost.message_annoucement.edit(embed = em)
                                    embed_message = discord.Embed(title="Boost edited", color=0x32cd32)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The boost was succesfully modified.")
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                else:
                                    await message.channel.send(embed=embed_message)
                        if message.content.startswith("!replace"):
                            if boost.type != "mm":
                                embed_message = discord.Embed(title="Boost must be M+", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The replace command can only be used for the M+ boost.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif boost_type != "done":
                                embed_message = discord.Embed(title="Boost must be started", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The replace command can only be used for boost already started.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            else:
                                nb_runs_field = False
                                nb_runs_field_nb = False
                                booster_id_field = False
                                good_id = False

                                data = [line.strip().split(':') for line in str_message.split('\n') if line.strip()]
                                data = [x for x in data if not len(x)<2]
                                for info in data:
                                    if info[0] == "number of runs already done":
                                        nb_runs_field = True
                                        info[1] = info[1].replace(" ","")
                                        if RepresentsInt(info[1]):
                                            nb_runs_done = int(info[1])
                                            nb_runs_field_nb = True
                                    if info[0] == "booster name":
                                        info[1] = info[1].replace(" ","")
                                        booster_id_field = True
                                        p = self.get_all_members()
                                        booster_l = list(filter(lambda m: sameName(m.display_name.lower(), info[1].lower()), p))
                                        if len(booster_l) != 0:
                                            booster = booster_l[0]
                                            good_id = True
                                if nb_runs_field is False:
                                    embed_message = discord.Embed(title="Missing booster number of runs already done field", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "Couldn't find the number of runs done field in the edit message.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                elif nb_runs_field_nb is False:
                                    embed_message = discord.Embed(title="Number of runs", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The number of runs must be an integer", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                elif nb_runs_done >= boost.nb_runs:
                                    embed_message = discord.Embed(title="Incorrect number of runs", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The number of runs must be inferior of the total number of runs of the boost.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                elif booster_id_field is False:
                                    embed_message = discord.Embed(title="Missing booster name field", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "Couldn't find the booster name field in the edit message.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                elif good_id is False:
                                    embed_message = discord.Embed(title="Couldn't find booster", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The booster's name entered doesn't not correspond to anyone in the Gino server.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                else:
                                    if message.content.startswith("!replacetank"):
                                        role = "tank"
                                    elif message.content.startswith("!replaceheal"):
                                        role = "heal"
                                    elif message.content.startswith("!replacedps"):
                                        role = "dps"
                                    boost.previous_booster.append([role, booster, nb_runs_done])
                                    em = boost.post(pb = True)
                                    await boost.message_annoucement.edit(embed=em)
                                    boost.auto_post = False
                                    embed_message = discord.Embed(title="Boost edited", color=0x32cd32)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The boost was succesfully modified. Auto-post has been set as false.")
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                        if message.content.startswith("!edit"):
                            ack = fillBoost(boost, message.content.lower())
                            if ack == "not gold":
                                embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The gold should be a number.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif ack == "not nb booster":
                                embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The number of boosters should be a number.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif ack == "not nb run":
                                embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The number of runs should be a number.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif ack == "not booster":
                                embed_message = discord.Embed(title="Wrong discord name", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The booster's discord name you entered does not correspond to anyone on Gino.\n", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif ack == "not nb key":
                                embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The key level should be a number.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif ack == "not armor stack":
                                embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The armor stack should be one of the following: Plate, Mail, Leather, Cloth.\nIf no armor stack are necessary, please just let the field empty.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif ack == "not faction":
                                embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The faction should be one of the following: horde, alliance.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            else:
                                boost.completeInfo()
                                em = boost.post()
                                boost.tags()
                                await boost.message_annoucement.edit(embed = em)
                                embed_message = discord.Embed(title="Boost edited", color=0x32cd32)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The boost was succesfully modified.")
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                        if message.content.startswith("!remove"):
                            removed_booster = False
                            if message.content.startswith("!removetank"):
                                if boost.tank_in == "":
                                    embed_message = discord.Embed(title="No tank in boost", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "There is currently no tank in the boost.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                else:
                                    boost.tank_in = ""
                                    removed_booster = True
                            if message.content.startswith("!removeheal"):
                                if boost.heal_in == "":
                                    embed_message = discord.Embed(title="No heal in boost", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "There is currently no heal in the boost.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                else:
                                    boost.heal_in = ""
                                    removed_booster = True
                            if message.content.startswith("!removedps1"):
                                if boost.dps_in[0] == "":
                                    embed_message = discord.Embed(title="No DPS in boost", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The first dps slot of the boost is not filled.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                else:
                                    boost.dps_in[0] = ""
                                    removed_booster = True
                            if message.content.startswith("!removedps2"):
                                if boost.dps_in[1] == "":
                                    embed_message = discord.Embed(title="No DPS in boost", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The second dps slot of the boost is not filled.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                else:
                                    boost.dps_in[1] = ""
                                    removed_booster = True
                            if message.content.startswith("!removedps3"):
                                if boost.dps_in[2] == "":
                                    embed_message = discord.Embed(title="No DPS in boost", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The 3rd dps slot of the boost is not filled.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                else:
                                    boost.dps_in[2] = ""
                                    removed_booster = True
                            if message.content.startswith("!removedps4"):
                                if boost.dps_in[3] == "":
                                    embed_message = discord.Embed(title="No DPS in boost", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The 3rd dps slot of the boost is not filled.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await message.channel.send(embed=embed_message)
                                else:
                                    boost.dps_in[3] = ""
                                    removed_booster = True
                            if removed_booster:
                                boost.booster_place += 1
                                em = boost.post()
                                await boost.message_annoucement.edit(embed = em)
                                embed_message = discord.Embed(title="Boost edited", color=0x32cd32)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The boost was succesfully modified.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                                if boost_type == "done":
                                    await boost.message_annoucement.clear_reactions()
                                    role_tag = discord.utils.get(self.__guild.roles, name = boost.role_tag[0])
                                    if len(boost.role_tag) == 2:
                                        role_tag_2 = discord.utils.get(self.__guild.roles, name = boost.role_tag[1])
                                        boost.tag_message = await boost.message_annoucement.channel.send("{} {} Let's go!".format(role_tag.mention,role_tag_2.mention))
                                    else:
                                        boost.tag_message = await boost.message_annoucement.channel.send("{} Let's go!".format(role_tag.mention))
                                    if boost.type in ["mm", "tazavesh"]:
                                        await boost.message_annoucement.add_reaction(self.tank_emo)
                                        await boost.message_annoucement.add_reaction(self.heal_emo)
                                    await boost.message_annoucement.add_reaction(self.dps_emo)
                                    await boost.message_annoucement.add_reaction(self.allowed_emo)
                                    await boost.message_annoucement.add_reaction(self.denied_emo)
                                    await boost.message_annoucement.add_reaction("🔧")

                                    for i in range(len(self.__boost_being_done)):
                                        if self.__boost_being_done[i] != "" and self.__boost_being_done[i].message_annoucement.id == boost_id:
                                            self.__boost_being_done.pop(i)
                                            break
                                    self.__boost_being_fill.append(boost)
            ############################## RAIDS ##################################
            if message.content.lower().startswith("here's the roster"):
                await message.add_reaction(self.mail_emo)
                await message.add_reaction(self.inv_emo)
                await message.add_reaction(self.allowed_emo)
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
            if emoji.is_unicode_emoji():
                emoji = str(emoji)
            try:
                if len(self.__boost_being_collected) > 100:
                    self.__boost_being_collected.pop(0)
                if len(self.__boost_being_fill)>100:
                    self.__boost_being_fill.pop(0)
                if len(self.__boost_being_done)>100:
                    self.__boost_being_done.pop(0)
            except:
                pass
            if user.id != self.__bot_id:
                # Boost collection
                if message.channel.id == self.__collecting_gold_id:
                    for boost in self.__boost_being_collected:
                        if boost.message_collecting.id == message.id:
                            user_role = [o.name.lower() for o in user.roles]
                            if emoji == self.allowed_emo and "gold collector" in user_role:
                                embed_message = discord.Embed(title="Gold Collection: {} - {}".format(boost.realm.capitalize(), boost.gold_faction.capitalize()), color=0x61b3f2)#7FFF00
                                embed_message.add_field(name="Advertiser", value = "{} - {}".format(boost.advertiser.mention, boost.advertiser.display_name), inline=True)
                                embed_message.add_field(name="Character to whisp", value = boost.who_to_w, inline=False)
                                embed_message.add_field(name="Gold", value = "{}k".format(boost.gold/1000), inline=False)
                                embed_message.add_field(name="Collected by", value = "{} - {}".format(user.mention, user.display_name), inline=True)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                boost.gold_collector = user


                                await boost.message_collecting.edit(embed = embed_message)
                                try:
                                    await boost.tmp_collecting_msg.delete()
                                except:
                                    pass
                                await message.channel.send("Thank you for collecting the gold {}! :heart:".format(user.mention))
                                await boost.message_collecting.clear_reactions()
                                self.__boost_being_collected.remove(boost)

                                em = boost.post()
                                boost.message_annoucement = await boost.annoucement_chan.send(embed=em)
                                gc_em = discord.Embed(title="Thanks for collecting the gold!", color=0x61b3f2)#7FFF00
                                if boost.type == "mm":
                                    gc_em.add_field(name="Mail message", value = "Please put the **discord name of the advertiser you're helping as mail title** and copy/paste the following message for the body:```+{} - {}```".format(boost.key_level, boost.message_annoucement.id), inline=False)
                                else:
                                    gc_em.add_field(name="Mail message", value = "Please put the **discord name of the advertiser you're helping as mail title** and copy/paste the following message for the body:```{} - {}```".format(boost.type, boost.message_annoucement.id), inline=False)
                                gc_em.add_field(name="Advertiser's name", value = "{}".format(boost.advertiser.display_name), inline=False)
                                gc_em.add_field(name="Collection realm", value = "{}".format(boost.real_realm.capitalize()), inline=True)
                                if boost.gold_faction.lower() == "alliance":
                                    gc_em.add_field(name="Who to mail", value = "MercsAlly-{}".format(main_connected_realm(boost.realm).capitalize()), inline=True)
                                else:
                                    gc_em.add_field(name="Who to mail", value = "MercsHorde-{}".format(main_connected_realm(boost.realm).capitalize()), inline=True)
                                if boost.inhouse:
                                    gc_em.add_field(name="Gold to send", value = "{:,}".format(boost.gold * 0.85))
                                else:
                                    gc_em.add_field(name="Gold to send", value = "{:,}".format(boost.gold))
                                gc_em.set_footer(text="Gino's Mercenaries")
                                await user.create_dm()
                                await user.dm_channel.send(embed=gc_em)
                                role_tag = discord.utils.get(self.__guild.roles, name = boost.role_tag[0])
                                if boost.no_ping == False:
                                    if len(boost.role_tag) == 2:
                                        role_tag_2 = discord.utils.get(self.__guild.roles, name = boost.role_tag[1])
                                        boost.tag_message = await boost.message_annoucement.channel.send("{} {} Let's go! Boost will open in 5s.".format(role_tag.mention,role_tag_2.mention))
                                    else:
                                        boost.tag_message = await boost.message_annoucement.channel.send("{} Let's go! Boost will open in 5s.".format(role_tag.mention))
                                await asyncio.sleep(5)
                                self.__boost_being_fill.append(boost)
                                if boost.type in ["mm", "tazavesh"]:
                                    await boost.message_annoucement.add_reaction(self.tank_emo)
                                    await boost.message_annoucement.add_reaction(self.heal_emo)
                                await boost.message_annoucement.add_reaction(self.dps_emo)
                                await boost.message_annoucement.add_reaction(self.allowed_emo)
                                await boost.message_annoucement.add_reaction(self.denied_emo)
                                await boost.message_annoucement.add_reaction("🔧")
                                if boost.no_ping == False:
                                    try:
                                        if len(boost.role_tag) == 2:
                                            role_tag_2 = discord.utils.get(self.__guild.roles, name = boost.role_tag[1])
                                            await boost.tag_message.edit(content="{} {} Let's go!".format(role_tag.mention,role_tag_2.mention))
                                        else:
                                            await boost.tag_message.edit(content="{} Let's go!".format(role_tag.mention))
                                    except:
                                        pass
                            if emoji == self.denied_emo and user == boost.advertiser:
                                embed_message = discord.Embed(title="Boost cancel", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The boost was canceled by the advertiser.", inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await boost.message_collecting.edit(embed=embed_message)
                                await boost.message_collecting.clear_reactions()
                                self.__boost_being_collected.remove(boost)
                                try:
                                    await boost.tmp_collecting_msg.delete()
                                except:
                                    pass
                            else:
                                await message.remove_reaction(emoji, user)
                            break
                # Boost annoucement
                if message.channel.id in self.__boost_annoucement_list_id:
                    boost_type = "done"
                    #l = 0
                    for boost in self.__boost_being_fill:
                        if boost.message_annoucement.id == message.id:
                            boost_type = "fill"
                            user_role = [o.name for o in user.roles]
                            by_pass = False
                            if "Manager" in user_role or "Moderator" in user_role or "Developer" in user_role:
                                by_pass = True
                            if emoji == self.tank_emo:
                                await add_booster(user, "tank", boost, user_role, by_pass, message, emoji)
                            if emoji == self.heal_emo:
                                await add_booster(user, "heal", boost, user_role, by_pass, message, emoji)
                            if emoji == self.dps_emo:
                                await add_booster(user, "dps", boost, user_role, by_pass, message, emoji)
                            if emoji == self.denied_emo:
                                if boost.advertiser.id == user.id or user.id == self.__day_id or (boost.helper != "" and boost.helper.id == user.id):
                                    embed_message = discord.Embed(title="Boost cancel", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "The boost was canceled.", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await boost.message_annoucement.edit(embed=embed_message)
                                    await boost.message_annoucement.clear_reactions()
                                    try:
                                        await boost.tag_message.delete()
                                    except:
                                        pass
                                    #self.__boost_being_fill.pop(l)
                                    self.__boost_being_fill.remove(boost)
                                else:
                                    await message.remove_reaction(emoji, user)
                            if emoji == "🔧":
                                if boost.advertiser.id == user.id or user.id == self.__day_id or by_pass or (boost.helper != "" and boost.helper.id == user.id):
                                    edit_boost_chan = discord.utils.get(self.__guild.channels, name='edit-boost', type=discord.ChannelType.text)
                                    information_role_channel = discord.utils.get(self.__guild.channels, name='edit-boost-info', type=discord.ChannelType.text)
                                    embed_message = discord.Embed(title="Boost id", color=0x61b3f2)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "Here is the boost id : {}\nTo edit the boost, please go to {}. For more information, you can check {}".format(boost.message_annoucement.id, edit_boost_chan.mention,information_role_channel.mention), inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await user.create_dm()
                                    await user.dm_channel.send(embed=embed_message)
                                    await message.remove_reaction(emoji, user)
                                else:
                                    await message.remove_reaction(emoji, user)
                            if emoji == self.allowed_emo:
                                if boost.advertiser.id == user.id or user.id == self.__day_id or (boost.helper != "" and boost.helper.id == user.id):
                                    if boost.booster_place <= 0 or (boost.tank_in != "" and boost.heal_in != "" and boost.dps_in[0] != "" and boost.dps_in[1] != ""):
                                        await boost.message_annoucement.clear_reactions()
                                        await boost.message_annoucement.add_reaction(self.allowed_emo)
                                        await boost.message_annoucement.add_reaction(self.denied_emo)
                                        await boost.message_annoucement.add_reaction("🔧")
                                        try:
                                            await boost.tag_message.delete()
                                        except:
                                            pass
                                        #self.__boost_being_fill.pop(l)
                                        self.__boost_being_fill.remove(boost)
                                        self.__boost_being_done.append(boost)
                                        em_adv = discord.Embed(title="Boost ready!", color=0x32cd32)
                                        if boost.type == "legacy":
                                            em_adv.add_field(name="\u200b", value = "Your boost is ready to go!\nPlease react with {} (if the boost was well done) or {} to close the boost.".format(boost.who_to_w, self.allowed_emo, self.denied_emo), inline=False)
                                        else:
                                            em_adv.add_field(name="\u200b", value = "Your boost is ready to go! The boosters will whisper ```{}```\nPlease react with {} (if the boost was well done) or {} to close the boost.".format(boost.who_to_w, self.allowed_emo, self.denied_emo), inline=False)
                                        em_adv.set_footer(text="Gino's Mercenaries")
                                        await boost.advertiser.create_dm()
                                        await boost.advertiser.dm_channel.send(embed=em_adv)
                                        discord_room = 0
                                        name = "Boost #"
                                        for h in range(1,10):
                                            current_name = name + str(h)
                                            current_chan = discord.utils.get(self.__guild.channels, name=current_name, type=discord.ChannelType.voice)
                                            if len(current_chan.members) == 0:
                                                discord_room = str(h)
                                                break
                                        invite = await current_chan.create_invite(max_age=600)
                                        embed_message = discord.Embed(title="Boost ready!", color=0x32cd32)#7FFF00
                                        if boost.type == "legacy":
                                            embed_message.add_field(name="\u200b", value = "Your legacy boost is ready. Please contact the advertiser for more information about the buyer. Have fun! :smile:", inline=False)
                                        else:
                                            embed_message.add_field(name="\u200b", value = "The boost in which you were tagged is ready! Please whisper the following character:\n ```/w {} inv```\nPlease also join discord room: [Boost #{}]({}).\nGood luck, have fun! :smile:".format(boost.who_to_w, discord_room, str(invite)), inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                        if boost.tank_in != "":
                                            await boost.tank_in.create_dm()
                                            await boost.tank_in.dm_channel.send(embed=embed_message)
                                        if boost.heal_in != "":
                                            await boost.heal_in.create_dm()
                                            await boost.heal_in.dm_channel.send(embed=embed_message)
                                        for x in range(boost.nb_dps):
                                            if boost.dps_in[x] != "":
                                                await boost.dps_in[x].create_dm()
                                                await boost.dps_in[x].dm_channel.send(embed=embed_message)
                                    else:
                                        await message.remove_reaction(emoji, user)

                                else:
                                    await message.remove_reaction(emoji, user)
                        #l += 1
                    if boost_type == "done":
                        w = 0
                        user_role = [o.name for o in user.roles]
                        by_pass = False
                        if "Raid Manager" in user_role or "Moderator" in user_role or "Developer" in user_role:
                            by_pass = True
                        for boost in self.__boost_being_done:
                            if message.id == boost.message_annoucement.id:
                                if emoji == "🔧":
                                    if boost.advertiser.id == user.id or user.id == self.__day_id or by_pass or (boost.helper != "" and boost.helper.id == user.id):
                                        edit_boost_chan = discord.utils.get(self.__guild.channels, name='edit-boost', type=discord.ChannelType.text)
                                        information_role_channel = discord.utils.get(self.__guild.channels, name='edit-boost-info', type=discord.ChannelType.text)
                                        embed_message = discord.Embed(title="Boost id", color=0x61b3f2)#7FFF00
                                        embed_message.add_field(name="\u200b", value = "Here is the boost id : {}\nTo edit the boost, please go to {}. For more information, you can check {}".format(boost.message_annoucement.id, edit_boost_chan.mention,information_role_channel.mention), inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                        await user.create_dm()
                                        await user.dm_channel.send(embed=embed_message)
                                        await message.remove_reaction(emoji, user)
                                    else:
                                        await message.remove_reaction(emoji, user)
                                if emoji == self.allowed_emo:
                                    if boost.advertiser.id == user.id or user.id == self.__day_id or (boost.helper != "" and boost.helper.id == user.id):
                                        await boost.message_annoucement.clear_reactions()
                                        self.__boost_being_done.pop(w)
                                        # POST BOOST
                                        sr = sheetReader()
                                        ally_bool = True
                                        if boost.faction == "horde":
                                            ally_bool = False
                                        if boost.advertiser != "":
                                            t_name = boost.advertiser.display_name
                                            if not check_name(t_name):
                                                boost.auto_post = False
                                        if boost.tank_in != "":
                                            t_name = boost.tank_in.display_name
                                            if not check_name(t_name):
                                                boost.auto_post = False
                                        if boost.heal_in != "":
                                            t_name = boost.heal_in.display_name
                                            if not check_name(t_name):
                                                boost.auto_post = False
                                        if boost.dps_in[0] != "":
                                            t_name = boost.dps_in[0].display_name
                                            if not check_name(t_name):
                                                boost.auto_post = False
                                        if boost.dps_in[1] != "":
                                            t_name = boost.dps_in[1].display_name
                                            if not check_name(t_name):
                                                boost.auto_post = False
                                        if boost.dps_in[2] != "":
                                            t_name = boost.dps_in[2].display_name
                                            if not check_name(t_name):
                                                boost.auto_post = False
                                        if boost.dps_in[3] != "":
                                            t_name = boost.dps_in[3].display_name
                                            if not check_name(t_name):
                                                boost.auto_post = False
                                        if boost.auto_post:
                                            player_index = 0
                                            if boost.type == "pvp" or boost.type == "torghast":
                                                player_index = boost.nb_boosters
                                            sr.post_boost(boost)
                                            name =  boost.advertiser.display_name
                                            user_name_serv = parseName(name)
                                            gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                            embed_message_adv = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                            embed_message_adv.add_field(name="Thank you!", value = "The boost has been added to the balance!\nThank you for advertising with us!", inline=False)
                                            if boost.type == "mm":
                                                embed_message_adv.add_field(name="Mail message", value = "Please put your **discord name as mail title** and copy/paste the following message for the body:```+{} - {}```If you are a not a regular advertiser, ignore this: the gold collector will mail the gold for you!".format(boost.key_level, boost.message_annoucement.id), inline=False)
                                            else:
                                                embed_message_adv.add_field(name="Mail message", value = "Please put your **discord name as mail title** and copy/paste the following message for the body:```{} - {}```If you are a not a regular advertiser, ignore this: the gold collector will mail the gold for you!".format(boost.type, boost.message_annoucement.id), inline=False)
                                            if "-" not in boost.realm and boost.realm.upper() != "GINOS":
                                                embed_message_adv.add_field(name="Collection realm", value = "{}".format(boost.real_realm.capitalize()), inline=True)
                                                if boost.gold_faction.lower() == "alliance":
                                                    embed_message_adv.add_field(name="Who to mail", value = "MercsAlly-{}".format(main_connected_realm(boost.realm).capitalize()), inline=True)
                                                else:
                                                    embed_message_adv.add_field(name="Who to mail", value = "MercsHorde-{}".format(main_connected_realm(boost.realm).capitalize()), inline=True)
                                                if boost.inhouse:
                                                    embed_message_adv.add_field(name="Gold to send", value = "{:,}".format(boost.gold * 0.85))
                                                else:
                                                    embed_message_adv.add_field(name="Gold to send", value = "{:,}".format(boost.gold))
                                            if gold == "Nbalance":
                                                ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                            else:
                                                embed_message_adv.add_field(name="Your balance", value = "You now have {} gold!".format(gold), inline=True)
                                                if boost.no_adv_cut:
                                                    embed_message_adv.add_field(name="Your cut", value = "Your cut was 0. :moneybag:".format(int(boost.gold*0.85*0.03)), inline=True)
                                                elif boost.inhouse:
                                                    embed_message_adv.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.03)), inline=True)
                                                else:
                                                    if boost.gold_collector == "":
                                                        if boost.helper == "":
                                                            if boost.type != "leveling" and boost.type != "pvp" and boost.type != "legacy":
                                                                embed_message_adv.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
                                                            elif boost.type == "legacy":
                                                                pass
                                                            else:
                                                                embed_message_adv.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.15)), inline=True)
                                                        else:
                                                            embed_message_adv.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.15)), inline=True)
                                                    else:
                                                        embed_message_adv.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.15)), inline=True)
                                            embed_message_adv.set_footer(text="Gino's Mercenaries")
                                        else:
                                            em = boost.end_post()
                                            await boost.unpost_chan.send(embed=em)
                                            embed_message_adv = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                            embed_message_adv.add_field(name="Thank you!", value = "The boost has been posted in {}, waiting to be added to the balance.\nThank you for advertising with us!".format(boost.unpost_chan.mention), inline=False)
                                            embed_message_adv.set_footer(text="Gino's Mercenaries")
                                        await boost.advertiser.create_dm()
                                        await boost.advertiser.dm_channel.send(embed = embed_message_adv)
                                        check_channel = discord.utils.get(self.__guild.channels, name='check-balance', type=discord.ChannelType.text)
                                        balance_channel = discord.utils.get(self.__guild.channels, name='balance-sheets', type=discord.ChannelType.text)
                                        if boost.tank_in != "":
                                            if boost.auto_post:
                                                name = boost.tank_in.display_name
                                                user_name_serv = parseName(name)
                                                gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {} and added to the balance!\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    embed_message.add_field(name="Your balance", value = "You now have {} gold!".format(gold), inline=True)
                                                    if boost.inhouse:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175)), inline=True)
                                                    else:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            else:
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {}. It will be added to the balance shortly.\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                embed_message.set_footer(text="Gino's Mercenaries")

                                            await boost.tank_in.create_dm()
                                            await boost.tank_in.dm_channel.send(embed = embed_message)
                                        if boost.heal_in != "":
                                            if boost.auto_post:
                                                name = boost.heal_in.display_name
                                                user_name_serv = parseName(name)
                                                gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {} and added to the balance!\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    embed_message.add_field(name="Your balance", value = "You now have {} gold!".format(gold), inline=True)
                                                    if boost.inhouse:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175)), inline=True)
                                                    else:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            else:
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {}. It will be added to the balance shortly.\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            await boost.heal_in.create_dm()
                                            await boost.heal_in.dm_channel.send(embed = embed_message)
                                        if boost.dps_in[0] != "":
                                            if boost.auto_post:
                                                name = boost.dps_in[0].display_name
                                                user_name_serv = parseName(name)
                                                gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {} and added to the balance!\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    embed_message.add_field(name="Your balance", value = "You now have {} gold!".format(gold), inline=True)
                                                    if boost.inhouse:
                                                        if player_index == 1:
                                                            if boost.no_adv_cut:
                                                                cut = int(boost.gold*0.225*0.85*4)
                                                            else:
                                                                cut = int(boost.gold*0.2175*0.85 *4)
                                                        elif player_index == 2 or boost.type == "island":
                                                            if boost.no_adv_cut:
                                                                cut = int(boost.gold*0.225*0.85*2)
                                                            else:
                                                                cut = int(boost.gold*0.2175*0.85 *2)
                                                        else:
                                                            if boost.no_adv_cut:
                                                                cut = int(boost.gold*0.225*0.85)
                                                            else:
                                                                cut = int(boost.gold*0.2175*0.85)
                                                        embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(cut), inline=True)
                                                    else:
                                                        if boost.type in ["torghast"] or player_index == 1:
                                                            if boost.no_adv_cut:
                                                                cut = int(boost.gold*0.22*4)
                                                            else:
                                                                if boost.type == "leveling" or boost.type == "pvp":
                                                                    cut = int(boost.gold*0.75)
                                                                else:
                                                                    cut = int(boost.gold*0.18 *4)
                                                        elif player_index == 2 or boost.type == "island":
                                                            if boost.no_adv_cut:
                                                                cut = int(boost.gold*0.22*2)
                                                            else:
                                                                cut = int(boost.gold*0.18 *2)
                                                        else:
                                                            if boost.no_adv_cut:
                                                                cut = int(boost.gold*0.22)
                                                            else:
                                                                cut = int(boost.gold*0.18)
                                                        if boost.type != "legacy":
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(cut), inline=True)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            else:
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {}. It will be added to the balance shortly.\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            await boost.dps_in[0].create_dm()
                                            await boost.dps_in[0].dm_channel.send(embed = embed_message)
                                        if boost.dps_in[1] != "":
                                            if boost.auto_post:
                                                name = boost.dps_in[1].display_name
                                                user_name_serv = parseName(name)
                                                gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {} and added to the balance!\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    embed_message.add_field(name="Your balance", value = "You now have {} gold!".format(gold), inline=True)
                                                    if player_index == 2 or boost.type == "island":
                                                        if boost.inhouse:
                                                            if boost.no_adv_cut:
                                                                embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.22*2)), inline=True)
                                                            else:
                                                                embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175*2)), inline=True)
                                                        else:
                                                            if boost.no_adv_cut:
                                                                embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.22*2)), inline=True)
                                                            else:
                                                                embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.18*2)), inline=True)
                                                    else:
                                                        if boost.inhouse:
                                                            if boost.no_adv_cut:
                                                                embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.22)), inline=True)
                                                            else:
                                                                embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175)), inline=True)
                                                        else:
                                                            if boost.no_adv_cut:
                                                                embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.22)), inline=True)
                                                            else:
                                                                embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            else:
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {}. It will be added to the balance shortly.\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            await boost.dps_in[1].create_dm()
                                            await boost.dps_in[1].dm_channel.send(embed = embed_message)
                                        if boost.dps_in[2] != "":
                                            if boost.auto_post:
                                                name = boost.dps_in[2].display_name
                                                user_name_serv = parseName(name)
                                                gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {} and added to the balance!\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    if boost.inhouse:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175)), inline=True)
                                                    else:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            else:
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {}. It will be added to the balance shortly.\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            await boost.dps_in[2].create_dm()
                                            await boost.dps_in[2].dm_channel.send(embed = embed_message)
                                        if boost.dps_in[3] != "":
                                            if boost.auto_post:
                                                name = boost.dps_in[3].display_name
                                                user_name_serv = parseName(name)
                                                gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {} and added to the balance!\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    embed_message.add_field(name="Your balance", value = "You now have {} gold!".format(gold), inline=True)
                                                    if boost.inhouse:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175)), inline=True)
                                                    else:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Your cut", value = "Your cut was {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            else:
                                                embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "The boost has been validated by {}. It will be added to the balance shortly.\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            await boost.dps_in[3].create_dm()
                                            await boost.dps_in[3].dm_channel.send(embed = embed_message)
                                    else:
                                        await message.remove_reaction(emoji, user)
                                if emoji == self.denied_emo:
                                    if boost.advertiser.id == user.id or user.id == self.__day_id or (boost.helper != "" and boost.helper.id == user.id):
                                        embed_message = discord.Embed(title="Boost cancel", color=0xdc143c)#7FFF00
                                        embed_message.add_field(name="\u200b", value = "The boost was canceled.", inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                        await boost.message_annoucement.edit(embed=embed_message)
                                        await boost.message_annoucement.clear_reactions()
                                        self.__boost_being_done.pop(w)
                                        embed_message = discord.Embed(title="Boost ended", color=0xdc143c)#7FFF00
                                        embed_message.add_field(name="Boost failed", value = "{} indicated the boost you performed has been failed or canceled. Your balance haven't been change.\n Please contact {} to have more information.".format(boost.advertiser.mention,boost.advertiser.mention), inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                        embed_message_adv = discord.Embed(title="Boost ended", color=0xdc143c)#7FFF00
                                        embed_message_adv.add_field(name="Boost failed", value = "You indicated the boost as failed. The balance haven't been modified.".format(boost.advertiser.mention,boost.advertiser.mention), inline=False)
                                        embed_message_adv.set_footer(text="Gino's Mercenaries")
                                        await boost.advertiser.create_dm()
                                        await boost.advertiser.dm_channel.send(embed = embed_message_adv)
                                        if boost.tank_in != "":
                                            await boost.tank_in.create_dm()
                                            await boost.tank_in.dm_channel.send(embed = embed_message)
                                        if boost.heal_in != "":
                                            await boost.heal_in.create_dm()
                                            await boost.heal_in.dm_channel.send(embed = embed_message)
                                        if boost.dps_in[0] != "":
                                            await boost.dps_in[0].create_dm()
                                            await boost.dps_in[0].dm_channel.send(embed = embed_message)
                                        if boost.dps_in[1] != "":
                                            await boost.dps_in[1].create_dm()
                                            await boost.dps_in[1].dm_channel.send(embed = embed_message)
                                        if boost.dps_in[2] != "":
                                            await boost.dps_in[2].create_dm()
                                            await boost.dps_in[2].dm_channel.send(embed = embed_message)
                                        if boost.dps_in[3] != "":
                                            await boost.dps_in[3].create_dm()
                                            await boost.dps_in[3].dm_channel.send(embed = embed_message)
                                    else:
                                        await message.remove_reaction(emoji, user)
                            w += 1
                # Raid accepted
                if emoji == self.mail_emo:
                    rl = False
                    user_role = [o.name for o in user.roles]
                    for role in user_role:
                        if role in self.raid_leader_role:
                            rl = True
                            break
                    if rl is True:
                        resp = get_list_tag(message.content)
                        list_tag = resp[0]
                        embed_rooster = discord.Embed(title="Accepted in raid", description="You've been selected for the raid in {}.\nPlease refer to the channel for more info!".format(channel.mention) ,color=0x61b3f2)#7FFF0
                        alreadyin = False
                        iter_raid = 0
                        for raid in self.__raids:
                            if raid[0] == message.id:
                                alreadyin = True
                                break
                            iter_raid += 1
                        if alreadyin is False:
                            iter_raid = len(self.__raids)
                            self.__raids.append([message.id, []])
                        for tag in list_tag:
                            member = discord.utils.get(self.__guild.members, id=int(tag))
                            if member not in self.__raids[iter_raid][1]:
                                self.__raids[iter_raid][1].append(member)
                                await member.create_dm()
                                await member.dm_channel.send(embed = embed_rooster)
                # Raid inv
                if emoji == self.inv_emo:
                    rl = False
                    user_role = [o.name for o in user.roles]
                    for role in user_role:
                        if role in self.raid_leader_role:
                            rl = True
                            break
                    if rl is True:
                        rep = get_list_tag(message.content)
                        list_tag = rep[0]
                        inv_message = rep[1]
                        embed_rooster = discord.Embed(title="Raid is ready" ,color=0x61b3f2)#7FFF0
                        iter_raid = 0
                        for raid in self.__raids:
                            if raid[0] == message.id:
                                self.__raids.pop(iter_raid)
                                break
                            iter_raid += 1
                        if inv_message != "":
                            inv = "```css\n" + inv_message + "```Copy paste that, it auto invites!"
                            embed_rooster.add_field(name="\u200b", value="The raid in {} is ready! Please log on your character and whisper the following char:".format(channel.mention) +inv, inline = False)
                            embed_rooster.add_field(name="\u200b", value="Good luck, have fun! :smile:", inline = False)
                        else:
                            embed_rooster.add_field(name="\u200b", value="The raid in {} is ready! Please log on your character and whisper the according char.".format(channel.mention), inline = False)
                            embed_rooster.add_field(name="\u200b", value="Good luck, have fun! :smile:", inline = False)

                        for tag in list_tag:
                            embed_rooster.set_footer(text="Gino's Mercenaries")
                            member = discord.utils.get(self.__guild.members, id=int(tag))
                            await member.create_dm()
                            await member.dm_channel.send(embed = embed_rooster)
                #Raid finish
                if emoji == self.allowed_emo and message.content.lower().startswith("here's the roster"):
                    rl = False
                    user_role = [o.name for o in user.roles]
                    for role in user_role:
                        if role in self.raid_leader_role:
                            rl = True
                            break
                    if rl is True:
                        rep = get_list_tag_cut(message.content)
                        list_tag = rep[0]
                        inv_message = rep[1]
                        cut = rep[2]
                        embed_rl = discord.Embed(title="GG on the raid!", description="Thank you for handling the raid: {}!\n Here is the list of boosters:".format(channel.mention) ,color=0x61b3f2)#7FFF0
                        embed_raiders = discord.Embed(title="GG on the raid!", description="Thank you for raiding with us on {}!\n Your balance will be updated soon.".format(channel.mention) ,color=0x61b3f2)#7FFF
                        embed_raiders.add_field(name="Your cut:", value="Your cut will be {} :moneybag:".format(cut), inline = False)
                        embed_raiders.set_footer(text="Gino's Mercenaries")
                        list_names = ""
                        for tag in list_tag:
                            member = discord.utils.get(self.__guild.members, id=int(tag))
                            list_names += onlyName(member.display_name) + "\n"
                            await member.create_dm()
                            await member.dm_channel.send(embed = embed_raiders)
                        embed_rl.add_field(name="Boosters", value=list_names, inline = False)
                        embed_rl.set_footer(text="Gino's Mercenaries")
                        await user.create_dm()
                        await user.dm_channel.send(embed = embed_rl)


        except:
                err = traceback.format_exc()
                if "AttributeError" not in err:
                    embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
                    embed_error.add_field(name="Error", value = err)
                    embed_error.set_footer(text="Gino's Mercenaries")
                    day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
                    await day_member.create_dm()
                    await day_member.dm_channel.send(embed=embed_error)
    ###########################################################################
    #                              On reaction remove                         #
    ###########################################################################
    async def on_raw_reaction_remove(self, payload):
        try:
            channel = discord.utils.get(self.__guild.channels, id=payload.channel_id, type=discord.ChannelType.text)
            message = await channel.fetch_message(payload.message_id)
            user = discord.utils.get(self.__guild.members, id=payload.user_id)
            emoji = payload.emoji
            if user.id != self.__bot_id:
                # Boost
                if message.channel.id in self.__boost_annoucement_list_id:
                    for boost in self.__boost_being_fill:
                        if boost.message_annoucement.id == message.id:
                            if boost.tank_in == user and emoji == self.tank_emo:
                                boost.tank_in = ""
                                boost.booster_place += 1
                                em = boost.post()
                                await boost.message_annoucement.edit(embed = em)
                                if len(boost.tank_waiting) > 0:
                                    for j in range(len(boost.tank_waiting)):
                                        if j < len(boost.tank_waiting) and boost.notIn(boost.tank_waiting[j]):
                                            boost.tank_in = boost.tank_waiting[j]
                                            boost.tank_waiting.pop(j)
                                            em = boost.post()
                                            await boost.message_annoucement.edit(embed = em)
                                            boost.booster_place -=1
                                            break
                            elif boost.heal_in == user and emoji == self.heal_emo:
                                boost.heal_in = ""
                                boost.booster_place += 1
                                em = boost.post()
                                await boost.message_annoucement.edit(embed = em)
                                if len(boost.heal_waiting) > 0:
                                    for j in range(len(boost.heal_waiting)):
                                        if j < len(boost.heal_waiting) and boost.notIn(boost.heal_waiting[j]):
                                            boost.heal_in = boost.heal_waiting[j]
                                            boost.heal_waiting.pop(j)
                                            em = boost.post()
                                            await boost.message_annoucement.edit(embed = em)
                                            boost.booster_place -=1
                                            break
                            elif emoji == self.dps_emo:
                                for j in range(len(boost.dps_in)):
                                    if user == boost.dps_in[j]:
                                        boost.dps_in[j] = ""
                                        boost.booster_place += 1
                                        em = boost.post()
                                        await boost.message_annoucement.edit(embed = em)
                                        if len(boost.dps_waiting) > 0:
                                            for k in range(len(boost.dps_waiting)):
                                                if  k < len(boost.dps_waiting) and boost.notIn(boost.dps_waiting[k]):
                                                    boost.dps_in[j] = boost.dps_waiting[k]
                                                    boost.dps_waiting.pop(k)
                                                    em = boost.post()
                                                    await boost.message_annoucement.edit(embed = em)
                                                    boost.booster_place -=1
                                                    break
                            if user in boost.tank_waiting:
                                if emoji == self.tank_emo:
                                    boost.tank_waiting.remove(user)
                                elif boost.tank_in == "" and len(boost.tank_waiting)>0:
                                    for j in range(len(boost.tank_waiting)):
                                        if j < len(boost.tank_waiting) and boost.notIn(boost.tank_waiting[j]):
                                            boost.tank_in = boost.tank_waiting[j]
                                            boost.tank_waiting.pop(j)
                                            em = boost.post()
                                            await boost.message_annoucement.edit(embed = em)
                                            boost.booster_place -=1
                                            break
                            if user in boost.heal_waiting:
                                if emoji == self.heal_emo:
                                    boost.heal_waiting.remove(user)
                                elif boost.heal_in == "" and len(boost.heal_waiting)>0:
                                    for j in range(len(boost.heal_waiting)):
                                        if j < len(boost.heal_waiting) and boost.notIn(boost.heal_waiting[j]):
                                            boost.heal_in = boost.heal_waiting[j]
                                            boost.heal_waiting.pop(j)
                                            em = boost.post()
                                            await boost.message_annoucement.edit(embed = em)
                                            boost.booster_place -=1
                                            break
                            if user in boost.dps_waiting:
                                if emoji == self.dps_emo:
                                    boost.dps_waiting.remove(user)
                                else:
                                    for i in range(boost.nb_dps):
                                        if boost.dps_in[i] == "" and len(boost.dps_waiting)>0:
                                            for j in range(len(boost.dps_waiting)):
                                                if j < len(boost.dps_waiting) and boost.notIn(boost.dps_waiting[j]):
                                                    boost.dps_in[i] = boost.dps_waiting[j]
                                                    boost.dps_waiting.pop(j)
                                                    em = boost.post()
                                                    await boost.message_annoucement.edit(embed = em)
                                                    boost.booster_place -=1
                                                    break
        except:
             err = traceback.format_exc()
             embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
             embed_error.add_field(name="Error", value = err)
             embed_error.set_footer(text="Gino's Mercenaries")
             day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
             await day_member.create_dm()
             await day_member.dm_channel.send(embed=embed_error)



async def add_booster(user, role, boost, user_role, by_pass, message, emoji):
    if role == "tank":
        await add_tank(user, boost, user_role, by_pass, message, emoji)
    if role == "heal":
        await add_heal(user, boost, user_role, by_pass, message, emoji)
    if role == "dps":
        await add_dps(user, boost, user_role, by_pass, message, emoji)

async def add_tank(user, boost, user_role, by_pass, message, emoji):
    if all(elem in user_role for elem in boost.role_tank) or by_pass:
        if boost.tank_in == "" and boost.notIn(user) and (boost.type == "mm" or boost.type == "tazavesh"):
            boost.tank_in = user
            em = boost.post()
            await boost.message_annoucement.edit(embed = em)
            boost.booster_place -= 1
        else:
            boost.tank_waiting.append(user)
    else:
        await user.create_dm()
        embed_message = discord.Embed(title="Not the permission", color=0xdc143c)#7FFF00
        embed_message.add_field(name="\u200b", value="You lack one of the following role to tag in the boost as tank : {}.".format(', '.join(boost.role_tank)), inline=False)
        embed_message.set_footer(text="Gino's Mercenaries")
        await user.dm_channel.send(embed=embed_message)
        await message.remove_reaction(emoji,user)

async def add_heal(user, boost, user_role, by_pass, message, emoji):
    if all(elem in user_role for elem in boost.role_heal) or by_pass:
        if boost.heal_in == "" and boost.notIn(user) and (boost.type == "mm" or boost.type == "tazavesh"):
            boost.heal_in = user
            em = boost.post()
            await boost.message_annoucement.edit(embed = em)
            boost.booster_place -= 1
        else:
            boost.heal_waiting.append(user)
    else:
        await user.create_dm()
        embed_message = discord.Embed(title="Not the permission", color=0xdc143c)#7FFF00
        embed_message.add_field(name="\u200b", value="You lack one of the following role to tag in the boost as heal : {}.".format(', '.join(boost.role_heal)), inline=False)
        embed_message.set_footer(text="Gino's Mercenaries")
        await user.dm_channel.send(embed=embed_message)
        await message.remove_reaction(emoji,user)

async def add_dps(user, boost, user_role, by_pass, message, emoji):
    if all(elem in user_role for elem in boost.role_dps) or by_pass:
        if boost.dps_in[0] == "" and boost.notIn(user):
            boost.dps_in[0] = user
            em = boost.post()
            await boost.message_annoucement.edit(embed = em)
            boost.booster_place -= 1
        elif boost.dps_in[1] == "" and boost.notIn(user) and boost.nb_dps > 1:
            boost.dps_in[1] = user
            em = boost.post()
            await boost.message_annoucement.edit(embed = em)
            boost.booster_place -= 1
        else:
            boost.dps_waiting.append(user)
    else:
        await user.create_dm()
        embed_message = discord.Embed(title="Not the permission", color=0xdc143c)#7FFF00
        embed_message.add_field(name="\u200b", value="You lack one of the following role to tag in the boost : {}.".format(', '.join(boost.role_dps)), inline=False)
        embed_message.set_footer(text="Gino's Mercenaries")
        await user.dm_channel.send(embed=embed_message)
        await message.remove_reaction(emoji, user)
