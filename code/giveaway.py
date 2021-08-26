import random
import discord
from utils import *

class giveaway:
    def __init__(self, role, prize, end_date, channel_id, nb_winners = 1):
        self.role = role
        self.participants = {}
        self.nb_winners = int(nb_winners)
        self.prize = prize
        self.end_date = end_date
        self.message = ""
        self.channel_id = channel_id

    def create_participants_list(self, guild):
        all_members = guild.members
        for i in range(len(all_members)):
            roles_str = [o.name for o in all_members[i].roles]
            if self.role in roles_str:
                self.participants[all_members[i]] = 1

    def get_participants_list(self):
        return list(self.participants.keys())

    def get_participants_str(self):
        participants_str = ""
        for member in self.participants:
            participants_str += "{} ".format(member.mention)
            if self.participants[member] > 1:
                participants_str += "x{}".format(self.participants[member])
            participants_str += "\n"
        return participants_str

    def add_participant(self, member):
        if member in self.participants:
            self.participants[member] += 1
        else:
            self.participants[member] = 1

    def select_winners(self):
        players = []
        for member in self.participants:
            for i in range(self.participants[member]):
                players.append(member)
        return random.sample(players, self.nb_winners)

    def giveaway_embed(self):
        embed_message = discord.Embed(title="🎉Nitro Giveaway! 🎉", color=0x9acd32)#7FFF00#9ACD32
        embed_message.add_field(name="Participant:", value=self.get_participants_str(), inline = False)
        embed_message.add_field(name="Prize:", value="{}".format(self.prize), inline = False)
        embed_message.add_field(name="Number of winners:", value="{}".format(self.nb_winners), inline = True)
        embed_message.add_field(name="End date:", value="{}".format(self.end_date), inline = True)
        embed_message.set_footer(text="Gino's Mercenaries")
        return embed_message
