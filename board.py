import numpy as np
import copy
import tkinter as tk
from tkinter import *

class Board:

	def __init__(self):
		#grid dimensions
		self.rows = 14
		self.cols = 8

		self.white_color = "White"
		self.black_color = "Black"

		self.board = np.array([[0 for x in range(self.cols)] for y in range(self.rows)])
		#dictionary for the pieces
		#key = tuple of location
		#value = name of piece, white_# or black_#
		self.white_pieces = {}
		self.black_pieces = {}

		self.all_buttons = {}

		#positions outside the game
		self.unplayable_block = [
			(0,0), (0,1), (0,2), (0,5), (0,6), (0,7),
			(1,0), (1,1), (1,6), (1,7),
			(2,0), (2,7),
			(11,0), (11,7),
			(12,0), (12,1), (12,6), (12,7),
			(13,0), (13,1), (13,2), (13,5), (13,6), (13,7)
		]
		#white player castle
		self.white_castle = [(0,3),(0,4)]
		#black player castle
		self.black_castle = [(13,3),(13,4)]

		#track the two pieces to swap for the player
		self.two_part_move = []
		self.two_part_color = []

		#track player pieces
		self.addPiece("white_1", 4,2)
		self.addPiece("white_2", 4,3)
		self.addPiece("white_3", 4,4)
		self.addPiece("white_4", 4,5)
		self.addPiece("white_5", 5,3)
		self.addPiece("white_6", 5,4)	
		#track ai pieces
		self.addPiece("black_1", 8,3)
		self.addPiece("black_2", 8,4)
		self.addPiece("black_3", 9,2)
		self.addPiece("black_4", 9,3)
		self.addPiece("black_5", 9,4)
		self.addPiece("black_6", 9,5)

		self.setUpBoard()

	#for ai stuff eventually
	def clone(self):
		deep_tmp = Board()
		deep_tmp.board = copy.deepcopy(self.board)
		deep_tmp.board = copy.deepcopy(self.white_pieces)
		deep_tmp.board = copy.deepcopy(self.black_pieces)

	#used to show board on terminal
	def printBoard(self):
		print(self.board)

	# ####################################################################################################################################
	# visual the game
	# ####################################################################################################################################
	def visual(self):
		
		sq_size = 40
		h = sq_size*self.rows
		w = sq_size*self.cols
		self.main_gui = tk.Tk()
		self.main_gui.geometry(str(w)+"x"+str(h))
		self.main_gui.title("Camelot")
		
		canvas = tk.Canvas(self.main_gui, width=w,height=h, background="White")
		
		self.uiMakeCanvas(canvas, "LightBlue", sq_size)

		canvas.pack()
		
	#Event Handlers
	#User clicked one of their pieces
	def clickPiece(self, row, col):
		self.two_part_move.append((row,col))
		self.two_part_color.append(self.all_buttons[(row,col)].cget("bg"))
		self.all_buttons[(row,col)].configure(bg="Yellow")

		return (row, col)
	
	def uiMakeCanvas(self, canvas, color, sq_size):
		for row in range(self.rows):
			for col in range(self.cols):

				makeButton = False
				button = tk.Button(text="%s,%s" % (row,col), bg=color, fg="Magenta")
				button.configure(width=sq_size, height=sq_size, activebackground="#33B5E5")
				#white player
				if ((row,col) in self.white_pieces):
					makeButton = True
					button.configure(bg=self.white_color, command=lambda row=row, col=col: self.clickPiece(row,col))
				#black player
				elif ((row,col) in self.black_pieces):
					makeButton = True
					button.configure(bg=self.black_color, command=lambda row=row, col=col: self.clickPiece(row,col))
				#empty board pieces
				elif ((row, col) not in self.unplayable_block):
					makeButton = True
					button.configure(bg=color, command=lambda row=row, col=col: self.clickPiece(row,col))
				#only make button if it is inside the game board
				if makeButton:
					button_window = canvas.create_window(sq_size/2+col*sq_size, sq_size/2+row*sq_size,width=sq_size, height=sq_size, window=button)
					self.all_buttons[(row,col)] = button
	
	# ####################################################################################################################################
	# Set up the board
	# addPiece - tracks the white/black pieces
	# setUpBord - makes the board
	# removeUnplayable - sets bounds
	# placeCastle - puts castles on board
	# placePieces - puts the game pieces
	# ####################################################################################################################################

	#track pieces that are white/black
	def addPiece(self, name, row, col):
		if "white" in name:
			self.white_pieces[(row,col)] = name
		elif "black" in name:
			self.black_pieces[(row, col)] = name

	#sets up the board for the game
	def setUpBoard(self):
		self.removeUnplayable()
		self.placeCastle()
		self.placePieces()

	#block off the unplayable pieces
	def removeUnplayable(self):
		for pos in self.unplayable_block:
			self.board[pos[0]][pos[1]] = 3

	#add the castle to the board
	def placeCastle(self):
		for val in self.white_castle:
			self.board[val[0],val[1]] = 4
		for val in self.black_castle:
			self.board[val[0],val[1]] = 5

	#place the player pieces
	def placePieces(self):
		for key in self.white_pieces:
			self.board[key[0]][key[1]]= 1
		for key in self.black_pieces:
			self.board[key[0]][key[1]] = 2

	# ####################################################################################################################################
	# Game Logic
	# Checking the kind of move made
	# validate_move
	# 	1 is capture 
	# 	2 is jump
	# 	3 is normal
	# 	0 is you fail
	# player is "white"/"black" 
	# piece is piece to move --> tuple (r,c) will eventually be passing a board location so use tuples...
	# move place piece will go to --> tuple (r,c)
	# checkWin: check to see if someone has won, draw after move made
	# FOR GRAPHICS: 
	# 	updateButtons: just changes the color of buttons cause logic is handled in backend :D
	# ####################################################################################################################################
	def makeMove(self, player, piece, move):
		goodMove = False

		validate_move = self.checkMove(player, piece, move)
		if validate_move != 0:
			#print("Board Before\n",self.board)
			#print("White Before\n", self.white_pieces)
			#print("Black Before\n", self.black_pieces)

			print ("MOVE MADE", validate_move)
			#if capture move made, figure out the captured move
			piece_to_remove = None
			if (validate_move == 1):
				r_diff = piece[0]-move[0]
				c_diff = piece[1]-move[1]
				piece_to_remove_row = int(piece[0] - r_diff/2)
				piece_to_remove_col = int(piece[1] - c_diff/2)
				piece_to_remove = (piece_to_remove_row,piece_to_remove_col)
			#update white_pieces/black_pieces
			if(player == "white"):
				if(piece_to_remove != None):
					self.black_pieces.pop(piece_to_remove)
					self.board[piece_to_remove[0],piece_to_remove[1]] = 0
				self.white_pieces[move] = self.white_pieces.pop(piece)
				#update board
				self.board[piece[0],piece[1]] = 0
				self.board[move[0], move[1]] = 1
			else:
				if(piece_to_remove != None):
					self.white_pieces.pop(piece_to_remove)
					self.board[piece_to_remove[0],piece_to_remove[1]] = 0
				self.black_pieces[move] = self.black_pieces.pop(piece)
				#update board
				self.board[piece[0],piece[1]] = 0
				self.board[move[0], move[1]] = 2

			self.updateButtons(player, piece_to_remove, piece, move)

			#print("Board After\n",self.board)
			#print("White After\n", self.white_pieces)
			#print("Black After\n", self.black_pieces)

			goodMove = True
		else: 
			self.all_buttons[piece].configure(bg=self.two_part_color[0])
			self.all_buttons[move].configure(bg=self.two_part_color[1])
			
			#temp_color = self.white_color if player =="white" else self.black_color
			#self.all_buttons[piece].configure(bg=temp_color)
			#self.all_buttons[move].configure(bg="LightBlue")
			#print ("move is invalid")
			goodMove = False

		#soft reset the two part move
		self.two_part_move = []
		self.two_part_color = []

		return goodMove

	'''
		Draw = 0
		White = 1
		Black = 2
		Continue = 3
	'''
	def checkWin(self,player):
		white_count = len(self.white_pieces)
		black_count = len(self.black_pieces)

		if (white_count == 1 and black_count == 1):
			return 0
		#white wins
		if (len(set(self.white_pieces.keys()).intersection(self.black_castle)) == 2):
			return 1
		elif(white_count > 1 and black_count == 1):
			return 1
		#black wins
		elif (len(set(self.black_pieces.keys()).intersection(self.white_castle)) == 2):
			return 2
		elif(white_count == 1 and black_count > 1):
			return 2
		return 3

	def updateButtons(self, player, piece_to_remove, old_piece_place, new_piece_place):
		if piece_to_remove != None:
			self.all_buttons[piece_to_remove].configure(bg="LightBlue")
		temp_color = self.white_color if player =="white" else self.black_color
		 #self.all_buttons[old_piece_place].cget("bg")
		self.all_buttons[old_piece_place].configure(bg="LightBlue")
		self.all_buttons[new_piece_place].configure(bg=str(temp_color))

	#will check to see if move is valid
	#if valid return true
	def checkMove(self, player, piece, move):
		#dont go on a wall
		if self.board[move[0],[move[1]]] != 3:
			#white player
			if player == "white":
				#valid white piece
				if piece in self.white_pieces:
					#check all 3 moves
					return self.checkThreeMoves(player,piece,move)
				else:
					print("moving a piece not white", piece, move) 
					return 0
			#black player
			elif player == "black":
				#valid black piece
				if piece in self.black_pieces:
					#check all 3 moves
					return self.checkThreeMoves(player, piece, move)
				else:
					print("moving a piece not black", piece, move)
					return 0
			else: 
				raise
		else:
			print("tried to press a non-valid button")
			return 0
	
	#checks all 3 moves
	#return true if any of 3 is true (following defines rules)
	#must make capture move if capture move available
	def checkThreeMoves(self, player,piece, move):		
		#check if capture move is mandatory
		capture_move_list = self.createListOfCaptureMoves(player)
		
		#window = self.createWindowForMove(player, piece, "capt")
		if len(capture_move_list) != 0:
			if move in capture_move_list:
				return 1
			else:
				print("Must make capture move")
				return 0
		#no capture move to make
		#check if cantering move
		#not mandatory
		window = self.createWindowForMove(player, piece, "jump")
		print(len(window))
		if len(window) != 0:
			if move in window:
				print ("Jumped")
				return 2
		#player made plain move
		if self.normalMove(player, piece, move):
			print("Normal")
			return 3
		else: 
			print("nothing")
			return 0

	#since capture move is manadatory
	#here is a list of them for the current player
	#the list will be the end positions for of the move 
	#i.e. if player is a 5,4 and enemy at 5,5 then position 5,6 is in the list (if nothing is in 5,6)
	def createListOfCaptureMoves(self, player):
		window = []
		players_pieces = self.white_pieces if player=="white" else self.black_pieces
		for piece_to_check in players_pieces:
			#print("piece", piece_to_check)
			window_for_piece = self.createWindowForMove(player, piece_to_check, "capt")
			#print("len(window_for_piece)",len(window_for_piece))
			if len(window_for_piece) != 0: 
				for cant_think_of_name in window_for_piece:
					window.append(cant_think_of_name)
			
		return window

	#type is either capt (for capturing move) or jump (for cantering move)
	#returns the window for the move made
	def createWindowForMove(self, player, piece, type):
		#window around piece
		window = []
		for row in range(piece[0]-1,piece[0]+2):
			for col in range(piece[1]-1,piece[1]+2):
				#out of bounds
				if(col < 0 or col > self.cols-1 or row < 0 or row > self.rows-1):
					continue
				if (row == 13 and (col == 3 or col==4)):
					continue
				#if (row == )
				#player white, aka 1
				#print("r",row,"c",col)
				if player == "white":
					if (type == "capt" and self.board[row,col] == 2) or (type == "jump" and self.board[row,col] == 1):
						self.createWindow(window, piece, row, col)
				elif player == "black":
					if (type == "capt" and self.board[row, col] == 1) or (type == "jump" and (self.board[row,col] == 2)):
						self.createWindow(window, piece, row, col)

		return window
	
	#create the window for a capture move or centering move 
	def createWindow(self, window, piece, row, col):
		#check to make sure there is room
		#left 
		if piece[1]-col == 1: 
			#top
			if piece[0]-row == 1:
				if self.board[row-1, col-1] == 0 or self.board[row-1, col-1] == 4 or self.board[row-1, col-1] == 5:
					window.append((row-1,col-1))
			#mid
			elif piece[0]-row == 0:
				if self.board[row, col-1] == 0  or self.board[row, col-1]  == 4 or self.board[row, col-1]  == 5:
					window.append((row,col-1))
			#bot
			elif piece[0]-row == -1:
				if self.board[row+1, col-1] == 0 or self.board[row+1, col-1] == 4 or self.board[row+1, col-1] == 5:
					window.append((row+1,col-1))
		#mid
		elif piece[1]-col == 0:
			#top
			if piece[0]-row == 1:
				if self.board[row-1,col] == 0 or self.board[row-1,col] == 4 or self.board[row-1,col] == 5:
					window.append((row-1, col))
			#bot
			elif piece[0]-row == -1:
				if self.board[row+1,col] == 0 or self.board[row+1,col] == 4 or self.board[row+1,col] == 5:
					window.append((row+1, col))
		#right
		elif piece[1]-col == -1: 
			#top
			if piece[0]-row == 1:
				if self.board[row-1, col+1] == 0 or self.board[row-1, col+1] == 4 or self.board[row-1, col+1] == 5:
					window.append((row-1, col+1))
			#mid
			elif piece[0]-row == 0:
				if self.board[row, col+1] == 0 or self.board[row, col+1] == 4 or self.board[row, col+1] == 5:
					window.append((row, col+1))
			#bot
			elif piece[0]-row == -1:
				if self.board[row+1, col+1] == 0 or self.boar[row+1, col+1] == 4 or self.board[row+1, col+1] == 5:
					window.append((row+1, col+1))
	
	#player made a normal move
	def normalMove(self, player, piece, move):
		r_diff = piece[0]-move[0]
		c_diff = piece[1]-move[1]
		
		if (abs(r_diff) <= 1 and abs(c_diff) <= 1) and  not(r_diff == 0 and c_diff == 0) and (self.board[move[0],move[1]]==0 or self.board[move[0],move[1]]==4 or self.board[move[0],move[1]]==5):
			return True
		else: 
			return False