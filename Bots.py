from collections import deque
from random import choice

###################### Лёгкий бот #####################

def random_bot(board, size):
    free_cells = list()
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                free_cells.append([i, j])
    cell = choice(free_cells)
    return cell

###################### Средний бот #####################

def get_best_move(board, size, player, turn):

    if turn == 2:
        return "pie_rule"

    center = size // 2 + 1
    candidates = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                board[i][j] = player
                val = -distance(board, size, 2) + distance(board, size, 1)
                candidates.append([i, j, val])
                board[i][j] = 0

    candidates.sort(reverse=True, key=lambda x: x[2])
    best_value = -9999999
    bonus_dist = 0
    best_move = None
    old_val = distance(board, size, 2)

    dist_top = dist_to_win(board, size, player, True)
    dist_bottom = dist_to_win(board, size, player, False) 

    for k in range(min(40, len(candidates))):
        i = candidates[k][0]
        j = candidates[k][1]
        val = candidates[k][2]

        optimal_distance = distance(board, size, player)
        if dist_top[i][j] + dist_bottom[i][j] == optimal_distance:
            bonus_dist = 0.5

        board[i][j] = 3 - player
        new_val = distance(board, size, 2)
        bonus_blocked = (new_val - old_val)
        board[i][j] = 0

        bonus_center = -0.3 * (abs(i - center) + abs(j - center))
        
        val = val + bonus_center + bonus_blocked + bonus_dist
        if val > best_value:
            best_value = val
            best_move = [i, j]
    return best_move

def distance(board, size, player):
    directions = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    q = deque()
    dist = [[-1]*size for i in range(size)]
    
    if player == 1:
        for i in range(size):
            if board[i][0] == 0 or board[i][0] == player:
                q.append((i, 0))
                if board[i][0] == player:
                    dist[i][0] = 0
                else:
                    dist[i][0] = 1
    else:
        for i in range(size):
            if board[0][i] == 0 or board[0][i] == player:
                q.append((0, i))
                if board[0][i] == player:
                    dist[0][i] = 0
                else:
                    dist[0][i] = 1

    while q:
        row, col = q.popleft()
        if player == 1 and col == size - 1:
            return dist[row][col]
        if player == 2 and row == size - 1:
            return dist[row][col]
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            if 0 <= new_row < size and 0 <= new_col < size and dist[new_row][new_col] == -1:
                if board[new_row][new_col] == 0:
                    dist[new_row][new_col] = dist[row][col] + 1
                    q.append((new_row, new_col))
                elif board[new_row][new_col] == player:
                    dist[new_row][new_col] = dist[row][col]
                    q.appendleft((new_row, new_col))
    return size * 2

def dist_to_win(board, size, player, start):
    q = deque()
    dist = [[-1]*size for i in range(size)]

    if start:
        for i in range(size):
            if board[0][i] in [player, 0]:
                q.append([0, i])
                if board[0][i] == player:
                    dist[0][i] = 0
                else:
                    dist[0][i] = 1
        if not q:
            return None
    else:
        for i in range(size):
            if board[size - 1][i] in [player, 0]:
                q.append([size - 1, i])
                if board[size - 1][i] == player:
                    dist[size - 1][i] = 0
                else:
                    dist[size - 1][i] = 1                
        if not q:
            return None
        
    steps = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]

    while len(q) > 0:
        r, c = q.popleft()
        for i in steps:
            row = r + i[0]
            col = c + i[1]
            if row >= 0 and row < size and col >= 0 and col < size and dist[row][col] == -1:
                if board[row][col] == 0:
                    dist[row][col] = dist[r][c] + 1
                    q.append((row, col))
                elif board[row][col] == player:
                    dist[row][col] = dist[r][c]
                    q.appendleft((row, col))
    
    return dist


###################### Сложный бот #####################

def get_best_move_hard(board, size, player, turn):
    if turn == 2:
        for i in range(size):
            for j in range(size):
                if board[i][j] == 1:
                    if i > size // 4 and size - i > size // 4 and j > size // 4 and size - j > size // 4:
                        return "pie_rule"
                    
    enemy_groups = get_enemy_groups(board, size, player)

    max_j, min_j, gap_j = startpos(board, size, 3 - player)

    max_i = -1
    min_i = size
    for i in range(size):
        for j in range(size):
            if board[i][j] == 2:
                if i > max_i: 
                    max_i = i
                if i < min_i: 
                    min_i = i

    old_val = distance(board, size, 2)

    enemy_dist = distance(board, size, 1)

    candidates = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                board[i][j] = player
                val = (-distance(board, size, 2) + distance(board, size, 1)) * 25
                candidates.append([i, j, val])
                board[i][j] = 0

    candidates.sort(reverse=True, key=lambda x: x[2])
    best_value = -9999999
    bonus_dist = 0
    best_move = None
    old_val = distance(board, size, 2)

    dist_top = dist_to_win(board, size, player, True)
    dist_bottom = dist_to_win(board, size, player, False) 

    for k in range(min(40, len(candidates))):
        i = candidates[k][0]
        j = candidates[k][1]
        val = candidates[k][2]

        optimal_distance = distance(board, size, player)
        if dist_top[i][j] + dist_bottom[i][j] == optimal_distance:
            bonus_dist = 75
        else:
            bonus_dist = 0

        board[i][j] = 3 - player
        new_val = distance(board, size, 2)
        bonus_blocked = (new_val - old_val)
        board[i][j] = 0
        
        val = val +  bonus_blocked + bonus_dist + bonuses(board, size, player, [i, j], max_j, min_j, gap_j, 
                                                        enemy_groups, optimal_distance, enemy_dist)
        if val > best_value:
            best_value = val
            best_move = [i, j]
    return best_move      

# Получение бонусов

def bonuses(board, size, player, cell, enemy_max_x, 
            enemy_min_x, enemy_gap, enemy_groups, old_distance, enemy_dist):
    val = 0
    i = cell[0]
    j = cell[1] 
    
    board[i][j] = player
    new_dist = distance(board, size, player)
    new_enemy_dist = distance(board, size, 3 - player)
    board[i][j] = 0

    if bridge_make(board, size, i, j, player):
        if new_dist < old_distance:
            val += 110

    if defend_bridge(board, size, i, j, player):
        val += 250

    if enemy_gap < 2 and player == 2:
        if j == enemy_max_x + 1 or j == enemy_min_x - 1:
            val += 300
        elif j == enemy_max_x + 2 or j == enemy_min_x - 2:
            val += 200    
    
    if new_enemy_dist == 0:
        val += 1000

    if enemy_gap <= 3:
        if check_groups(size, i, j, enemy_groups):
            val += 500
        if enemy_dist < new_enemy_dist:
            val += 300

    return val

# Получение стартовых границ

def startpos(board, size, player):
    q = deque()
    group_board = [[0]*size for k in range(size)]

    for i in range(size):
        if board[i][0] == 1:
            q.append([i, 0])
            if board[i][0] == player:
                group_board[i][0] = player

    steps = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    while len(q) > 0:
        t = q.popleft()
        for k in steps:
            row = t[0] + k[0] 
            col = t[1] + k[1]
            if row >= 0 and row < size and col >= 0 and col < size and board[row][col] == player:
                if group_board[row][col] == player:
                    continue
                group_board[row][col] = player
                q.append((row, col))
     
    max_x = -1
    
    for i in range(size):
        for j in range(size):
            if group_board[i][j] == player and j > max_x:
                max_x = j
    
    q = deque()
    group_board = [[0]*size for k in range(size)]

    for i in range(size):
        if board[i][size - 1] == 1:
            q.append([i, size - 1])
            if board[i][size - 1] == player:
                group_board[i][size - 1] = player 

    steps = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    while len(q) > 0:
        t = q.popleft()
        for k in steps:
            row = t[0] + k[0] 
            col = t[1] + k[1]
            if row >= 0 and row < size and col >= 0 and col < size and board[row][col] == player:
                if group_board[row][col] == player:
                    continue                
                group_board[row][col] = player
                q.append((row, col))
    
    min_x = size
    
    for i in range(size):
        for j in range(size):
            if group_board[i][j] == player and j < min_x:
                min_x = j

    return max_x, min_x, min_x - max_x

# Постройка и защита мостов

def bridge_make(board, size, i, j, player):
    steps = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    for k in range(6):
        row = i + steps[k][0]
        col = j + steps[k][1]
        if row >= 0 and row < size and col >= 0 and col < size and board[row][col] == 0:
            row2 = row + steps[(k+1) % 6][0]
            col2 = col + steps[(k+1) % 6][1]
            if row2 >= 0 and row2 < size and col2 >= 0 and col2 < size and board[row2][col2] == player:
                return True
    return False

def defend_bridge(board, size, i, j, player):
    steps = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    neighbours = []
    for r, c in steps:
        row = i + r
        col = j + c
        if row >= 0 and row < size and col >= 0 and col < size and board[row][col] == player:
            neighbours.append(1)
        elif row >= 0 and row < size and col >= 0 and col < size and board[row][col] == 3 - player:
            neighbours.append(2)
        else:
            neighbours.append(0)
    for k in range(6):
        if neighbours[k] == 1 and neighbours[(k+1) % 6] == 2 and neighbours[(k+2) % 6] == 1:
            return True
    return False

# Проверка групп

def get_enemy_groups(board, size, player):
    enemy_groups = [[0]*size for i in range(size)]
    group_number = 1
    for i in range(size):
        for j in range(size):
            if board[i][j] == 3 - player and enemy_groups[i][j] == 0:
                enemy_groups = group_search(board, size, i, j, player, enemy_groups, group_number)
                group_number += 1
    return enemy_groups

def group_search(board, size, i, j, player, enemy_board, group_number):
    q = deque()
    q.append([i, j])
    enemy_board[i][j] = group_number
    steps = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    while len(q) > 0:
        t = q.popleft()
        for k in steps:
            row = t[0] + k[0] 
            col = t[1] + k[1]
            if row >= 0 and row < size and col >= 0 and col < size and board[row][col] == 3 - player:
                if board[row][col] == 3 - player and enemy_board[row][col] == 0:
                    enemy_board[row][col] = group_number
                    q.append((row, col))
    
    return enemy_board

def check_groups(size, i, j, enemy_board):
    groups = []
    steps = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    for k in steps:
        row = i + k[0] 
        col = j + k[1]
        if row >= 0 and row < size and col >= 0 and col < size:
            if enemy_board[row][col] != 0 and enemy_board[row][col] not in groups:
                groups.append(enemy_board[row][col])
    if len(groups) > 1:
        return True
    return False