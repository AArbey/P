Ce Projet est un programme en Python conçu pour le logiciel de messagerie Discord, permettant à l'utilisateur de connecter un bot(==robot) dans un canal vocal et de lui faire jouer de la musique provenant de Youtube, que ça soit via un lien ou en effectuant automatiquement une recherche sur Youtube a partir d'un nom donné par l'utilisateur. Il inclus aussi un jeux de Puissance 4 jouable directement depuis Discord.

J'ai personnelement créer une machine virtuelle sous Linux fonctionnant en permanence sur ma box internet pour que le robot soit toujours connecté sur le serveur.

J'utilise pour ce programme les librairies suivantes:
  discord.py: Permet la communication entre mon programme et Discord
  discord-py-slash-command(discord_slash): Permet l'utilisation des /, nouveux moyen créer par Discord pour créer des commandes pour des bots
  youtube_dl: pour télécharger des vidéos youtube 
  ffmpeg: pour jouer les audios venant des vidéos
  youtubesearchpython: pour rechercher des vidéos sur youtube et récupérer leur lien
  gTTS(google text to speech): pour créer un fichier audio à partir de la synthèse vocal de google
 
Attention! Le code ne fonctionnera pas tout seul, il est nécessaire de rajouter le Token ainsi que le guild_id que je ne peux inclure ici car ils sont privés et que Discord n'autorise pas leur partage.
