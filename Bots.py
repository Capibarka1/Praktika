from collections import deque
from copy import deepcopy
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

    dist_top = dist_for_bridges(board, size, player, True)
    dist_bottom = dist_for_bridges(board, size, player, False) 

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

def dist_for_bridges(board, size, player, start):
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

def get_best_move_hard(board, size, player, turn, depth):
    if turn == 2:
        for i in range(size):
            for j in range(size):
                if board[i][j] == 1:
                    if i > size // 4 and size - i > size // 4 and j > size // 4 and size - j > size // 4:
                        return "pie_rule"
                    
    enemy_groups = get_enemy_groups(board, size, player)

    min_i, max_i, min_j, max_j = start_borders(board, size)

    print('min_i итог =', min_i, '             max_i итог =', max_i)

    best_score = -999999

    top_moves = get_top_moves(board, size, player, min_i, max_i, min_j, max_j, enemy_groups)
    for v, i, j in top_moves:
        board[i][j] = player
        new_min_i = min(min_i, i)
        new_max_i = max(max_i, i)
        bonus = bonuses(board, size, player, [i, j], min_i, max_i, min_j, max_j, enemy_groups)
        print('bonus =', bonus)
        val = minimax(board, size, 3 - player, depth - 1, bonus, min_j, max_j, new_min_i, new_max_i, enemy_groups)
        print('val =', val)
        board[i][j] = 0
        if val > best_score:
            best_score = val
            best_move = [i, j]
    print(f'best = {best_score}')
    return best_move

def minimax(board, size, player, depth, score, min_x, max_x, enemy_min_x, enemy_max_x, enemy_groups):

    if depth == 0:
        return score
    
    moves = get_top_moves(board, size, player, min_x, max_x, enemy_min_x, enemy_max_x, enemy_groups)

    candidates = []
    for v, i, j in moves:
        board[i][j] = player
        new_min_x = min(min_x, i)
        new_max_x = max(max_x, i)
        bonus = bonuses(board, size, player, [i, j], min_x, max_x, enemy_min_x, enemy_max_x, enemy_groups)
        new_score = bonus + score
        val = minimax(board, size, 3 - player, depth - 1, new_score, enemy_min_x, enemy_max_x, new_min_x, new_max_x, enemy_groups)
        candidates.append([i, j, val])
        board[i][j] = 0
    
    if player == 1:
        candidates.sort(key=lambda x: x[2])
        return candidates[0][2]
    else:
        candidates.sort(reverse=True, key=lambda x: x[2])
        return candidates[0][2]

def bonuses(board, size, player, cell, min_x, max_x, enemy_min_x, enemy_max_x, enemy_groups):
    val = 0
    i = cell[0]
    j = cell[1]

    if check_groups(size, i, j, enemy_groups) == True:
        if enemy_max_x - enemy_min_x > size - 4:
            val += 500
            if player == 1:
                if j < min_x:
                    val += 200
                if j > max_x:
                    val += 200
            if player == 2:
                if i < min_x:
                    val += 200
                if i > max_x:
                    val += 200

    if enemy_max_x - enemy_min_x > size // 2:
        if player == 1:
            if i == enemy_max_x + 1 and board[i-1][j] == 2:
                val += 100
            if i == enemy_min_x - 1 and board[i+1][j] == 2:
                val += 100
        elif player == 2:
            if j == enemy_max_x + 1 and board[i][j-1] == 1:
                val += 100
            if j == enemy_min_x - 1 and board[i][j+1] == 1:
                val += 100

    steps = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    val_neighbors = 0
    neighbours_count = 0
    for r, c in steps:
        row = i + r
        col = j + c
        if row >= 0 and row < size and col >= 0 and col < size and board[row][col] == player:
            val_neighbors += 1
            neighbours_count += 10
        if row >= 0 and row < size and col >= 0 and col < size and board[row][col] == 3 - player:
            val_neighbors -= 8
    val += val_neighbors

    if player == 1:
        if min_x == size or max_x == -1:
            val = -5 * (abs(i - size // 2) + abs(j - size // 2))
        else:
            if j < min_x and neighbours_count > 0:
                val += (min_x - j) * 20
            if j > max_x and neighbours_count > 0:
                val += (j - max_x) * 20
    else:
        if min_x == size or max_x == -1:
            val = -5 * (abs(i - size // 2) + abs(j - size // 2))
        else:
            if i < min_x and neighbours_count > 0:
                val += (min_x - i) * 20
            if i > max_x and neighbours_count > 0:
                val += (i - max_x) * 20       
    
    if enemy_max_x - enemy_min_x > size // 2:
        if player == 2:
            if j == enemy_max_x + 1:
                val += (j - enemy_max_x) * 30
            if j == enemy_min_x - 1:
                val += (enemy_min_x - j) * 30
        else:
            if i == enemy_max_x + 1:
                val += (i - enemy_max_x) * 30
            if i == enemy_min_x - 1:
                val += (enemy_min_x - i) * 30            
 
    if bridge(board, size, i, j, player):
        val += 45

    if bridge_make(board, size, i, j, player):
        if player == 1:
            if j < min_x:
                val += (min_x - j) * 30
            if j > max_x:
                val += (j - max_x) * 30
        else:
            if i < min_x:
                val += (min_x - i) * 30
            if i > max_x:
                val += (i - max_x) * 30        
    
    if defend_bridge(board, size, i, j, player):
        val += 300

    return val

def start_borders(board, size):
    min_i = size
    max_i = -1
    min_j = size
    max_j = -1
    for i in range(size):
        for j in range(size):
            if board[i][j] == 2:
                if i < min_i:
                    min_i = i
                if i > max_i:
                    max_i = i
            if board[i][j] == 1:
                if j < min_j:
                    min_j = j
                if j > max_j:
                    max_j = j
    
    return [min_i, max_i, min_j, max_j]

def get_top_moves(board, size, player, min_x, max_x, enemy_min_x, enemy_max_x, enemy_groups, moves_count=80):
    moves = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                score = bonuses(board, size, player, [i, j], min_x, max_x, enemy_min_x, enemy_max_x, enemy_groups)
                moves.append([score, i, j])
    moves.sort(reverse=True, key=lambda x: x[0])
    moves = moves[:moves_count]
    return moves

def bridge(board, size, i, j, player):
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
        if neighbours[k] == 1 and neighbours[(k+1) % 6] == 0 and neighbours[(k+2) % 6] == 1:
            return True
    return False

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
    steps = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    while len(q) > 0:
        t = q.popleft()
        for k in steps:
            row = t[0] + k[0] 
            col = t[1] + k[1]
            if row >= 0 and row < size and col >= 0 and col < size and board[row][col] == 3 - player:
                if board[i][j] == 3 - player and enemy_board[i][j] == 0:
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