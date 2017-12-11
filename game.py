from board import Board
from alphaBetaAgent import AlphaBetaAgent
import time

def humansFight(game_board, player, gameOn, printName, printWin, changePlayer):
	while True:
			
			game_board.main_gui.update_idletasks()
			game_board.main_gui.update()

			if gameOn == 3:
				#white 0
				if player == 0:
					if printName:
						print("player 1")
						printName = False
						
					if(len(game_board.two_part_move) == 2):
						piece = game_board.two_part_move[0]
						move = game_board.two_part_move[1]
						is_valid_move = game_board.makeMove("white", piece, move, True)
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
						is_valid_move = game_board.makeMove("black", piece, move, True)
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

def humanAIFight(game_board, player, gameOn, printName, printWin, changePlayer):
	#one shot
	aB_agent = AlphaBetaAgent()
	aB_board = game_board.clone()
	#aB_agent_move = aB_agent.alphaBetaSearch(aB_board)
	#print("I AM FREE")
	#print (aB_agent_move)
	while True:
		
		game_board.main_gui.update_idletasks()
		game_board.main_gui.update()

		if gameOn == 3:
			#white 0
			if player == 0:
				if printName:
					print("##############################")		
					print("player 1")
					print("##############################")
					printName = False
					
				if(len(game_board.two_part_move) == 2):
					piece = game_board.two_part_move[0]
					move = game_board.two_part_move[1]
					is_valid_move = game_board.makeMove("white", piece, move, True)
					gameOn = game_board.checkWin(player)
					if(is_valid_move):
						changePlayer = True
					else:
						changePlayer = False
						print("invalid, try again")
			elif player == 1:
				if printName:
					print("##############################")
					print("player 2")
					printName = False
				aB_board = game_board.clone()
				
				depth = 1
				aB_agent_move = None
				start_time = time.time()
				print("# Start Time:", start_time)
				while(time.time() - start_time <= 10):
					print("\n##### Depth", depth, "#####")
					temp_move = aB_agent.alphaBetaSearch(aB_board, "black", depth, time.time())
					depth +=1
					if (aB_agent_move == None or temp_move[1] > aB_agent_move[1]):
						aB_agent_move = temp_move
				print("My Official Move is:",aB_agent_move)
				
				is_valid_move = game_board.makeMove("black", aB_agent_move[0][0], aB_agent_move[0][1], True)
				gameOn = game_board.checkWin(player)
				if(is_valid_move):
					changePlayer = True
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

def AIAIFight(game_board, player, gameOn, printName, printWin, changePlayer):
	#one shot
	aB_agent = AlphaBetaAgent()
	aB_board = game_board.clone()
	
	aB_agent_w = AlphaBetaAgent()
	aB_board_w = game_board.clone()

	while True:
		
		game_board.main_gui.update_idletasks()
		game_board.main_gui.update()

		if gameOn == 3:
			#white
			if player == 0:
				if printName:
					print("##############################")					
					print("player 1")
					printName = False
				aB_board_w = game_board.clone()
				
				depth = 1
				aB_agent_move = None
				start_time = time.time()
				print("# Start Time:", start_time)
				while(time.time() - start_time <= 10):
					print("\n##### Depth", depth, "#####")
					temp_move = aB_agent_w.alphaBetaSearch(aB_board_w, "white", depth, time.time())
					depth +=1
					if (aB_agent_move == None or temp_move[1] > aB_agent_move[1]):
						aB_agent_move = temp_move
				print("My Official Move is:",aB_agent_move)
				
				is_valid_move = game_board.makeMove("white", aB_agent_move[0][0], aB_agent_move[0][1], True)
				gameOn = game_board.checkWin(player)
				if(is_valid_move):
					changePlayer = True
				else:
					changePlayer = False
					print("invalid, try again")
			#black
			elif player == 1:
				if printName:
					print("##############################")		
					print("player 2")
					printName = False
				aB_board = game_board.clone()
				
				depth = 1
				aB_agent_move = None
				start_time = time.time()
				print("# Start Time:", start_time)
				while(time.time() - start_time <= 10):
					print("\n##### Depth", depth, "#####")
					temp_move = aB_agent.alphaBetaSearch(aB_board, "black", depth, time.time())
					depth +=1
					if (aB_agent_move == None or temp_move[1] > aB_agent_move[1]):
						aB_agent_move = temp_move
				print("My Official Move is:",aB_agent_move)

				is_valid_move = game_board.makeMove("black", aB_agent_move[0][0], aB_agent_move[0][1], True)
				gameOn = game_board.checkWin(player)
				if(is_valid_move):
					changePlayer = True
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



def main():
	game_board = Board()

	#go first go 2nd?
	go_first = None
	game_board.shouldIGoFirst()
	while go_first == None:
		game_board.start_gui.update_idletasks()
		game_board.start_gui.update()

		go_first = game_board.playerPicked()
		
	game_board.visual()

	game_board.printBoard()

	player = go_first

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

	#humansFight(game_board, player, gameOn, printName, printWin, changePlayer)
	humanAIFight(game_board, player, gameOn, printName, printWin, changePlayer)
	#AIAIFight(game_board, player, gameOn, printName, printWin, changePlayer)


if __name__ == '__main__':
	main()