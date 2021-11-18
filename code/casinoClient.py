from datetime import datetime
import random
import discord
import os
import asyncio
from sheet import *
from utils import *
from bet import *

class casinoClient(discord.Client):
    ###########################################################################
    #                                       Init                              #
    ###########################################################################
    def __init__(self, guild_name):
        self.guild_name = guild_name
        self.__list_admin_roles = ["EN - Manager", "Developer"]
        self.__bets = []
        self.__dr_bet = []
        self.__me_win = False
        self.__day_id = 302188753206771714
        self.testy = False
        self.lottery_message = ""
        self.lottery_pot = 0
        self.lottery_1st = 0
        self.lottery_2nd = 0
        self.lottery_3rd = 0
        self.lottery_winners = []
        self.lottery_ticket = 0
        self.lottery_entries = 0
        self.lottery_default_ticket = 30000
        self.lottery_time_remaining =  0
        self.lottery_players = []
        self.lottery_state = "close"
        self.next_run = datetime.now() + timedelta(minutes= 1 )
        if self.testy == False:
            # Gino
            self.__bot_id = 725313938895667210
            self.__bet_chan_list_id = [709019009106051104, 709019069206233199, 709019109257642014]
            self.__lottery_id = 886705583556821003
        else:
            # Jmone
            self.__bot_id = 686307367343751317
            self.__bet_chan_list_id = [708975742242914314, 706436097504182292, 708975772072935424]
        intents = discord.Intents.all()
        super(casinoClient, self).__init__(intents=intents)

    ###########################################################################
    #                              On ready function                          #
    ###########################################################################
    async def on_ready(self):
        self.__guild = discord.utils.get(self.guilds, name=self.guild_name)
        #me = discord.utils.get(self.__guild.members, id=self.__day_id)
        #await me.create_dm()

        self.allowed_emo = discord.utils.get(self.__guild.emojis, name ="allowed")
        self.denied_emo = discord.utils.get(self.__guild.emojis, name ="denied")
        self.chip_emo = discord.utils.get(self.__guild.emojis, name="chip")
        self.coin_emo = discord.utils.get(self.__guild.emojis, name="gold_coin")
        print("ready")
        await self.timer()

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
             # Ping
            elif message.content.lower() == "close_lottery":
                user_id = message.author.id
                if user_id == self.__day_id:
                    str_time_remaining = "Finish"
                    self.lottery_winners = self.draw_winner()
                    lottery_embed = await self.lottery_embed(str_time_remaining, winning_state=True)
                    await self.lottery_message.edit(embed = lottery_embed)
                    await self.lottery_message.clear_reactions()
                    help_chan = discord.utils.get(self.__guild.channels, id=794724553661480960, type=discord.ChannelType.text)
                    winner_1 = self.lottery_winners[0].mention if self.lottery_winners[0] != "No winner." else self.lottery_winners[0]
                    winner_2 = self.lottery_winners[1].mention if self.lottery_winners[1] != "No winner." else ''
                    winner_3 = self.lottery_winners[2].mention if self.lottery_winners[2] != "No winner." else ''
                    await self.lottery_message.channel.send(f"{winner_1} {winner_2} {winner_3} Congratulations :tada:. Please open a ticket in {help_chan.mention} to claim your gold.\nThank you all for playing !")
                    self.finish_lottery()
                    await message.channel.send("Done. :smile:")

            # love Dench
            elif message.content.lower() == "loveDench":
                user_id = message.author.id
                if user_id == self.__day_id:
                    chan_cas = discord.utils.get(self.__guild.channels, id=709019109257642014, type=discord.ChannelType.text)
                    await chan_cas.send("I love you Dench")
            # casino cheat
            elif message.content.lower() == "win":
                user_id = message.author.id
                if user_id == self.__day_id:
                    if self.__me_win == True:
                        self.__me_win = False
                    else:
                        self.__me_win = True
            # Last Webhook
            elif message.content.lower() == "last_webhook":
                user_id = message.author.id
                if user_id == self.__day_id:
                    await message.channel.send("Last Webhook:\n{}".format(self.__last_webhook))
            # List status
            elif message.content.lower() == "list_status":
                user_id = message.author.id
                if user_id == self.__day_id:
                    await message.channel.send("Here is the bet list:\n{}\n{}".format(self.__bets, self.__dr_bet))

            # Casgino set up
            elif message.content.lower() == "casgino set up":

                user_id = message.author.id
                if user_id == self.__day_id:
                    # TAGS
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

        # rename reloading
        elif message.channel.name == "private-bot-commands" and message.content.startswith("!rename"):
            reload_dict()
            await message.add_reaction(self.allowed_emo)
        
        elif message.channel.name == "private-bot-commands" and message.content.startswith("!close_lottery"):
            if self.lottery_state == "close":
                await message.channel.send("There is no lottery ongoing")
            else:
                str_time_remaining = "Finish"
                self.lottery_winners = self.draw_winner()
                lottery_embed = await self.lottery_embed(str_time_remaining, winning_state=True)
                await self.lottery_message.edit(embed = lottery_embed)
                await self.lottery_message.clear_reactions()
                help_chan = discord.utils.get(self.__guild.channels, id=794724553661480960, type=discord.ChannelType.text)
                winner_1 = self.lottery_winners[0].mention if self.lottery_winners[0] != "No winner." else self.lottery_winners[0]
                winner_2 = self.lottery_winners[1].mention if self.lottery_winners[1] != "No winner." else ""
                winner_3 = self.lottery_winners[2].mention if self.lottery_winners[2] != "No winner." else ""
                await self.lottery_message.channel.send(f"{winner_1} {winner_2} {winner_3} Congratulations !!!! :tada:. Please open a ticket in {help_chan.mention} to claim your gold !\nThank you all for playing")
                self.finish_lottery()
                await message.channel.send("Done. Please wait 60 seconds before starting a new lottery.")
        # lottery
        elif message.channel.name == "private-bot-commands" and message.content.startswith("!lottery"):
            if self.lottery_state == "open":
                await message.channel.send("There is already a lottery ongoing. Please start by closing it using the command: ```!close_lottery```")
            else:
                self.lottery_ticket = self.lottery_default_ticket
                try:
                    val = message.content.split(" ")
                    gold = val[1]
                    gold = int(gold)
                    self.lottery_ticket = gold
                except:
                    pass
                self.lottery_state = "open"
                sr = sheetReader()
                self.lottery_time_remaining = sr.close_lottery_date() - datetime.now() 
                str_time_remaining = pretty_time_remaining(self.lottery_time_remaining.total_seconds())
                lottery_chan = discord.utils.get(self.__guild.channels, id=self.__lottery_id, type=discord.ChannelType.text)
                self.lottery_pot = self.lottery_ticket
                self.lottery_entries = 0
                self.lottery_1st, self.lottery_2nd, self.lottery_3rd = define_lottery_pot(self.lottery_pot)
                
                lottery_embed = await self.lottery_embed(str_time_remaining)
                self.lottery_message = await lottery_chan.send(embed= lottery_embed)
                await self.lottery_message.add_reaction(self.chip_emo)
                await message.add_reaction(self.allowed_emo)
                self.next_run = datetime.now() + timedelta(minutes= 1 )
                await self.timer()

        ############################## Casgino $$ #############################
        elif message.channel.id in self.__bet_chan_list_id and message.content.startswith("!bet "):
            try:
                tmp_message = await message.channel.send("Creating bet...")
                casgino_info_chan = discord.utils.get(self.__guild.channels, name='casgino-bot-information', type=discord.ChannelType.text)
                message_split = message.content.split()
                user_role = [o.name for o in message.author.roles]
                sr = sheetReader()
                error = ""
                if sr.close_bet_date() is False:
                    error = "betclose"
                elif "Casino Ban" in user_role:
                    error = "Casban"
                else:
                    if len(message_split) < 3:
                        error = "missinfo"
                    if RepresentsInt(message_split[1]):
                        gold = int(message_split[1])
                        if gold < 1000:
                            error = "notenoughgold"
                        if gold > 50000 and "Casino Restricted" in user_role:
                            error = "casrest"
                        name = message.author.display_name
                        user_name_serv = parseName(name)
                        balance_gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                        balance_gold = str(balance_gold)
                        if balance_gold == "Nbalance":
                            error = "Nbalance"
                        else:
                            balance_gold = balance_gold.replace(",", "")
                            balance_gold = int(balance_gold)
                            if balance_gold < gold:
                                error = "nogoldbalance"
                    else:
                        error = "gold"
                    # only keep ppl tag in message_split
                    message_split = message_split[2:]
                    players = []
                    if message.channel.name == "casino-hardcore":
                        available_place = 4
                    else:
                        available_place = 1
                    for gambler in message_split:
                        if available_place == 0:
                            break
                        if gambler.startswith("<"):
                            gambler = gambler[3:]
                            gambler = gambler[:-1]
                            if RepresentsInt(gambler):
                                gambler_member = discord.utils.get(self.__guild.members, id=int(gambler))
                                if gambler_member:
                                    if gambler_member == message.author or gambler_member in players:
                                        error = "twicegambler"
                                    else:
                                        players.append(gambler_member)
                                        available_place -= 1
                            else:
                                error = "tag"
                        else:
                            error = "tag"
                    if players == [] and error == "":
                        error = "missinfo"
                try:
                    await tmp_message.delete()
                except:
                    pass
                if error == "":
                    players.insert(0, message.author)
                    bet = betOb(players, gold, 0)
                    embed_bet = bet.get_post_embed()
                    bet.message_annoucement = await message.channel.send(embed=embed_bet)
                    await bet.message_annoucement.add_reaction(self.chip_emo)
                    await bet.message_annoucement.add_reaction(self.denied_emo)
                    self.__bets.append(bet)
                    tag_str = bet.tags()
                    tag_str += " let's roll!"
                    bet.tag_message = await message.channel.send(tag_str)#tag

                elif error == "missinfo":
                    embed_message = discord.Embed(title="Missing information", description="Please refer to {} to check how to create bets! :moneybag:".format(casgino_info_chan.mention), color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "betclose":
                    embed_message = discord.Embed(title="The casino is currently closed", description="The casino closes 3 dayys before the end of the cycle to help make sure everybody gets their gold!\nSee you next cycle :moneybag:", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "Nbalance":
                    embed_message = discord.Embed(title="Not in balance", description="It seems that you are not in the balance. Please add yourself and make some gold before gambling here!", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "nogoldbalance":
                    embed_message = discord.Embed(title="Not enough in balance", description="You bet for more than you currently own", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "twicegambler":
                    embed_message = discord.Embed(title="Double gambler", description="You tagged the same person twice!", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "notenoughgold":
                    embed_message = discord.Embed(title="Not enough gold", description="You can only bet more than 1k.", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "gold":
                    embed_message = discord.Embed(title="Gold must be a number", description="Gold must be a number. Please use integer format (100000 instead of 100k)! :moneybag:", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "Casban":
                    embed_message = discord.Embed(title="Casino Ban", description="You can not create bets while being casino ban!", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "casrest":
                    embed_message = discord.Embed(title="Casino Restricted", description="You can not bet more then 50k while being casino Restricted.", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "tag":
                    embed_message = discord.Embed(title="Incorrect gambler", description="Couldn't find the gambler(s) you included. Please tag people you want to bet with or use the key word *anyone1*", color=0xdc143c)#7FFF00
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

        elif message.channel.id in self.__bet_chan_list_id  and message.channel.name == "casino-hardcore" and message.content.startswith("!betanyone "):
            try:
                tmp_message = await message.channel.send("Creating bet...")
                casgino_info_chan = discord.utils.get(self.__guild.channels, name='casgino-bot-information', type=discord.ChannelType.text)
                hardcore_chan = discord.utils.get(self.__guild.channels, name='casino-hardcore', type=discord.ChannelType.text)
                gambler_role = discord.utils.get(self.__guild.roles, name = "Gambler")
                message_split = message.content.split()
                user_role = [o.name for o in message.author.roles]
                error = ""
                sr = sheetReader()
                if message.channel.name != "casino-hardcore":
                    error = "multibet"
                elif "Casino Ban" in user_role:
                    error = "Casban"
                elif sr.close_bet_date() is False:
                    error = "betclose"
                else:
                    if len(message_split) < 3:
                        error = "missinfo"
                    else:
                        if RepresentsInt(message_split[1]):
                            gold = int(message_split[1])
                            if gold < 1000:
                                error = "notenoughgold"
                            if gold > 50000 and "Casino Restricted" in user_role:
                                error = "casrest"
                            name = message.author.display_name
                            user_name_serv = parseName(name)
                            balance_gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                            balance_gold = str(balance_gold)
                            if balance_gold == "Nbalance":
                                error = "Nbalance"
                            else:
                                balance_gold = balance_gold.replace(",", "")
                                balance_gold = int(balance_gold)
                                if balance_gold < gold:
                                    error = "nogoldbalance"
                        else:
                            error = "gold"
                        # only keep ppl tag in message_split
                        players = []
                        if RepresentsInt(message_split[2]):
                            nb_public = int(message_split[2])
                            nb_public = min(4, nb_public)
                            for i in range(nb_public):
                                players.append("anyone")
                        else:
                            error = "missinfo"
                        if players == [] and error == "":
                            error = "missinfo"
                try:
                    await tmp_message.delete()
                except:
                    pass
                if error == "":
                    players.insert(0, message.author)
                    bet = betOb(players, gold, nb_public)
                    embed_bet = bet.get_post_embed()
                    bet.message_annoucement = await message.channel.send(embed=embed_bet)
                    await bet.message_annoucement.add_reaction(self.chip_emo)
                    await bet.message_annoucement.add_reaction(self.denied_emo)
                    self.__bets.append(bet)
                    tag_str = "{}".format(gambler_role.mention)
                    tag_str += " let's roll!"
                    bet.tag_message = await message.channel.send(tag_str)#tag

                elif error == "missinfo":
                    embed_message = discord.Embed(title="Missing information", description="Please refer to {} to check how to create bets! :moneybag:".format(casgino_info_chan.mention), color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "casrest":
                    embed_message = discord.Embed(title="Casino Restricted", description="You can not bet more then 50k while being casino Restricted.", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "betclose":
                    embed_message = discord.Embed(title="The casino is currently closed", description="The casino closes 3 dayys before the end of the cycle to help making sure everybody gets his gold!\nSee you next cycle :moneybag:", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "multibet":
                    embed_message = discord.Embed(title="No multi-bet", description="**!betanyone** is only allowed for the hardcore bets in {}".format(hardcore_chan.mention), color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "Nbalance":
                    embed_message = discord.Embed(title="Not in balance", description="It seems that you are not in the balance. Please add yourself and make some gold before gambling here!", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "nogoldbalance":
                    embed_message = discord.Embed(title="Not enough in balance", description="You bet for more than you currently own", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "twicegambler":
                    embed_message = discord.Embed(title="Double gambler", description="You tagged the same person twice!", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "notenoughgold":
                    embed_message = discord.Embed(title="Not enough gold", description="You can only bet more than 1k.", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "gold":
                    embed_message = discord.Embed(title="Gold must be a number", description="Gold must be a number. Please use integer format (100000 instead of 100k)! :moneybag:", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "Casban":
                    embed_message = discord.Embed(title="Casino Ban", description="You can not create bets while being casino ban!", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "tag":
                    embed_message = discord.Embed(title="Incorrect gambler", description="Couldn't find the gambler(s) you included. Please tag people you want to bet with or use the key word *anyone1*", color=0xdc143c)#7FFF00
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

        elif message.channel.id in self.__bet_chan_list_id  and message.channel.name == "casino-deathroll" and message.content.startswith("!betanyone "):
            try:
                tmp_message = await message.channel.send("Creating bet...")
                casgino_info_chan = discord.utils.get(self.__guild.channels, name='casgino-bot-information', type=discord.ChannelType.text)
                hardcore_chan = discord.utils.get(self.__guild.channels, name='casino-hardcore', type=discord.ChannelType.text)
                gambler_role = discord.utils.get(self.__guild.roles, name = "Gambler")
                message_split = message.content.split()
                user_role = [o.name for o in message.author.roles]
                error = ""
                sr = sheetReader()
                if "Casino Ban" in user_role:
                    error = "Casban"
                elif sr.close_bet_date() is False:
                    error = "betclose"
                else:
                    if len(message_split) < 3:
                        error = "missinfo"
                    else:
                        if RepresentsInt(message_split[1]):
                            gold = int(message_split[1])
                            if gold < 1000:
                                error = "notenoughgold"
                            if gold > 50000 and "Casino Restricted" in user_role:
                                error = "casrest"
                            name = message.author.display_name
                            user_name_serv = parseName(name)
                            balance_gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                            balance_gold = str(balance_gold)
                            if balance_gold == "Nbalance":
                                error = "Nbalance"
                            else:
                                balance_gold = balance_gold.replace(",", "")
                                balance_gold = int(balance_gold)
                                if balance_gold < gold:
                                    error = "nogoldbalance"
                        else:
                            error = "gold"
                        # only keep ppl tag in message_split
                        players = []
                        if RepresentsInt(message_split[2]):
                            nb_public = int(message_split[2])
                            nb_public = min(4, nb_public)
                            for i in range(nb_public):
                                players.append("anyone")
                        else:
                            error = "missinfo"
                        if players == [] and error == "":
                            error = "missinfo"
                try:
                    await tmp_message.delete()
                except:
                    pass
                if error == "":
                    players.insert(0, message.author)
                    bet = betOb(players, gold, nb_public)
                    embed_bet = bet.get_post_embed()
                    bet.message_annoucement = await message.channel.send(embed=embed_bet)
                    await bet.message_annoucement.add_reaction(self.chip_emo)
                    await bet.message_annoucement.add_reaction(self.denied_emo)
                    self.__bets.append(bet)
                    tag_str = "{}".format(gambler_role.mention)
                    tag_str += " let's roll!"
                    bet.tag_message = await message.channel.send(tag_str)#tag

                elif error == "missinfo":
                    embed_message = discord.Embed(title="Missing information", description="Please refer to {} to check how to create bets! :moneybag:".format(casgino_info_chan.mention), color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "onlyone":
                    embed_message = discord.Embed(title="Deathroll is 1v1", description="Deathroll can only be played 1v1, please une !betanyone xxx 1", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "casrest":
                    embed_message = discord.Embed(title="Casino Restricted", description="You can not bet more then 50k while being casino Restricted.", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "betclose":
                    embed_message = discord.Embed(title="The casino is currently closed", description="The casino closes 3 dayys before the end of the cycle to help making sure everybody gets his gold!\nSee you next cycle :moneybag:", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "multibet":
                    embed_message = discord.Embed(title="No multi-bet", description="**!betanyone** is only allowed for the hardcore bets in {}".format(hardcore_chan.mention), color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "Nbalance":
                    embed_message = discord.Embed(title="Not in balance", description="It seems that you are not in the balance. Please add yourself and make some gold before gambling here!", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "nogoldbalance":
                    embed_message = discord.Embed(title="Not enough in balance", description="You bet for more than you currently own", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "twicegambler":
                    embed_message = discord.Embed(title="Double gambler", description="You tagged the same person twice!", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "notenoughgold":
                    embed_message = discord.Embed(title="Not enough gold", description="You can only bet more than 1k.", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "gold":
                    embed_message = discord.Embed(title="Gold must be a number", description="Gold must be a number. Please use integer format (100000 instead of 100k)! :moneybag:", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "Casban":
                    embed_message = discord.Embed(title="Casino Ban", description="You can not create bets while being casino ban!", color=0xdc143c)#7FFF00
                    embed_message.set_footer(text="Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                elif error == "tag":
                    embed_message = discord.Embed(title="Incorrect gambler", description="Couldn't find the gambler(s) you included. Please tag people you want to bet with or use the key word *anyone1*", color=0xdc143c)#7FFF00
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

    ###########################################################################
    #                              On reaction add                            #
    ###########################################################################
    async def on_raw_reaction_add(self, payload):
        try:
            channel = discord.utils.get(self.__guild.channels, id=payload.channel_id, type=discord.ChannelType.text)
            message = await channel.fetch_message(payload.message_id)
            user = discord.utils.get(self.__guild.members, id=payload.user_id)
            user_role = [o.name for o in user.roles]
            emoji = payload.emoji
            if emoji.is_unicode_emoji():
                emoji = str(emoji)
            if len(self.__bets)>10:
                self.__bets.pop(0)
            if len(self.__dr_bet)>10:
                self.__dr_bet.pop(0)
            if user.id != self.__bot_id:
                # Bet
                if message.channel.id in self.__bet_chan_list_id:
                    iter = 0
                    for bet in self.__dr_bet:
                        if bet.message_annoucement.id == message.id and bet.over == False:
                            if user in bet.players:
                                sr = sheetReader()
                                if emoji == self.chip_emo:
                                    if "Casino Restricted" in user_role and bet.gold > 50000:
                                        await user.create_dm()
                                        embed_message = discord.Embed(title="Casino Restricted", color=0xdc143c)#7FFF00
                                        embed_message = discord.Embed(title="Casino Restricted", description="You can not bet more then 50k while being casino Restricted.", color=0xdc143c)#7FFF00
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                        await user.dm_channel.send(embed=embed_message)
                                        await message.remove_reaction(emoji,user)
                                        break
                                    if "Casino Ban" in user_role:
                                        await user.create_dm()
                                        embed_message = discord.Embed(title="Casino ban", color=0xdc143c)#7FFF00
                                        embed_message.add_field(name="\u200b", value="You can't join bet while being casino ban!", inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                        await user.dm_channel.send(embed=embed_message)
                                        await message.remove_reaction(emoji,user)
                                        break
                                    if (bet.round % 2 == 0 and user == bet.players[1]) or (bet.round % 2 == 1 and user == bet.players[0]):
                                        if emoji == self.chip_emo:
                                            ans = bet.roll_deathroll()
                                            over = ans[0]
                                            embed = ans[1]
                                            await message.remove_reaction(emoji,user)
                                            await bet.message_annoucement.edit(embed = embed)
                                            if over is True:
                                                await bet.message_annoucement.clear_reactions()
                                                await channel.send(":tada: Congratulations {} :tada: You won {}! :moneybag:".format(bet.winner.mention, bet.winning_gold))
                                                sr.roll(bet.winner, bet.losers, bet.winning_gold, bet.gold)
                                                self.__dr_bet.pop(iter)
                                    else:
                                        await message.remove_reaction(emoji,user)

                                if emoji == self.denied_emo:
                                    self.__dr_bet.pop(iter)
                                    emebed_edit = bet.cancel(user, "canceled the bet. Its entry fee will still be taken.")
                                    await bet.message_annoucement.edit(embed = emebed_edit)
                                    bet.losers = [user]
                                    sr.roll("", bet.losers, 0, bet.gold)
                                    try:
                                        await bet.tag_message.delete()
                                    except:
                                        pass
                                    await bet.message_annoucement.clear_reactions()
                                    break

                            else:
                                if emoji == self.chip_emo:
                                    if "Casino Restricted" in user_role and bet.gold > 50000:
                                        await user.create_dm()
                                        embed_message = discord.Embed(title="Casino Restricted", color=0xdc143c)#7FFF00
                                        embed_message = discord.Embed(title="Casino Restricted", description="You can not bet more then 50k while being casino Restricted.", color=0xdc143c)#7FFF00
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                        await user.dm_channel.send(embed=embed_message)
                                        await message.remove_reaction(emoji,user)
                                        break
                                    if "Casino Ban" in user_role:
                                        await user.create_dm()
                                        embed_message = discord.Embed(title="Casino ban", color=0xdc143c)#7FFF00
                                        embed_message.add_field(name="\u200b", value="You can't join bet while being casino ban!", inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                        await user.dm_channel.send(embed=embed_message)
                                        await message.remove_reaction(emoji,user)
                                        break
                                    sr = sheetReader()
                                    if user not in bet.confirmed_players:
                                        if bet.nb_public_gambler > 0:
                                            name = user.display_name
                                            user_name_serv = parseName(name)
                                            balance_gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                            if balance_gold == "Nbalance":
                                                await message.remove_reaction(emoji,user)
                                                break
                                            else:
                                                balance_gold = balance_gold.replace(",", "")
                                                balance_gold = int(balance_gold)
                                                if balance_gold < bet.gold:
                                                    await message.remove_reaction(emoji,user)
                                                    break
                                                else:
                                                    for q in range(len(bet.players)):
                                                        if isinstance(bet.players[q], str):
                                                            if bet.players[q] == "anyone":
                                                                bet.players.pop(q)
                                                                bet.players.insert(q, user)
                                                                break
                                                    bet.confirmed_players.append(user)
                                                    em = bet.get_post_embed()
                                                    await bet.message_annoucement.edit(embed = em)
                                                    bet.places -= 1
                                        else:
                                            await message.remove_reaction(emoji,user)
                                        if bet.places == 0:
                                            try:
                                                await bet.tag_message.delete()
                                            except:
                                                pass
                                            ans = bet.roll_deathroll()
                                            over = ans[0]
                                            embed = ans[1]
                                            await message.remove_reaction(emoji,user)
                                            await bet.message_annoucement.edit(embed = embed)
                                            if over is True:
                                                await bet.message_annoucement.clear_reactions()
                                                await channel.send(":tada: Congratulations {} :tada: You won {}! :moneybag:".format(bet.winner.mention, bet.winning_gold))
                                                sr.roll(bet.winner, bet.losers, bet.winning_gold, bet.gold)
                                                self.__dr_bet.pop(iter)
                        iter += 1
                    iter = 0
                    for bet in self.__bets:
                        if bet.message_annoucement.id == message.id:
                            if emoji == self.chip_emo:
                                if "Casino Restricted" in user_role and bet.gold > 50000:
                                    await user.create_dm()
                                    embed_message = discord.Embed(title="Casino Restricted", color=0xdc143c)#7FFF00
                                    embed_message = discord.Embed(title="Casino Restricted", description="You can not bet more then 50k while being casino Restricted.", color=0xdc143c)#7FFF00
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await user.dm_channel.send(embed=embed_message)
                                    await message.remove_reaction(emoji,user)
                                    break
                                if "Casino Ban" in user_role:
                                    await user.create_dm()
                                    embed_message = discord.Embed(title="Casino ban", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value="You can't join bet while being casino ban!", inline=False)
                                    embed_message.set_footer(text="Gino's Mercenaries")
                                    await user.dm_channel.send(embed=embed_message)
                                    await message.remove_reaction(emoji,user)
                                    break
                                sr = sheetReader()
                                if user not in bet.confirmed_players:
                                    if user in bet.players:
                                        ####
                                        name = user.display_name
                                        user_name_serv = parseName(name)
                                        balance_gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                        balance_gold = str(balance_gold)
                                        if balance_gold == "Nbalance":
                                            self.__bets.pop(iter)
                                            emebed_edit = bet.cancel(user, "is currently not in the balance.")
                                            await bet.message_annoucement.edit(embed = emebed_edit)
                                            await bet.message_annoucement.clear_reactions()
                                            try:
                                                await bet.tag_message.delete()
                                            except:
                                                pass
                                            break
                                        else:
                                            balance_gold = balance_gold.replace(",", "")
                                            balance_gold = int(balance_gold)
                                            if balance_gold < bet.gold:
                                                self.__bets.pop(iter)
                                                emebed_edit = bet.cancel(user, "doesn't have enough gold in its balance currently.")
                                                await bet.message_annoucement.edit(embed = emebed_edit)
                                                await bet.message_annoucement.clear_reactions()
                                                try:
                                                    await bet.tag_message.delete()
                                                except:
                                                    pass
                                                break
                                            elif "Casino Restricted" in user_role and bet.gold > 50000:
                                                await user.create_dm()
                                                embed_message = discord.Embed(title="Casino Restricted", color=0xdc143c)#7FFF00
                                                embed_message = discord.Embed(title="Casino Restricted", description="You can not bet more then 50k while being casino Restricted.", color=0xdc143c)#7FFF00
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                                await user.dm_channel.send(embed=embed_message)
                                                await message.remove_reaction(emoji,user)
                                                break
                                            else:
                                                bet.confirmed_players.append(user)
                                                em = bet.get_post_embed()
                                                await bet.message_annoucement.edit(embed = em)
                                                bet.places -= 1

                                    elif bet.nb_public_gambler > 0:
                                        name = user.display_name
                                        user_name_serv = parseName(name)
                                        balance_gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                        if balance_gold == "Nbalance":
                                            await message.remove_reaction(emoji,user)
                                            break
                                        else:
                                            balance_gold = balance_gold.replace(",", "")
                                            balance_gold = int(balance_gold)
                                            if balance_gold < bet.gold:
                                                await message.remove_reaction(emoji,user)
                                                break
                                            else:
                                                for q in range(len(bet.players)):
                                                    if isinstance(bet.players[q], str):
                                                        if bet.players[q] == "anyone":
                                                            bet.players.pop(q)
                                                            bet.players.insert(q, user)
                                                            break
                                                bet.confirmed_players.append(user)
                                                em = bet.get_post_embed()
                                                await bet.message_annoucement.edit(embed = em)
                                                bet.places -= 1
                                    else:
                                        await message.remove_reaction(emoji,user)
                                    if bet.places == 0:
                                        try:
                                            await bet.tag_message.delete()
                                        except:
                                            pass
                                        if channel.name == "casino-hardcore":
                                            roll_result = bet.roll_hardcore()
                                            await bet.message_annoucement.clear_reactions()
                                            await bet.message_annoucement.edit(embed = roll_result)
                                            await channel.send(":tada: Congratulations {} :tada: You won {}! :moneybag:".format(bet.winner.mention, bet.winning_gold))
                                            sr.roll(bet.winner, bet.losers, bet.winning_gold, bet.gold)
                                        elif channel.name == "casino-regular":
                                            roll_result = bet.roll_regular()
                                            await bet.message_annoucement.clear_reactions()
                                            await bet.message_annoucement.edit(embed = roll_result)
                                            await channel.send(":tada: Congratulations {} :tada: You won {}! :moneybag:".format(bet.winner.mention, bet.winning_gold))
                                            sr.roll(bet.winner, bet.losers, bet.winning_gold, bet.loosing_gold)
                                        else:
                                            roll_results = bet.roll_deathroll()
                                            over = roll_results[0]
                                            roll_result = roll_results[1]
                                            if over is True:
                                                await bet.message_annoucement.clear_reactions()
                                                await channel.send(":tada: Congratulations {} :tada: You won {}! :moneybag:".format(bet.winner.mention, bet.winning_gold))
                                                sr.roll(bet.winner, bet.losers, bet.winning_gold, bet.gold)
                                            else:
                                                await bet.message_annoucement.edit(embed = roll_result)
                                                await message.remove_reaction(emoji,user)
                                                self.__dr_bet.append(bet)
                                        self.__bets.pop(iter)
                                else:
                                    await message.remove_reaction(emoji,user)
                            if emoji == self.denied_emo:
                                if bet.nb_public_gambler > 0:
                                    if user == bet.author:
                                        self.__bets.pop(iter)
                                        emebed_edit = bet.cancel(user, "canceled the bet.")
                                        await bet.message_annoucement.edit(embed = emebed_edit)
                                        try:
                                            await bet.tag_message.delete()
                                        except:
                                            pass
                                        await bet.message_annoucement.clear_reactions()
                                        break
                                    else:
                                        if user in bet.players:
                                            for j in range(len(bet.players)):
                                                if bet.players[j] == user:
                                                    bet.players[j] = "anyone"
                                            for j in range(len(bet.confirmed_players)):
                                                if bet.confirmed_players[j] == user:
                                                    bet.confirmed_players.pop(j)
                                            bet.places += 1
                                            emebed_edit = bet.get_post_embed()
                                            await bet.message_annoucement.edit(embed = emebed_edit)
                                            await message.remove_reaction(emoji,user)
                                        else:
                                            await message.remove_reaction(emoji,user)

                                else:
                                    if user in bet.players:
                                        self.__bets.pop(iter)
                                        emebed_edit = bet.cancel(user, "canceled the bet.")
                                        await bet.message_annoucement.edit(embed = emebed_edit)
                                        try:
                                            await bet.tag_message.delete()
                                        except:
                                            pass
                                        await bet.message_annoucement.clear_reactions()
                                        break

                                    else:
                                        await message.remove_reaction(emoji,user)


                        iter += 1
        
                if message.channel.id == self.__lottery_id and emoji == self.chip_emo and message.id == self.lottery_message.id:
                    str_time_remaining = pretty_time_remaining(self.lottery_time_remaining.total_seconds())
                    lottery_embed = await self.lottery_embed(str_time_remaining, working=True)
                    await self.lottery_message.edit(embed = lottery_embed) 
                    sr = sheetReader()
                    # Checking gold
                    name = user.display_name
                    user_name_serv = parseName(name)
                    balance_gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                    if balance_gold == "Nbalance":
                        await message.remove_reaction(emoji,user)
                        await user.create_dm()
                        embed_message = discord.Embed(title="Not enough in balance", description="You don't have enough gold in your balance to join the lottery.", color=0xdc143c)#7FFF00
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await user.dm_channel.send(embed=embed_message)
                    else:
                        balance_gold = balance_gold.replace(",", "")
                        balance_gold = int(balance_gold)
                        if balance_gold < self.lottery_ticket:
                            await message.remove_reaction(emoji,user)
                            await user.create_dm()
                            embed_message = discord.Embed(title="Not enough in balance", description="You don't have enough gold in your balance to join the lottery.", color=0xdc143c)#7FFF00
                            embed_message.set_footer(text="Gino's Mercenaries")
                            await user.dm_channel.send(embed=embed_message)
                        else:
                            sr.add_gold(user_name_serv[0],user_name_serv[1], self.lottery_ticket * -1)
                            # All good, gold has been deducted
                            ## Updating lotery variable
                            self.lottery_pot += self.lottery_ticket
                            self.lottery_entries += 1
                            self.lottery_1st, self.lottery_2nd, self.lottery_3rd = define_lottery_pot(self.lottery_pot)
                            self.lottery_time_remaining = sr.close_lottery_date() - datetime.now() 
                            str_time_remaining = pretty_time_remaining(self.lottery_time_remaining.total_seconds())
                            self.lottery_players.append(user)
                            
                            ## Updating embed
                            lottery_embed = await self.lottery_embed(str_time_remaining)
                            await self.lottery_message.edit(embed = lottery_embed) 
                            await message.remove_reaction(emoji,user)

                            # End message user
                            balance_gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                            await user.create_dm()
                            embed_message = discord.Embed(title="Good luck!", description=f"Thank you for playing in our lottery.\n Make sure to check {channel.mention} in {str_time_remaining}. You can enter the lottery again if you wish to increase your chance!", color=0x00b967)#7FFF00
                            embed_message.add_field(name="Your balance", value = f"You currently have {balance_gold} gold remaining in your balance.")
                            embed_message.set_footer(text="Gino's Mercenaries")
                            await user.dm_channel.send(embed=embed_message)
        except:
            err = traceback.format_exc()
            embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
            embed_error.add_field(name="Error", value = err)
            embed_error.set_footer(text="Gino's Mercenaries")
            day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
            await day_member.create_dm()
            await day_member.dm_channel.send(embed=embed_error)

    ###########################################################################
    #                           Class Specific functions                      #
    ###########################################################################
    # lottery embed

    async def lottery_embed(self, str_time_remaining, winning_state = False, working = False):
        if winning_state:
            lottery_em = discord.Embed(title="Gino {} Lottery - Finished".format(datetime.now().strftime("%B")), description="Congratulations to our winners :tada:".format(self.lottery_1st, self.coin_emo, self.chip_emo), color=0x00b967 )
        else:
            lottery_em = discord.Embed(title="Gino {} Lottery".format(datetime.now().strftime("%B")), description="Up to {:,} {} to win! Join by reacting with {}.".format(self.lottery_1st, self.coin_emo, self.chip_emo), color=0x00b967 )
        lottery_em.add_field(name="Entries:", value="{:,} {}".format(self.lottery_entries, self.chip_emo), inline = True)
        lottery_em.add_field(name="Ticket price:", value="{:,} {}".format(self.lottery_ticket, self.coin_emo), inline = True)
        lottery_em.add_field(name="\u200b", value="\u200b", inline = True)
        if winning_state:
            winner_1 = self.lottery_winners[0].display_name if self.lottery_winners[0] != "No winner." else self.lottery_winners[0]
            winner_2 = self.lottery_winners[1].display_name if self.lottery_winners[1] != "No winner." else self.lottery_winners[1]
            winner_3 = self.lottery_winners[2].display_name if self.lottery_winners[2] != "No winner." else self.lottery_winners[2]
            lottery_em.add_field(name="Prizes:", value=":first_place: {0:,} {1} - {4} \n :second_place: {2:,} {1} - {5}\n:third_place: {3:,} {1} - {6}".format(self.lottery_1st, self.coin_emo, self.lottery_2nd, self.lottery_3rd, winner_1, winner_2, winner_3), inline = False)
        else:
            lottery_em.add_field(name="Prizes:", value=":first_place: {0:,} {1} \n :second_place: {2:,} {1}\n:third_place: {3:,} {1}".format(self.lottery_1st, self.coin_emo, self.lottery_2nd, self.lottery_3rd), inline = False)
        lottery_em.add_field(name="Time remaining", value=str_time_remaining)
        if working:
            lottery_em.add_field(name="Adding new entry", value="Working :gear:")
        lottery_em.set_footer(text="Gino's Mercenaries - To receive the gold on a specific realm, an extra 5% of your win will be ask.")
        return lottery_em
    
    def draw_winner(self):
        if len(self.lottery_players) >= 3:
            return random.sample(self.lottery_players, 3)  
        else:
            winners = random.sample(self.lottery_players, len(self.lottery_players))
            while len(winners) < 3:
                winners.append("No winner.")
            return winners

    async def update_lottery(self):
        sr = sheetReader()
        self.lottery_time_remaining = sr.close_lottery_date() - datetime.now() 
        print(self.lottery_time_remaining.total_seconds())
        print(pretty_time_remaining(self.lottery_time_remaining.total_seconds()))
        if self.lottery_time_remaining.total_seconds() > 0:
            str_time_remaining = pretty_time_remaining(self.lottery_time_remaining.total_seconds())
            ## Updating embed
            lottery_embed = await self.lottery_embed(str_time_remaining)
            await self.lottery_message.edit(embed = lottery_embed)
        else:
            str_time_remaining = "Finish"
            self.lottery_winners = self.draw_winner()
            lottery_embed = await self.lottery_embed(str_time_remaining, winning_state=True)
            await self.lottery_message.edit(embed = lottery_embed)
            await self.lottery_message.clear_reactions()
            help_chan = discord.utils.get(self.__guild.channels, id=794724553661480960, type=discord.ChannelType.text)
            winner_1 = self.lottery_winners[0].mention if self.lottery_winners[0] != "No winner." else self.lottery_winners[0]
            winner_2 = self.lottery_winners[1].mention if self.lottery_winners[1] != "No winner." else ''
            winner_3 = self.lottery_winners[2].mention if self.lottery_winners[2] != "No winner." else ''
            await self.lottery_message.channel.send(f"{winner_1} {winner_2} {winner_3} Congratulations :tada:. Please open a ticket in {help_chan.mention} to claim your gold. \nThank you all for playing!")
            self.finish_lottery()


    def finish_lottery(self):
        self.lottery_message = ""
        self.lottery_pot = 0
        self.lottery_1st = 0
        self.lottery_2nd = 0
        self.lottery_3rd = 0
        self.lottery_winners = []
        self.lottery_ticket = 0
        self.lottery_entries = 0
        self.lottery_default_ticket = 30000
        self.lottery_time_remaining =  0
        self.lottery_players = []
        self.lottery_state = "close"

    async def timer(self, do_it_now = False):
        if self.lottery_state == "close":
            print("Finishing timer()")
            return
        elif do_it_now == False:
            delta_t = self.next_run - datetime.now()
            sec2wait = delta_t.seconds
            if sec2wait >= 0:
                await asyncio.sleep(sec2wait)
            print("done")  
        if self.lottery_state == "close":
            print("Finishing timer()")
            return


        #str_time_remaining = pretty_time_remaining(self.lottery_time_remaining.total_seconds())
        await self.update_lottery()
        self.next_run = self.next_run + timedelta(minutes=1)
        await self.timer()