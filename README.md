# Bot stuff

This is a repo about me, making a bot to optimise a World of Warcraft gold boosting community generating hundreds of milions of gold, in a shitty way.

## How it works

World of Warcraft is a game where the best equipements are rewarded to players doing the hardest content.
A lot of casual players, or advanced players creating multiples characters, don't do this hard content by their own because they lack the motivation, time or skill.

For gold, players can buy our service: a **boost**. The casual player, called the **buyer, client or boostee** , will contact one of our **advertiser**.
The advertiser will set up a group of strong players, called **boosters** to help the client obtaining the loot he seeks.
On average, each booster (there are 4 of them in a boost) get 18% of the total pot. The advertiser will also get 18%. The 10% remaining will go to the community owner which is the bot owner.

## Gold reference

200k gold in wow is roughly 20€. Every month, this bot helps generating about 120M+ gold, which represents, unproperly, 12.000€.
The bot has been running since Febuary 2020. This makes (as of September 2021) a total of 228.00€.
10% of that total can be counted has pure benifts, the 90 other percent are redistributed to the actors of the community 

Buying gold in World of Warcraft can be done in blizzard shop. Selling it is against the game rules. A good rule of thumb is to consider that the gold under the table for roughly half its price, ie for 11.400€
As the community has no interest in doing RMT (Real Money Transaction, aka selling real gold for €), no one actually gain 11.400€ from this bot. (Let's furthermore s)
It just helped making a lot of people very rich in one (if not the) most popular multiplayer role-playing game

## Install

To run the code, one only need the ```discord``` python package.
To make the scripts run 24/7 I used a Amazon EC2 server with the ```forever``` javascript package. This was probably not the best way to do that

## Dependecies 

The bots are built on several google sheets and google forms.

### Balance sheet

The balance sheet is a google sheet that keep track of all the sells made with the bot. 
It also serves as *invoices*. Having to handle payments over all Europe realms (mostly French German and UK), it helps to keep track what the community owns to who.

### Submit Form

To trigger the creation of a boost, several googles forms were created.
A webhook needs to send the form answer to discord. I used a webhook I found on Stackoverflow.


## Discord API

Discord API can be found [here](https://discordpy.readthedocs.io/en/stable/api.html)