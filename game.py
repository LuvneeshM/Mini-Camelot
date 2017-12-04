from board import Board



def main():
	game_board = Board()

	game_board.visual()

	game_board.printBoard()

	player = 0

	changePlayer = False

	printName = True
	printWin = True
	'''
		Draw = 0
		White = 1
		Black = 2
		Continue  = 3
	'''
	gameOn = 3

	while True:
		
		game_board.main_gui.update_idletasks()
		game_board.main_gui.update()

		if gameOn == 3:
			#white 0
			if player == 0:
				if printName:
					print("player 1")
					printName = False
					print ((game_board.getDictOfAllMoves("white").values()))
				if(len(game_board.two_part_move) == 2):
					piece = game_board.two_part_move[0]
					move = game_board.two_part_move[1]
					is_valid_move = game_board.makeMove("white", piece, move)
					gameOn = game_board.checkWin(player)
					if(is_valid_move):
						changePlayer = True
						print ("valid")
					else:
						changePlayer = False
						print("invalid, try again")
			elif player == 1:
				if printName:
					print("player 2")
					printName = False
				if(len(game_board.two_part_move) == 2):
					piece = game_board.two_part_move[0]
					move = game_board.two_part_move[1]
					is_valid_move = game_board.makeMove("black", piece, move)
					gameOn = game_board.checkWin(player)
					if(is_valid_move):
						changePlayer = True
						print("valid")
					else: 
						changePlayer = False
						print("invalid, try again")

			if changePlayer == True:
				player = (player+1)%2
				changePlayer = False
				printName = True
		elif gameOn == 0 and printWin:
			print("Draw")
			game_board.makeCanvasWinner("Its a Draw")
			printWin = False
		elif gameOn == 1 and printWin:
			print("White Wins")
			game_board.makeCanvasWinner("Player Wins")
			printWin = False
		elif gameOn == 2 and printWin:
			print("Black Wins")
			game_board.makeCanvasWinner("AI Wins")
			printWin = False

		
		'''
		#white 1
		if player == 0:
			print("player_1")
			piece = tuple(int(x.strip()) for x in input("pick piece ").split(','))
			move = tuple(int(x.strip()) for x in input("make move ").split(','))
			while(game_board.makeMove("white", piece, move) == False):
				piece = tuple(int(x.strip()) for x in input("pick piece ").split(','))
				move = tuple(int(x.strip()) for x in input("make move ").split(','))
		elif player == 1:
			print("player_2")
			piece = tuple(int(x.strip()) for x in input("pick piece ").split(','))
			move = tuple(int(x.strip()) for x in input("make move ").split(','))
			while(game_board.makeMove("black", piece, move) == False):
				piece = tuple(int(x.strip()) for x in input("pick piece ").split(','))
				move = tuple(int(x.strip()) for x in input("make move ").split(','))
		player = (player+1)%2
		'''
if __name__ == '__main__':
	main()