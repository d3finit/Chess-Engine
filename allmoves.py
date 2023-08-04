else:
      for i in track(range(len(os.listdir("./full_games/"))), description="Loading full_games..."):
          f = open("./full_games/" + os.listdir("./full_games/")[i])

          temp_games = []

          run = True
          while run:
              game = chess.pgn.read_game(f)

              if game is None:
                  run = False

              temp_games.append(game)

          temp_games.pop()

          for temp_game in temp_games:
              temp_board = temp_game.board()
              for move in temp_game.mainline_moves():
                  if board == temp_board:
                      allmoves.append([move, -1])
                  else:
                      pass

                      temp_board.push(move)

                  if len(allmoves) >= 1:
                      break

      reccomended_moves = Sort_Tuple(allmoves)
      reccomended_moves.reverse()

      first_game.add_variation(chess.Move.from_uci(str(reccomended_moves[0][0])))
      board.push(chess.Move.from_uci(str(reccomended_moves[0][0])))
      clear()
      print(board)
      # print(f"I reccomend the move: {reccomended_moves[0][0]} with a confidence of {reccomended_moves[0][1]}")
