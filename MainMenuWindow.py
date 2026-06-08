from PySide6.QtWidgets import QMainWindow, QWidget, QDialog, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt

from RulesWindow import RulesDialog
from CustomWidgets import EditedButton, EditedLabel
from Dialogs import CustomDialog
from GameWindow import GameWindow
from MusicAndSoundsWindow import MusicAndSoundsWindow
from Settings import SettingsWindow
from Sounds import GameSounds

import glob
import os
import tempfile
import json
import uuid

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Гекс")

        self.central_widget = QStackedWidget()

        self.setCentralWidget(self.central_widget)

        self.main_menu = QWidget()
        
        self.central_widget.addWidget(self.main_menu)

        self.central_widget.setCurrentIndex(0)
        
        self.title_label = EditedLabel("Гекс", self.main_menu, 0.4)
        self.new_game_btn = EditedButton("Новая игра", self.main_menu, 0.6) 
        self.continue_btn = EditedButton("Продолжить", self.main_menu, 0.6)
        self.settings_btn = EditedButton("Настройки", self.main_menu, 0.6)
        self.sound_btn = EditedButton("Звук и музыка", self.main_menu, 0.6)
        self.exit_btn = EditedButton("Выход", self.main_menu, 0.6)
        self.rules_btn = EditedButton("?", self.main_menu, 0.7)
        
        for btn in [self.new_game_btn, self.continue_btn, self.settings_btn, self.sound_btn, self.exit_btn, self.rules_btn]:
            btn.setMinimumSize(0, 0)
        self.title_label.setMinimumSize(0, 0)

        self.rules_btn.setProperty("class", "help")

        self.new_game_btn.clicked.connect(self.on_new_game)
        self.continue_btn.clicked.connect(self.on_continue)
        self.settings_btn.clicked.connect(self.on_settings)
        self.sound_btn.clicked.connect(self.on_sound)
        self.rules_btn.clicked.connect(self.on_rules)
        self.exit_btn.clicked.connect(self.on_exit)

        self.resize(800, 600)
        self.saved_settings = {
            'music': 50,
            'sounds': 50,
            'mode': 'player_vs_player',
            'board_size': 11,
            'color1': '#ff0000',
            'color2': '#0000ff',
            'bgcolor': '#ffffff',
            'name1': "Игрок 1",
            'name2': "Игрок 2",
        }
        appdata_path = os.path.join(os.getenv('APPDATA'), 'Hex', 'config.json')
        if os.path.exists(appdata_path):
            if self.valid_config(appdata_path):
                with open(appdata_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.saved_settings = {
                    'music': data['music'],
                    'sounds': data['sounds'],
                    'mode': data['game_mode'],
                    'board_size': data['board_size'],
                    'color1': data['player1_color'],
                    'color2': data['player2_color'],
                    'bgcolor': data['background_color'],
                    'name1': data['player1_name'],
                    'name2': data['player2_name'],
                }

        self.overlay = QWidget(self.centralWidget())
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.7);")
        self.overlay.hide()

        self.game_sounds = GameSounds()
        self.game_sounds.change_volume('sound_effects', self.saved_settings['sounds'] / 100)
        self.game_sounds.change_volume('music', self.saved_settings['music'] / 100)

        self.continue_is_active()

        saves_path = os.path.join(os.getenv('APPDATA'), 'Hex', 'saves')
        if os.path.exists(saves_path):
            files = glob.glob(os.path.join(saves_path, '*.json'))
            if len(files) > 10:
                self.del_files(files)

    def write_config(self, saved_settings):
        appdata_path = os.path.join(os.getenv('APPDATA'), 'Hex', 'config.json')
        dirpath = os.path.dirname(appdata_path)

        data = {
            'music': int(saved_settings['music']),
            'sounds': int(saved_settings['sounds']),
            'game_mode': saved_settings['mode'],
            'board_size': saved_settings['board_size'],
            'player1_name': saved_settings['name1'],
            'player2_name': saved_settings['name2'],
            'player1_color': saved_settings['color1'],
            'player2_color': saved_settings['color2'],
            'background_color': saved_settings['bgcolor'],
        }

        os.makedirs(dirpath, exist_ok=True)
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', dir=dirpath, delete=False, encoding='utf-8') as tmp:
                tmp_path = tmp.name
                json.dump(data, tmp, indent=4, ensure_ascii=False)
            os.replace(tmp_path, appdata_path)
        except Exception:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
        
    def del_files(self, files):
        files_with_time = []
        for i in range(len(files)):
            time = os.path.getmtime(files[i])
            files_with_time.append([files[i], time])
        files_with_time.sort(key=lambda x: x[1])
        while len(files_with_time) > 10:
            os.remove(files_with_time[0][0])
            files_with_time.pop(0)

    def valid_config(self, appdata_path):
        try:
            with open(appdata_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            json_objects = {'sounds', 'music', 'game_mode', 'board_size',  'player1_name', 'player2_name',
                           'player1_color', 'player2_color', 'background_color'}
            
            for key in json_objects:
                if key in data:
                    continue
                else:
                    return False
                
            if not type(data['sounds']) == int:
                return False
            if not type(data['music']) == int:
                return False
            if not type(data['board_size']) == int:
                return False
            if not(type(data['game_mode']) == str and type(data['player1_name']) == str and type(data['player2_name']) == str):
                return False
            if not(type(data['player1_color']) == str and type(data['player2_color']) == str and type(data['background_color']) == str):
                return False
            
            if data['music'] < 0 or data['music'] > 100:
                return False
            if data['sounds'] < 0 or data['sounds'] > 100:
                return False
            if data['game_mode'] not in ['player_vs_player', 'bot_easy', 'bot_medium', 'bot_hard']:
                return False
            if data['board_size'] not in [9, 11, 13, 15, 17]:
                return False
            if len(data['player1_name']) > 20 or len(data['player1_name']) <= 0:
                return False
            if len(data['player2_name']) > 20 or len(data['player2_name']) <= 0:
                return False
            
            colors = [data['player1_color'], data['player2_color'], data['background_color']]
            for col in colors:
                if len(col) == 7 and col[0] == '#':
                    for i in range(1, 7):
                        if col[i] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
                            return False
                else:
                    return False
            return True
        except json.JSONDecodeError:
            return False

    def valid_save(self, save_path):
        try:
            with open(save_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            json_objects = {'current_player', 'cells', 'board_size', 'game_mode',
                             'first_turn', 'player_names', 'colors', 'game_id'}
            
            for key in json_objects:
                if key in data:
                    continue
                else:
                    return False

            if not type(data['current_player']) == int:
                return False
            if not (type(data['board_size']) == int and type(data['first_turn']) == bool):
                return False
            if not type(data['player_names']) == list:
                return False
            if not len(data['player_names']) == 2:
                return False
            if not type(data['colors']) == list:
                return False
            if not len(data['colors']) == 3:
                return False
            if not type(data['cells']) == list:
                return False
            if not(type(data['game_mode']) == str and type(data['player_names'][0]) == str and type(data['player_names'][1]) == str):
                return False
            if not(type(data['colors'][0]) == str and type(data['colors'][1]) == str and type(data['colors'][2]) == str):
                return False
            if not type(data['game_id']) == str:
                return False

            if data['current_player'] not in [1, 2]:
                return False
            if data['game_mode'] not in ['player_vs_player', 'bot_easy', 'bot_medium', 'bot_hard']:
                return False
            if data['board_size'] not in [9, 11, 13, 15, 17]:
                return False
            if len(data['player_names'][0]) > 20 or len(data['player_names'][0]) <= 0:
                return False
            if len(data['player_names'][1]) > 20 or len(data['player_names'][1]) <= 0:
                return False
            if data['game_id'].strip() == '':
                return False

            colors = [data['colors'][0], data['colors'][1], data['colors'][2]]
            for col in colors:
                if len(col) == 7 and col[0] == '#':
                    for i in range(1, 7):
                        if col[i] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
                            return False
                else:
                    return False

            if len(data['cells']) == data['board_size']:
                for i in range(data['board_size']):
                    if len(data['cells'][i]) == data['board_size']:
                        continue
                    else:
                        return False
            else:
                return False
            
            for i in range(data['board_size']):
                for j in range(data['board_size']):
                    if type(data['cells'][i][j]) == int:
                        if data['cells'][i][j] in [0, 1, 2]:
                            continue
                        else:
                            return False
                    else:
                        return False
            return True
        
        except (json.JSONDecodeError, KeyError, TypeError):
            return False
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.central_widget.currentIndex() == 0:
            self.on_exit()
        else:
            super().keyPressEvent(event)
    
    def change_window(self):
        self.central_widget.setCurrentIndex(0)
        self.continue_is_active()

    def on_game_end(self):
        self.del_gameid(self.game_window.game_id)
        self.change_window()
    
    def del_gameid(self, game_id):
        saves_path = os.path.join(os.getenv('APPDATA'), 'Hex', 'saves')
        files = glob.glob(os.path.join(saves_path, '*.json'))
        to_delete = []
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data['game_id'] == game_id:
                        to_delete.append(file)
            except:
                continue
        for file in to_delete:
            os.remove(file)
    
    def on_new_game (self):
        self.game_sounds.click_sound.play()
    
        board = []
        for i in range(self.saved_settings['board_size']):
            row = []
            for j in range(self.saved_settings['board_size']):
                row.append(0)
            board.append(row)

        game_id = str(uuid.uuid4())

        saves_path = os.path.join(os.getenv('APPDATA'), 'Hex', 'saves')
        if os.path.exists(saves_path):
            files = glob.glob(os.path.join(saves_path, '*.json'))
            if files:
                self.overlay.setGeometry(0,0, self.width(), self.height())
                self.overlay.raise_()
                self.overlay.show()

                dlg = CustomDialog(self.width(), self.height(), "New_game", self.game_sounds)
                dlg.move(self.center.x() - dlg.width()//2, self.center.y() - dlg.height()//2)

                if dlg.exec() == QDialog.Accepted:
                    self.overlay.hide()

                    max_time = 0.0
                    for i in range(len(files)):
                        time_file = os.path.getmtime(files[i])
                        if time_file > max_time:
                            max_time = time_file
                            file = files[i]
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            id = data['game_id']
                        self.del_gameid(id)
                    except:
                        None
                else:
                    self.overlay.hide()
                    return
                
        self.game_window = GameWindow(self.width(), self.height(), game_id, board, self.saved_settings['mode'], 
                                      self.saved_settings['board_size'], self.saved_settings['color1'], 
                                      self.saved_settings['color2'], self.saved_settings['bgcolor'], 1, False, 
                                      self.saved_settings['name1'], self.saved_settings['name2'], 
                                      self.game_sounds, self.write_config, self.saved_settings)
                
        if self.central_widget.count() > 1:
            old = self.central_widget.widget(1)
            self.central_widget.removeWidget(old)
            old.deleteLater()
        self.central_widget.addWidget(self.game_window)
        self.game_window.exit.connect(self.change_window)
        self.game_window.end.connect(self.on_game_end)
        self.central_widget.setCurrentIndex(1)

    def continue_is_active(self):
        saves_path = os.path.join(os.getenv('APPDATA'), 'Hex', 'saves')
        files = glob.glob(os.path.join(saves_path, '*.json'))
        if files:
            self.continue_btn.setEnabled(True)
        else:
            self.continue_btn.setEnabled(False)        
    
    def on_continue (self):
        self.game_sounds.click_sound.play()
        saves_path = os.path.join(os.getenv('APPDATA'), 'Hex', 'saves')
        files = glob.glob(os.path.join(saves_path, '*.json'))

        max_time = 0.0
        for i in range(len(files)):
            time_file = os.path.getmtime(files[i])
            if time_file > max_time:
                max_time = time_file
                file = files[i]

        file_path = os.path.join(saves_path, file)
        if not self.valid_save(file_path):
            message = QMessageBox()
            message.setText(r"""Файл сохранения повреждён. Игра не будет продолжена. 
                            Повреждённый файл находится в папке %APPDATA%\Hex\saves\. Удалите или исправьте его""")
            message.setStyleSheet('color: #000000;')
            message.setIcon(QMessageBox.Icon.Critical)
            message.exec()
            return None
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.game_window = GameWindow(self.width(), self.height(), data['game_id'], data['cells'], data['game_mode'], data['board_size'], 
                                      data['colors'][0], data['colors'][1], data['colors'][2], data['current_player'], data['first_turn'],
                                      data['player_names'][0], data['player_names'][1], self.game_sounds, self.write_config, self.saved_settings)

        if self.central_widget.count() > 1:
            old = self.central_widget.widget(1)
            self.central_widget.removeWidget(old)
            old.deleteLater()
        self.central_widget.addWidget(self.game_window)
        self.game_window.exit.connect(self.change_window)
        self.game_window.end.connect(self.on_game_end)
        self.central_widget.setCurrentIndex(1)

    def on_settings(self):
        self.game_sounds.click_sound.play()
        self.overlay.setGeometry(0,0, self.width(), self.height())
        self.overlay.raise_()
        self.overlay.show()

        dlg = SettingsWindow(self.width(), self.height(), self.saved_settings['mode'], self.saved_settings['board_size'], 
              self.saved_settings['color1'], self.saved_settings['color2'], self.saved_settings['bgcolor'], 
              self.saved_settings['name1'], self.saved_settings['name2'], self.game_sounds)

        dlg.move(self.center.x() - dlg.width()//2, self.center.y() - dlg.height()//2)

        if dlg.exec() == QDialog.Accepted:
            match dlg.gamemode.currentText():
                case 'Игрок против игрока':
                    mode = 'player_vs_player'
                case 'Бот (лёгкий)':
                    mode = 'bot_easy'
                case 'Бот (средний)':
                    mode = 'bot_medium'
                case 'Бот (сложный)':       
                    mode = 'bot_hard'     
                    
            self.saved_settings = {
                'music': self.saved_settings['music'],
                'sounds': self.saved_settings['sounds'],
                'mode': mode,
                'board_size': int(dlg.fieldsize.currentText().split('x')[0]),
                'color1': f'#{format(dlg.color1.red(), '02x')}{format(dlg.color1.green(), '02x')}{format(dlg.color1.blue(), '02x')}',
                'color2': f'#{format(dlg.color2.red(), '02x')}{format(dlg.color2.green(), '02x')}{format(dlg.color2.blue(), '02x')}',
                'bgcolor': f'#{format(dlg.bgcolor.red(), '02x')}{format(dlg.bgcolor.green(), '02x')}{format(dlg.bgcolor.blue(), '02x')}',
                'name1': dlg.name_player1.text(),
                'name2': dlg.name_player2.text(),
            }

            self.write_config(self.saved_settings)

        self.overlay.hide()

    def on_sound(self):
        self.game_sounds.click_sound.play()
        self.overlay.setGeometry(0,0, self.width(), self.height())
        self.overlay.raise_()
        self.overlay.show()

        dlg = MusicAndSoundsWindow(self.width(), self.height(), self.game_sounds, self.saved_settings, self.write_config)
        dlg.move(self.center.x() - dlg.width()//2, self.center.y() - dlg.height()//2)

        dlg.exec()
                
        self.overlay.hide()

    def on_rules(self):
        self.game_sounds.click_sound.play()
        self.overlay.setGeometry(0,0, self.width(), self.height())
        self.overlay.raise_()
        self.overlay.show()

        dlg = RulesDialog(self.width(), self.height(), self.game_sounds)

        dlg.move(self.center.x() - dlg.width()//2, self.center.y() - dlg.height()//2)

        dlg.exec()
        
        self.overlay.hide()
        
    def on_exit(self):
        self.game_sounds.click_sound.play()
        self.overlay.setGeometry(0,0, self.width(), self.height())
        self.overlay.raise_()
        self.overlay.show()

        dlg = CustomDialog(self.width(), self.height(), "exit_MainMenu", self.game_sounds)

        dlg.move(self.center.x() - dlg.width()//2, self.center.y() - dlg.height()//2)

        if dlg.exec() == QDialog.Accepted:
            self.close()
        
        self.overlay.hide()

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()

        self.center = self.geometry().center()

        title_width = int(w * 0.4)
        title_height = int(h * 0.3)
        title_x = (w - title_width) // 2
        title_y = int(h * 0.1)
        self.title_label.setGeometry(title_x, title_y, title_width, title_height)

        button_width = int(w * 0.2)
        button_height = int(h * 0.06)
        button_x = (w - button_width) // 2
        button_y = int(h * 0.05 + title_height + title_y)
        self.new_game_btn.setGeometry(button_x, button_y, button_width, button_height)

        button_y = int(h * 0.03 + button_y + button_height) 
        self.continue_btn.setGeometry(button_x, button_y, button_width, button_height)

        button_y = int(h * 0.03 + button_y + button_height)
        self.settings_btn.setGeometry(button_x, button_y, button_width, button_height)

        button_y = int(h * 0.03 + button_y + button_height)
        self.sound_btn.setGeometry(button_x, button_y, button_width, button_height)

        button_y = int(h * 0.03 + button_y + button_height)
        self.exit_btn.setGeometry(button_x, button_y, button_width, button_height)

        diameter = int(h * 0.08)
        button_x = int(w * 0.04)
        button_y = h - diameter - int(h * 0.04)
        self.rules_btn.setGeometry(button_x, button_y, diameter, diameter)
        
        radius = self.rules_btn.width() // 2
        self.rules_btn.setStyleSheet(f"""
            QPushButton {{
                border-radius: {radius}px;
                border-style: solid;
                border-width: 1px;
                border-color: #000000;
                font-family: Arial;
                background-color: #95A5A6;
                color: #000000;
            }}
            .help:hover {{
                background-color: #7f8c8d;
            }}

            .help:pressed {{
                background-color: #6c7b7d;
            }}
        """)

        return super().resizeEvent(event)
    
    def moveEvent(self, event):
        self.center = self.geometry().center()
        return super().moveEvent(event)