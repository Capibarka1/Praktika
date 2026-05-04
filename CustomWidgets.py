from PySide6.QtWidgets import QPushButton, QLabel, QTextEdit, QWidget, QFrame, QHBoxLayout, QLineEdit, QComboBox
from PySide6.QtGui import QFontMetrics, QColor, QBrush, QPen, QGuiApplication, QPainter
from PySide6.QtCore import Qt, QPoint, QPointF

class PlayerNameLabel(QWidget):
    def __init__(self, player_name, color, parent=None, font_scale=0.4, current=True):

        self.color = color

        super().__init__(parent)
        self.frame = QFrame(self)
        if current:
            self.frame.setStyleSheet(f"border: 3px solid {color}; background-color: #f0f0f0;")
        else:
            self.frame.setStyleSheet("border: 1px solid black; background-color: #f0f0f0;")

        layout = QHBoxLayout(self.frame)
        layout.setContentsMargins(5,0,5,0)

        self.indicator = QWidget()
        self.indicator.setStyleSheet(f"background-color: {color}; border: 3px solid black;")
        layout.addWidget(self.indicator)

        self.name_label = EditedLabel(player_name, self.frame, font_scale)
        self.name_label.setStyleSheet("border-width: 0px; qproperty-alignment: AlignVCenter")
        layout.addWidget(self.name_label)
        self.update()

    def set_current(self, is_current):
        if is_current:
            self.frame.setStyleSheet(f"border: 3px solid {self.color}; background-color: #f0f0f0;")
        else:
            self.frame.setStyleSheet("border: 1px solid black; background-color: #f0f0f0;")
    
    def swich_colors(self, color, curr):
        self.color = color
        self.set_current(curr)
        self.indicator.setStyleSheet(f"background-color: {self.color}; border: 3px solid black;")
        self.update()

    def resizeEvent(self, event):
        self.frame.setGeometry(0, 0, self.width(), self.height())
        sqr_size = int(self.height() * 0.3)
        self.indicator.setFixedSize(sqr_size, sqr_size)
        super().resizeEvent(event)

class EditedLabel(QLabel):
    def __init__(self, text, parent=None, font_scale=0.5):
        super().__init__(parent)
        self.full_text = text
        self.font_scale = font_scale
        self.setText(text)
        self.update()

    def resizeEvent(self, event):
        new_size = self.height() * self.font_scale
        new_size = max(12, new_size)
        font = self.font()
        font.setPointSizeF(new_size)
        self.setFont(font)

        if '\n' in self.full_text:
            self.setText(self.full_text)
        else:
            fm = QFontMetrics(self.font())
            available_width = self.width()
            elided = fm.elidedText(self.full_text, Qt.ElideRight, available_width)
            self.setText(elided)
        super().resizeEvent(event)

    def change_name(self, new_name):
        self.full_text = "Ход: " + new_name
        new_size = self.height() * self.font_scale
        new_size = max(12, new_size)
        font = self.font()
        font.setPointSizeF(new_size)
        self.setFont(font)

        if '\n' in self.full_text:
            self.setText(self.full_text)
        else:
            fm = QFontMetrics(self.font())
            available_width = self.width()
            elided = fm.elidedText(self.full_text, Qt.ElideRight, available_width)
            self.setText(elided)

class EditedTextEdit(QTextEdit):
    def __init__(self, parent=None, font_scale=0.5):
        super().__init__(parent)
        self.font_scale = font_scale
        self.update()

    def resizeEvent(self, event):
        new_size = self.height() * self.font_scale
        new_size = max(12, new_size)
        font = self.font()
        font.setPointSizeF(new_size)
        self.setFont(font)
        super().resizeEvent(event)

class EditedLineEdit(QLineEdit):
    def __init__(self, parent=None, font_scale=0.5):
        super().__init__(parent)
        self.font_scale = font_scale
        self.update()

    def resizeEvent(self, event):
        new_size = self.height() * self.font_scale
        new_size = max(12, new_size)
        font = self.font()
        font.setPointSizeF(new_size)
        self.setFont(font)
        super().resizeEvent(event)

class EditedButton(QPushButton):
    def __init__(self, text, parent=None, font_scale=0.5, min_font_size=12):
        super().__init__(parent)
        self.full_text = text
        self.font_scale = font_scale
        self.min_font_size = min_font_size
        self.update()

    def resizeEvent(self, event):
        new_size = self.height() * self.font_scale
        new_size = max(self.min_font_size, new_size)
        font = self.font()
        font.setPointSizeF(new_size)
        self.setFont(font)

        if '\n' in self.full_text:
            self.setText(self.full_text)
        else:
            fm = QFontMetrics(self.font())
            available_width = self.width()
            elided = fm.elidedText(self.full_text, Qt.ElideRight, available_width)
            self.setText(elided)
        super().resizeEvent(event)

class EditedComboBox(QComboBox):
    def __init__(self, parent=None, font_scale=0.35):
        super().__init__(parent)
        self.font_scale = font_scale
        self.setStyleSheet("QComboBox {padding-left: 5px;}")
        self.update()

    def resizeEvent(self, event):
        new_size = self.height() * self.font_scale
        new_size = max(12, new_size)
        font = self.font()
        font.setPointSizeF(new_size)
        self.setFont(font)
        super().resizeEvent(event)

class VolumeSlider(QWidget):
    def __init__(self, parent, game_sounds, type_sl, settings, save_sounds, value=1):
        super().__init__(parent)
        self.value = value
        self.type_sl = type_sl
        self.settings = settings
        self.save_sounds = save_sounds
        self.game_sounds = game_sounds
        self.drag_event = False
        self.track_width = 0
        self.track_height = 0
        self.track_y = 0
        self.track_x = 0
        self.circle_radius = 0
        self.circle_center = QPointF(0, 0)

        screen = QGuiApplication.primaryScreen()
        self.screen_width = screen.size().width()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        self.track_height = int(h * 0.4)
        self.track_width = w * 0.8
        self.track_x = w * 0.1
        self.circle_radius = self.track_height

        r = self.track_height // 2
        
        self.track_y = (h - self.track_height) // 2
        self.circle_center = QPointF(self.track_width * self.value + self.track_x, self.track_y + (self.track_height // 2))

        painter.setBrush(QBrush(QColor("#D9D9D9")))
        painter.setPen(QPen(Qt.black, 2))

        painter.drawRoundedRect(self.track_x, self.track_y, self.track_width, self.track_height, r, r)
        painter.drawEllipse(QPoint(self.circle_center.x(), self.circle_center.y()), self.circle_radius, self.circle_radius)

        return super().paintEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            dx = event.position().x() - self.circle_center.x()
            dy = event.position().y() - self.circle_center.y()
            if dx ** 2 + dy ** 2 <= (self.track_height) ** 2:
                self.drag_event = True
                self.start_value = self.value
                self.start_x = event.globalPosition().x()
                self.update()
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        if self.drag_event == True and self.type_sl == 'sound_effects':
            self.game_sounds.change_volume(self.type_sl, self.value)
            self.settings['sounds'] = self.value * 100
            self.save_sounds(self.settings)
        if self.drag_event == True and self.type_sl == 'music':
            self.game_sounds.change_volume(self.type_sl, self.value)
            self.settings['music'] = self.value * 100
            self.save_sounds(self.settings)
        self.drag_event = False
        self.update()
        return super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.drag_event:
            if self.track_width > 50:
                pos = event.position()
                min_x = self.track_x
                max_x = self.track_width + self.track_x
                new_x = max(min_x, min(max_x, pos.x()))
                self.value = round((new_x - min_x) / self.track_width, 2)
                self.update()
            else:
                delta = event.globalPosition().x() - self.start_x
                delta_val = ((100 / self.screen_width) * delta) / 100
                new_value = self.start_value + delta_val
                new_value = max(0.0, min(1.0, new_value))
                self.value = round(new_value, 2)
                self.update()   
        if self.drag_event and self.type_sl == 'music':
            self.game_sounds.change_volume(self.type_sl, self.value)
        if self.drag_event and self.type_sl == 'sound_effects':
            self.game_sounds.change_volume(self.type_sl, self.value)
        return super().mouseMoveEvent(event)
    
    def get_volume(self):
        return self.value
