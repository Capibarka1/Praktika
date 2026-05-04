from PySide6.QtWidgets import QWidget, QScrollArea, QFrame, QVBoxLayout
from CustomWidgets import EditedButton, EditedLabel, PlayerNameLabel
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import QSize, Signal
import qtawesome as qta

from VictoryWindow import VictoryWindow
from GameSettings import GameSettings
from Board import GameField


class GameWindow(QWidget):

    end = Signal()
    exit = Signal()
    
    def __init__(self, parent_width, parent_height, game_id, board, gamemode, board_size,  
                 player1_color, player2_color, background_color, num_of_currentPlayer, first_turn,
                 player1_name, player2_name, game_sounds, save_sounds, saved_settings):
        super().__init__()

        self.main_container = QWidget(self)

        self.game_id = game_id

        self.game_sounds = game_sounds
        self.save_sounds = save_sounds

        self.saved_settings = saved_settings

        self.gamemode = gamemode
        self.board_size = board_size
        self.pl1_name = player1_name
        self.pl2_name = player2_name
        self.player1_color = player1_color
        self.player2_color = player2_color
        self.background_color = background_color

        if num_of_currentPlayer == 1:
            self.player1Name_label = PlayerNameLabel(player1_name, player1_color, self.main_container, 0.4, True)
        else:
            self.player1Name_label = PlayerNameLabel(player1_name, player1_color, self.main_container, 0.4, False)

        if num_of_currentPlayer == 2:
            self.player2Name_label = PlayerNameLabel(player2_name, player2_color, self.main_container, 0.4, True)
        else:
            self.player2Name_label = PlayerNameLabel(player2_name, player2_color, self.main_container, 0.4, False)
    
        self.turn_label = EditedLabel(f"Ход: {player1_name}", self.main_container, 0.4)
        self.turn_label.setStyleSheet("border: 1px solid black; background-color: #f0f0f0;")

        self.settings_btn = EditedButton("", self.main_container, 0.5)
        self.PieRule_btn = EditedButton("Применить\nPie rule", self.main_container, 0.1, 10)
        
        if first_turn == True:
            self.PieRule_btn.show()
        else:
            self.PieRule_btn.hide()
        
        self.settings_btn.setIcon(QIcon("settings.webp"))

        self.turn_label.setProperty("class", "GameField_label")
        self.settings_btn.setProperty("class", "settings_btn")

        self.settings_btn.clicked.connect(self.on_settings)
        self.PieRule_btn.clicked.connect(lambda: self.pie_rule(True))
        self.PieRule_btn.pressed.connect(self.game_sounds.click_sound.play)

        gear_icon = qta.icon("fa6s.gear", color="#000000")
        self.settings_btn.setIcon(gear_icon)

        self.frame = QFrame(self)
        self.frame.setStyleSheet("border: 2px solid black;")

        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_field = QScrollArea()
        self.scroll_field.setFrameShape(QFrame.NoFrame)
        self.scroll_field.setWidgetResizable(True)
        layout.addWidget(self.scroll_field)

        self.color1 = QColor(int(player1_color[1:3], 16), int(player1_color[3:5], 16), int(player1_color[5:7], 16))
        self.color2 = QColor(int(player2_color[1:3], 16), int(player2_color[3:5], 16), int(player2_color[5:7], 16))
        bgcolor = QColor(int(background_color[1:3], 16), int(background_color[3:5], 16), int(background_color[5:7], 16))
        
        self.game_field = GameField(self.main_container, self.width(), self.height(), board, gamemode, 
                                    board_size, self.color1, self.color2, num_of_currentPlayer, 
                                    first_turn, self.game_sounds)

        self.scroll_field.setStyleSheet(f'background-color: {background_color}')
        
        self.scroll_field.setWidget(self.game_field)

        self.game_field.turn_changed.connect(self.update_turn_highlight)
        self.game_field.victory.connect(self.victory)
        self.game_field.pie_rule_used.connect(lambda: self.pie_rule(False))

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.7);")
        self.overlay.hide()

        self.update_turn_highlight()
        self.resize(parent_width, parent_height)

    def update_turn_highlight(self):
        current_turn = self.game_field.get_current_pl()
        self.player1Name_label.set_current(current_turn % 2 == 1)
        self.player2Name_label.set_current(current_turn % 2 == 0)
        if current_turn == 1:
            self.turn_label.change_name(self.pl1_name)
        else:
            self.turn_label.change_name(self.pl2_name)
        self.pie_rule_update()

    def on_settings (self):
        self.overlay.setGeometry(0,0, self.width(), self.height())
        self.overlay.show()

        self.game_sounds.click_sound.play()

        game_info = self.game_field.get_board_info()
        board_info = {
            'board_size': self.board_size,
            'cells': game_info['cells'],
            'game_mode': self.gamemode,
            'current_player': game_info['current_player'],
            'player_names': [self.pl1_name, self.pl2_name],
            'colors': [self.player1_color, self.player2_color, self.background_color],
            'first_turn': game_info['first_turn'],
            'game_id': self.game_id
        }

        self.center_global = self.mapToGlobal(self.rect().center())

        self.game_settings = GameSettings(self.width(), self.height(), self.game_sounds, self.saved_settings, self.save_sounds, board_info)
        self.game_settings.exit_pressed.connect(lambda: self.exit.emit())
        self.game_settings.move(self.center_global.x() - self.game_settings.width()//2, self.center_global.y() - self.game_settings.height()//2)
        
        self.game_settings.exec()

        self.overlay.hide()
        
    def pie_rule(self, players_click):
        if players_click:
            self.game_sounds.click_sound.play()
        self.game_field.pie_rule()
        self.player1_color, self.player2_color = self.player2_color, self.player1_color

        self.player1Name_label.swich_colors(self.player1_color, True)
        self.player2Name_label.swich_colors(self.player2_color, False)

    def pie_rule_update(self):
        if self.game_field.get_pierule_used() == False and self.game_field.get_turn() == 2:
            self.PieRule_btn.show()
        else:
            self.PieRule_btn.hide()

    def victory(self):
        current_player = self.game_field.get_current_pl()

        self.overlay.setGeometry(0,0, self.width(), self.height())
        self.overlay.show()

        self.center_global = self.mapToGlobal(self.rect().center())

        self.game_sounds.victory_sound.play()

        if current_player == 1:
            dlg = VictoryWindow(self.width(), self.height(), self.pl1_name, self.game_sounds)
        else:
            dlg = VictoryWindow(self.width(), self.height(), self.pl2_name, self.game_sounds)

        dlg.move(self.center_global.x() - dlg.width()//2, self.center_global.y() - dlg.height()//2)
        dlg.exec()
        self.overlay.hide()

        self.end.emit()

    def update_game_field(self):
        self.field_size = min(self.width() // (pow(3, .5) * self.board_size), self.height() // self.board_size)

        a = max(self.field_size / pow(3,.5), 10)

        if a == 10:
            self.field_size = a * pow(3,.5)
        
        horiz = 1.5 * 10
        vert = pow(3,.5) * 10

        width_need = horiz * (self.board_size * 2)
        height_need = vert * (self.board_size * 1.6)
        
        if width_need > self.scroll_field.width() or height_need > self.scroll_field.height():
            if self.scroll_field.width() < self.scroll_field.height():
                self.scroll_field.setWidgetResizable(False)
                self.game_field.setFixedSize(int(width_need), int(self.scroll_field.height()))
            elif self.scroll_field.width() > self.scroll_field.height():
                self.scroll_field.setWidgetResizable(False)
                self.game_field.setFixedSize(int(self.scroll_field.width()), int(height_need))
        else:
            self.game_field.setMinimumSize(0, 0)
            self.game_field.setMaximumSize(1000000, 1000000)
            self.scroll_field.setWidgetResizable(True)
    
    def resizeEvent(self, event):
        self.main_container.setGeometry(0, 0, self.width(), self.height())

        w = self.width()
        h = self.height()

        turn_label_width = int(w * 0.2)
        turn_label_heigth = int(h * 0.05)
        turn_label_x = (w - turn_label_width) // 2
        turn_label_y = int(h - h * 0.95)
        self.turn_label.setGeometry(turn_label_x, turn_label_y, turn_label_width, turn_label_heigth)

        player1Name_label_width = int(w * 0.25)
        player1Name_label_heigth = int(h * 0.05)
        player1Name_label_x = int(turn_label_x - w * 0.04 - player1Name_label_width)
        player1Name_label_y = int(h - h * 0.95)

        self.player1Name_label.setGeometry(player1Name_label_x, player1Name_label_y, player1Name_label_width, player1Name_label_heigth)

        player2Name_label_width = int(w * 0.25)
        player2Name_label_heigth = int(h * 0.05)
        player2Name_label_x = int(turn_label_x + turn_label_width + w * 0.04)
        player2Name_label_y = int(h - h * 0.95)
        self.player2Name_label.setGeometry(player2Name_label_x, player2Name_label_y, player2Name_label_width, player2Name_label_heigth)

        settings_btn_diameter = int(h * 0.08)
        settings_btn_x = int(w - w * 0.98)
        settings_btn_y = int(h - h * 0.97)
        self.settings_btn.setGeometry(settings_btn_x, settings_btn_y, settings_btn_diameter, settings_btn_diameter)

        settings_btn_radius = settings_btn_diameter // 2

        self.settings_btn.setStyleSheet(f"""
            .settings_btn {{
                border-radius: {settings_btn_radius}px;
                border-style: solid;
                border-width: 1px;
                border-color: #000000;
                font-family: Arial;
                background-color: #95A5A6;
                color: #000000;
            }}
            .settings_btn:hover {{
                background-color: #7f8c8d;
            }}

            .settings_btn:pressed {{
                background-color: #6c7b7d;
            }}
        """)

        self.settings_btn.setIconSize(QSize(settings_btn_diameter * 0.7, settings_btn_diameter * 0.7)) 

        PieRule_btn_width = int(w * 0.1)
        PieRule_btn_height = int(h * 0.1)
        PieRule_btn_x = int(w - w * 0.97)
        PieRule_btn_y = (h - PieRule_btn_height) // 2
        self.PieRule_btn.setGeometry(PieRule_btn_x, PieRule_btn_y, PieRule_btn_width, PieRule_btn_height)

        self.PieRule_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                border: 1px solid black;
                border-radius: 10px;
                font-family: Arial;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)

        GameField_width = int(w * 0.7)
        GameField_height = int(h * 0.8)
        GameField_x = (w - GameField_width) // 2
        GameField_y = int(h - h * 0.85)
        self.frame.setGeometry(GameField_x, GameField_y, GameField_width, GameField_height)
        self.frame.update()
        self.update()

        self.update_game_field()
        self.game_field.updateGeometry()

        return super().resizeEvent(event)