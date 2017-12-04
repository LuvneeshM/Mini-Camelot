from tree import *
from board import Board
import time
import copy
import math

class AlphaBetaAgent:


	def alphaBetaSearch(self, board):
		alpha = [float("inf")]
		beta = [float("-inf")]

		tree = Tree()
		rootNode = tree.root
		rootNode.board = board.clone()

		self.start_time = time.time()
		print("s-time",self.start_time)
		v = self.maxValue(rootNode, alpha, beta)

		print("I am done")
		#return action in ACTIONS(state) with value v
		print("rootNode.child_array",len(rootNode.child_array))

	def maxValue(self, node, alpha, beta):
		if self.terminalState(node, "black"):
			return self.utility(node, "black")
		v = float("-inf")


		#for each action a in Actions(state) do
		moves = node.board.createListOfCaptureMoves("black")
		#if no capture moves available then pick from other moves
		if len(moves) == 0:
			moves = node.board.getDictOfAllMoves("black")


		#piece will be the key
		#move_to will be the peice to move to
		for piece in node.board.black_pieces:
			if piece in moves.keys():
				for move_to in moves[piece]:
					v = max(v, self.minValue(self.applyAction(node,piece,move_to, "black"), alpha, beta) )
					if v >= beta[0]:
						return v
					alpha[0] = max(alpha[0],v)
		if v == float("-inf"):
			print("We fked up maxValue")
			raise
		return v					
	
	def minValue(self, node, alpha, beta):
		if self.terminalState(node, "white"):
			return self.utility(node,"white")

		v = float("inf")
		#for each action a in Actions(state) do
		moves = node.board.createListOfCaptureMoves("white")
		#if no capture moves available then pick from other moves
		if len(moves) == 0:
			moves = node.board.getDictOfAllMoves("white")

		#piece will be the key
		#move_to will be the peice to move to
		for piece in node.board.white_pieces:
			if piece in moves.keys():
				for move_to in moves[piece]:
					v = min(v, self.maxValue(self.applyAction(node,piece,move_to, "white"), alpha, beta) )
					if v <= alpha[0]:
						return v
					beta[0] = min(beta[0],v)
		if v == float("-inf"):
			print("We fked up minValue")
			raise
		return v					

	#terminalState function
	def terminalState(self,node, player):
		#check if time is up 
		#then force this to be a terminal node
		if time.time() - self.start_time >= 10:
			print("over 10")
			return True
		
		'''
		Draw = 0
		White = 1
		Black = 2
		Continue = 3
		'''
		did_i_win = node.board.checkWin(player)
		if did_i_win != 3: #and did_i_win != 0:
			print("How you won: ", node.board.checkWin(player))
			print("the boardn",node.board.printBoard())
			print(player," won")
			return True

		return False

	#utility function
	def utility(self, node, player):
		pieces_left = len(node.board.white_pieces) - len(node.board.black_pieces)
		if player == "black":
			pieces_left *= -1

		return pieces_left

	def applyAction(self, node, piece, move_to, player):
		#make clone
		temp_node = node.clone()
		temp_node.depth += 1 
		#make move
		temp_node.board.makeMove(player, piece, move_to)
		#add to node children
		#print("applyAction")
		node.child_array.append(temp_node)

		return temp_node
