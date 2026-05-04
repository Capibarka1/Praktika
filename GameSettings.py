from PySide6.QtWidgets import QWidget, QDialog
from PySide6.QtCore import Qt, Signal
from CustomWidgets import EditedLabel, EditedButton, VolumeSlider

from Dialogs import CustomDialog

from datetime import datetime
import json
import os
import glob
import tempfile

class GameSettings(QDialog):

    exit_pressed = Signal()

    def __init__(self, parent_width, parent_height, game_sounds, 
                 saved_settings, save_sounds, board_info):
        super().__init__()
        self.setModal(True)

        self.parent_width = parent_width
        self.parent_height = parent_height

        self.game_sounds = game_sounds
        self.board_info = board_info
        self.saved_settings = saved_settings

        self.main_container = QWidget(self)

        self.back_btn = EditedButton("Назад", self.main_container, 0.5)
        self.save_btn = EditedButton("Сохранить", self.main_container, 0.5)
        self.exit_btn = EditedButton("Выйти", self.main_container, 0.5)
        self.music_label = EditedLabel("Музыка", self.main_container, 0.5)
        self.sounds_label = EditedLabel("Звуки", self.main_container, 0.5)
        self.music = VolumeSlider(self.main_container, game_sounds, 'music', 
                                  saved_settings, save_sounds, saved_settings['music'] / 100)
        self.sounds = VolumeSlider(self.main_container, game_sounds, 'sound_effects', 
                                   saved_settings, save_sounds, saved_settings['sounds'] / 100)

        self.resize(parent_width * 0.6, parent_height * 0.5)

        self.exit_btn.clicked.connect(self.exit)
        self.back_btn.clicked.connect(self.back)
        self.save_btn.clicked.connect(self.save_game)

        self.exit_btn.setAutoDefault(False)
        self.back_btn.setAutoDefault(False)
        self.save_btn.setAutoDefault(False)

        self.overlay = QWidget(self.main_container)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.7);")
        self.overlay.hide()

        self.setWindowFlag(Qt.FramelessWindowHint, True)
    
    def back(self):
        self.game_sounds.click_sound.play()
        self.reject()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.reject()
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def exit(self):
        self.game_sounds.click_sound.play()
        self.overlay.setGeometry(0,0, self.width(), self.height())
        self.overlay.show()        

        dlg = CustomDialog(self.parent_width , self.parent_height, "Leave", self.game_sounds)
        dlg.move(self.center.x() - dlg.width()//2, self.center.y() - dlg.height()//2)

        if dlg.exec() == QDialog.Accepted:
            self.exit_pressed.emit()
            self.close()

        self.overlay.hide()
    
    def save_game(self):
        self.game_sounds.click_sound.play()
        self.overlay.setGeometry(0,0, self.width(), self.height())
        self.overlay.show()

        dlg = CustomDialog(self.parent_width , self.parent_height, "Save", self.game_sounds)
        dlg.move(self.center.x() - dlg.width()//2, self.center.y() - dlg.height()//2)

        if dlg.exec() == QDialog.Accepted:
            saves_path = os.path.join(os.getenv('APPDATA'), 'Hex', 'saves')
            os.makedirs(saves_path, exist_ok=True)
            files = glob.glob(os.path.join(saves_path, '*.json'))
            if len(files) >= 10:
                self.del_files(files)
            self.write_game_save(self.board_info)
        
        self.overlay.hide()
    
    def del_files(self, files):
        files_with_time = []
        for i in range(len(files)):
            time = os.path.getmtime(files[i])
            files_with_time.append([files[i], time])
        files_with_time.sort(key=lambda x: x[1])
        print(len(files_with_time))
        while len(files_with_time) > 9:
            os.remove(files_with_time[0][0])
            files_with_time.pop(0)
    
    def write_game_save(self, saved_game):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        saves_path = os.path.join(os.getenv('APPDATA'), 'Hex', 'saves', 'save_' + now + '.json')
        dirpath = os.path.dirname(saves_path)

        board_info = {
            'board_size': saved_game['board_size'],
            'cells': saved_game['cells'],
            'game_mode': saved_game['game_mode'],
            'current_player': saved_game['current_player'],
            'player_names': saved_game['player_names'],
            'colors': saved_game['colors'],
            'first_turn': saved_game['first_turn'],
            'game_id': saved_game['game_id']
        }

        os.makedirs(dirpath, exist_ok=True)
        try:
            with tempfile.NamedTemporaryFile(mode='w', dir=dirpath, delete=False, encoding='utf-8') as tmp:
                tmp_path = tmp.name
                json.dump(board_info, tmp, indent=4, ensure_ascii=False)
            os.replace(tmp_path, saves_path)
        except Exception:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def resizeEvent(self, event):
        self.main_container.setGeometry(0, 0, self.width(), self.height())

        self.center = self.geometry().center()

        w = self.width()
        h = self.height()

        back_btn_width = int(w * 0.4)
        back_btn_height = int(h * 0.1)
        back_btn_x = (w - back_btn_width) // 2
        back_btn_y = int(h - h * 0.9)
        self.back_btn.setGeometry(back_btn_x, back_btn_y, back_btn_width, back_btn_height)

        save_btn_width = int(w * 0.4)
        save_btn_height = int(h * 0.1)
        save_btn_x = (w - save_btn_width) // 2
        save_btn_y = int(back_btn_y + back_btn_height + h * 0.05)
        self.save_btn.setGeometry(save_btn_x, save_btn_y, save_btn_width, save_btn_height)

        exit_btn_width = int(w * 0.4)
        exit_btn_height = int(h * 0.1)
        exit_btn_x = (w - exit_btn_width) // 2
        exit_btn_y = int(save_btn_y + save_btn_height + h * 0.05)
        self.exit_btn.setGeometry(exit_btn_x, exit_btn_y, exit_btn_width, exit_btn_height)

        music_width = int(w * 0.625)
        music_height = int(h * 0.075)
        music_x = int(w - music_width) // 2
        music_y = int(exit_btn_y + exit_btn_height + h * 0.2 - music_height * 0.3)
        self.music.setGeometry(music_x, music_y, music_width, music_height)

        sounds_width = int(w * 0.625)
        sounds_height = int(h * 0.075)
        sounds_x = int(w - music_width) // 2
        sounds_y = int(music_y + music_height + h * 0.1 - sounds_height * 0.6)
        self.sounds.setGeometry(sounds_x, sounds_y, sounds_width, sounds_height)

        music_label_width = int(w * 0.15)
        music_label_height = int(h * 0.1)
        music_label_x = music_x - music_label_width - int(w * 0.03) + sounds_width * 0.1
        music_label_y = int(music_y + music_height // 2 - music_label_height // 2)
        self.music_label.setGeometry(music_label_x, music_label_y, music_label_width, music_label_height)

        sounds_label_width = int(w * 0.15)
        sounds_label_height = int(h * 0.1)
        sounds_label_x = sounds_x - sounds_label_width - int(w * 0.03) + sounds_width * 0.1
        sounds_label_y = int(sounds_y + sounds_height // 2 - sounds_height // 2)
        self.sounds_label.setGeometry(sounds_label_x, sounds_label_y, sounds_label_width, sounds_label_height)

        return super().resizeEvent(event)