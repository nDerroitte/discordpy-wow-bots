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

class auraManagementClient(discord.Client):
    ###########################################################################
    #                                       Init                              #
    ###########################################################################
    def __init__(self, guild_name):
        self.guild_name = guild_name
        self.__list_admin_roles = ["EN - Manager", "Developer"]
        self.__list_bot_roles = ["Bot"]
        self.__list_modo_roles = ["EN - Manager", "Developer", "Moderator"]
        self.__day_id = 302188753206771714
        self.to_update_members = []
        self.booking_id = 1
        self.ticket_id = 1
        self.giveaway_list = []
        self.list_nitro_str = ""
        self.__bot_id = 815643678689198090
        self.__strike_chan_id = 654520688870293525
        self.__booking_chan_id = 770335611478343691
        self.price_dict = {683130342651068426 : "pve", 633334207334055948 :"pvp", 676097936584867850 : "legacy", 677127738993279010 : "mercs"}
        self.__mercs_chan_id = 677127738993279010
        self.__mercs_ticket_id = 760498945209270362
        self.__public_strike_chan_id = 815530788761108480
        intents = discord.Intents.all()
        super(auraManagementClient, self).__init__(intents=intents)

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
                    embed_message = discord.Embed(title="Demande de boost", color=0x9acd32)#7FFF00#9ACD32
                    embed_message.add_field(name="Bienvenue :wave:", value="Salut! Tu as une question ou cherches des boosters?\nRéagis avec 🇫🇷\n \u200b", inline = False)
                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
                    tmp = await booking_channel.send(embed=embed_message)
                    await tmp.add_reaction("🇫🇷")

            elif message.content.lower() == "request_mercs":
                user_id = message.author.id
                if user_id == self.__day_id:
                    booking_channel = discord.utils.get(self.__guild.channels, id=self.__mercs_ticket_id, type=discord.ChannelType.text)
                    embed_message = discord.Embed(title="Support ticket", description="Hey! Tu as une question ou tu cherches une information que tu ne trouves pas dans le discord? Réagis avec :mailbox:. ", color=0x9acd32)#7FFF00#9ACD32
                    embed_message.add_field(name="Pas de  DM", value="S'il vous plait, veuillez toujours préférer ouvrir un ticket plutôt que d'envoyer un message privé.", inline = False)
                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
                    tmp = await booking_channel.send(embed=embed_message)
                    await tmp.add_reaction("📫")

        ############################## Strike $$ #############################
        ############################## price list #############################
        elif message.channel.name == "private-bot-commands" and message.content.startswith("!price"):
            if message.content.startswith("!pricepve"):
                id = message.content.split("!pricepve",1)[1]
                pc = priceSheet()
                return_dict = pc.price_sheet("pve", id)
            if message.content.startswith("!pricepvp"):
                id = message.content.split("!pricepvp",1)[1]
                pc = priceSheet()
                return_dict = pc.price_sheet("pvp", id)
            if message.content.startswith("!pricelegacy"):
                id = message.content.split("!pricelegacy",1)[1]
                pc = priceSheet()
                return_dict = pc.price_sheet("legacy", id)
            if len(return_dict) == 0 or return_dict[0] == "error" or return_dict[0] == "break":
                    embed_error = discord.Embed(title="Oops" ,color=0x61b3f2)#7FFF0
                    embed_error.add_field(name="Error", value = "That didn't work. No data were found")
                    embed_error.set_footer(text="Gino's Mercenaries")
            else:
                price_channel = discord.utils.get(self.__guild.channels, id=return_dict[0], type=discord.ChannelType.text)
                mercs_channel = discord.utils.get(self.__guild.channels, id= self.__mercs_chan_id, type=discord.ChannelType.text)
                embed_message = discord.Embed(title=return_dict[2], description=return_dict[3], color=0x9acd32)#7FFF00#9ACD32
                for field in return_dict[4]:
                    embed_message.add_field(name=field["name"], value=field["value"], inline = True)
                    embed_message.add_field(name="\u200b", value="\u200b", inline = True)
                    if "price" in field:
                        embed_message.add_field(name="Price", value=field["price"], inline = True)
                    else:
                        embed_message.add_field(name="\u200b", value="\u200b", inline = True)
                embed_message.set_footer(text="Gino's Mercenaries")
                try:
                    await price_channel.send(file=discord.File('images/{}'.format(return_dict[1])))
                except:
                    pass
                await price_channel.send(embed=embed_message)
                await mercs_channel.send(embed=embed_message)
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
            if len(self.giveaway_list) > 0 and channel.id == self.giveaway_list[0].channel_id:
                for ga in self.giveaway_list:
                    if message.id == ga.message.id:
                        if emoji == "🔧":
                            await user.create_dm()
                            await user.dm_channel.send(ga.message.id)
                            await message.remove_reaction(emoji, user)
                        if emoji == "🎉":
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
            if channel.id == self.__mercs_ticket_id and user.id != self.__bot_id:
                mod_role = discord.utils.get(self.__guild.roles, name='Moderateurs')
                category = discord.utils.get(self.__guild.categories, name='📢aura squad')
                overwrites = {
                    self.__guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    mod_role : discord.PermissionOverwrite(read_messages=True),
                    user: discord.PermissionOverwrite(read_messages=True)
                }
                chan_name = "ticket-{}".format(self.booking_id)
                chan_created = await self.__guild.create_text_channel(chan_name, category=category, position = 0, overwrites=overwrites)
                embed_eng = discord.Embed(title="Hello!", color=0x9acd32)#7FFF00#9ACD32
                embed_eng.add_field(name="How to close this ticket?", value="Simply react to this message with {}.".format(self.allowed_emo), inline = False)
                embed_eng.set_footer(text="Gino's Mercenaries")
                tmp_message = await chan_created.send(embed = embed_eng)
                await tmp_message.add_reaction(self.allowed_emo)
                await chan_created.send("Hello {}!\nJ'ai crée ce ticket avec les membres du staff. Comment peut-on t'aider?".format(user.mention))
                self.booking_id += 1
                await message.remove_reaction(emoji,user)
            if channel.id == self.__booking_chan_id and user.id != self.__bot_id:
                trusted_role = discord.utils.get(self.__guild.roles, name='Advertiser')
                category = discord.utils.get(self.__guild.categories, name='🌌aura community')
                overwrites = {
                    self.__guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    trusted_role : discord.PermissionOverwrite(read_messages=True),
                    user: discord.PermissionOverwrite(read_messages=True)
                }
                chan_name = "Booking-{}".format(self.booking_id)
                chan_created = await self.__guild.create_text_channel(chan_name, category=category, position = 0, overwrites=overwrites)
                if emoji.name == "🇫🇷":
                    trusted_role = discord.utils.get(self.__guild.roles, name='Advertiser')
                    embed_fr = discord.Embed(title="Bienvenue 🇫🇷", color=0x9acd32)#7FFF00#9ACD32
                    embed_fr.add_field(name="Comment clore ce ticket?", value="Appuie simplement sur {}.".format(self.allowed_emo), inline = False)
                    embed_fr.set_footer(text="Gino's Mercenaries")
                    tmp_message = await chan_created.send(embed = embed_fr)
                    await tmp_message.add_reaction(self.allowed_emo)
                    await chan_created.send("Hello {}!\nJ'ai crée ce channel avec nos {}. Comment peut-on t'aider?".format(user.mention, trusted_role.mention))
                self.booking_id += 1
                await message.remove_reaction(emoji,user)
            if channel.name.startswith("booking") and user.id != self.__bot_id:
                if emoji == self.allowed_emo and len(message.embeds)> 0:
                    trusted_role = discord.utils.get(self.__guild.roles, name='Advertiser')
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
            if channel.name.startswith("ticket") and user.id != self.__bot_id:
                if emoji == self.allowed_emo and len(message.embeds)> 0:
                    mod_role = discord.utils.get(self.__guild.roles, name='Moderateurs')
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
