from random import randint
import discord
from utils import *

class betOb:
    def __init__(self, players, gold, nb_public):
        self.players = players
        self.confirmed_players = [self.players[0]]
        self.nb_players = len(players)
        self.places = self.nb_players - 1
        self.nb_public_gambler = nb_public
        self.gold = gold
        self.pot = gold * self.nb_players
        self.winning_gold = 0
        self.author = self.players[0]
        self.message_annoucement = ""
        self.tag_message = ""
        self.winner = ""
        self.losers = []
        self.rolls = []
        self.round = 1
        self.user_turn = ""
        self.roll_history = ""
        self.last_roll = self.pot
        self.loosing_gold = 0
        self.over = False

    def get_post_embed(self):
        embed_title = ""
        if self.nb_public_gambler == 0:
            embed_title = "{}k private bet!".format(int(self.pot/1000))
        else:
            embed_title = "{}k public bet!".format(int(self.pot/1000))
        gambler_str = ""
        status_str = ""
        for i in range(self.nb_players):
            if isinstance(self.players[i], str):
                if self.players[i] == "anyone":
                    gambler_str += "Open spot. React to join!\n"
                    status_str += ":yellow_circle:\n"
            elif self.players[i] in self.confirmed_players:
                status_str += ":green_circle:\n"
                gambler_str += "{} - Ready to roll!\n".format(self.players[i].mention)
            else:
                status_str += ":orange_circle:\n"
                gambler_str += "{} - Unconfirmed yet!\n".format(self.players[i].mention)

        embed_message = discord.Embed(title=embed_title, description="{} created a new bet! :moneybag:".format(self.author.mention), color=0x9acd32)#7FFF00#9ACD32
        embed_message.add_field(name="Entry fee:", value="{}k".format(int(self.gold/1000)), inline = True)
        embed_message.add_field(name="Total pot:", value="{}k".format(int(self.pot/1000)), inline = True)
        embed_message.add_field(name="\u200b", value="\u200b", inline = True)
        embed_message.add_field(name="Status:", value=status_str, inline = True)
        embed_message.add_field(name="Gamblers:", value=gambler_str, inline = True)
        embed_message.add_field(name="\u200b", value="\u200b", inline = True)
        embed_message.set_footer(text="Gino's Mercenaries")
        return embed_message

    def tags(self):
        tag_str = ""
        for i in range(self.nb_players):
            if isinstance(self.players[i], str):
                continue
            else:
                tag_str += "{} ".format(self.players[i].mention)
        return tag_str

    def cancel(self, user, message):
        embed_message = discord.Embed(title="Bet canceled", description= "{} {}".format(user.mention, message),color=0xdc143c)#7FFF00
        embed_message.set_footer(text="Gino's Mercenaries")
        return embed_message

    def roll_deathroll(self):
        self.winning_gold = int(0.95* self.pot)
        over = False
        if self.nb_public_gambler == 0:
            embed_title = "{}k private bet!".format(int(self.pot/1000))
        else:
            embed_title = "{}k public bet!".format(int(self.pot/1000))

        self.last_roll = randint(1, self.last_roll)
        if self.last_roll == 1:
            over = True
            self.over = True

        if self.round % 2 == 0:
            self.user_turn = self.players[1].display_name
            self.roll_history += "{} rolled {} :game_die:\n".format(self.user_turn, self.last_roll)
            if over is True:
                self.winner = self.players[0]
                self.losers = self.players
        else:
            self.user_turn = self.players[0].display_name
            self.roll_history += "**Round {}**\n{} rolled {} :game_die:\n".format(int(self.round/2)+1,self.user_turn, self.last_roll)
            if over is True:
                self.winner = self.players[1]
                self.losers = self.players
        self.round += 1
        if over is True:
            embed_message = discord.Embed(title=embed_title, description="{} won the bet! :tada:".format(self.winner.mention), color=0x9acd32)#7FFF00#9ACD32
        else:
            embed_message = discord.Embed(title=embed_title, color=0x9acd32)#7FFF00#9ACD32
        embed_message.add_field(name="Entry fee:", value="{}k".format(int(self.gold/1000)), inline = True)
        embed_message.add_field(name="Total pot:", value="{}k".format(int(self.pot/1000)), inline = True)
        embed_message.add_field(name="Rounds:", value=self.roll_history, inline = False)
        if over is False:
            if self.round % 2 == 0:
                embed_message.add_field(name="Turn:", value="It's {}'s turn".format(self.players[1].mention), inline = False)
            else:
                embed_message.add_field(name="Turn:", value="It's {}'s turn".format(self.players[0].mention), inline = False)
        embed_message.set_footer(text="Gino's Mercenaries")
        return [over, embed_message]

    def roll_regular(self):
        embed_title = ""
        if self.nb_public_gambler == 0:
            embed_title = "{}k private bet!".format(int(self.pot/1000))
        else:
            embed_title = "{}k public bet!".format(int(self.pot/1000))
        gambler_str = ""
        roll_str = ""
        winner_iter = -1
        max_roll = -1

        roll1 = randint(1,self.pot)
        roll2 = randint(1,self.pot)
        while roll2 == roll1:
            roll2 = randint(1,bet.gold)
        roll_str = "{} :game_die:\n{} :game_die:".format(roll1, roll2)
        if roll1 > roll2:
            winner_iter = 0
            gold_diff = roll1 - roll2
        else:
            winner_iter = 1
            gold_diff = roll2 - roll1
        self.winning_gold = int(gold_diff * 0.95)
        self.loosing_gold = gold_diff

        for i in range(self.nb_players):
            gambler_str += "{}\n".format(self.players[i].mention)

        for i in range(self.nb_players):
            if i == winner_iter:
                self.winner = self.players[i]
            else:
                self.losers.append(self.players[i])


        embed_message = discord.Embed(title=embed_title, description="{} won the bet! :tada:".format(self.winner.mention), color=0x9acd32)#7FFF00#9ACD32
        embed_message.add_field(name="Entry fee:", value="{}k".format(int(self.gold/1000)), inline = True)
        embed_message.add_field(name="Total pot:", value="{}k".format(int(self.pot/1000)), inline = True)
        embed_message.add_field(name="\u200b", value="\u200b", inline = True)
        embed_message.add_field(name="Rolls:", value=roll_str, inline = True)
        embed_message.add_field(name="Gamblers:", value=gambler_str, inline = True)
        embed_message.add_field(name="\u200b", value="\u200b", inline = True)
        embed_message.set_footer(text="Gino's Mercenaries")
        return embed_message

    def roll_hardcore(self):
        self.winning_gold = int(0.95 * self.pot)
        embed_title = ""
        if self.nb_public_gambler == 0:
            embed_title = "{}k private bet!".format(int(self.pot/1000))
        else:
            embed_title = "{}k public bet!".format(int(self.pot/1000))
        gambler_str = ""
        roll_str = ""
        winner_iter = -1
        max_roll = -1
        for i in range(self.nb_players):
            current_roll = randint(1,100)
            while current_roll in self.rolls:
                current_roll = randint(1,100)
            if current_roll > max_roll:
                max_roll = current_roll
                winner_iter = i
            self.rolls.insert(0, current_roll)
            gambler_str += "{}\n".format(self.players[i].mention)
            roll_str += "{} :game_die: \n".format(current_roll)

        for i in range(self.nb_players):
            if i == winner_iter:
                self.winner = self.players[i]
            self.losers.append(self.players[i])


        embed_message = discord.Embed(title=embed_title, description="{} won the bet! :tada:".format(self.winner.mention), color=0x9acd32)#7FFF00#9ACD32
        embed_message.add_field(name="Entry fee:", value="{}k".format(int(self.gold/1000)), inline = True)
        embed_message.add_field(name="Total pot:", value="{}k".format(int(self.pot/1000)), inline = True)
        embed_message.add_field(name="\u200b", value="\u200b", inline = True)
        embed_message.add_field(name="Rolls:", value=roll_str, inline = True)
        embed_message.add_field(name="Gamblers:", value=gambler_str, inline = True)
        embed_message.add_field(name="\u200b", value="\u200b", inline = True)
        embed_message.set_footer(text="Gino's Mercenaries")
        return embed_message
