from datetime import datetime
import traceback
import json
import discord
import os
import asyncio
from sheet import *
from utils import *
from boost import *


class pvpClient(discord.Client):
    ###########################################################################
    #                                       Init                              #
    ###########################################################################
    def __init__(self, guild_name):
        self.guild_name = guild_name
        self.__day_id = 302188753206771714
        self.__bot_id = 829355173435408404
        self.testy = False
        if self.testy: #Jmone
            self.request_2_ally = 839772035348561930
            self.request_3_ally = 839772053200044073
            self.request_2_horde = 839772107780259850
            self.request_3_horde = 839772125064724490
            self.request_rbg_ally = 839772089303957504
            self.request_rbg_horde = 839772148616527932
            self.request_coach_ally = 839772658081464380
            self.request_coach_horde = 839772615337836551
            self.ongoing_boost = 839772217289867265
            self.completed_boost_ally = 839772241834016788
            self.completed_boost_horde = 839772273392353280
            self.__collecting_gold_id = 741569122957262849
        else:
            self.request_2_ally = 826508540860170301
            self.request_3_ally = 826513235796426762
            self.request_2_horde = 826518618426310716
            self.request_3_horde = 826518652744499280
            self.request_rbg_ally = 826513327986573312
            self.request_rbg_horde = 826518665256108032
            self.request_coach_ally = 826513298744410181
            self.request_coach_horde = 826518679196925962
            self.ongoing_boost = 826795308758335558
            self.completed_boost_ally = 826531910032949302
            self.completed_boost_horde = 826532958508286003
            self.__collecting_gold_id = 741953895604944946
        self.pvp_channels = [self.request_2_ally, self.request_3_ally, self.request_2_horde, self.request_3_horde, self.request_rbg_ally, self.request_rbg_horde, self.request_coach_ally, self.request_coach_horde]
        self.__boost_request = []
        self.__ongoing_boosts =[]
        self.__boost_being_collected = []
        self.__last_webhook = []
        intents = discord.Intents.all()
        super(pvpClient, self).__init__(intents=intents)

    ###########################################################################
    #                              On ready function                          #
    ###########################################################################
    async def on_ready(self):
        print(self.guild_name)
        self.__guild = discord.utils.get(self.guilds, name=self.guild_name)
        #me = discord.utils.get(self.__guild.members, id=self.__day_id)
        #await me.create_dm()
        print("running")
        print(self.__guild)
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
        self.alliance_emo = discord.utils.get(self.__guild.emojis, name="alliance")
        self.horde_emo = discord.utils.get(self.__guild.emojis, name="horde")
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
            # Ping
            if message.content.lower() == "ping":
                user_id = message.author.id
                if user_id == self.__day_id:
                    await message.channel.send("Pog!!!!")
            # list_status
            elif message.content.lower() == "list_status":
                 user_id = message.author.id
                 if user_id == self.__day_id:
                     await message.channel.send(self.__boost_request)
            # Select command
            elif message.content.lower().startswith("!select "):
                user = message.author
                error = ""
                values = message.content.split(" ")
                try:
                    id = values[1]
                    booster_1 = values[2]
                except:
                    error = "incorrect_use"
                try:
                    id = int(id)
                except:
                    error = "id_as_number"
                found = False
                for boost in self.__boost_request:
                    if boost.message_annoucement.id == id:
                        found = True
                        if boost.advertiser.id == user.id or user.id == self.__day_id or (boost.helper != "" and boost.helper.id == user.id):
                            if boost.nb_boosters == 2:
                                try:
                                    booster_2 = values[3]
                                except:
                                    error = "missing_2nd_booster"
                                try:
                                    name = booster_2.replace(" ","")
                                    name = onlyName(name)
                                    p = self.get_all_members()
                                    booster = list(filter(lambda m: sameName(m.display_name.lower(), name.lower()), p))[0]
                                    boost.dps_in[1] = booster
                                except:
                                    error = "booster_2_no_exit"
                            try:
                                name = booster_1.replace(" ","")
                                name = onlyName(name)
                                p = self.get_all_members()
                                booster = list(filter(lambda m: sameName(m.display_name.lower(), name.lower()), p))[0]
                                boost.dps_in[0] = booster
                            except:
                                error = "booster_1_no_exit"
                            if error == "":
                                ongoing_boost_chan = discord.utils.get(self.__guild.channels, id=self.ongoing_boost)
                                await boost.message_annoucement.delete()
                                try:
                                    await boost.tag_message.delete()
                                except:
                                    pass
                                # GOLD COLLECTION IF NEEDED
                                roles = boost.advertiser.roles
                                role_str = [y.name.lower() for y in roles]
                                new_adv = False
                                if "new advertiser" in role_str:
                                    new_adv = True
                                    if "alliance advertiser" in role_str or "horde advertiser" in role_str or "trusted advertiser" in role_str or "gold collector" in role_str:
                                        new_adv = False
                                if new_adv:
                                    # DM the new adv
                                    gold_collecting_chan = discord.utils.get(self.__guild.channels, id=self.__collecting_gold_id)
                                    embed_message = discord.Embed(title="Gold Collection", color=0x61b3f2, description="Thank you for your boost!\nAs you are a new advertiser, a Gold Collector will collect the gold before the boost is validated as ongoing boost.\nPlease check {} where you'll be able to see who you have to invite to collect the gold.".format(gold_collecting_chan.mention))#7FFF00
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await boost.advertiser.create_dm()
                                    await boost.advertiser.send(embed= embed_message)
                                    # Post in collection (add message in boost)
                                    embed_message = discord.Embed(title="Gold Collection: {} - {}".format(boost.realm.capitalize(), boost.faction.capitalize()), color=0x61b3f2)#7FFF00
                                    embed_message.add_field(name="Advertiser", value = "{} - {}".format(boost.advertiser.mention, boost.advertiser.display_name))
                                    embed_message.add_field(name="Character to whisp", value = boost.who_to_w, inline=False)
                                    embed_message.add_field(name="Gold", value = "{}k".format(boost.gold/1000), inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    boost.message_collecting = await gold_collecting_chan.send(embed = embed_message)
                                    await boost.message_collecting.add_reaction(self.allowed_emo)
                                    await boost.message_collecting.add_reaction(self.denied_emo)
                                    gold_collector_role = discord.utils.get(self.__guild.roles, name='Gold Collector')
                                    boost.tmp_collecting_msg = await gold_collecting_chan.send("{} Can one of you collect the gold?\nPlease warn the others by writing in this chan that you will take care of it.\nPress {} only when collected please!".format(gold_collector_role.mention, self.allowed_emo))
                                    # add boost in list
                                    self.__boost_request.remove(boost)
                                    self.__boost_being_collected.append(boost)
                                else:
                                    # ADV DM
                                    embed_message = discord.Embed(title="PvP boost Validation", description="Thanks for validating the boost. Please contact the booster that you selected to start the boost.", color=0xEBC334)#7FFF00
                                    embed_message.add_field(name="Ongoing boost and how to close it", value="A boost recap has been posted in {}. When the boost is finish, simply use {} to post it in the balance.".format(ongoing_boost_chan.mention, self.allowed_emo), inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await boost.advertiser.create_dm()
                                    await boost.advertiser.send(embed=embed_message)
                                    # ONGOING EMBED
                                    embed_message = discord.Embed(title="PvP ongoing boost", color=0xEBC334)#7FFF00
                                    embed_message.add_field(name="Boost", value = "```{}```".format(boost.notes), inline=False)
                                    embed_message.add_field(name="Gold", value = "{:,} {}".format(int(boost.gold), self.coin_emo), inline=True)
                                    embed_message.add_field(name="Buyer's PvP experience", value = "{}".format(boost.buyer_name), inline=True)
                                    embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
                                    embed_message.add_field(name="Advertiser", value = boost.advertiser.mention, inline=True)
                                    if boost.dps_in[0] != "":
                                        embed_message.add_field(name="Booster", value = "{} - {}".format(boost.dps_in[0].mention, boost.dps_in[0].display_name), inline=True)
                                    if boost.dps_in[1] != "":
                                        embed_message.add_field(name="Booster", value = "{} - {}".format(boost.dps_in[1].mention, boost.dps_in[1].display_name), inline=True)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    self.__ongoing_boosts.append(boost)
                                    self.__boost_request.remove(boost)
                                    boost.ongoing_message = await ongoing_boost_chan.send(embed=embed_message)
                                    await boost.ongoing_message.add_reaction(self.allowed_emo)
                                    await boost.ongoing_message.add_reaction(self.denied_emo)
                                    # BOOSTER DM
                                    # Selected
                                    if boost.faction.lower() == "alliance":
                                        fact_emo = self.alliance_emo
                                    else:
                                        fact_emo = self.horde_emo
                                    embed_message_s = discord.Embed(title="PvP boost - Selected", description="You were selected for a PvP boost.", color=0xEBC334)#7FFF00
                                    embed_message_s.add_field(name="Boost Recap", value="{} {} - {} - {} - Notes: *{}*".format(boost.gold, self.coin_emo, fact_emo, boost.pvp_type.capitalize(), boost.notes), inline=False)
                                    embed_message_s.add_field(name="Next steps", value="{} will contact you soon to start the boost. If she/he doesn't, feel free to send a little dm!".format(boost.advertiser.mention), inline=False)
                                    embed_message_s.set_footer(text="Gino's Mercenaries")
                                    # Not selected
                                    embed_message = discord.Embed(title="PvP boost - Not selected", description="The PvP boost you applied in is no longer looking for boosters and you were not selected.", color=0xEBC334)#7FFF00
                                    embed_message.add_field(name="Boost Recap", value="{} {} - {} - {} - Notes: *{}*".format(boost.gold, self.coin_emo, fact_emo, boost.pvp_type.capitalize(), boost.notes), inline=False)
                                    embed_message.add_field(name="What happened", value="{} selected another PvP booster(s) for the boost. Please feel free to message him/her for more information".format(boost.advertiser.mention), inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    for booster in boost.dps_waiting:
                                        if booster != boost.dps_in[0] and booster != boost.dps_in[1]:
                                            await booster.create_dm()
                                            await booster.send(embed=embed_message)
                                        else:
                                            await booster.create_dm()
                                            await booster.send(embed=embed_message_s)
                        else:
                            error = "no_write"
                if found == False:
                    error = "boost_not_found"
                if error == "incorrect_use":
                    embed_message = discord.Embed(title="Incorrect use of the select command", description="Could not found the boost id and the booster-name in your message. Please use the command as presented and avoid adding unecessery spaces!", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "id_as_number":
                    embed_message = discord.Embed(title="Incorrect ID", description="The ID you entered is not a number.", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "boost_not_found":
                    embed_message = discord.Embed(title="Incorrect ID", description="There is no boost request with the ID you entered.", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "missing_2nd_booster":
                    embed_message = discord.Embed(title="Missing booster", description="For a 3v3 boost, please enter both booster at the same time.", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "booster_1_no_exit":
                    embed_message = discord.Embed(title="Could not find booster", description="Could not find the first booster you entered in discord", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "booster_2_no_exit":
                    embed_message = discord.Embed(title="Could not find booster", description="Could not find the second booster you entered in discord", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)

        ############################## reload #############################
        elif message.channel.name == "private-bot-commands" and message.content.startswith("!rename"):
            reload_dict()
            await message.add_reaction(self.allowed_emo)
        
        ################## form ###########################
        elif message.channel.name == "form" and message.author.id != self.__bot_id:
            to_handle = False
            if len(message.embeds)> 0:
                error = ""
                em = message.embeds[0]
                for field in em.fields:
                    if field.name =="Type of boost:":
                        if field.value.lower() == "pvp":
                            to_handle = True
            if to_handle:
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
                    boost.type = "pvp"
                    for field in em.fields:
                        if field.name == "Faction:":
                            boost.faction = field.value.lower()
                        if field.name == "Status:":
                            status = field.value.lower()
                        if field.name == "Boost description:":
                            boost.notes = field.value
                        if field.name == "Gold:":
                            boost.gold = int(field.value)
                        if field.name == "Gold faction:":
                            boost.gold_faction  = field.value
                        if field.name == "Collection Realm:":
                            boost.realm = main_connected_realm(field.value.lower())
                            boost.real_realm = field.value.lower()
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
                                    if boost.dps_in[1] == "" and boost.nb_boosters == 2:
                                        error = "DPS3v3"
                                except:
                                    error = "DPS"
                        if field.name == "Boost type:":
                            if field.value == "2v2":
                                boost.nb_boosters = 1
                                boost.pvp_type = "arena"
                            if field.value == "3v3":
                                boost.nb_boosters = 2
                                boost.pvp_type = "arena"
                            if field.value.upper() == "RBG":
                                boost.nb_boosters = 1
                                boost.pvp_type = "rbg"
                            if field.value.lower() == "coaching":
                                boost.nb_boosters = 1
                                boost.pvp_type = "coaching"
                        if field.name == "Buyer's PvP experience:":
                            boost.buyer_name = field.value
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
                        if status == "request":
                            if boost.faction == "alliance":
                                if boost.pvp_type == "arena" and boost.nb_boosters == 1:
                                    boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.request_2_ally)
                                if boost.pvp_type == "arena" and boost.nb_boosters == 2:
                                    boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.request_3_ally)
                                if boost.pvp_type == "rbg":
                                    boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.request_rbg_ally)
                                if boost.pvp_type == "coaching":
                                    boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.request_coach_ally)
                            elif boost.faction == "horde":
                                if boost.pvp_type == "arena" and boost.nb_boosters == 1:
                                    boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.request_2_horde)
                                if boost.pvp_type == "arena" and boost.nb_boosters == 2:
                                    boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.request_3_horde)
                                if boost.pvp_type == "rbg":
                                    boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.request_rbg_horde)
                                if boost.pvp_type == "coaching":
                                    boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.request_coach_horde)
                            em = boost.post()
                            boost.message_annoucement = await boost.annoucement_chan.send(embed=em)
                            role_tag = discord.utils.get(self.__guild.roles, name = boost.role_tag[0])
                            if boost.no_ping == False:
                                boost.tag_message = await boost.message_annoucement.channel.send("{} You can apply by pressing {}".format(role_tag.mention, self.dps_emo))
                            self.__boost_request.append(boost)
                            await boost.message_annoucement.add_reaction(self.dps_emo)
                            await boost.message_annoucement.add_reaction(self.denied_emo)
                            boost.pvp_id = boost.message_annoucement.id
                            await message.add_reaction(self.allowed_emo)
                        if status == "ongoing":
                            ongoing_boost_chan = discord.utils.get(self.__guild.channels, id=self.ongoing_boost)
                            # GOLD COLLECTION IF NEEDED
                            roles = boost.advertiser.roles
                            role_str = [y.name.lower() for y in roles]
                            new_adv = False
                            if "new advertiser" in role_str:
                                new_adv = True
                                if "alliance advertiser" in role_str or "horde advertiser" in role_str or "trusted advertiser" in role_str or "gold collector" in role_str:
                                    new_adv = False
                            if new_adv:
                                # DM the new adv
                                gold_collecting_chan = discord.utils.get(self.__guild.channels, id=self.__collecting_gold_id)
                                embed_message = discord.Embed(title="Gold Collection", color=0x61b3f2, description="Thank you for your boost!\nAs you are a new advertiser, a Gold Collector will collect the gold before the boost is validated as ongoing boost.\nPlease check {} where you'll be able to see who you have to invite to collect the gold.".format(gold_collecting_chan.mention))#7FFF00
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await boost.advertiser.create_dm()
                                await boost.advertiser.send(embed= embed_message)
                                # Post in collection (add message in boost)
                                embed_message = discord.Embed(title="Gold Collection: {} - {}".format(boost.realm.capitalize(), boost.faction.capitalize()), color=0x61b3f2)#7FFF00
                                embed_message.add_field(name="Advertiser", value = "{} - {}".format(boost.advertiser.mention, boost.advertiser.display_name))
                                embed_message.add_field(name="Character to whisp", value = boost.who_to_w, inline=False)
                                embed_message.add_field(name="Gold", value = "{}k".format(boost.gold/1000), inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                boost.message_collecting = await gold_collecting_chan.send(embed = embed_message)
                                await boost.message_collecting.add_reaction(self.allowed_emo)
                                await boost.message_collecting.add_reaction(self.denied_emo)
                                gold_collector_role = discord.utils.get(self.__guild.roles, name='Gold Collector')
                                boost.tmp_collecting_msg = await gold_collecting_chan.send("{} Can one of you collect the gold?\nPlease warn the others by writing in this chan that you will take care of it.\nPress {} only when collected please!".format(gold_collector_role.mention, self.allowed_emo))
                                boost.pvp_id = boost.tmp_collecting_msg.id
                                # add boost in list
                                self.__boost_being_collected.append(boost)
                            else:
                                # ADV DM
                                embed_message = discord.Embed(title="PvP boost ongoing", color=0xEBC334)#7FFF00
                                embed_message.add_field(name="Ongoing boost and how to close it", value="A boost recap has been posted in {}. When the boost is finish, simply use {} to post it in the balance.".format(ongoing_boost_chan.mention, self.allowed_emo), inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await boost.advertiser.create_dm()
                                await boost.advertiser.send(embed=embed_message)
                                # ONGOING EMBED
                                embed_message = discord.Embed(title="PvP ongoing boost", color=0xEBC334)#7FFF00
                                embed_message.add_field(name="Boost", value = "```{}```".format(boost.notes), inline=False)
                                embed_message.add_field(name="Gold", value = "{:,} {}".format(int(boost.gold), self.coin_emo), inline=True)
                                embed_message.add_field(name="Buyer's PvP experience", value = "{}".format(boost.buyer_name), inline=True)
                                embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
                                embed_message.add_field(name="Advertiser", value = boost.advertiser.mention, inline=True)
                                if boost.dps_in[0] != "":
                                    embed_message.add_field(name="Booster", value = "{} - {}".format(boost.dps_in[0].mention, boost.dps_in[0].display_name), inline=True)
                                if boost.dps_in[1] != "":
                                    embed_message.add_field(name="Booster", value = "{} - {}".format(boost.dps_in[1].mention, boost.dps_in[1].display_name), inline=True)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                self.__ongoing_boosts.append(boost)
                                boost.ongoing_message = await ongoing_boost_chan.send(embed=embed_message)
                                await boost.ongoing_message.add_reaction(self.allowed_emo)
                                await boost.ongoing_message.add_reaction(self.denied_emo)
                        if status == "completed":
                            sr = sheetReader()
                            ally_bool = True
                            if boost.faction == "horde":
                                ally_bool = False
                                completed_chan = discord.utils.get(self.__guild.channels, id=self.completed_boost_horde)
                            if ally_bool:
                                completed_chan = discord.utils.get(self.__guild.channels, id=self.completed_boost_ally)

                            embed_completed = discord.Embed(title="PvP completed boost", color=0xEBC334)#7FFF00
                            embed_completed.add_field(name="Boost", value = "```{}```".format(boost.notes), inline=False)
                            embed_completed.add_field(name="Gold", value = "{:,} {}".format(int(boost.gold), self.coin_emo), inline=True)
                            embed_completed.add_field(name="Buyer's PvP experience", value = "{}".format(boost.buyer_name), inline=True)
                            embed_completed.add_field(name="\u200b", value = "\u200b", inline=True)
                            embed_completed.add_field(name="Advertiser", value = boost.advertiser.mention, inline=True)
                            if boost.dps_in[0] != "":
                                embed_completed.add_field(name="Booster", value = "{} - {}".format(boost.dps_in[0].mention, boost.dps_in[0].display_name), inline=True)
                            if boost.dps_in[1] != "":
                                embed_completed.add_field(name="Booster", value = "{} - {}".format(boost.dps_in[1].mention, boost.dps_in[1].display_name), inline=True)
                            embed_completed.set_footer(text="Gino's Mercenaries")
                            await completed_chan.send(embed=embed_completed)
                            if boost.advertiser != "":
                                t_name = boost.advertiser.display_name
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
                            if boost.auto_post:
                                player_index = boost.nb_boosters
                                sr.post_boost(boost)
                                name =  boost.advertiser.display_name
                                user_name_serv = parseName(name)
                                gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                embed_message_adv = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                embed_message_adv.add_field(name="Thank you!", value = "The boost has been added to the balance!\nThank you for advertising with us!", inline=False)
                                embed_message_adv.add_field(name="Mail message", value = "Please put your **discord name as mail title** and copy/paste the following message for the body:```PvP - {}```If you are a New Advertiser, ignore this: the gold collector will mail the gold for you!".format(boost.pvp_id), inline=False)
                                if "-" not in boost.realm and boost.realm.upper() != "GINOS":
                                    embed_message_adv.add_field(name="Collection realm", value = "{}".format(boost.real_realm.capitalize()), inline=True)
                                    if boost.gold_faction.lower() == "alliance":
                                        embed_message_adv.add_field(name="Who to mail", value = "MercsAlly-{}".format(main_connected_realm(boost.realm).capitalize()), inline=True)
                                    else:
                                        embed_message_adv.add_field(name="Who to mail", value = "MercsHorde-{}".format(main_connected_realm(boost.realm).capitalize()), inline=True)
                                    embed_message_adv.add_field(name="Gold to send", value = "{:,}".format(boost.gold))
                                if gold == "Nbalance":
                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                else:
                                    embed_message_adv.add_field(name="Your balance", value = "You now have {} gold!".format(gold), inline=True)
                                embed_message_adv.set_footer(text="Gino's Mercenaries")
                            else:
                                em = boost.end_post()
                                await boost.unpost_chan.send(embed=em)
                                embed_message_adv = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                embed_message_adv.add_field(name="Thank you!", value = "The boost has been posted in {}, waiting to be added to the balance.\nThank you for advertising with us!".format(boost.unpost_chan.mention), inline=False)
                                embed_message_adv.set_footer(text="Gino's Mercenaries")
                            await boost.advertiser.create_dm()
                            await boost.advertiser.dm_channel.send(embed = embed_message_adv)
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
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                else:
                                    embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                    embed_message.add_field(name="Thank you!", value = "The boost has been validated by {}. It will be added to the balance shortly.\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                await boost.dps_in[1].create_dm()
                                await boost.dps_in[1].dm_channel.send(embed = embed_message)

                    elif error == "double":
                        embed_message = discord.Embed(title="Double post detected.", color=0xdc143c)#7FFF00
                        embed_message.add_field(name="\u200b", value="Google form seems to have sent the answer twice. Second will be ingore.\n If it was two different boosts, you posted them with less then 30 secs, impressive! In that case, simply repost the second one.", inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.channel.send(embed=embed_message)
                    elif error == "DPS3v3":
                        embed_message = discord.Embed(title="Missing one booster", color=0xdc143c)#7FFF00
                        embed_message.add_field(name="\u200b", value="You selected 3v3 but only added one booster.", inline=False)
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


    async def on_raw_reaction_add(self, payload):
        try:
            channel = discord.utils.get(self.__guild.channels, id=payload.channel_id, type=discord.ChannelType.text)
            try:
                message = await channel.fetch_message(payload.message_id)
                user = discord.utils.get(self.__guild.members, id=payload.user_id)
                emoji = payload.emoji
            except:
                return
            try:
                if emoji.is_unicode_emoji():
                    emoji = str(emoji)
            except:
                pass
            try:
                if len(self.__boost_request) > 300:
                    self.__boost_request.pop(0)
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
                                boost.gold_collector = user
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await boost.message_collecting.edit(embed = embed_message)
                                try:
                                    await boost.tmp_collecting_msg.delete()
                                except:
                                    pass
                                await message.channel.send("Thank you for collecting the gold {}! :heart:".format(user.mention))
                                await boost.message_collecting.clear_reactions()
                                self.__boost_being_collected.remove(boost)
                                gc_em = discord.Embed(title="Thanks for collecting the gold!", color=0x61b3f2)#7FFF00
                                gc_em.add_field(name="Mail message", value = "Please put the  **new advertiser's discord name as mail title** and copy/paste the following message for the body:```PvP - {}```".format(boost.pvp_id), inline=False)
                                gc_em.add_field(name="New advertiser's name", value = "{}".format(boost.advertiser.display_name), inline=False)
                                gc_em.add_field(name="Collection realm", value = "{}".format(boost.real_realm.capitalize()), inline=True)
                                if boost.gold_faction.lower() == "alliance":
                                    gc_em.add_field(name="Who to mail", value = "MercsAlly-{}".format(main_connected_realm(boost.realm).capitalize()), inline=True)
                                else:
                                    gc_em.add_field(name="Who to mail", value = "MercsHorde-{}".format(main_connected_realm(boost.realm).capitalize()), inline=True)
                                gc_em.add_field(name="Gold to send", value = "{:,}".format(boost.gold))
                                gc_em.set_footer(text="Gino's Mercenaries")
                                await user.create_dm()
                                await user.dm_channel.send(embed=gc_em)
                                ongoing_boost_chan = discord.utils.get(self.__guild.channels, id=self.ongoing_boost)
                                # ADV DM
                                embed_message = discord.Embed(title="PvP boost Validation", description="Thanks for validating the boost. Please contact the booster that you selected to start the boost.", color=0xEBC334)#7FFF00
                                embed_message.add_field(name="Ongoing boost and how to close it", value="A boost recap has been posted in {}. When the boost is finish, simply use {} to post it in the balance.".format(ongoing_boost_chan.mention, self.allowed_emo), inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                await boost.advertiser.create_dm()
                                await boost.advertiser.send(embed=embed_message)
                                # ONGOING EMBED
                                embed_message = discord.Embed(title="PvP ongoing boost", color=0xEBC334)#7FFF00
                                embed_message.add_field(name="Boost", value = "```{}```".format(boost.notes), inline=False)
                                embed_message.add_field(name="Gold", value = "{:,} {}".format(int(boost.gold), self.coin_emo), inline=True)
                                embed_message.add_field(name="Buyer's PvP experience", value = "{}".format(boost.buyer_name), inline=True)
                                embed_message.add_field(name="\u200b", value = "\u200b", inline=True)
                                embed_message.add_field(name="Advertiser", value = boost.advertiser.mention, inline=True)
                                if boost.dps_in[0] != "":
                                    embed_message.add_field(name="Booster", value = "{} - {}".format(boost.dps_in[0].mention, boost.dps_in[0].display_name), inline=True)
                                if boost.dps_in[1] != "":
                                    embed_message.add_field(name="Booster", value = "{} - {}".format(boost.dps_in[1].mention, boost.dps_in[1].display_name), inline=True)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                self.__ongoing_boosts.append(boost)
                                boost.ongoing_message = await ongoing_boost_chan.send(embed=embed_message)
                                await boost.ongoing_message.add_reaction(self.allowed_emo)
                                await boost.ongoing_message.add_reaction(self.denied_emo)
                                # BOOSTER DM
                                # Selected
                                if boost.faction.lower() == "alliance":
                                    fact_emo = self.alliance_emo
                                else:
                                    fact_emo = self.horde_emo
                                embed_message_s = discord.Embed(title="PvP boost - Selected", description="You were selected for a PvP boost.", color=0xEBC334)#7FFF00
                                embed_message_s.add_field(name="Boost Recap", value="{} {} - {} - {} - Notes: *{}*".format(boost.gold, self.coin_emo, fact_emo, boost.pvp_type.capitalize(), boost.notes), inline=False)
                                embed_message_s.add_field(name="Next steps", value="{} will contact you soon to start the boost. If she/he doesn't, feel free to send a little dm!".format(boost.advertiser.mention), inline=False)
                                embed_message_s.set_footer(text="Gino's Mercenaries")
                                # Not selected
                                embed_message = discord.Embed(title="PvP boost - Not selected", description="The PvP boost you applied in is no longer looking for boosters and you were not selected.", color=0xEBC334)#7FFF00
                                embed_message.add_field(name="Boost Recap", value="{} {} - {} - {} - Notes: *{}*".format(boost.gold, self.coin_emo, fact_emo, boost.pvp_type.capitalize(), boost.notes), inline=False)
                                embed_message.add_field(name="What happened", value="{} selected another PvP booster(s) for the boost. Please feel free to message him/her for more information".format(boost.advertiser.mention), inline=False)
                                embed_message.set_footer(text="Gino's Mercenaries")
                                for booster in boost.dps_waiting:
                                    if booster != boost.dps_in[0] and booster != boost.dps_in[1]:
                                        await booster.create_dm()
                                        await booster.send(embed=embed_message)
                                    else:
                                        await booster.create_dm()
                                        await booster.send(embed=embed_message_s)

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
                if message.channel.id in self.pvp_channels:
                    for boost in self.__boost_request:
                        if boost.message_annoucement.id == message.id:
                            if emoji == self.dps_emo:
                                if user not in boost.dps_waiting:
                                    boost.dps_waiting.append(user)
                                    await message.remove_reaction(emoji, user)
                                    embed_message = discord.Embed(title="PvP boost Apply", description="Thanks for applying in the PvP boost!", color=0xEBC334)#7FFF00
                                    if boost.faction.lower() == "alliance":
                                        fact_emo = self.alliance_emo
                                    else:
                                        fact_emo = self.horde_emo
                                    embed_message.add_field(name="Boost Recap", value="{} {} - {} - {} - Notes: *{}*".format(boost.gold, self.coin_emo, fact_emo, boost.pvp_type.capitalize(), boost.notes), inline=False)
                                    embed_message.add_field(name="Next steps", value="{} will review the applications and contact the first booster that suits. Feel free to take contact with him/her to receive/give extra information!".format(boost.advertiser.mention), inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await user.create_dm()
                                    await user.dm_channel.send(embed=embed_message)
                                    embed_message = discord.Embed(title="PvP boost Applications", description="{} - {} - {} just applied in your PvP boost!\nPlease review the application and use the *select command* if you'd like to select him as a booster.".format(user.mention, user.display_name, str(user)), color=0xEBC334)#7FFF00
                                    embed_message.add_field(name="Boost Recap", value="{} {} - {} - {} - Notes: *{}*".format(boost.gold, self.coin_emo, fact_emo, boost.pvp_type.capitalize(), boost.notes), inline=False)
                                    boosters_applications = ""
                                    for booster in boost.dps_waiting:
                                        boosters_applications += "{} - {} - {} \n".format(booster.mention, booster.display_name, str(booster))
                                    embed_message.add_field(name="List of boosters", value=boosters_applications, inline=False)
                                    if boost.pvp_type == "arena" and boost.nb_boosters == 2:
                                        embed_message.add_field(name="Select command", value="To select the two boosters for your boost, **please dm this bot (GinoPvP)** the following command:```!select {} name1-realm1 name2-realm2```".format(boost.pvp_id), inline=False)
                                    else:
                                        embed_message.add_field(name="Select command", value="To select the booster for your boost, **please dm this bot (GinoPvP)** the following command:```!select {} name-realm```".format(boost.pvp_id), inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await boost.advertiser.create_dm()
                                    await boost.advertiser.send(embed=embed_message)
                                else:
                                    await message.remove_reaction(emoji, user)
                            if emoji == self.denied_emo:
                                if boost.advertiser.id == user.id or user.id == self.__day_id or (boost.helper != "" and boost.helper.id == user.id):
                                    await boost.message_annoucement.delete()
                                    try:
                                        await boost.tag_message.delete()
                                    except:
                                        pass
                                    self.__boost_request.remove(boost)
                                    if boost.faction.lower() == "alliance":
                                        fact_emo = self.alliance_emo
                                    else:
                                        fact_emo = self.horde_emo
                                    embed_message = discord.Embed(title="PvP boost canceled", description="The PvP boost you applied in is canceled.", color=0xEBC334)#7FFF00
                                    embed_message.add_field(name="Boost Recap", value="{} {} - {} - {} - Notes: *{}*".format(boost.gold, self.coin_emo, fact_emo, boost.pvp_type.capitalize(), boost.notes), inline=False)
                                    embed_message.add_field(name="More info", value="Feel free to contact {} to get more information".format(boost.advertiser.mention), inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    for booster in boost.dps_waiting:
                                        await booster.create_dm()
                                        await booster.send(embed=embed_message)
                                else:
                                    await message.remove_reaction(emoji, user)
                # Boost Completed
                if message.channel.id == self.ongoing_boost:
                    for boost in self.__ongoing_boosts:
                        if boost.ongoing_message.id == message.id:
                            if emoji == self.denied_emo:
                                if boost.advertiser.id == user.id or user.id == self.__day_id or (boost.helper != "" and boost.helper.id == user.id):
                                    await boost.ongoing_message.delete()
                                    try:
                                        await boost.tag_message.delete()
                                    except:
                                        pass
                                    if boost.faction.lower() == "alliance":
                                        fact_emo = self.alliance_emo
                                    else:
                                        fact_emo = self.horde_emo
                                    embed_message = discord.Embed(title="PvP boost canceled", description="The PvP boost you applied in is canceled.", color=0xEBC334)#7FFF00
                                    embed_message.add_field(name="Boost Recap", value="{} {} - {} - {} - Notes: *{}*".format(boost.gold, self.coin_emo, fact_emo, boost.pvp_type.capitalize(), boost.notes), inline=False)
                                    embed_message.add_field(name="More info", value="Feel free to contact {} to get more information".format(boost.advertiser.mention), inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await boost.dps_in[0].create_dm()
                                    await boost.dps_in[0].send(embed=embed_message)
                                    if boost.nb_boosters == 2:
                                        await boost.dps_in[1].create_dm()
                                        await boost.dps_in[1].send(embed=embed_message)
                                    self.__ongoing_boosts.remove(boost)
                                else:
                                    await message.remove_reaction(emoji, user)
                            if emoji == self.allowed_emo:
                                if boost.advertiser.id == user.id or user.id == self.__day_id or (boost.helper != "" and boost.helper.id == user.id):
                                    try:
                                        await boost.ongoing_message.delete()
                                    except:
                                        pass
                                    self.__ongoing_boosts.remove(boost)
                                    sr = sheetReader()
                                    ally_bool = True
                                    if boost.faction == "horde":
                                        ally_bool = False
                                        completed_chan = discord.utils.get(self.__guild.channels, id=self.completed_boost_horde)
                                    if ally_bool:
                                        completed_chan = discord.utils.get(self.__guild.channels, id=self.completed_boost_ally)

                                    embed_completed = discord.Embed(title="PvP completed boost", color=0xEBC334)#7FFF00
                                    embed_completed.add_field(name="Boost", value = "```{}```".format(boost.notes), inline=False)
                                    embed_completed.add_field(name="Gold", value = "{:,} {}".format(int(boost.gold), self.coin_emo), inline=True)
                                    embed_completed.add_field(name="Buyer's PvP experience", value = "{}".format(boost.buyer_name), inline=True)
                                    embed_completed.add_field(name="\u200b", value = "\u200b", inline=True)
                                    embed_completed.add_field(name="Advertiser", value = boost.advertiser.mention, inline=True)
                                    if boost.dps_in[0] != "":
                                        embed_completed.add_field(name="Booster", value = "{} - {}".format(boost.dps_in[0].mention, boost.dps_in[0].display_name), inline=True)
                                    if boost.dps_in[1] != "":
                                        embed_completed.add_field(name="Booster", value = "{} - {}".format(boost.dps_in[1].mention, boost.dps_in[1].display_name), inline=True)
                                    embed_completed.set_footer(text="Gino's Mercenaries")
                                    await completed_chan.send(embed=embed_completed)
                                    if boost.advertiser != "":
                                        t_name = boost.advertiser.display_name
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
                                    if boost.auto_post:
                                        player_index = boost.nb_boosters
                                        sr.post_boost(boost)
                                        name =  boost.advertiser.display_name
                                        user_name_serv = parseName(name)
                                        gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                        embed_message_adv = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                        embed_message_adv.add_field(name="Thank you!", value = "The boost has been added to the balance!\nThank you for advertising with us!", inline=False)
                                        embed_message_adv.add_field(name="Mail message", value = "Please put your **discord name as mail title** and copy/paste the following message for the body:```PvP - {}```If you are a New Advertiser, ignore this: the gold collector will mail the gold for you!".format(boost.pvp_id), inline=False)
                                        if "-" not in boost.realm and boost.realm.upper() != "GINOS":
                                            embed_message_adv.add_field(name="Collection realm", value = "{}".format(boost.real_realm.capitalize()), inline=True)
                                            if boost.gold_faction.lower() == "alliance":
                                                embed_message_adv.add_field(name="Who to mail", value = "MercsAlly-{}".format(main_connected_realm(boost.realm).capitalize()), inline=True)
                                            else:
                                                embed_message_adv.add_field(name="Who to mail", value = "MercsHorde-{}".format(main_connected_realm(boost.realm).capitalize()), inline=True)
                                            embed_message_adv.add_field(name="Gold to send", value = "{:,} {}".format(boost.gold, self.coin_emo))
                                        if gold == "Nbalance":
                                            ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                        else:
                                            embed_message_adv.add_field(name="Your balance", value = "You now have {} gold!".format(gold), inline=True)
                                        embed_message_adv.set_footer(text="Gino's Mercenaries")
                                    else:
                                        em = boost.end_post()
                                        await boost.unpost_chan.send(embed=em)
                                        embed_message_adv = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                        embed_message_adv.add_field(name="Thank you!", value = "The boost has been posted in {}, waiting to be added to the balance.\nThank you for advertising with us!".format(boost.unpost_chan.mention), inline=False)
                                        embed_message_adv.set_footer(text="Gino's Mercenaries")
                                    await boost.advertiser.create_dm()
                                    await boost.advertiser.dm_channel.send(embed = embed_message_adv)
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
                                            embed_message.set_footer(text="Gino's Mercenaries")
                                        else:
                                            embed_message = discord.Embed(title="Boost ended", color=0x32cd32)#7FFF00
                                            embed_message.add_field(name="Thank you!", value = "The boost has been validated by {}. It will be added to the balance shortly.\nThank you for boosting with us!".format(boost.advertiser.mention), inline=False)
                                            embed_message.set_footer(text="Gino's Mercenaries")
                                        await boost.dps_in[1].create_dm()
                                        await boost.dps_in[1].dm_channel.send(embed = embed_message)
                                else:
                                    await message.remove_reaction(emoji, user)


        except:
            err = traceback.format_exc()
            embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
            embed_error.add_field(name="Error", value = err)
            embed_error.set_footer(text="Gino's Mercenaries")
            day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
            await day_member.create_dm()
            await day_member.dm_channel.send(embed=embed_error)
