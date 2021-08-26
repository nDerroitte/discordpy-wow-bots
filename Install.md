#Gino bot
## Lié le bot au serveur
### Créer le bot sur discord app
* Créer un bot
* Créer un lien autho2
```https://discordapp.com/api/oauth2/authorize?client_id=686611501389316108&permissions=8&scope=bot```
A copié dans le browser et ajouté à Gino quand on a les droits.
* Mettre les Privileged Gateway Intents a true

### Modifié le .env


* Le GUILD TOKEN a modifié avec le nom du serv
* Le bot TOKEN correspond a celui de Gino

## Lié le bot au google sheet
* Utiliser un ancien json!!!!


OU 

* Créer un projet [ici](https://console.developers.google.com/navigation-error;errorUrl=%2Fapis%2Fdashboard%3Fproject%3Dprice-list-291313/permissions?project=price-list-291313&organizationId=0)
* Ajoute Google Drive API et Google Sheet API
* Configurer l'écran d'autorisation (email = natan.derroitte)
* Crérer identifiant Oauth -> Application Web
* Le télécharger / rename
* générer une email avec https://cloud.google.com/iam/docs/service-accounts
* Et la suite jsp