temp=alivePlayers
            for player in temp:
                if not boardCheck(board, player) and count>players:
                    alivePlayers.remove(player)
                    drawPieces(board)
                    winnerSub=screen.copy().subsurface(gameRect)
                if len(alivePlayers)==1:
                    screen.set_clip()
                    mode='winner'