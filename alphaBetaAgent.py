from tree import *
from board import Board
import time
import copy
import math

class AlphaBetaAgent:

	def __init__(self):
		self.depth = 0
		self.nodes = 0
		self.prune_in_max = 0
		self.prune_in_min = 0
		self.max_depth = 5


	def alphaBetaSearch(self, board, player):

		self.depth = 0
		self.nodes = 0
		self.prune_in_max = 0
		self.prune_in_min = 0


		alpha = [float("-inf")]
		beta = [float("inf")]

		tree = Tree()
		rootNode = tree.root

		rootNode.board = board.clone()

		self.start_time = time.time()
		print("s-time",self.start_time)
		


		v = self.maxValue(rootNode, alpha, beta, player)

		print(v)

		print("elapsed-time",time.time()-self.start_time)
		print("I am done")
		print("MAYBE RIGHT Depth", self.depth)
		print("Nodes", self.nodes)
		print("prune_in_min", self.prune_in_min)
		print("prune_in_max", self.prune_in_max)
		print("alpha", alpha)
		print("beta", beta)
		print("V", v)
		#return action in ACTIONS(state) with value v
		for k in rootNode.child_array:
			print("move", k.my_move)
			input(k.v)
			if k.v == v:
				return k.my_move


		raise
		
		

	def maxValue(self, node, alpha, beta, player):
		if self.terminalState(node, player):
			return self.utility(node, player)
		v = float("-inf")


		#for each action a in Actions(state) do
		moves = node.board.createListOfCaptureMoves(player)
		#if no capture moves available then pick from other moves
		if len(moves) == 0:
			moves = node.board.getDictOfAllMoves(player)


		#piece will be the key
		#move_to will be the peice to move to
		if player == "black":
			counter = 0
			for piece in node.board.black_pieces:
				if piece in moves.keys():
					for move_to in moves[piece]:
						#if (time.time() - self.start_time <= 20):
						v = max(v, self.minValue(self.applyAction(node,piece,move_to, "white"), alpha, beta,"white" ))

						node.v = v

						if v >= beta[0]:
							#pruning
							self.prune_in_max += 1
							return v
						alpha[0] = max(alpha[0],v)
			if v == float("-inf"):
				print("We fked up maxValue")
				raise
		if player == "white":
			for piece in node.board.white_pieces:
				if piece in moves.keys():
					for move_to in moves[piece]:
						#if (time.time() - self.start_time <= 20):
						v = max(v, self.minValue(self.applyAction(node,piece,move_to, "black"), alpha, beta, "black"))
						
						node.v = v

						if v >= beta[0]:
							#pruning
							self.prune_in_max += 1
							return v
						alpha[0] = max(alpha[0],v)
			if v == float("-inf"):
				print("We fked up maxValue")
				raise
		return v					
	
	def minValue(self, node, alpha, beta, player):
		if self.terminalState(node, player):
			return self.utility(node,player)

		v = float("inf")
		#for each action a in Actions(state) do
		moves = node.board.createListOfCaptureMoves(player)
		#if no capture moves available then pick from other moves
		if len(moves) == 0:
			moves = node.board.getDictOfAllMoves(player)
		#piece will be the key
		#move_to will be the peice to move to
		if player == "white":
			for piece in node.board.white_pieces:
				if piece in moves.keys():
					for move_to in moves[piece]:
						#if (time.time() - self.start_time <= 20):
						v = min(v, self.maxValue(self.applyAction(node,piece,move_to, "black"), alpha, beta, "black" ))
						
						node.v = v

						if v <= alpha[0]:
							self.prune_in_min += 1
							return v
						beta[0] = min(beta[0],v)
			if v == float("-inf"):
				print("We fked up minValue")
				raise
		if player == "black":
			for piece in node.board.black_pieces:
				if piece in moves.keys():
					for move_to in moves[piece]:
						#if (time.time() - self.start_time <= 20):
						v = min(v, self.maxValue(self.applyAction(node,piece,move_to, "white"), alpha, beta, "white" ))
						
						node.v = v

						if v <= alpha[0]:
							self.prune_in_min += 1
							return v
						beta[0] = min(beta[0],v)
			if v == float("-inf") or v == float("inf"):
				print("We fked up minValue")
				raise
		return v					

	#terminalState function
	def terminalState(self,node, player):
		#check if time is up 
		#then force this to be a terminal node
		if time.time() - self.start_time >= 10:
			print("over 10", player)
			return True
		
		

		#max depth
		if node.depth == self.max_depth:
			#print("Max Depth Reached", node.depth)
			return True

		'''
		Draw = 0
		White = 1
		Black = 2
		Continue = 3
		'''
		did_i_win = node.board.checkWin(player)
		if did_i_win != 3: #and did_i_win != 0:
			#print("How you won: ", did_i_win)
			#print("the board terminal")
			#node.parent.board.printBoard()
			#input(player)
			return True

		return False

	#utility function
	def utility(self, node, player):

		opp_to_my_castle = 1.0
		me_to_opp_castle = 1.0

		INF = 100000

		total_piece = len(node.board.black_pieces) + len(node.board.white_pieces)

		if (player == "white"):
			for i in node.board.white_pieces:
				me_to_opp_castle += ((4.0 - float(i[0]))**2  +(13-float(i[1]))**2 )**0.5 				
			val_me = len(node.board.white_pieces)*(INF/(me_to_opp_castle*15))

			for j in node.board.black_pieces:
				opp_to_my_castle += ((4.0 - float(j[0]))**2 + (float(j[1]))**2 )**0.5
			val_opp = INF/(opp_to_my_castle * 100 * len(node.board.black_pieces))

			return val_me + val_opp

		if(player == "black"):
			for i in node.board.black_pieces:
				me_to_opp_castle += ((4.0 - float(i[0]))**2 + (float(i[1]))**2 )**0.5 
			
			val_me = len(node.board.black_pieces)*(INF/(me_to_opp_castle*total_piece))

			for j in node.board.white_pieces:
				opp_to_my_castle += ((4.0 - float(j[0]))**2 + (8-float(j[1]))**2 )**0.5
			val_opp = INF/(opp_to_my_castle * 100 * len(node.board.white_pieces))

			return val_me + val_opp
			

	def applyAction(self, node, piece, move_to, player):
		self.nodes += 1
		#make clone
		temp_node = node.clone()
		temp_node.depth += 1 
		#this is my_move
		temp_node.my_move = (piece,move_to)
		#who am I
		temp_node.player = player
		#make move
		if(player == "white"):
			temp_node.board.makeMove("black", piece, move_to, False)
		elif(player == "black"):
			temp_node.board.makeMove("white", piece, move_to, False)
		#add to node children
		node.child_array.append(temp_node)
		#tell my child, I am the MAN
		temp_node.parent = node
		return temp_node
