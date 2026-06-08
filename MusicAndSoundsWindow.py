from PySide6.QtWidgets import QWidget, QDialog
from PySide6.QtCore import Qt
from CustomWidgets import EditedLabel, EditedButton, VolumeSlider

class MusicAndSoundsWindow(QDialog):
    def __init__(self, parent_width, parent_height, game_sounds, saved_settings, save_sounds):
        super().__init__()
        self.setModal(True)

        self.game_sounds = game_sounds

        self.main_container = QWidget(self)

        self.message = EditedLabel("Звуки и музыка", self.main_container, 0.3)
        self.music_label = EditedLabel("Музыка", self.main_container, 0.5)
        self.sounds_label = EditedLabel("Звуки", self.main_container, 0.5)
        self.music = VolumeSlider(self.main_container, game_sounds, 'music',
                                   saved_settings, save_sounds, saved_settings['music'] / 100)
        self.sounds = VolumeSlider(self.main_container, game_sounds, 'sound_effects', 
                                   saved_settings, save_sounds, saved_settings['sounds'] / 100)
        self.exit_btn = EditedButton("Назад", self.main_container, 0.5)

        self.message.setStyleSheet("border: 1px solid black")

        self.resize(parent_width * 0.6, parent_height * 0.5)

        self.exit_btn.setAutoDefault(False)

        self.exit_btn.clicked.connect(self.on_exit)

        self.setWindowFlag(Qt.FramelessWindowHint, True)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.on_exit()
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def on_exit(self):
        self.game_sounds.click_sound.play()
        self.close()

    def resizeEvent(self, event):
        self.main_container.setGeometry(0, 0, self.width(), self.height())

        w = self.width()
        h = self.height()

        message_width = int(w * 0.6)
        message_height = int(h * 0.25)
        message_x = (w - message_width) // 2
        message_y = int(h * 0.1)
        self.message.setGeometry(message_x, message_y, message_width, message_height)

        music_width = int(w * 0.625)
        music_height = int(h * 0.1)
        music_x = int(w - music_width) // 2
        music_y = int(message_y + message_height + h * 0.1 - music_height * 0.3)
        self.music.setGeometry(music_x, music_y, music_width, music_height)

        sounds_width = int(w * 0.625)
        sounds_height = int(h * 0.1)
        sounds_x = int(w - sounds_width) // 2
        sounds_y = int(music_y + music_height + h * 0.1 - sounds_height * 0.6)
        self.sounds.setGeometry(sounds_x, sounds_y, sounds_width, sounds_height)

        music_label_width = int(w * 0.15)
        music_label_height = int(h * 0.10)
        music_label_x = int(music_x - w * 0.05 - music_label_width + music_width * 0.1)
        music_label_y = int(music_y + music_height // 2 - music_label_height // 2)
        self.music_label.setGeometry(music_label_x, music_label_y, music_label_width, music_label_height)

        sounds_label_width = int(w * 0.15)
        sounds_label_height = int(h * 0.10)
        sounds_label_x = int(sounds_x - w * 0.05 - sounds_label_width + sounds_width * 0.1)
        sounds_label_y = int(sounds_y + sounds_height // 2 - sounds_height // 2)
        self.sounds_label.setGeometry(sounds_label_x, sounds_label_y, sounds_label_width, sounds_label_height)

        exit_btn_width = int(w * 0.4)
        exit_btn_height = int(h * 0.1)
        exit_btn_x = (w - exit_btn_width) // 2
        exit_btn_y = int(h - h * 0.1 - exit_btn_height)
        self.exit_btn.setGeometry(exit_btn_x, exit_btn_y, exit_btn_width, exit_btn_height)

        return super().resizeEvent(event)