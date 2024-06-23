if board[y][x][0] == opponent or board[y][x][0] == 0:
                    board_copy = copy.deepcopy(board)
                    alivePlayers_copy = copy.deepcopy(alivePlayers)
                    dummy_add(x, y, opponent)
                    eval, _ = minimax(depth - 1, alpha, beta, True, player)
                    
                    board = copy.deepcopy(board_copy)
                    alivePlayers = copy.deepcopy(alivePlayers_copy)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (x, y)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval, best_move
