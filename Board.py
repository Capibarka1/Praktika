from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPolygonF, QBrush, QPen, QPainter
from PySide6.QtCore import QPointF, Qt, Signal
from collections import deque

from Bots import random_bot, get_best_move, get_best_move_hard

class GameField(QWidget):

    turn_changed = Signal()
    victory = Signal()
    pie_rule_used = Signal()

    def __init__(self, parent, parent_width, parent_height, board, gamemode, board_size, 
                 color_1p, color_2p, current_player, pie_rule_is_used, game_sounds):
        super().__init__(parent)

        self.game_sounds = game_sounds
        self.board = board
        self.gamemode = gamemode
        self.parent_width = parent_width
        self.parent_height = parent_height
        self.board_size = board_size
        self.color_1p = color_1p
        self.color_2p = color_2p
        self.current_pl = current_player

        self.pie_rule_is_used = pie_rule_is_used

        self.poligons = []
        self.board = board

        self.field_size = min(self.width() // (pow(3, .5) * self.board_size), self.height() // self.board_size)

        self.r=self.field_size/2 # радиус вписанной окружности
        self.R=self.field_size/pow(3,.5) # радиус описанной окружности
        self.a=self.R # сторона шестиугольника

        self.x = self.width() / 2
        self.y = (self.height() / 2 - (self.board_size - 1) * self.r) + (self.height() % self.board_size) // 2
    
    def pie_rule(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 1:
                    self.board[i][j] = 2
                    self.current_pl = 3 - self.current_pl
                    self.pie_rule_is_used = True
                    self.turn_changed.emit()
                    self.color_1p, self.color_2p = self.color_2p, self.color_1p
                    self.update()
                    break
            if self.pie_rule_is_used:
                break
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # включает сглаживание при рисовании.

        x = self.x
        y = self.y
        start_x = x
        start_y = y

        horiz = 1.5 * self.a
        vert = pow(3,.5) * self.a // 2

        if self.poligons == []:
            for i in range(self.board_size):
                for j in range(self.board_size):
                    points = [
                        QPointF(self.x+self.a/2,self.y+self.r),
                        QPointF(self.x+self.R,self.y),
                        QPointF(self.x+self.a/2,self.y-self.r),
                        QPointF(self.x-self.a/2,self.y-self.r),
                        QPointF(self.x-self.R,self.y),
                        QPointF(self.x-self.a/2,self.y+self.r),
                    ]

                    self.x += horiz
                    self.y += vert

                    self.poligons.append([QPolygonF([                    
                        points[0], points[1], points[2], points[3], points[4], points[5],
                    ]), i, j])
                    
                self.x = x - horiz
                self.y = y + vert
                x = self.x
                y = self.y
            self.x = start_x
            self.y = start_y

        x = self.x
        y = self.y

        for i in range (self.board_size):
            for j in range (self.board_size):
                points = [
                    QPointF(self.x+self.a/2,self.y+self.r),
                    QPointF(self.x+self.R,self.y),
                    QPointF(self.x+self.a/2,self.y-self.r),
                    QPointF(self.x-self.a/2,self.y-self.r),
                    QPointF(self.x-self.R,self.y),
                    QPointF(self.x-self.a/2,self.y+self.r),
                    QPointF(self.x+self.a/2,self.y+self.r),
                ]

                self.x += horiz
                self.y += vert

                painter.setPen(QPen(Qt.black, 2)) 

                if self.board[i][j] == 1:
                    painter.setBrush(QBrush(self.color_1p))
                    for k in range(self.board_size ** 2):
                        if self.poligons[k][1] == i and self.poligons[k][2] == j:
                            painter.drawPolygon(self.poligons[k][0])
                elif self.board[i][j] == 2:
                    painter.setBrush(QBrush(self.color_2p))
                    for k in range(self.board_size ** 2):
                        if self.poligons[k][1] == i and self.poligons[k][2] == j:
                            painter.drawPolygon(self.poligons[k][0])
                else:
                    painter.setBrush(QBrush(Qt.white))
                    for k in range(self.board_size ** 2):
                        if self.poligons[k][1] == i and self.poligons[k][2] == j:
                            painter.drawPolygon(self.poligons[k][0])

                painter.setBrush(QBrush(Qt.NoBrush))

                if i == 0:
                    for k in range(6):
                        if k in [1, 2]:
                            painter.setPen(QPen(self.color_2p, 4))  
                            painter.drawLine(points[k], points[k+1])                
                if j == 0:
                    for k in range(6):
                        if k in [2, 3]:
                            painter.setPen(QPen(self.color_1p, 4))  
                            painter.drawLine(points[k], points[k+1])
                if j == self.board_size - 1:
                    for k in range(6):
                        if k in [0, 5]:
                            painter.setPen(QPen(self.color_1p, 4))  
                            painter.drawLine(points[k], points[k+1])
                if i == self.board_size - 1:
                    for k in range(6):
                        if k in [4, 5]:
                            painter.setPen(QPen(self.color_2p, 4))  
                            painter.drawLine(points[k], points[k+1])

            self.x = x - horiz
            self.y = y + vert
            x = self.x
            y = self.y
        self.x = start_x
        self.y = start_y
    
    def resizeEvent(self, event):
        self.field_size = min(self.width() // (pow(3, .5) * self.board_size), self.height() // self.board_size)

        self.r=self.field_size/2 # радиус вписанной окружности
        self.a=self.R = max(self.field_size/pow(3,.5), 10) # сторона шестиугольника

        if self.a == 10:
            self.field_size = 10 * pow(3,.5)
            self.r=self.field_size/2

        self.x = self.width() // 2
        self.y = (self.height() / 2 - (self.board_size - 1) * self.r)
        self.poligons.clear()
        self.update()
        return super().resizeEvent(event)

    def mousePressEvent(self, event):
        pos = event.position()
        for i in range(len(self.poligons)):
            if self.poligons[i][0].containsPoint(pos, Qt.OddEvenFill) and self.board[i // self.board_size][i % self.board_size] == 0:
                self.board[self.poligons[i][1]][self.poligons[i][2]] = self.current_pl
                if self.win_search(self.board_size, self.board, self.current_pl):
                    self.victory.emit()
                    return
                self.current_pl = 3 - self.current_pl
                self.turn_changed.emit()
                self.game_sounds.turn_sound.play()
                self.update()
                self.bot_turn()
                return

    def get_current_pl(self):
        return self.current_pl
    
    def get_turn(self):
        turn = 1
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] != 0:
                    turn += 1
        if self.pie_rule_is_used:
            turn += 1
        return turn
    
    def get_pierule_used(self):
        return self.pie_rule_is_used
    
    def get_board_info(self):
        info = {
            'cells': self.board,
            'current_player': self.current_pl,
            'first_turn': self.pie_rule_is_used
        }
        return info

    def bot_turn(self):
        if self.gamemode != 'player_vs_player' and self.current_pl == 2:
            match self.gamemode:
                case 'bot_easy':
                    self.bot_easy(self.board, self.board_size)
                case 'bot_medium':
                    if self.bot_medium(self.board, self.board_size) == 'pie_rule': 
                        return
                case 'bot_hard':
                    if self.bot_hard(self.board, self.board_size) == 'pie_rule': 
                        return
            if self.win_search(self.board_size, self.board, 2):
                self.victory.emit()
                return
            self.current_pl = 3 - self.current_pl
            self.turn_changed.emit()
            self.update()   

    def win_search(self, size: int, field_of_play: list[list], player_num: int) -> bool:

        q = deque()

        if player_num == 1:
            for i in range(size):
                if field_of_play[i][0] == player_num:
                    q.append([i, 0])
            if not q:
                return False
        else:
            for i in range(size):
                if field_of_play[0][i] == player_num:
                    q.append([0, i])
            if not q:
                return False
        
        steps = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
        visited = set()
        while len(q) > 0:
            t = q.popleft()
            for i in steps:
                row = t[0] + i[0] 
                col = t[1] + i[1]
                if row >= 0 and row < size and col >= 0 and col < size and field_of_play[row][col] == player_num:
                    new_key = (row, col)
                    if new_key not in visited:
                        if col == size - 1 and player_num == 1:
                            return True
                        elif row == size - 1 and player_num == 2:
                            return True
                        visited.add(new_key)
                        q.append((row, col))
    
    def bot_easy(self, board, board_size):
        cell = random_bot(board, board_size)
        self.board[cell[0]][cell[1]] = 2
        self.update()

    def bot_medium(self, board, board_size):
        cell = get_best_move(board, board_size, 2, self.get_turn())
        if cell == 'pie_rule':
            self.pie_rule_used.emit()
            return 'pie_rule'
        self.board[cell[0]][cell[1]] = 2
        self.update()

    def bot_hard(self, board, board_size):
        cell = get_best_move_hard(board, board_size, 2, self.get_turn(), 2)
        if cell == 'pie_rule':
            self.pie_rule_used.emit()
            return 'pie_rule'
        self.board[cell[0]][cell[1]] = 2
        self.update()