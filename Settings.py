from PySide6.QtWidgets import QWidget, QDialog, QPushButton, QColorDialog, QScrollArea, QFrame
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from CustomWidgets import EditedLabel, EditedButton, EditedLineEdit, EditedComboBox
from Dialogs import CustomDialog


class SettingsWindow(QDialog):

    def __init__(self, parent_width, parent_height, gamemode, board_size, player1_color, 
                 player2_color, background_color, player1_name, player2_name, game_sounds):
        super().__init__()
        self.setModal(True)

        self.game_sounds = game_sounds

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.middle_widget = QWidget()
        self.scroll_area.setWidget(self.middle_widget)

        self.exit_btn = EditedButton("X", self, 0.6)
        self.title = EditedLabel("Настройки", self, 0.6)
        self.gamemode_label = EditedLabel("Режим игры", self.middle_widget, 0.4)

        self.gamemode = EditedComboBox(self.middle_widget, 0.35)
        self.gamemode.insertItem(0, "Игрок против игрока")
        self.gamemode.insertItem(1, "Бот (лёгкий)")
        self.gamemode.insertItem(2, "Бот (средний)")
        self.gamemode.insertItem(3, "Бот (сложный)")
        self.gamemode.setCurrentIndex(0)

        match gamemode:
            case "Player_vs_player":
                self.gamemode.setCurrentIndex(0)
            case "bot_easy":
                self.gamemode.setCurrentIndex(1)
            case "bot_medium":
                self.gamemode.setCurrentIndex(2)
            case "bot_hard":
                self.gamemode.setCurrentIndex(3)


        self.fieldsize_label = EditedLabel("Размер поля", self.middle_widget, 0.4)

        self.fieldsize = EditedComboBox(self.middle_widget, 0.35)
        self.fieldsize.insertItem(0, "9x9")
        self.fieldsize.insertItem(1, "11x11")
        self.fieldsize.insertItem(2, "13x13")
        self.fieldsize.insertItem(3, "15x15")
        self.fieldsize.insertItem(4, "17x17")

        match board_size:
            case 9:
                self.fieldsize.setCurrentIndex(0)
            case 11:
                self.fieldsize.setCurrentIndex(1)
            case 13:
                self.fieldsize.setCurrentIndex(2)
            case 15:
                self.fieldsize.setCurrentIndex(3)
            case 17:
                self.fieldsize.setCurrentIndex(4)
        

        self.player1_color_label = EditedLabel("Цвет 1 игрока", self.middle_widget, 0.4)
        self.player1_color = QPushButton(self.middle_widget)

        self.color1 = QColor(int(player1_color[1:3], 16), int(player1_color[3:5], 16), int(player1_color[5:7], 16))

        self.player1_color.setStyleSheet(f"""
            .QPushButton {{
                border: 1px solid black;
                background-color: rgb({self.color1.red()},{self.color1.green()},{self.color1.blue()});
            }}
        """)

        self.player2_color_label = EditedLabel("Цвет 2 игрока", self.middle_widget, 0.4)
        self.player2_color = QPushButton(self.middle_widget)

        self.color2 = QColor(int(player2_color[1:3], 16), int(player2_color[3:5], 16), int(player2_color[5:7], 16))

        self.player2_color.setStyleSheet(f"""
            .QPushButton {{
                border: 1px solid black;
                background-color: rgb({self.color2.red()},{self.color2.green()},{self.color2.blue()});
            }}
        """)

        self.bg_color_label = EditedLabel("Цвет фона игрового поля", self.middle_widget, 0.4)
        self.bg_color = QPushButton(self.middle_widget)

        self.bgcolor = QColor(int(background_color[1:3], 16), int(background_color[3:5], 16), int(background_color[5:7], 16))

        self.bg_color.setStyleSheet(f"""
            .QPushButton {{
                border: 1px solid black;
                background-color: rgb({self.bgcolor.red()},{self.bgcolor.green()},{self.bgcolor.blue()});
            }}
        """)

        self.name_player1_label = EditedLabel("Имя первого игрока", self.middle_widget, 0.4)
        self.name_player1 = EditedLineEdit(self.middle_widget, 0.35)
        self.name_player2_label = EditedLabel("Имя второго игрока", self.middle_widget, 0.4)
        self.name_player2 = EditedLineEdit(self.middle_widget, 0.35)
        self.save_btn = EditedButton("Сохранить", self, 0.6)

        self.resize(parent_width * 0.7, parent_height * 0.9)

        self.exit_btn.clicked.connect(self.exit)
        self.player1_color.clicked.connect(lambda: self.color_dialog('color1' , self.player1_color, self.color2, self.bgcolor, True))
        self.player2_color.clicked.connect(lambda: self.color_dialog('color2' , self.player2_color, self.color1, self.bgcolor, True))
        self.bg_color.clicked.connect(lambda: self.color_dialog('bgcolor', self.bg_color, self.color2, self.color1, False))
        self.save_btn.clicked.connect(self.save)

        self.gamemode_label.setProperty("class", "settings_labels")
        self.fieldsize_label.setProperty("class", "settings_labels")
        self.player1_color_label.setProperty("class", "settings_labels")
        self.player2_color_label.setProperty("class", "settings_labels")
        self.bg_color_label.setProperty("class", "settings_labels")
        self.name_player1_label.setProperty("class", "settings_labels")
        self.name_player2_label.setProperty("class", "settings_labels")

        self.name_player1.setProperty("class", "names")
        self.name_player2.setProperty("class", "names")

        self.name_player1.setMaxLength(20)
        self.name_player2.setMaxLength(20)
        self.name_player1.setText(player1_name)
        self.name_player2.setText(player2_name)

        self.name_player1.editingFinished.connect(lambda: self.on_name_changed(self.name_player1, "Игрок 1"))
        self.name_player2.editingFinished.connect(lambda: self.on_name_changed(self.name_player2, "Игрок 2"))

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.7);")
        self.overlay.hide()

        self.setWindowFlag(Qt.FramelessWindowHint, True)
    
    def on_name_changed(self, player_name, defaultname):
        if not player_name.text().strip():
            player_name.setText(defaultname)
    
    def is_low_contrast(self, c1, c2, sat_threshold=80, val_threshold=60, hue_threshold=30):

        h1 = c1.hue()
        s1 = c1.saturation()
        v1 = c1.value()
        h2 = c2.hue()
        s2 = c2.saturation()
        v2 = c2.value()

        if abs(v1 - v2) > val_threshold:
            return False

        if abs(s1 - s2) > sat_threshold:
            return False
        
        diff_hue = min(abs(h1 - h2), abs(360 - abs(h1 - h2)))
        if diff_hue > hue_threshold:
            return False

        return True
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.exit()
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def exit(self):
        self.overlay.setGeometry(0,0, self.width(), self.height())
        self.overlay.show()
        self.game_sounds.click_sound.play()
        dlg = CustomDialog(self.width(), self.height(), "exit_GameSettings", self.game_sounds)

        dlg.move(self.center.x() - dlg.width()//2, self.center.y() - dlg.height()//2)

        if dlg.exec() == QDialog.Accepted:
            self.close()
        
        self.overlay.hide()

    def save(self):
        self.game_sounds.click_sound.play()
        self.accept()
    
    def set_color(self, target_btn, new_color):
        target_btn.setStyleSheet(f"""
        .QPushButton {{
            border: 1px solid black;
            background-color: rgb({new_color.red()},{new_color.green()},{new_color.blue()});
            }}
        """)
        self.update()

    def color_dialog(self, target_color, target_btn, check_color1, check_color2, include_white):
        color_dlg = QColorDialog()
        color_dlg.setStyleSheet("QWidget { color: #000000; }")
        if color_dlg.exec() != QDialog.Accepted:
            return
        new_color = color_dlg.currentColor()

        checks = [check_color1, check_color2, QColor(0, 0, 0)]

        if include_white:
            checks.append(QColor(255, 255, 255))

        found = False
        for i in checks:
            if self.is_low_contrast(new_color, i):
                found = True
                break

        if found: 
            self.overlay.setGeometry(0,0, self.width(), self.height())
            self.overlay.show()
            dlg = CustomDialog(self.width(), self.height(), 'Color_error', self.game_sounds)
            if dlg.exec() == QDialog.Rejected:
                self.update()
                self.overlay.hide()
                return
        
        setattr(self, target_color, new_color)
        self.set_color(target_btn, new_color)
        self.overlay.hide()
        self.update()  

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()

        top_h = int(h * 0.13)
        bottom_h = int(h * 0.10)
        middle_h = h - top_h - bottom_h

        self.scroll_area.setGeometry(0, top_h, w, middle_h)

        current_y = int(h * 0.07)

        self.center = self.geometry().center()

        exit_btn_diameter = int(h * 0.08)
        exit_btn_x = int(w * 0.03)
        exit_btn_y = int(h * 0.03)
        self.exit_btn.setGeometry(exit_btn_x, exit_btn_y, exit_btn_diameter , exit_btn_diameter)
        self.exit_btn.setStyleSheet(f"border-radius: {exit_btn_diameter // 2}px; border: 1px solid black;")

        title_width = int(w * 0.5)
        title_height = int(h * 0.1)
        title_x = (w - title_width) // 2
        title_y = int(h - h * 0.97)
        self.title.setGeometry(title_x, title_y, title_width, title_height)

        gamemode_width = int(w * 0.35)
        gamemode_height = int(h * 0.06)
        gamemode_x = int(w - w * 0.1 - gamemode_width)
        self.gamemode.setGeometry(gamemode_x, current_y, gamemode_width, gamemode_height)

        gamemode_label_width = int(w * 0.40)
        gamemode_label_height = int(h * 0.05)
        gamemode_label_x = int(gamemode_x - w * 0.1 - gamemode_label_width)
        gamemode_label_y = int(current_y + gamemode_height // 2 - gamemode_label_height // 2)
        self.gamemode_label.setGeometry(gamemode_label_x, gamemode_label_y, gamemode_label_width, gamemode_label_height)

        current_y += gamemode_height + int(h * 0.03)

        fieldsize_width = int(w * 0.15)
        fieldsize_height = int(h * 0.06)
        fieldsize_x = int(w - w * 0.3 - fieldsize_width)
        self.fieldsize.setGeometry(fieldsize_x, current_y, fieldsize_width, fieldsize_height)

        fieldsize_label_width = int(w * 0.40)
        fieldsize_label_height = int(h * 0.05)
        fieldsize_label_x = int(fieldsize_x - w * 0.1 - fieldsize_label_width)
        fieldsize_label_y = int(current_y + fieldsize_height // 2 - fieldsize_label_height // 2)
        self.fieldsize_label.setGeometry(fieldsize_label_x, fieldsize_label_y, fieldsize_label_width, fieldsize_label_height)

        current_y += fieldsize_height + int(h * 0.03)

        player1_color_width = int(w * 0.1)
        player1_color_height = int(w * 0.1)
        player1_color_x = int(w - w * 0.35 - player1_color_width)
        self.player1_color.setGeometry(player1_color_x, current_y, player1_color_width, player1_color_height)

        player1_color_label_width = int(w * 0.40)
        player1_color_label_height = int(h * 0.05)
        player1_color_label_x = int(player1_color_x - w * 0.1 - player1_color_label_width )
        player1_color_label_y = int(current_y+ player1_color_height // 2 - player1_color_label_height // 2)
        self.player1_color_label.setGeometry(player1_color_label_x, player1_color_label_y, player1_color_label_width, player1_color_label_height)

        current_y += player1_color_height + int(h * 0.02)
    
        player2_color_width = int(w * 0.1)
        player2_color_height = int(w * 0.1)
        player2_color_x = int(w - w * 0.35 - player2_color_width)
        self.player2_color.setGeometry(player2_color_x, current_y, player2_color_width, player2_color_height)

        player2_color_label_width = int(w * 0.40)
        player2_color_label_height = int(h * 0.05)
        player2_color_label_x = int(player2_color_x - w * 0.1 - player2_color_label_width)
        player2_color_label_y = int(current_y + player2_color_height // 2 - player2_color_label_height // 2)
        self.player2_color_label.setGeometry(player2_color_label_x, player2_color_label_y, player2_color_label_width, player2_color_label_height)

        current_y += player2_color_height + int(h * 0.02)

        bg_color_width = int(w * 0.1)
        bg_color_height = int(w * 0.1)
        bg_color_x = int(w - w * 0.35 - bg_color_width)
        self.bg_color.setGeometry(bg_color_x, current_y, bg_color_width, bg_color_height)

        bg_color_label_width = int(w * 0.40)
        bg_color_label_height = int(h * 0.05)
        bg_color_label_x = int(bg_color_x - w * 0.1 - bg_color_label_width)
        bg_color_label_y = int(current_y + bg_color_height // 2 - bg_color_label_height // 2)
        self.bg_color_label.setGeometry(bg_color_label_x, bg_color_label_y, bg_color_label_width, bg_color_label_height)

        current_y += bg_color_height + int(h * 0.03)

        name_player1_width = int(w * 0.35)
        name_player1_height = int(h * 0.06)
        name_player1_x = int(w - w * 0.10 - name_player1_width)
        self.name_player1.setGeometry(name_player1_x, current_y, name_player1_width, name_player1_height)

        name_player1_label_width = int(w * 0.40)
        name_player1_label_height = int(h * 0.05)
        name_player1_label_x = int(name_player1_x - w * 0.1 - name_player1_label_width)
        name_player1_label_y = int(current_y + name_player1_height // 2 - name_player1_label_height // 2)
        self.name_player1_label.setGeometry(name_player1_label_x, name_player1_label_y, name_player1_label_width, name_player1_label_height)

        current_y += name_player1_height + int(h * 0.03)

        name_player2_width = int(w * 0.35)
        name_player2_height = int(h * 0.06)
        name_player2_x = int(w - w * 0.10 - name_player2_width)
        self.name_player2.setGeometry(name_player2_x, current_y, name_player2_width, name_player2_height)

        name_player2_label_width = int(w * 0.40)
        name_player2_label_height = int(h * 0.05)
        name_player2_label_x = int(name_player2_x - w * 0.1 - name_player2_label_width)
        name_player2_label_y = int(current_y + name_player2_height // 2 - name_player2_label_height // 2)
        self.name_player2_label.setGeometry(name_player2_label_x, name_player2_label_y, name_player2_label_width, name_player2_label_height)

        current_y += name_player2_height

        self.middle_widget.setFixedHeight(current_y + int(h * 0.03)) 

        save_btn_width = int(w * 0.35)
        save_btn_height = int(h * 0.07)
        save_btn_x = (w - save_btn_width) // 2
        save_btn_y = int(h - h * 0.03 - save_btn_height)
        self.save_btn.setGeometry(save_btn_x, save_btn_y, save_btn_width, save_btn_height)
        
        return super().resizeEvent(event)