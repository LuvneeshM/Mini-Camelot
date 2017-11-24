from board import Board

def main():
	game_board = Board()
	game_board.printBoard()

	player = 0

	while True:
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

if __name__ == '__main__':
	main()