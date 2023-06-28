import dobotapi

# Dobot initialisieren und einer Variable zuweisen
bot = dobotapi.Dobot()


# Verbindung aufbauen
bot.connect()
# Lade .playback File
playback_file = "./Testablauf.playback"
bot.SetPlaybackCmd(playback_file)
# Starte das Playback
bot.Playback()
# Verbindung trennen
bot.close()
