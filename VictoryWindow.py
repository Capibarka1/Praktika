from PySide6.QtWidgets import QWidget, QDialog
from PySide6.QtCore import Qt
from CustomWidgets import EditedLabel, EditedButton


class VictoryWindow(QDialog):
    def __init__(self, parent_width, parent_height, winner_name, game_sounds):
        super().__init__()
        self.setModal(True)

        self.game_sounds = game_sounds

        self.main_container = QWidget(self)

        self.message = EditedLabel(f"{winner_name}\nпобедил!", self.main_container, 0.15)
        self.accept_btn = EditedButton("Главное меню", self.main_container, 0.5)

        self.accept_btn.clicked.connect(self.on_exit)

        self.message.setStyleSheet("border: 1px solid black")

        self.resize(parent_width * 0.4, parent_height * 0.3)

        self.setWindowFlag(Qt.FramelessWindowHint, True)

    def on_exit(self):
        self.game_sounds.click_sound.play()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.on_exit()
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.on_exit()
        else:
            super().keyPressEvent(event)
    
    def resizeEvent(self, event):
        self.main_container.setGeometry(0, 0, self.width(), self.height())

        w = self.width()
        h = self.height()

        message_width = int(w * 0.7)
        message_height = int(h * 0.5)
        message_x = (w - message_width) // 2
        message_y = int(h - h * 0.9)
        self.message.setGeometry(message_x, message_y, message_width, message_height)

        accept_btn_width = int(w * 0.60)
        accept_btn_height = int(h * 0.15)
        accept_btn_x = (w - accept_btn_width) // 2
        accept_btn_y = int(h - h * 0.1 - accept_btn_height)
        self.accept_btn.setGeometry(accept_btn_x, accept_btn_y, accept_btn_width, accept_btn_height)

        return super().resizeEvent(event)

