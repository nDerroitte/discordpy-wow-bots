from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import requests
import discord
import os
import asyncio
from sheet import *
from utils import *
from strikeSheet import *


class timeClient(discord.Client):
    ###########################################################################
    #                                       Init                              #
    ###########################################################################
    def __init__(self, guild_name):
        self.guild_name = guild_name
        self.__day_id = 302188753206771714
        self.giveaway_list = []
        dt_wanted = datetime.now() + timedelta(days=1)
        self.next_run = datetime(dt_wanted.year, dt_wanted.month, dt_wanted.day, 15, 0)
        self.invites_dict = {}

        intents = discord.Intents.all()
        super(timeClient, self).__init__(intents=intents)

    ###########################################################################
    #                              On ready function                          #
    ###########################################################################
    async def on_ready(self):
        self.__guild = discord.utils.get(self.guilds, name=self.guild_name)
        #me = discord.utils.get(self.__guild.members, id=self.__day_id)
        #await me.create_dm()
        print("running")
        print(self.__guild)
        self.allowed_emo = discord.utils.get(self.__guild.emojis, name ="allowed")
        self.denied_emo = discord.utils.get(self.__guild.emojis, name ="denied")
        self.heal_emo = discord.utils.get(self.__guild.emojis, name ="heal")
        self.tank_emo = discord.utils.get(self.__guild.emojis, name ="tank")
        self.dps_emo = discord.utils.get(self.__guild.emojis, name ="dps")

        #await self.birthday()
        await self.timer()
        self.invites = self.__guild.invites()


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
                    await message.channel.send("Pong. :smile:")
            # Ping
            if message.content.lower() == "bday now":
                user_id = message.author.id
                if user_id == self.__day_id:
                    await self.birthday()

            # Ping
            if message.content.lower() == "untrike":
                user_id = message.author.id
                if user_id == self.__day_id:
                    await self.timer(do_it_now=True)

            elif message.content.lower() == "list_status":
                user_id = message.author.id
                if user_id == self.__day_id:
                    await message.channel.send(self.giveaway_list)

            elif message.content.lower() == "invite_start":
                await self.generate_inv_dict()
                sr = sheetStrike()
                sr.invite_start(self.invites_dict)


        elif "check-invites" in message.channel.name and message.content == "!i":
            await self.generate_inv_dict()
            sr = sheetStrike()
            dicto = sr.invite_current_uses(self.invites_dict)
            em = self.generate_invite_embed_private(dicto, message.author)
            await message.author.create_dm()
            await message.author.dm_channel.send(embed= em)
            await message.add_reaction(self.allowed_emo)


        # reset all star
        elif message.channel.name == "private-bot-commands" and message.content == "!reset91":
            # STEP DURING : Upgrade prestige that deserves it
            boosters = []
            all_members = message.guild.members
            for i in range(len(all_members)):
                roles_str = [o.name.lower() for o in all_members[i].roles]
                if "m+ prestige" in roles_str and "m+ allstars" not in roles_str:
                    boosters.append(all_members[i])
            len_to_update_members = len(boosters)
            count = 0
            for i in range(len_to_update_members):
                if i % 100 == 0 :
                    print(f'{i} / {len_to_update_members}')
                booster = boosters.pop()
                roles_str = [y.name.lower() for y in booster.roles]
                user_name_serv = parseName(booster.display_name)
                get_url = "https://raider.io/api/v1/characters/profile?region=eu&realm={}&name={}&fields=mythic_plus_scores_by_season%3Acurrent".format(user_name_serv[1].lower(),user_name_serv[0].lower().capitalize())
                r = requests.get(get_url)
                if r.status_code == 200:
                    data = r.json()
                    rio_heal = data["mythic_plus_scores_by_season"][0]['scores']['healer']
                    rio_tank = data["mythic_plus_scores_by_season"][0]['scores']['tank']
                    rio_dps = data["mythic_plus_scores_by_season"][0]['scores']['dps']
                    if rio_tank > 2150 or rio_heal > 2150 or rio_dps > 2150:
                        count += 1 
                        print(user_name_serv)
                        if "m+ allstars" not in roles_str:
                            m_all_star = discord.utils.get(self.__guild.roles, name='M+ AllStars')
                            await booster.add_roles(m_all_star)
                        if rio_heal > 2150 and "healer all star" not in roles_str:
                            healer_all_star = discord.utils.get(self.__guild.roles, name='Healer All Star')
                            await booster.add_roles(healer_all_star)
                        if rio_tank > 2150 and "tank all star" not in roles_str:
                            tank_all_star = discord.utils.get(self.__guild.roles, name='Tank All Star')
                            await booster.add_roles(tank_all_star)
                        if rio_dps > 2150 and "dps all star" not in roles_str:
                            dps_all_star = discord.utils.get(self.__guild.roles, name='DPS All Star')
                            await booster.add_roles(dps_all_star)
            
            print(count)
            await message.add_reaction(self.allowed_emo)
            # STEP 1 : Remove prestige if not all started
            # boosters = []
            # all_members = message.guild.members#list(self.get_all_members())
            # for i in range(len(all_members)):
            #     roles_str = [o.name.lower() for o in all_members[i].roles]
            #     if "m+ prestige" in roles_str and "m+ allstars" not in roles_str:
            #         boosters.append(all_members[i])
            # print(len(boosters))
            # len_to_update_members = len(boosters)
            # for i in range(len_to_update_members):
            #     booster = boosters.pop()
            #     roles_str = [y.name.lower() for y in booster.roles]
            #     if "m+ prestige" in roles_str:
            #         m_all_star = discord.utils.get(self.__guild.roles, name='M+ Prestige')
            #         await booster.remove_roles(m_all_star)
            #     if "healer prestige" in roles_str:
            #         healer_all_star = discord.utils.get(self.__guild.roles, name='Healer Prestige')
            #         await booster.remove_roles(healer_all_star)
            #     if "tank prestige"  in roles_str:
            #         tank_all_star = discord.utils.get(self.__guild.roles, name='Tank Prestige')
            #         await booster.remove_roles(tank_all_star)
            #     if "dps prestige"  in roles_str:
            #         dps_all_star = discord.utils.get(self.__guild.roles, name='DPS Prestige')
            #         await booster.remove_roles(dps_all_star)
            # # STEP 2 : Remove All star role
            # boosters = []
            # all_members = message.guild.members#list(self.get_all_members())
            # for i in range(len(all_members)):
            #     roles_str = [o.name for o in all_members[i].roles]
            #     if "M+ AllStars" in roles_str:
            #         boosters.append(all_members[i])
            # print(len(boosters))
            # len_to_update_members = len(boosters)
            # for i in range(len_to_update_members):
            #     booster = boosters.pop()
            #     roles_str = [y.name.lower() for y in booster.roles]
            #     if "m+ allstars" in roles_str:
            #         m_all_star = discord.utils.get(self.__guild.roles, name='M+ AllStars')
            #         await booster.remove_roles(m_all_star)
            #     if "healer all star" in roles_str:
            #         healer_all_star = discord.utils.get(self.__guild.roles, name='Healer All Star')
            #         await booster.remove_roles(healer_all_star)
            #     if "tank all star"  in roles_str:
            #         tank_all_star = discord.utils.get(self.__guild.roles, name='Tank All Star')
            #         await booster.remove_roles(tank_all_star)
            #     if "dps all star"  in roles_str:
            #         dps_all_star = discord.utils.get(self.__guild.roles, name='DPS All Star')
            #         await booster.remove_roles(dps_all_star)
            print("all done")

        elif message.channel.name == "private-bot-commands" and message.content == "!invites":
            await self.generate_inv_dict()
            sr = sheetStrike()
            dicto = sr.invite_current_uses(self.invites_dict)
            em = self.generate_invite_embed(dicto)
            await message.channel.send(embed=em)
            await message.add_reaction(self.allowed_emo)

        elif message.channel.name == "private-bot-commands" and message.content == "!invites_start":
            await message.channel.send("Working on it, can take a couple of minutes. Will {} when done!".format(self.allowed_emo))
            await self.generate_inv_dict()
            sr = sheetStrike()
            sr.invite_start(self.invites_dict)
            await message.add_reaction(self.allowed_emo)
            await message.channel.send("Done.")

        elif message.channel.name == "private-bot-commands" and message.content == "!invites_reset":
            await message.channel.send("Working on it, can take a couple of minutes. Will {} when done!".format(self.allowed_emo))
            await self.generate_inv_dict()
            sr = sheetStrike()
            sr.invite_reset()
            await message.add_reaction(self.allowed_emo)
            await message.channel.send("Done.")



    async def generate_inv_dict(self):
        self.invites_dict = {}
        current_invites = await self.__guild.invites()
        for inv in current_invites:
            creator = inv.inviter
            if creator in self.invites_dict:
                self.invites_dict[creator] +=  inv.uses
            else:
                self.invites_dict[creator] =  inv.uses
        self.invites_dict = {k: v for k, v in self.invites_dict.items() if v}
        self.invites_dict = dict(sorted(self.invites_dict.items(), key=lambda item: item[1], reverse = True))

    def generate_invite_embed(self, dicto):
        if len(dicto) == 0:
            embed_message = discord.Embed(title="List of invites", description="Here is the top 10 of the list:", color=0x9acd32)#7FFF00#9ACD32
            embed_message.add_field(name="Membres", value="No invitation yet!", inline = True)
            embed_message.set_footer(text="Gino's Mercenaries")
            return embed_message
        creators = []
        for creator in list(dicto.keys()):
            creators.append("{}".format(creator.name))
        uses = list(dicto.values())[:10]
        uses = map(str, uses)
        creators = creators[:10]
        embed_message = discord.Embed(title="List of invites", description="Here is the top 10 of the list:", color=0x9acd32)#7FFF00#9ACD32
        embed_message.add_field(name="Membres", value="{}".format('\n'.join(creators)), inline = True)
        embed_message.add_field(name="Number of invites", value="{}".format('\n'.join(uses)), inline = True)
        embed_message.set_footer(text="Gino's Mercenaries")
        return embed_message

    def generate_invite_embed_private(self, dicto, user):
        if len(dicto) == 0:
            embed_message = discord.Embed(title="List of invites", description="", color=0x9acd32)#7FFF00#9ACD32
            embed_message.add_field(name="Membres", value="No invitation yet!", inline = True)
            embed_message.set_footer(text="Gino's Mercenaries")
            return embed_message
        creators = []
        for creator in list(dicto.keys()):
            creators.append("{}".format(creator.name))
        uses = list(dicto.values())[:10]
        uses = map(str, uses)
        creators = creators[:10]
        my_invite = 0
        if user in dicto:
            my_invite = dicto[user]
        embed_message = discord.Embed(title="List of invites", description="You currently have {} invites.\nHere is the top 10 of the list:".format(my_invite), color=0x9acd32)#7FFF00#9ACD32
        embed_message.add_field(name="Membres", value="{}".format('\n'.join(creators)), inline = True)
        embed_message.add_field(name="Number of invites", value="{}".format('\n'.join(uses)), inline = True)
        embed_message.set_footer(text="Gino's Mercenaries")
        return embed_message

    async def timer(self, do_it_now = False):
        if do_it_now == False:
            delta_t = self.next_run - datetime.now()
            sec2wait = delta_t.seconds
            print(sec2wait)
            await asyncio.sleep(sec2wait)
            print("done")
        try:
            chan = discord.utils.get(self.__guild.channels, name='strikes', type=discord.ChannelType.text)
            ss = sheetStrike()
        except:
            return
        ask = ss.update()
        if len(ask[0]) == 0:
            print("debug")
            pass
        else:
            ask_message = discord.Embed(title="Unstrike message", description="Hi, here is the list of boosters  I've removed a strike from today:", color=0x9acd32)#7FFF00#9ACD32
            ask_message.add_field(name="Name", value = "{}".format('.\n'.join(ask[0])), inline=True)
            ask_message.add_field(name="Number of strikes", value = "{}".format('\n'.join(ask[1])), inline=True)
            ask_message.add_field(name="Last strike", value = "{}".format('.\n'.join(ask[2])), inline=True)
            ask_message.add_field(name=":tada:", value = "See you tomorrow!", inline=False)
            ask_message.set_footer(text="Gino's Mercenaries")
            await chan.send(embed=ask_message)

        await self.birthday()
        self.next_run = self.next_run + timedelta(hours=24)
        await self.timer()

    async def birthday(self):
        birthday_members = []
        # Retrieving the members
        p = self.get_all_members()
        for discord_member in p:
            delta_day = datetime.now() - discord_member.joined_at
            delta_day = delta_day.days
            roles_str = [o.name.lower() for o in discord_member.roles]
            if delta_day == 365 and "customer" in roles_str:
                birthday_members.append(discord_member)
        triple_list = [birthday_members[i::3] for i in range(3)]
        # Printing part
        if len(birthday_members) == 0:
            print("debug")
            pass
        else:
            rqst_chan = discord.utils.get(self.__guild.channels, id=757163555815686144, type=discord.ChannelType.text)
            ask_message = discord.Embed(title="Birthday message", description="Thank you for being part of our community!", color=0x9acd32)#7FFF00#9ACD32
            ask_message.add_field(name="Happy *one year* Birthday :tada:", value = "It's been a full year since you joined us today! Thanks a lot.", inline=False)
            ask_message.add_field(name=":cupcake:", value = "{}".format('\n'.join([x.mention for x in triple_list[0]])), inline=True)
            if len(triple_list[1]) > 0:
                ask_message.add_field(name="\u200b", value = "{}".format('\n'.join([x.mention for x in triple_list[1]])), inline=True)
            else:
                ask_message.add_field(name="\u200b", value = "\u200b", inline=True)
            if len(triple_list[2]) > 0:
                ask_message.add_field(name="\u200b", value = "{}".format('\n'.join([x.mention for x in triple_list[2]])), inline=True)
            else:
                ask_message.add_field(name="\u200b", value = "\u200b", inline=True)
            ask_message.add_field(name="Promotion", value = "To thank you, we'd like to offer you a 10% reduction on any boost you'd like. Please contact your favorite advertiser or head over to {} to claim your promotion!".format(rqst_chan.mention), inline=True)
            ask_message.set_footer(text="Gino's Mercenaries")
            chan = discord.utils.get(self.__guild.channels, id=886389884984651897, type=discord.ChannelType.text)
            await chan.send(embed=ask_message)
            await chan.send("{} \nHappy one-year-with-us birthday! :tada:".format(', '.join([x.mention for x in birthday_members])))
