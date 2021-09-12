import os
import re
from importlib import reload
import name_dict_lib

def check_name(name):
    user_name_serv = parseName(name)
    if user_name_serv[0] == "" or user_name_serv[1] == "":
        return False
    return True

def parseName(name):
    #reload(name_dict_lib)
    name = name.lower()
    if len(name) == 0:
        return ["", ""]
    if name[0] == "[":
        name = name.split("] ")[1]
    if name in name_dict_lib.name_dict:
        name_realm = name_dict_lib.name_dict[name]
        serv = name_realm.split("-")[1]
        name = name_realm.split("-")[0]
        return [name, serv]
    elif "-" in name:
        serv = name.split("-")[1]
        name = name.split("-")[0]
        return [name, serv]
    elif name == "":
        return ["noname",""]
    else:
        return [name, ""]

def reload_dict():
    reload(name_dict_lib)

def sameName(name1, name2):
    name1 = onlyName(name1)
    name2 = onlyName(name2)
    if name1.lower() == name2.lower():
        return True
    return False

def onlyName(name):
    #reload(name_dict_lib)
    name = name.lower()
    if name[0] == "[" and "] " in name:
        name = name.split("] ")[1]
    elif name[0] == "[" and "]" in name:
        name = name.split("]")[1]
    if name in name_dict_lib.name_dict:
        return name_dict_lib.name_dict[name]
    return name

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def mention_or_nada(data):
    if data == "":
        return ""
    else:
        return_str = data.mention + " - " + data.display_name
        return return_str


def fillBoost(boost, str_message):
    data = [line.strip().split(':') for line in str_message.split('\n') if line.strip()]
    data = [x for x in data if not len(x)<2]
    for info in data:
        if info[1] != "":
            info[1] = info[1].strip()
        if info[0] == "armor stack":
            info[1] = info[1].replace(" ","")
            if info[1] != "":
                if info[1].lower() not in ["plate", "mail", "leather","cloth","no","noarmorstack","/","nostack","noarmorstacks"]:
                    return "not armor stack"
                elif info[1].lower() in ["plate", "mail", "leather","cloth"]:
                    boost.armor_stack = info[1]
                else:
                    boost.armor_stack = "/"
            else:
                boost.armor_stack = "/"
        if info[0] == "boost" or info[0] == "boost note":
            if info[1].replace(" ","") != "":
                boost.notes = info[1].capitalize()
        if info[0] == "auto post":
            if info[1].replace(" ","") != "":
                if info[1] == "false":
                    boost.auto_post = False
        if info[0] == "gold":
            if info[1].replace(" ","") != "":
                if RepresentsInt(info[1]):
                    boost.gold = int(info[1])
                else:
                    boost.nb_boosters = 0
                    return "not gold"
        if info[0] == "gold realm":
            if info[1].replace(" ","") != "":
                boost.realm = main_connected_realm(info[1].lower())
                boost.real_realm = info[1].lower()
        if info[0] == "character to whisper":
            if info[1].replace(" ","") != "":
                boost.who_to_w = info[1]
        if info[0] == "buyer name":
            if info[1].replace(" ","") != "":
                boost.buyer_name = info[1].capitalize()
        if info[0] == "buyer spec":
            if info[1].replace(" ","") != "":
                boost.buyer_spec = info[1].capitalize()
        if info[0] == "character to whisper":
            if info[1].replace(" ","") != "":
                boost.who_to_w = info[1]
                boost.dps_in[i] = booster_l[0]
        if info[0] == "key level":
            if info[1].replace(" ","") != "":
                boost.key_level = info[1]
                info[1] = info[1].replace("+","")
                if RepresentsInt(info[1]):
                    boost.key_level = int(info[1])
                else:
                    boost.key_level = 0
                    return "not nb key"
        if info[0] == "key":
            if info[1].replace(" ","") != "":
                boost.key = info[1].capitalize()
        if info[0] == "number of run(s)":
            if info[1].replace(" ","") != "":
                if RepresentsInt(info[1]):
                    boost.nb_runs = int(info[1])
                else:
                    boost.nb_runs = 0
                    return "not nb run"
    return "ok"

def get_name_realm_aura(message):
    name_realm = ""
    for line in message.splitlines():
        line = line.replace(" ", "")
        if "pseudo" in line.lower() or ("nom" in line.lower() and "royaume" in line.lower()):
            try:
                name_realm = line.split(':')[1]
                name_realm = name_realm.replace(" ", "")
                break
            except:
                pass
    return name_realm


def get_faction(message):
    if "alliance" in message.lower():
        return "alliance"
    else:
        return  "horde"


def get_name_realm(message):
    name_realm = ""
    for line in message.splitlines():
        line = line.replace(" ", "")
        if "name" in line.lower() and "realm" in line.lower():
            try:
                name_realm = line.split(':')[1]
                name_realm = name_realm.replace(" ", "")
                break
            except:
                pass
    return name_realm

def get_list_tag_cut(message):
    cut_reg = "(Cut|cut) *:* *[0-9]*(k*|K*)"
    try:
        reg_cut = re.search(cut_reg, message)
        if reg_cut is not None:
            cut_str = str(re.search(cut_reg, message).group(0))
            cut = str(re.search("[0-9]*\.*[0-9]+(k*|K*)", cut_str).group(0))
        else:
            cut = "[still unknown, it was not fill by the raid leader yet! :cry:]"
    except:
        cut = "[still unknown, it was not fill by the raid leader yet! :cry:]"
    rep = get_list_tag(message)
    rep.append(cut)
    return rep

def get_list_tag(message):
    list_tag = []
    inv = ""
    for i in range(len(message)):
        current_tag = ""
        if (message[i] == '<' and message[i+1] == '@' and message[i+2] == '!'):
            j = 0
            while message[i+3+j] != '>':
                current_tag += message[i+3+j]
                j += 1
            list_tag.append(current_tag)
            i += (j+2)
        if (message[i] == '/' and message[i+1].lower() == "w"):
            j = 0
            try:
                inv += "/w"
                while not (message[i+2+j] == ' ' and message[i+2+j+1].lower() == 'i' and message[i+2+j+2].lower() == 'n' and message[i+2+j+3].lower() == 'v'):
                    inv += message[i+2+j]
                    j+= 1
                inv += " inv"
            except:
                inv = ""
    return [list_tag, inv]

def main_connected_realm(realm):
    if realm == "hellscream":
        return "aggramar"
    if realm == "hellfire":
        return "arathor"
    if realm == "shadowsong":
        return "aszune"
    if realm == "stormrage":
        return "azuremyst"
    if realm == "nordrassil":
        return "bronzedragonflight"
    if realm in ["aerie peak", "aeriepeak"]:
        return "bronzebeard"
    if realm in ["earthen ring", "earthenring"]:
        return "darkmoonfaire"
    if realm == "turalyon":
        return "doomhammer"
    if realm == "ghostlands":
        return "dragonblight"
    if realm in ["burning blade", "burningblade"]:
        return "drakthul"
    if realm == "terenas":
        return "emeralddream"
    if realm in ["aggra", "Frostmane"]:
        return "grimbatol"
    if realm == "bloodhoof":
        return "khadgar"
    if realm == "mazrigos":
        return "lightbringer"
    if realm in ["azjolnerub", "azjol-nerub"]:
        return "quelthalas"
    if realm == "dentarg":
        return "tarrenmill"
    if realm == "wildhammer":
        return "thunderhorn"
    if realm in ["genjuros", "neptulon"]:
        return "darksorrow"
    if realm in ["terrokar", "saurfang"]:
        return "darkspear"
    if realm in ["alonsus", "anachronos"]:
        return "kultiras"
    if realm in ["jaedenar", "dunemaul", "auchindoun"]:
        return "sylvanas"
    if realm in ["vek'nilash", "eonar", "veknilash", "bladesedge"]:
        return "bronzebeard"
    if realm in ["zenedar", "frostwhisper"]:
        return "bladefist"
    if realm in ["kor'gall", "korgall", "executus", "bloodfeather", "shattered hand", "shatteredhand"]:
        return "burningsteppes"
    if realm in ["shattered halls", "shatteredhalls", "boulderfist", "daggerspine", "talnivarr", "trollbane", "ahn'qiraj", "ahnqiraj", "balnazzar", "laughing skull", "laughingskull", "sunstrider"]:
        return "chromaggus"
    if realm in ["sporeggar", "scarshield legion", "scarshieldlegion", "the venture co", "theventureco", "ravenholdt"]:
        return "defiasbrotherhood"
    if realm in ["hakkar", "crushridge", "agamaggan", "bloodscalp", "twilight's hammer", "twilight'shammer", "twilights hammer", "twilightshammer"]:
        return "emeriss"
    if realm in ["dragonmaw", "spinebreaker", "vashj", "stormreaver"]:
        return "haomarush"
    if realm in ["the sha'tar", "thesha'tar", "the shatar","theshatar" ,"steamwheedle cartel", "steamwheedlecartel"]:
        return "moonglade"
    if realm in ["kilrogg", "nagrand", "runetotem"]:
        return "arathor"
    if realm in ["lightning's blade", "lightning'sblade", "lightnings blade", "lightningsblade", "deathwing", "karazhan"]:
        return "themaelstrom"
    if realm in ["skullcrasher", "al'akir", "alakir", "xavius"]:
        return "burninglegion"
    if realm == "nethersturm":
        return "alexstrasza"
    if realm == "rexxar":
        return "alleria"
    if realm in ["krag'jin", "kragjin"]:
        return "azshara"
    if realm in ["der mithrilorden", "dermithrilorden"]:
        return "derratvondalaran"
    if realm == "forscherlige":
        return "dienachtwache"
    if realm in ["die ewige wacht", "dieewigewacht"]:
        return "diesilbernehand"
    if realm == "norgannon":
        return "dunmorough"
    if realm == "ulduar":
        return "gilneas"
    if realm == "ambossar":
        return "kargath"
    if realm == "arygos":
        return "khazgoroth"
    if realm in ["tichondrius", "lordaeron"]:
        return "lordaeBlackmooreron"
    if realm in ["baelgun", "lothar"]:
        return "azshara"
    if realm in ["proudmoore", "madmortem"]:
        return "alexstrasza"
    if realm == "malygos":
        return "malfurion"
    if realm == "teldrassil":
        return "perenolde"
    if realm == "durotan":
        return "tirion"
    if realm == "malorne":
        return "ysera"
    if realm == "todeswache":
        return "zirkeldescenarius"
    if realm in ["vol'jin", "voljin"]:
        return "chantséternels"
    if realm in ["marécage de zangar", "marécagedezangar"]:
        return "dalaran"
    if realm == "varimathras":
        return "elune"
    if realm == "suramar":
        return "medivh"
    if realm in ["drek'thar", "drekthar", "eitrigg", "krasus"]:
        return "uldaman"
    if realm in ["azrak-arahm", "rashgarroth", "throk'feroth", "throkferoth"]:
        return "kael'thas"
    if realm in ["rajaxx", "gul'dan", "festung der stürme", "nathrezim", "kil'jaeden", "kiljaeden"]:
        return "anetheron"
    if realm in ["nazjatar", "frostmourne", "zuluhed", "dalvengyr"]:
        return "anub'arak"
    if realm in ["un'goro", "sen'jin", "senjin"]:
        return "area 52"
    if realm in ["vek'lor","veklor", "blutkessel", "kel'thuzad", "wrathbringer"]:
        return "arthas"
    if realm in ["nera'thor", "nera'thor", "mannoroth", "nefarian", "gorgonnash"]:
        return "destromath"
    if realm in ["shattrath", "nozdormu"]:
        return "garrosh"
    if realm in ["die arguswacht", "diearguswacht", "die todeskrallen", "dietodeskrallen", "der abyssische rat", "derabyssischerat", "das syndikat", "dassyndikat", "das konsortium", "daskonsortium"]:
        return "kultderverdammten"
    if realm in ["echsenkessel", "taerar"]:
        return "malganis"
    if realm in ["dethecus", "mug'thol", "mugthol", "terrordar", "theradras"]:
        return "onyxia"
    if realm in ["cho'gall", "chogall","sinstralis", "eldre'thalas", "eldrethalas"]:
        return "dalaran"
    if realm in ["les clairvoyants","lesclairvoyants", "les sentinelles", "lessentinelles", "confrerieduthorium", "confrerie du thorium"]:
        return "kirintor"
    if realm in ["naxxramas", "arathi", "temple noir", "templenoir"]:
        return "illidan"
    if realm in ["culte de la rive noire", "cultedelarivenoire", "conseil des ombres", "conseildesombres"]:
        return "lacroisadeécarlate"
    if realm in ["garona", "ner'zhul", "nerzhul"]:
        return "sargeras"
    return realm

def append_dict(nick, name):
    str_to_add = "\n    \"{}\" : \"{}\",".format(nick.lower(), name.lower())
    lines = open('name_dict_lib.py').read().splitlines()
    lines[1] = lines[1] + str_to_add
    open('name_dict_lib.py','w').write('\n'.join(lines))

def change_nick(old_name, new_name):
    reload(name_dict_lib)
    char_name = name_dict_lib.name_dict[old_name]
    lines = open('name_dict_lib.py').read().splitlines()
    for i in range(len(lines)):
        if "\"" +old_name +"\"" in lines[i]:
            lines[i] = "    \"{}\" : \"{}\",".format(new_name.lower(), char_name.lower())
    open('name_dict_lib.py','w').write('\n'.join(lines))
