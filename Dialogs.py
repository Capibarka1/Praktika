from PySide6.QtWidgets import QWidget, QDialog, QTextEdit
from PySide6.QtCore import Qt
from CustomWidgets import EditedButton, EditedTextEdit


class CustomDialog(QDialog):
    def __init__(self, parent_width, parent_height, type, game_sounds):
        super().__init__()
        self.setModal(True)

        self.game_sounds = game_sounds

        self.parent_width = parent_width
        self.parent_height = parent_height

        self.main_container = QWidget(self)

        self.message = EditedTextEdit(self.main_container, 0.1)

        self.accept_btn = EditedButton("Да", self.main_container, 0.4)
        self.decline_btn = EditedButton("Нет", self.main_container, 0.4)

        self.accept_btn.clicked.connect(self.accepting)
        self.decline_btn.clicked.connect(self.rejecting)

        self.message.setProperty("class", "message")

        match type:
            case "exit_MainMenu":
                self.message.setPlainText("Вы точно хотите выйти из игры?")
            case "exit_GameSettings":
                self.message.setPlainText("Вы хотите выйти? Все несохраненные изменения будут утеряны.")
            case "Leave":
                self.message.setPlainText("Вы уверены, что хотите выйти в главное меню? Несохранённый прогресс будет потерян.")
            case "Save":
                self.message.setPlainText("Сохранить текущее состояние игры?")
            case "New_game":
                self.message.setPlainText("Начать новую игру? Текущий сохранённый прогресс будет потерян.")
            case "Color_error":
                self.message.setPlainText("""Выбранный цвет слишком близок к цвету фишек, фона, не закрашенных ячеек 
                                          или цвету граней шестиугольников. Игровое поле может стать нечитаемым. Продолжить?""")

        self.message.setAlignment(Qt.AlignCenter) 

        self.message.setReadOnly(True)

        self.resize(parent_width * 0.5, parent_height * 0.5)

        self.message.setLineWrapMode(QTextEdit.WidgetWidth)

        self.setWindowFlag(Qt.FramelessWindowHint, True)
    
    def accepting(self):
        self.game_sounds.click_sound.play()
        self.accept()
    
    def rejecting(self):
        self.game_sounds.click_sound.play()
        self.reject()

    def resizeEvent(self, event):
        self.main_container.setGeometry(0, 0, self.width(), self.height())

        w = self.width()
        h = self.height()

        message_width = int(w * 0.75)
        message_height = int(h * 0.5)
        message_x = (w - message_width) // 2
        message_y = int(h - h * 0.9)
        self.message.setGeometry(message_x, message_y, message_width, message_height)

        accept_btn_width = int(w * 0.25)
        accept_btn_height = int(h * 0.2)
        accept_btn_x = (w - w * 0.8)
        accept_btn_y = int(h - h * 0.1 - accept_btn_height)
        self.accept_btn.setGeometry(accept_btn_x, accept_btn_y, accept_btn_width, accept_btn_height)

        decline_btn_width = int(w * 0.25)
        decline_btn_height = int(h * 0.2)
        decline_btn_x = (w - w * 0.2 - accept_btn_width)
        decline_btn_y = int(h - h * 0.1 - decline_btn_height)
        self.decline_btn.setGeometry(decline_btn_x, decline_btn_y, decline_btn_width, decline_btn_height)

        return super().resizeEvent(event)