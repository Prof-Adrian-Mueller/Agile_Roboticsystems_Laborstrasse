import dobotapi

# Dobot initialisieren und einer Variable zuweisen
dobot = dobotapi.Dobot
# Verbindung aufbauen
dobot.ConnectDobot()
# Lade .playback File
playback_file = "./Testablauf.playback"
dobot.SetPlaybackCmd(playback_file)
# Starte das Playback
dobot.Playback()
# Verbindung trennen
dobot.DisconnectDobot()