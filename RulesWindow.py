from PySide6.QtWidgets import QWidget, QDialog
from CustomWidgets import EditedButton, EditedTextEdit
from PySide6.QtCore import Qt

class RulesDialog(QDialog):
    def __init__(self, parent_width, parent_height, game_sounds):
        super().__init__()
        
        self.game_sounds = game_sounds

        self.main_container = QWidget(self)

        self.rules_text = EditedTextEdit(self.main_container, 0.04)
        self.exit_btn = EditedButton ("Назад", self.main_container, 0.6)

        self.exit_btn.clicked.connect(self.on_exit)
        self.exit_btn.setAutoDefault(False)
        
        self.rules_text.setReadOnly(True)

        self.resize(parent_width * 0.5, parent_height * 0.9)
        
        with open("rules.txt", "r", encoding='utf-8') as f:
            self.rules = f.read()
        
        self.rules_text.setPlainText(self.rules)

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

        exit_btn_width = int(w * 0.3)
        exit_btn_height = int(h * 0.05)
        exit_btn_x = (w - exit_btn_width) // 2
        exit_btn_y = int(h * 0.025)
        self.exit_btn.setGeometry(exit_btn_x, exit_btn_y, exit_btn_width, exit_btn_height)

        rules_width = int(w * 0.9)
        rules_height = int(h * 0.85)
        rules_x = (w - rules_width) // 2
        rules_y = int(h - h * 0.05 - rules_height)
        self.rules_text.setGeometry(rules_x, rules_y, rules_width, rules_height)

        return super().resizeEvent(event)

