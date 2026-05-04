from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QSoundEffect, QMediaPlayer, QAudioOutput

class GameSounds:
    def __init__(self):
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("sounds/click.wav"))
        self.turn_sound = QSoundEffect()
        self.turn_sound.setSource(QUrl.fromLocalFile("sounds/move.wav"))
        self.victory_sound = QSoundEffect()
        self.victory_sound.setSource(QUrl.fromLocalFile("sounds/victory.wav"))
        self.music_player = QMediaPlayer()
        self.music_player.setSource(QUrl.fromLocalFile("sounds/music.mp3"))
        self.music_player.setLoops(QMediaPlayer.Loops.Infinite)
        self.music_player_audio = QAudioOutput()
        self.music_player.setAudioOutput(self.music_player_audio)
        self.music_player.play()
    
    def change_volume(self, type, new_vol):
        if type == 'sound_effects':
            self.click_sound.setVolume(new_vol)
            self.turn_sound.setVolume(new_vol)
            self.victory_sound.setVolume(new_vol)
        else:
            self.music_player_audio.setVolume(new_vol)