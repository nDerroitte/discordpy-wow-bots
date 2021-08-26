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

class AuraClient(discord.Client):
    ###########################################################################
    #                                       Init                              #
    ###########################################################################
    def __init__(self, guild_name):
        self.guild_name = guild_name
        self.__list_admin_roles = ["EN - Manager", "Developer"]
        self.__list_bot_roles = ["Bot"]
        self.__list_modo_roles = ["General Management", "Dev", "Moderateurs"]
        self.__day_id = 302188753206771714
        self.testy = False
        self.to_update_members = []
        self.__boost_being_fill = []
        self.__boost_being_done = []
        self.__boost_being_collected = []
        self.__last_webhook = []
        self.__raids = []
        self.__collecting_gold_id = 815619802449575986
        self.__bot_id = 815659991079583766
        self.__horde_mm = 778867428134223883
        self.__apply_chan_list_id = [778869689841221662]
        ### no use yet
        self.__pvp = 778867691095457833

        self.__apply_adv_chan_list_id = 629129518623227914
        self.__boost_annoucement_list_id = [778867428134223883, 778867691095457833]

        intents = discord.Intents.all()
        super(AuraClient, self).__init__(intents=intents)

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
        self.coin_emo = discord.utils.get(self.__guild.emojis, name="gold_coin")
        self.mercs_emo = discord.utils.get(self.__guild.emojis, name="mercs")
        self.armor_emo = discord.utils.get(self.__guild.emojis, name="armor")
        self.bronze_key_emo = discord.utils.get(self.__guild.emojis, name="bronze_key")
        self.silver_key_emo = discord.utils.get(self.__guild.emojis, name="silver_key")
        self.gold_key_emo = discord.utils.get(self.__guild.emojis, name="gold_key")
        self.nb_emo = discord.utils.get(self.__guild.emojis, name="tallycounter")
        self.heal_emo = discord.utils.get(self.__guild.emojis, name ="heal")
        self.tank_emo = discord.utils.get(self.__guild.emojis, name ="tank")
        self.dps_emo = discord.utils.get(self.__guild.emojis, name ="dps")

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

            if message.content.lower() == "reload":
                user_id = message.author.id
                if user_id == self.__day_id:
                    reload_dict()
                    await message.channel.send("Reload. :smile:")

            if message.content.lower() == "changement_role":
                all_members = self.__guild.members#list(self.get_all_members())
                member_to_add = []
                for member in all_members:
                    roles_str = [y.name.lower() for y in member.roles]
                    print(roles_str)
                    if "aura squad" in roles_str and "m+ horde" not in roles_str:
                        member_to_add.append(member)
                count = 0
                print(len(member_to_add))
                for member in member_to_add:

                    try:
                        name = member.display_name
                        user_name_serv = parseName(name)
                        roles = member.roles
                        roles_str = [y.name.lower() for y in roles]
                        roles_added = []
                        nickname = name
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
                            roles_added.append("M+ Horde")
                            fact = discord.utils.get(self.__guild.roles, name='M+ Horde')
                            await member.add_roles(fact)
                            if rio_tank > 950 or rio_heal > 950 or rio_dps > 950:
                                if wow_class.lower() not in roles_str:
                                    roles_added.append(wow_class)
                                    wow_class_rank = discord.utils.get(self.__guild.roles, name=wow_class)
                                    await member.add_roles(wow_class_rank)
                                if faction == "alliance" and "m+ alliance" not in roles_str:
                                    roles_added.append("M+ Alliance")
                                    fact = discord.utils.get(self.__guild.roles, name='M+ Alliance')
                                    await member.add_roles(fact)
                                elif faction == "horde" and "m+ horde" not in roles_str:
                                    roles_added.append("M+ Horde")
                                    fact = discord.utils.get(self.__guild.roles, name='M+ Horde')
                                    await member.add_roles(fact)
                                if data["class"] in ["Rogue", "Monk", "Demon Hunter","Druid"] and "Leather" not in roles_str:
                                    roles_added.append("Leather")
                                    Leather = discord.utils.get(self.__guild.roles, name='Leather')
                                    await member.add_roles(Leather)
                                if data["class"] in ["Paladin", "Warrior", "Death Knight"] and "Plate" not in roles_str:
                                    roles_added.append("Plate")
                                    Plate = discord.utils.get(self.__guild.roles, name='Plate')
                                    await member.add_roles(Plate)
                                if data["class"] in ["Hunter", "Shaman"] and "Mail" not in roles_str:
                                    roles_added.append("Mail")
                                    Mail = discord.utils.get(self.__guild.roles, name='Mail')
                                    await member.add_roles(Mail)
                                if data["class"] in ["Priest", "Mage", "Warlock"] and "Cloth" not in roles_str:
                                    roles_added.append("Cloth")
                                    Cloth = discord.utils.get(self.__guild.roles, name='Cloth')
                                    await member.add_roles(Cloth)
                                if rio_heal > 950 and "healer prospect" not in roles_str:
                                    roles_added.append("Healer Prospect")
                                    healer_prospect = discord.utils.get(self.__guild.roles, name='Healer Prospect')
                                    await member.add_roles(healer_prospect)
                                if rio_tank > 950 and "tank prospect" not in roles_str:
                                    roles_added.append("Tank Prospect")
                                    tank_prospect = discord.utils.get(self.__guild.roles, name='Tank Prospect')
                                    await member.add_roles(tank_prospect)
                                if rio_dps > 950 and "dps prospect" not in roles_str:
                                    roles_added.append("DPS Prospect")
                                    dps_prospect = discord.utils.get(self.__guild.roles, name='DPS Prospect')
                                    await member.add_roles(dps_prospect)
                            if rio_tank > 1300 or rio_heal > 1300 or rio_dps > 1300:
                                if "m+ prestige" not in roles_str:
                                    roles_added.append("M+ Prestige")
                                    m_prestige = discord.utils.get(self.__guild.roles, name='M+ Prestige')
                                    await member.add_roles(m_prestige)
                                if rio_heal > 1300 and "healer prestige" not in roles_str:
                                    healer_prestige = discord.utils.get(self.__guild.roles, name='Healer Prestige')
                                    await member.add_roles(healer_prestige)
                                if rio_tank > 1300 and "tank prestige" not in roles_str:
                                    roles_added.append("Tank Prestige")
                                    tank_prestige = discord.utils.get(self.__guild.roles, name='Tank Prestige')
                                    await member.add_roles(tank_prestige)
                                if rio_dps > 1300 and "dps prestige" not in roles_str:
                                    roles_added.append("DPS Prestige")
                                    dps_prestige = discord.utils.get(self.__guild.roles, name='DPS Prestige')
                                    await member.add_roles(dps_prestige)
                            if rio_tank > 1600 or rio_heal > 1600 or rio_dps > 1600:
                                if "m+ allstars" not in roles_str:
                                    roles_added.append("M+ AllStars")
                                    m_all_star = discord.utils.get(self.__guild.roles, name='M+ AllStars')
                                    await member.add_roles(m_all_star)
                                if rio_heal > 1600 and "healer all star" not in roles_str:
                                    roles_added.append("Healer All Star")
                                    healer_all_star = discord.utils.get(self.__guild.roles, name='Healer All Star')
                                    await member.add_roles(healer_all_star)
                                if rio_tank > 1600 and "tank all star" not in roles_str:
                                    roles_added.append("Tank All Star")
                                    tank_all_star = discord.utils.get(self.__guild.roles, name='Tank All Star')
                                    await member.add_roles(tank_all_star)
                                if rio_dps > 1600 and "dps all star" not in roles_str:
                                    roles_added.append("DPS All Star")
                                    dps_all_star = discord.utils.get(self.__guild.roles, name='DPS All Star')
                                    await member.add_roles(dps_all_star)
                    except:
                            err = traceback.format_exc()
                            embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
                            embed_error.add_field(name="Error", value = err)
                            embed_error.set_footer(text="Gino's Mercenaries")
                            day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
                            await day_member.create_dm()
                            await day_member.dm_channel.send(embed=embed_error)
                    count += 1
                    print(count)
                    if count % 100 == 0:
                        print("Sleeping 100 sec")
                        await asyncio.sleep(10)

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
                    embed_error.set_footer(text="Aura & Gino's Mercenaries")
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
                    information_role_channel = discord.utils.get(self.__guild.channels, name='information-roles', type=discord.ChannelType.text)
                    other_role_chan = discord.utils.get(self.__guild.channels, name='autres-roles', type=discord.ChannelType.text)
                    mm_roles_channel = discord.utils.get(self.__guild.channels, name='m-roles', type=discord.ChannelType.text)
                    embed_message = discord.Embed(title="Roles", color=0x61b3f2)#7FFF00
                    embed_message.add_field(name="Roles M+", value="Vous avez besoin de 950 de r.io pour le rôle de prospect booster (jusqu'aux +9), 1k2 pour le rôle de prestige booster (jusqu'aux +13) et 1k6 pour le rôle de allstar booster (14 et au-dessus).", inline=False)
                    embed_message.add_field(name="\u200b",value="Si vous souhaitez actualiser vos rôles, vous pouvez utiliser la commande !update nom-royaume dans {} (avec le nom de votre personnage à la place du nom et le nom du royaume à la place du royaume).\nCette commande fonctionne aussi pour obtenir les rôles sur vos rerolls.\n".format(mm_roles_channel.mention), inline=False)
                    embed_message.add_field(name="Changement de rôle ou de royaume", value="Si vous souhaitez changer votre nom de personnage ou faire une demande de rôle (Par exemple torghast runner), veuillez ouvrir une requête dans {}. ".format(other_role_chan.mention))
                    embed_message.add_field(name="Supprimer vos rôles", value="Si vous souhaitez supprimer vos rôles, veuillez ouvrir une requete dans {}. ".format(other_role_chan.mention))
                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
                    await information_role_channel.send(embed=embed_message)

        elif message.channel.name == "m-roles" and message.content.startswith("!update "):
            try:
                name = message.content.split(" ", 1)[1]
                user_name_serv = parseName(name)
                other_role_chan = discord.utils.get(self.__guild.channels, name='autres-roles', type=discord.ChannelType.text)
                if user_name_serv[0] == "" or user_name_serv[1] == "":
                    embed_message = discord.Embed(title="Oops", color=0xdc143c)#7FFF00
                    embed_message.add_field(name="\u200b", value="Le pseudo doit etre de la forme nom-serveur.", inline=False)
                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                else:
                    roles = message.author.roles
                    roles_str = [y.name.lower() for y in roles]
                    roles_added = []
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
                        if rio_tank > 950 or rio_heal > 950 or rio_dps > 950:
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
                            if rio_heal > 950 and "healer prospect" not in roles_str:
                                roles_added.append("Healer Prospect")
                                healer_prospect = discord.utils.get(self.__guild.roles, name='Healer Prospect')
                                await message.author.add_roles(healer_prospect)
                            if rio_tank > 950 and "tank prospect" not in roles_str:
                                roles_added.append("Tank Prospect")
                                tank_prospect = discord.utils.get(self.__guild.roles, name='Tank Prospect')
                                await message.author.add_roles(tank_prospect)
                            if rio_dps > 950 and "dps prospect" not in roles_str:
                                roles_added.append("DPS Prospect")
                                dps_prospect = discord.utils.get(self.__guild.roles, name='DPS Prospect')
                                await message.author.add_roles(dps_prospect)
                        if rio_tank > 1300 or rio_heal > 1300 or rio_dps > 1300:
                            if "m+ prestige" not in roles_str:
                                roles_added.append("M+ Prestige")
                                m_prestige = discord.utils.get(self.__guild.roles, name='M+ Prestige')
                                await message.author.add_roles(m_prestige)
                            if rio_heal > 1300 and "healer prestige" not in roles_str:
                                healer_prestige = discord.utils.get(self.__guild.roles, name='Healer Prestige')
                                await message.author.add_roles(healer_prestige)
                            if rio_tank > 1300 and "tank prestige" not in roles_str:
                                roles_added.append("Tank Prestige")
                                tank_prestige = discord.utils.get(self.__guild.roles, name='Tank Prestige')
                                await message.author.add_roles(tank_prestige)
                            if rio_dps > 1300 and "dps prestige" not in roles_str:
                                roles_added.append("DPS Prestige")
                                dps_prestige = discord.utils.get(self.__guild.roles, name='DPS Prestige')
                                await message.author.add_roles(dps_prestige)
                        if rio_tank > 1600 or rio_heal > 1600 or rio_dps > 1600:
                            if "m+ allstars" not in roles_str:
                                roles_added.append("M+ AllStars")
                                m_all_star = discord.utils.get(self.__guild.roles, name='M+ AllStars')
                                await message.author.add_roles(m_all_star)
                            if rio_heal > 1600 and "healer all star" not in roles_str:
                                roles_added.append("Healer All Star")
                                healer_all_star = discord.utils.get(self.__guild.roles, name='Healer All Star')
                                await message.author.add_roles(healer_all_star)
                            if rio_tank > 1600 and "tank all star" not in roles_str:
                                roles_added.append("Tank All Star")
                                tank_all_star = discord.utils.get(self.__guild.roles, name='Tank All Star')
                                await message.author.add_roles(tank_all_star)
                            if rio_dps > 1600 and "dps all star" not in roles_str:
                                roles_added.append("DPS All Star")
                                dps_all_star = discord.utils.get(self.__guild.roles, name='DPS All Star')
                                await message.author.add_roles(dps_all_star)

                        embed_message = discord.Embed(title="Roles updated", color=0xffd700)#7FFF00
                        if len(roles_added) > 0:
                            embed_message.add_field(name="\u200b", value = "Tu as été ajouté les roles suivants: {}.".format(', '.join(roles_added)), inline=False)
                        else:
                            embed_message.add_field(name="\u200b", value = "Pas de nouveaux roles ontété trouvés.")
                        embed_message.add_field(name="\u200b", value = "Si tu penses qu'un ou plusieurs rôles sont manquants, tu peux contacter un administrateur ou envoyer une demande dans {}.".format(other_role_chan.mention), inline=False)
                        embed_message.set_footer(text="Aura & Gino's Mercenaries")
                        await message.author.create_dm()
                        await message.author.dm_channel.send(embed=embed_message)
                        await message.channel.send("Je t'ai envoyé un DM {}.".format(message.author.mention))
                    else:
                        embed_message = discord.Embed(title="Oops", color=0xdc143c)#7FFF00
                        embed_message.add_field(name="\u200b", value="Impossible de trouver {} sur raider.io. Check ton nom et serveur pour être sur que ce soit correcte.\n".format(name), inline=False)
                        embed_message.set_footer(text="Aura & Gino's Mercenaries")
                        await message.channel.send(embed=embed_message)
            except:
                 err = traceback.format_exc()
                 embed_error = discord.Embed(title="New error detected!" ,color=0x61b3f2)#7FFF0
                 embed_error.add_field(name="Error", value = err)
                 embed_error.set_footer(text="Gino's Mercenaries")
                 day_member = discord.utils.get(self.__guild.members, id=self.__day_id)
                 await day_member.create_dm()
                 await day_member.dm_channel.send(embed=embed_error)

        elif message.channel.name == "check-balance" and message.content == "!b":
            user_id = message.author.id
            #adv = discord.utils.get(self.__guild.members, id=self.user_id)
            name = message.author.display_name
            user_name_serv = parseName(name)
            sr = sheetReader()
            gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
            await message.author.create_dm()
            await message.channel.send("Je t'ai envoyé ta balance en DM {}.".format(message.author.mention))
            embed_message = discord.Embed(title="Ta balance", color=0x32cd32)#7FFF00
            if gold == "Nbalance":
                embed_message.add_field(name="Pas dans la balance pour l'instant.", value = "{}".format(name), inline=True)
                embed_message.set_footer(text="Aura &Gino's Mercenaries")
                await message.author.dm_channel.send(embed=embed_message)
            else:
                embed_message.add_field(name="\u200b", value="Tu as pour l'instant {} golds.".format(gold))
                embed_message.set_footer(text="Aura @Gino's Mercenaries")
                await message.author.dm_channel.send(embed=embed_message)
        elif message.channel.name == "add-balance" and (message.content == "!addally" or message.content == "!addhorde"):
            ally_bool = True
            if message.content == "!addhorde":
                ally_bool = False
            name = message.author.display_name
            user_name_serv = parseName(name)
            if user_name_serv[0] == "" or user_name_serv[1] == "":
                embed_message = discord.Embed(title="Oops", color=0xdc143c)#7FFF00
                embed_message.add_field(name="\u200b", value="Your nickname must be in the form Name-Realm to be added to the balance.", inline=False)
                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                await message.channel.send(embed=embed_message)
            else:
                sr = sheetReader()
                ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                check_channel = discord.utils.get(self.__guild.channels, name='check-balance', type=discord.ChannelType.text)

                if ack == "ok":
                    embed_message = discord.Embed(title="Bienvenue!", color=0xffd700)#7FFF00
                    embed_message.add_field(name="\u200b", value = "{} a été ajouté à la balance. Tu peux maintenant regarder tes golds dans {}.".format(name, check_channel.mention), inline=False)
                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                if ack == "AlreadyIn":
                    embed_message = discord.Embed(title="Oops!", color=0xdc143c)#7FFF00
                    embed_message.add_field(name="\u200b", value = "{} est déjà dans la balance. Tu peux vérifier en regardant tes golds dans {}".format(name, check_channel.mention), inline=False)
                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)

        elif message.channel.name == "edit-boost" and message.content.startswith("!"):
            tmp1 = message.content.split(" ", 1)
            if len(tmp1) < 2:
                edit_boost_chan = discord.utils.get(self.__guild.channels, name='edit-boost-info', type=discord.ChannelType.text)
                embed_message = discord.Embed(title="Incorrect form", color=0xdc143c)#7FFF00
                embed_message.add_field(name="\u200b", value = "The command is not valid. Please refer to {} to edit boost.".format(edit_boost_chan.mention), inline=False)
                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                await message.channel.send(embed=embed_message)
            boost_id = tmp1[1].split("\n",1)[0]
            if not RepresentsInt(boost_id):
                form_channel = discord.utils.get(self.__guild.channels, name='post-boost-form', type=discord.ChannelType.text)
                embed_message = discord.Embed(title="Incorrect boost id", color=0xdc143c)#7FFF00
                embed_message.add_field(name="\u200b", value = "The boost id enter does not correspond to a valid number.\n ", inline=False)
                embed_message.set_footer(text="Aura & Gino's Mercenaries")
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
                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
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
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        elif good_id is False:
                            embed_message = discord.Embed(title="Couldn't find booster", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The booster's name entered doesn't not correspond to anyone in the Gino server.", inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
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
                                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
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
                                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
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
                                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                else:
                                    nb_dps_good = True
                                    if boost.dps_in[3] == "":
                                        boost.booster_place -= 1
                                    boost.dps_in[3] = booster
                            else:
                                embed_message = discord.Embed(title="Command not found", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The command you entered is unknown.", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            if nb_dps_good:
                                em = boost.post()
                                await boost.message_annoucement.edit(embed = em)
                                embed_message = discord.Embed(title="Boost edited", color=0x32cd32)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The boost was succesfully modified.")
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            else:
                                await message.channel.send(embed=embed_message)
                    if message.content.startswith("!replace"):
                        if boost.type != "mm":
                            embed_message = discord.Embed(title="Boost must be M+", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The replace command can only be used for the M+ boost.", inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        elif boost_type != "done":
                            embed_message = discord.Embed(title="Boost must be started", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The replace command can only be used for boost already started.", inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
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
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif nb_runs_field_nb is False:
                                embed_message = discord.Embed(title="Number of runs", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The number of runs must be an integer", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif nb_runs_done >= boost.nb_runs:
                                embed_message = discord.Embed(title="Incorrect number of runs", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The number of runs must be inferior of the total number of runs of the boost.", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif booster_id_field is False:
                                embed_message = discord.Embed(title="Missing booster name field", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "Couldn't find the booster name field in the edit message.", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            elif good_id is False:
                                embed_message = discord.Embed(title="Couldn't find booster", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The booster's name entered doesn't not correspond to anyone in the Gino server.", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
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
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                    if message.content.startswith("!edit"):
                        ack = fillBoost(boost, message.content.lower())
                        if ack == "not gold":
                            embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The gold should be a number.", inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        elif ack == "not nb booster":
                            embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The number of boosters should be a number.", inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        elif ack == "not nb run":
                            embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The number of runs should be a number.", inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        elif ack == "not booster":
                            embed_message = discord.Embed(title="Wrong discord name", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The booster's discord name you entered does not correspond to anyone on Gino.\n", inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        elif ack == "not nb key":
                            embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The key level should be a number.", inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        elif ack == "not armor stack":
                            embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The armor stack should be one of the following: Plate, Mail, Leather, Cloth.\nIf no armor stack are necessary, please just let the field empty.", inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        elif ack == "not faction":
                            embed_message = discord.Embed(title="Missing information", color=0xdc143c)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The faction should be one of the following: horde, alliance.", inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                        else:
                            boost.completeInfo()
                            em = boost.post()
                            boost.tags()
                            await boost.message_annoucement.edit(embed = em)
                            embed_message = discord.Embed(title="Boost edited", color=0x32cd32)#7FFF00
                            embed_message.add_field(name="\u200b", value = "The boost was succesfully modified.")
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                    if message.content.startswith("!remove"):
                        removed_booster = False
                        if message.content.startswith("!removetank"):
                            if boost.tank_in == "":
                                embed_message = discord.Embed(title="No tank in boost", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "There is currently no tank in the boost.", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            else:
                                boost.tank_in = ""
                                removed_booster = True
                        if message.content.startswith("!removeheal"):
                            if boost.heal_in == "":
                                embed_message = discord.Embed(title="No heal in boost", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "There is currently no heal in the boost.", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            else:
                                boost.heal_in = ""
                                removed_booster = True
                        if message.content.startswith("!removedps1"):
                            if boost.dps_in[0] == "":
                                embed_message = discord.Embed(title="No DPS in boost", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The first dps slot of the boost is not filled.", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            else:
                                boost.dps_in[0] = ""
                                removed_booster = True
                        if message.content.startswith("!removedps2"):
                            if boost.dps_in[1] == "":
                                embed_message = discord.Embed(title="No DPS in boost", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The second dps slot of the boost is not filled.", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            else:
                                boost.dps_in[1] = ""
                                removed_booster = True
                        if message.content.startswith("!removedps3"):
                            if boost.dps_in[2] == "":
                                embed_message = discord.Embed(title="No DPS in boost", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The 3rd dps slot of the boost is not filled.", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
                                await message.channel.send(embed=embed_message)
                            else:
                                boost.dps_in[2] = ""
                                removed_booster = True
                        if message.content.startswith("!removedps4"):
                            if boost.dps_in[3] == "":
                                embed_message = discord.Embed(title="No DPS in boost", color=0xdc143c)#7FFF00
                                embed_message.add_field(name="\u200b", value = "The 3rd dps slot of the boost is not filled.", inline=False)
                                embed_message.set_footer(text="Aura & Gino's Mercenaries")
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
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await message.channel.send(embed=embed_message)
                            if boost_type == "done":
                                await boost.message_annoucement.clear_reactions()
                                role_tag = discord.utils.get(self.__guild.roles, name = boost.role_tag[0])
                                if len(boost.role_tag) == 2:
                                    role_tag_2 = discord.utils.get(self.__guild.roles, name = boost.role_tag[1])
                                    boost.tag_message = await boost.message_annoucement.channel.send("{} {} Let's go!".format(role_tag.mention,role_tag_2.mention))
                                else:
                                    boost.tag_message = await boost.message_annoucement.channel.send("{} Let's go!".format(role_tag.mention))
                                if boost.type in ["mm", "mechagone"]:
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

        elif message.channel.name == "form" and message.author.id != self.__bot_id:
            if len(message.embeds)> 0:
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
                        embed_message.set_footer(text="Aura & Gino's Mercenaries")
                        await message.channel.send(embed=embed_message)
                # Utiliser un contains
                # Si Gino tout seul, mettre un alias
                if error == "adv":
                    embed_message = discord.Embed(title="Advertiser not found", color=0xdc143c)#7FFF00
                    embed_message.add_field(name="\u200b", value="The advertiser from the Google form ({}) can not be found.".format(adv_field.value), inline=False)
                    embed_message.set_footer(text="Aura & Gino's Mercenaries")
                    await message.channel.send(embed=embed_message)
                else:
                    unpost_channel = discord.utils.get(self.__guild.channels, name='boost-unposted', type=discord.ChannelType.text)
                    boost = boostOb(adv, unpost_channel, self.tank_emo, self.heal_emo, self.dps_emo, self.allowed_emo, self.denied_emo, self.coin_emo, self.mercs_emo, self.armor_emo, self.bronze_key_emo, self.silver_key_emo, self.gold_key_emo, self.nb_emo)
                    boost.faction = "horde"
                    for field in em.fields:
                        if field.name =="Type of boost:":
                            if field.value == "M+":
                                boost.type = "mm"
                            elif field.value == "Freehold":
                                boost.type = "leveling"
                            else:
                                boost.type = field.value.lower()
                        if field.name == "Boost description:":
                            boost.notes = field.value
                        if field.name == "Gold:":
                            boost.gold = int(field.value)
                        if field.name == "Gold faction:":
                            boost.gold_faction  = field.value
                        if field.name == "Collection Realm:":
                            boost.realm = main_connected_realm(field.value.lower())
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
                        if boost.type in ["torghast", "mm","mechagone","island","leveling"]:
                            if boost.faction == "alliance":
                                boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.__ally_mm)
                            elif boost.faction == "horde":
                                boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.__horde_mm)
                        if boost.type == "pvp":
                            boost.annoucement_chan = discord.utils.get(self.__guild.channels, id=self.__pvp)

                        roles = adv.roles
                        role_str = [y.name.lower() for y in roles]
                        new_adv = False
                        if "new advertiser" in role_str:
                            new_adv = True
                            if "alliance advertiser" in role_str or "horde advertiser" in role_str or "trusted advertiser" in role_str or "gold collector" in role_str:
                                new_adv = False
                        if new_adv:
                            # DM the new adv
                            gold_collecting_chan = discord.utils.get(self.__guild.channels, id=self.__collecting_gold_id)
                            embed_message = discord.Embed(title="Gold Collection", color=0x61b3f2, description="Thank you for your boost!\nAs you are a new advertiser, a Gold Collector will collect the gold before the boost is posted on discord.\nPlease check {} where you'll be able to see who you have to invite to collect the gold.".format(gold_collecting_chan.mention))#7FFF00
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            await adv.create_dm()
                            await adv.dm_channel.send(embed= embed_message)
                            # Post in collection (add message in boost)
                            embed_message = discord.Embed(title="Gold Collection: {} - {}".format(boost.realm.capitalize(), boost.faction.capitalize()), color=0x61b3f2)#7FFF00
                            embed_message.add_field(name="Advertiser", value = "{} - {}".format(boost.advertiser.mention, boost.advertiser.display_name))
                            embed_message.add_field(name="Character to whisp", value = boost.who_to_w, inline=False)
                            embed_message.add_field(name="Gold", value = "{}k".format(boost.gold/1000), inline=False)
                            embed_message.set_footer(text="Aura & Gino's Mercenaries")
                            boost.message_collecting = await gold_collecting_chan.send(embed = embed_message)
                            await boost.message_collecting.add_reaction(self.allowed_emo)
                            await boost.message_collecting.add_reaction(self.denied_emo)
                            gold_collector_role = discord.utils.get(self.__guild.roles, name='Gold Collector')
                            boost.tmp_collecting_msg = await gold_collecting_chan.send("{} Quelqu'un peut collecter les golds?\nPrevenez les autres si vous le faites pour eviter les doublons! \n Appuiyez {} seulement quand collecté svp!".format(gold_collector_role.mention, self.allowed_emo))
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
                            if boost.type in ["mm", "mechagone"]:
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
                        embed_message.set_footer(text="Aura & Gino's Mercenaries")
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
                        embed_message.set_footer(text="Aura & Gino's Mercenaries")
                        await message.channel.send(embed=embed_message)


    async def on_raw_reaction_add(self, payload):
        try:
            channel = discord.utils.get(self.__guild.channels, id=payload.channel_id, type=discord.ChannelType.text)
            message = await channel.fetch_message(payload.message_id)
            user = discord.utils.get(self.__guild.members, id=payload.user_id)
            emoji = payload.emoji
            if emoji.is_unicode_emoji():
                emoji = str(emoji)
            try:
                if len(self.__boost_being_collected) > 10:
                    self.__boost_being_collected.pop(0)
                if len(self.__boost_being_fill)>10:
                    self.__boost_being_fill.pop(0)
                if len(self.__boost_being_done)>100:
                    self.__boost_being_done.pop(0)
            except:
                pass
            if user.id != self.__bot_id:
                print("b")
                # Apply
                if message.channel.id in self.__apply_chan_list_id:
                    bool_modo = False
                    for role in user.roles:
                        if role.name in self.__list_modo_roles:
                            bool_modo = True
                    if bool_modo == True and emoji == self.allowed_emo:
                        if "apply" in channel.name:
                            print("a")
                            # GET NAME and rename:
                            name_realm = get_name_realm_aura(message.content)
                            print(name_realm)
                            user_name_realm = parseName(name_realm)
                            await message.author.edit(nick=name_realm.capitalize())
                            # roles
                            roles = message.author.roles
                            roles_str = [y.name.lower() for y in roles]
                            if "lueur" in roles_str:
                                customer_role = discord.utils.get(self.__guild.roles, name='Lueur')
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
                                if rio_tank > 950 or rio_heal > 950 or rio_dps > 950:
                                    wow_class_rank = discord.utils.get(self.__guild.roles, name=wow_class)
                                    await message.author.add_roles(wow_class_rank)
                                    if faction == "alliance":
                                        fact = discord.utils.get(self.__guild.roles, name='M+ Alliance')
                                        await message.author.add_roles(fact)
                                    elif faction == "horde":
                                        fact = discord.utils.get(self.__guild.roles, name='M+ Horde')
                                        await message.author.add_roles(fact)
                                    if data["class"] in ["Rogue", "Monk", "Demon Hunter","Druid"]:
                                        leather = discord.utils.get(self.__guild.roles, name='Leather')
                                        await message.author.add_roles(leather)
                                    if data["class"] in ["Paladin", "Warrior", "Death Knight"]:
                                        plate = discord.utils.get(self.__guild.roles, name='Plate')
                                        await message.author.add_roles(plate)
                                    if data["class"] in ["Hunter", "Shaman"]:
                                        mail = discord.utils.get(self.__guild.roles, name='Mail')
                                        await message.author.add_roles(mail)
                                    if data["class"] in ["Priest", "Mage", "Warlock"]:
                                        cloth = discord.utils.get(self.__guild.roles, name='Cloth')
                                        await message.author.add_roles(cloth)
                                    if rio_heal > 950:
                                        healer_prospect = discord.utils.get(self.__guild.roles, name='Healer Prospect')
                                        await message.author.add_roles(healer_prospect)
                                    if rio_tank > 950:
                                        tank_prospect = discord.utils.get(self.__guild.roles, name='Tank Prospect')
                                        await message.author.add_roles(tank_prospect)
                                    if rio_dps > 950:
                                        dps_prospect = discord.utils.get(self.__guild.roles, name='DPS Prospect')
                                        await message.author.add_roles(dps_prospect)
                                if rio_tank > 1300 or rio_heal > 1300 or rio_dps > 1300:
                                    m_prestige = discord.utils.get(self.__guild.roles, name='M+ Prestige')
                                    await message.author.add_roles(m_prestige)
                                    if rio_heal > 1300:
                                        healer_prestige = discord.utils.get(self.__guild.roles, name='Healer Prestige')
                                        await message.author.add_roles(healer_prestige)
                                    if rio_tank > 1300:
                                        tank_prestige = discord.utils.get(self.__guild.roles, name='Tank Prestige')
                                        await message.author.add_roles(tank_prestige)
                                    if rio_dps > 1300:
                                        dps_prestige = discord.utils.get(self.__guild.roles, name='DPS Prestige')
                                        await message.author.add_roles(dps_prestige)
                                if rio_tank > 1600 or rio_heal > 1600 or rio_dps > 1600:
                                    m_all_star = discord.utils.get(self.__guild.roles, name='M+ AllStars')
                                    await message.author.add_roles(m_all_star)
                                    if rio_heal > 1600:
                                        healer_all_star = discord.utils.get(self.__guild.roles, name='Healer All Star')
                                        await message.author.add_roles(healer_all_star)
                                    if rio_tank > 1600:
                                        tank_all_star = discord.utils.get(self.__guild.roles, name='Tank All Star')
                                        await message.author.add_roles(tank_all_star)
                                    if rio_dps > 1600:
                                        dps_all_star = discord.utils.get(self.__guild.roles, name='DPS All Star')
                                        await message.author.add_roles(dps_all_star)
                        # MESSAGE:
                        mm_roles_chan = discord.utils.get(self.__guild.channels, name='m-roles', type=discord.ChannelType.text)
                        other_role_chan = discord.utils.get(self.__guild.channels, name='autres-roles', type=discord.ChannelType.text)
                        add_balance_chan = discord.utils.get(self.__guild.channels, name='add-balance', type=discord.ChannelType.text)
                        check_balance_chan = discord.utils.get(self.__guild.channels, name='check-balance', type=discord.ChannelType.text)
                        embed_message = discord.Embed(title="Bienvenue!", color=0x61b3f2, description="Tu as été accepté comme booster dans notre communauté!")#7FFF00
                        embed_message.add_field(name="Vérification", value="Tu as été renommé sur le discord. Vérifie que le nom donné correspond bien a ton pseudo IG. Tu seras payé sur base de ce pseudo.\nNous t'avons également ajouté des rôles en fonction de ton raider.io. Pour d'autres roles, ou ajouter des alts, va sur {} pour les roles M+ et {} pour le reste.".format(mm_roles_chan.mention, other_role_chan.mention),inline=False)
                        embed_message.add_field(name="S'ajouter a la balance", value="La première chose à faire est s'encoder dans la balance. Pour ce faire, utilise **!addhorde** dans {}. **Il ne faut faire cela qu'une fois!**".format(add_balance_chan.mention), inline=False)
                        embed_message.add_field(name="Rejoinder un boost", value="Les boosts seront postés dans les channels d'annonces. Dans la plupart des cas, il suffit de réagir avec l'emoji de son role pour rejoinder ({} {} {}). **Si tu ne vois pas les emojis, c'est que tu es arrivé trop tard.**\nPour certains boosts (PVP par exemple), Il faudra peut-être MP l'advertiser. Cela sera précisé dans l'annonce.".format(self.dps_emo,self.tank_emo,self.heal_emo),inline=False)
                        embed_message.add_field(name="Recevoir mes golds", value="Ayant des boosters dans toutes l'Europe, nous payons nos mercenaires une fois toutes les 3-4 semaines. Plus d'infos seront données dans les annonces en fin de cycle.", inline=False)
                        embed_message.set_footer(text="Gino's Mercenaries")
                        await message.author.create_dm()
                        await message.author.dm_channel.send(embed= embed_message)
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
                                em = boost.post()
                                boost.message_annoucement = await boost.annoucement_chan.send(embed=em)
                                role_tag = discord.utils.get(self.__guild.roles, name = boost.role_tag[0])
                                if boost.no_ping == False:
                                    if len(boost.role_tag) == 2:
                                        role_tag_2 = discord.utils.get(self.__guild.roles, name = boost.role_tag[1])
                                        boost.tag_message = await boost.message_annoucement.channel.send("{} {} Let's go! Boost will open in 5s.".format(role_tag.mention,role_tag_2.mention))
                                    else:
                                        boost.tag_message = await boost.message_annoucement.channel.send("{} Let's go! Boost will open in 5s.".format(role_tag.mention))
                                await asyncio.sleep(5)
                                self.__boost_being_fill.append(boost)
                                if boost.type in ["mm", "mechagone"]:
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
                                    embed_message = discord.Embed(title="Boost annulé", color=0xdc143c)#7FFF00
                                    embed_message.add_field(name="\u200b", value = "Le boost a été annulé.", inline=False)
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
                                        print(boost.booster_place)
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
                                        em_adv.add_field(name="\u200b", value = "Ton boost est prêt! Les boosters vont /w ```{}```\nReact avec {} (si le boost s'est bien passé) ou {} pour le fermer.".format(boost.who_to_w, self.allowed_emo, self.denied_emo), inline=False)
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
                                        embed_message.add_field(name="\u200b", value = "Le boost dans lequel tu as tag est prêt! Envoie ceci à l'advertiser s'il te plait:\n ```/w {} inv```\nAussi, rejoins le channel discord suivant: [Boost #{}]({}).\nGood luck, have fun! :smile:".format(boost.who_to_w, discord_room, str(invite)), inline=False)
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
                                            embed_message_adv.add_field(name="Merci!", value = "Le boost a été ajouté à la balance!\nMerci d'advertise avec nous!", inline=False)
                                            if gold == "Nbalance":
                                                ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                            else:
                                                embed_message_adv.add_field(name="Ta balance", value = "Tu as maintenant {} gold!".format(gold), inline=True)
                                                if boost.no_adv_cut:
                                                    embed_message_adv.add_field(name="Ton cut", value = "Ton cut est 0. :moneybag:".format(int(boost.gold*0.85*0.03)), inline=True)
                                                elif boost.inhouse:
                                                    embed_message_adv.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.03)), inline=True)
                                                else:
                                                    if boost.gold_collector == "":
                                                        if boost.helper == "":
                                                            if boost.type != "leveling" and boost.type != "pvp":
                                                                embed_message_adv.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
                                                            else:
                                                                embed_message_adv.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.15)), inline=True)
                                                        else:
                                                            embed_message_adv.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.15)), inline=True)
                                                    else:
                                                        embed_message_adv.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.15)), inline=True)
                                            embed_message_adv.set_footer(text="Gino's Mercenaries")
                                        else:
                                            em = boost.end_post()
                                            await boost.unpost_chan.send(embed=em)
                                            embed_message_adv = discord.Embed(title="Boost fini", color=0x32cd32)#7FFF00
                                            embed_message_adv.add_field(name="Merci!", value = "Le boost a été posté dans {}, en attendant d'être ajouté à la balance.\nMerci d'avertise avec nous!".format(boost.unpost_chan.mention), inline=False)
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
                                                embed_message = discord.Embed(title="Boost fini", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Merci", value = "Le boost a été validé par {} et ajouté à ta balance!\nMerci de booster avec nous!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    embed_message.add_field(name="Ta balance", value = "Tu as maintenant {} gold!".format(gold), inline=True)
                                                    if boost.inhouse:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175)), inline=True)
                                                    else:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
                                                embed_message.set_footer(text="Gino's Mercenaries")
                                            else:
                                                embed_message = discord.Embed(title="Boost fini", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "Le boost a été validé par {} et ajouté à ta balance!\nMerci de booster avec nous!".format(boost.advertiser.mention), inline=False)
                                                embed_message.set_footer(text="Gino's Mercenaries")

                                            await boost.tank_in.create_dm()
                                            await boost.tank_in.dm_channel.send(embed = embed_message)
                                        if boost.heal_in != "":
                                            if boost.auto_post:
                                                name = boost.heal_in.display_name
                                                user_name_serv = parseName(name)
                                                gold = sr.get_gold(user_name_serv[0],user_name_serv[1])
                                                embed_message = discord.Embed(title="Boost fini", color=0x32cd32)#7FFF00
                                                embed_message.add_field(name="Thank you!", value = "Le boost a été validé par {} et ajouté à ta balance!\nMerci de booster avec nous!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    embed_message.add_field(name="Ta balance", value = "Tu as maintenant {} gold!".format(gold), inline=True)
                                                    if boost.inhouse:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175)), inline=True)
                                                    else:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
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
                                                embed_message.add_field(name="Thank you!", value = "Le boost a été validé par {} et ajouté à ta balance!\nMerci de booster avec nous!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    embed_message.add_field(name="Ta balance", value = "Tu as maintenant {} gold!".format(gold), inline=True)
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
                                                        embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(cut), inline=True)
                                                    else:
                                                        if boost.type in ["torghast", "leveling"] or player_index == 1:
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
                                                        embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(cut), inline=True)
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
                                                embed_message.add_field(name="Thank you!", value = "Le boost a été validé par {} et ajouté à ta balance!\nMerci de booster avec nous!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    embed_message.add_field(name="Ta balance", value = "Tu as maintenant {} gold!".format(gold), inline=True)
                                                    if player_index == 2 or boost.type == "island":
                                                        if boost.inhouse:
                                                            if boost.no_adv_cut:
                                                                embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.22*2)), inline=True)
                                                            else:
                                                                embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175*2)), inline=True)
                                                        else:
                                                            if boost.no_adv_cut:
                                                                embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.22*2)), inline=True)
                                                            else:
                                                                embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.18*2)), inline=True)
                                                    else:
                                                        if boost.inhouse:
                                                            if boost.no_adv_cut:
                                                                embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.22)), inline=True)
                                                            else:
                                                                embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175)), inline=True)
                                                        else:
                                                            if boost.no_adv_cut:
                                                                embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.22)), inline=True)
                                                            else:
                                                                embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
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
                                                embed_message.add_field(name="Thank you!", value = "Le boost a été validé par {} et ajouté à ta balance!\nMerci de booster avec nous!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    if boost.inhouse:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175)), inline=True)
                                                    else:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
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
                                                embed_message.add_field(name="Thank you!", value = "Le boost a été validé par {} et ajouté à ta balance!\nMerci de booster avec nous!".format(boost.advertiser.mention), inline=False)
                                                if gold == "Nbalance":
                                                    ack = sr.add_balance(user_name_serv[0], user_name_serv[1], ally_bool)
                                                else:
                                                    embed_message.add_field(name="Ta balance", value = "Tu as maintenant {} gold!".format(gold), inline=True)
                                                    if boost.inhouse:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.85*0.2175)), inline=True)
                                                    else:
                                                        if boost.no_adv_cut:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.22)), inline=True)
                                                        else:
                                                            embed_message.add_field(name="Ton cut", value = "Ton cut est {:,}. :moneybag:".format(int(boost.gold*0.18)), inline=True)
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
                                        embed_message = discord.Embed(title="Boost annulé", color=0xdc143c)#7FFF00
                                        embed_message.add_field(name="\u200b", value = "Le boost est annulé.", inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                        await boost.message_annoucement.edit(embed=embed_message)
                                        await boost.message_annoucement.clear_reactions()
                                        self.__boost_being_done.pop(w)
                                        embed_message = discord.Embed(title="Boost fini", color=0xdc143c)#7FFF00
                                        embed_message.add_field(name="Boost raté", value = "{} a indiqué que le boost a été raté ou annulé. Votre balance n'a pas été modifiée.\n Contactez {} pour plus d'info!".format(boost.advertiser.mention,boost.advertiser.mention), inline=False)
                                        embed_message.set_footer(text="Gino's Mercenaries")
                                        embed_message_adv = discord.Embed(title="Boost fini", color=0xdc143c)#7FFF00
                                        embed_message_adv.add_field(name="Boost raté", value = "Vous avez indiqué que le boost a été raté ou annulé. Votre balance n'a pas été modifiée.".format(boost.advertiser.mention,boost.advertiser.mention), inline=False)
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


        except:
                err = traceback.format_exc()
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
            print(message.reactions)
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
        if boost.tank_in == "" and boost.notIn(user) and (boost.type == "mm" or boost.type == "mechagone"):
            boost.tank_in = user
            em = boost.post()
            await boost.message_annoucement.edit(embed = em)
            boost.booster_place -= 1
        else:
            boost.tank_waiting.append(user)
    else:
        await user.create_dm()
        embed_message = discord.Embed(title="Not the permission", color=0xdc143c)#7FFF00
        embed_message.add_field(name="\u200b", value="Tu manques un ou plusieurs de ces rôles pour booster comme tank : {}.".format(', '.join(boost.role_tank)), inline=False)
        embed_message.set_footer(text="Gino's Mercenaries")
        await user.dm_channel.send(embed=embed_message)
        await message.remove_reaction(emoji,user)

async def add_heal(user, boost, user_role, by_pass, message, emoji):
    if all(elem in user_role for elem in boost.role_heal) or by_pass:
        if boost.heal_in == "" and boost.notIn(user) and (boost.type == "mm" or boost.type == "mechagone"):
            boost.heal_in = user
            em = boost.post()
            await boost.message_annoucement.edit(embed = em)
            boost.booster_place -= 1
        else:
            boost.heal_waiting.append(user)
    else:
        await user.create_dm()
        embed_message = discord.Embed(title="Not the permission", color=0xdc143c)#7FFF00
        embed_message.add_field(name="\u200b", value="Tu manques un ou plusieurs de ces rôles pour booster comme heal : {}.".format(', '.join(boost.role_heal)), inline=False)
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
        embed_message.add_field(name="\u200b", value="Tu manques un ou plusieurs de ces rôles pour rejoinder ce boost: {}.".format(', '.join(boost.role_dps)), inline=False)
        embed_message.set_footer(text="Gino's Mercenaries")
        await user.dm_channel.send(embed=embed_message)
        await message.remove_reaction(emoji, user)
