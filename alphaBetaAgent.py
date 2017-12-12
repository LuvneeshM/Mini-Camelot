from tree import *
from board import Board
import time
import copy
import math
import random

class AlphaBetaAgent:

	def __init__(self):
		self.depth = 0
		self.nodes = 0
		self.prune_in_max = 0
		self.prune_in_min = 0
		self.max_depth = 1
		self.MAX = 1000
		self.MIN = -1000

	def alphaBetaSearch(self, board, player, max_depth, start_time, level):

		self.depth = 0
		self.nodes = 0
		self.prune_in_max = 0
		self.prune_in_min = 0
		self.level = level
		self.max_depth = max_depth

		self.max_player = player
		if(self.max_player == "black"):
			self.min_player = "white"
		else:
			self.min_player = "black"

		alpha = [float(-1000)]
		beta = [float(1000)]

		tree = Tree()
		rootNode = tree.root

		rootNode.board = board.clone()


		self.start_time = start_time
		print("# Start Time:",self.start_time)
		
		v = self.maxValue(rootNode, alpha, beta, player)
		print("# Elapsed Time:",time.time()-self.start_time)
		print("# Max Depth Reached", self.max_depth)#self.max_depth)
		print("# Nodes Generated:", self.nodes)
		print("# Prune In Min:", self.prune_in_min)
		print("# Prune In Max:", self.prune_in_max)
		print("# Alpha:", alpha)
		print("# Beta:", beta)
		print("# V Calculated:", v)

		#return action in ACTIONS(state) with value v
		print("# My V", rootNode.v)
		for k in rootNode.child_array:
			if k.v == v:
				print("# Move Returning:",k.my_move)
				return (k.my_move,v)
				print("##############################")		
		
	def maxValue(self, node, alpha, beta, player):
		if self.terminalState(node, player):
			if (self.level == 1):
				return self.utility(node, player)
			elif (self.level == 2):
				return self.utility2(node, player, True)
			else:
				return self.utility3(node, player, False)

		v = float("-inf")

		#for each action a in Actions(state) do
		moves = node.board.createListOfCaptureMoves(player)
		#if no capture moves available then pick from other moves
		if len(moves) == 0:
			moves = node.board.getDictOfAllMoves(player)
		#piece will be the key
		#move_to will be the peice to move to
		if player == "black":
			for piece in node.board.black_pieces:
				if piece in moves.keys():
					for move_to in moves[piece]:
						v = max(v, self.minValue(self.applyAction(node,piece,move_to, "white"), alpha, beta,"black"))

						node.v = v
						
						if v > beta[0]:
							#pruning
							self.prune_in_max += 1
							return v
						alpha[0] = max(alpha[0],v)
			
		#for ai vs ai
		if player == "white":
			for piece in node.board.white_pieces:
				if piece in moves.keys():
					for move_to in moves[piece]:
						v = max(v, self.minValue(self.applyAction(node,piece,move_to, "black"), alpha, beta, "white"))
						
						node.v = v

						if v > beta[0]:
							#pruning
							self.prune_in_max += 1
							return v
						alpha[0] = max(alpha[0],v)
			
		return v					
	
	def minValue(self, node, alpha, beta, player):
		if self.terminalState(node, player):
			if (self.level == 1):
				return self.utility(node, player)
			elif (self.level == 2):
				return self.utility2(node, player, True)
			else:
				return self.utility3(node, player, False)

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
						v = min(v, self.maxValue(self.applyAction(node,piece,move_to, "black"), alpha, beta, "white" ))
						
						node.v = v
						if v < alpha[0]:
							self.prune_in_min += 1
							return v
						beta[0] = min(beta[0],v)

		#for ai vs ai		
		if player == "black":
			for piece in node.board.black_pieces:
				if piece in moves.keys():
					for move_to in moves[piece]:
						v = min(v, self.maxValue(self.applyAction(node,piece,move_to, "white"), alpha, beta, "black" ))
						
						node.v = v

						if v < alpha[0]:
							self.prune_in_min += 1
							return v
						beta[0] = min(beta[0],v)
		
		return v					

	#terminalState function
	def terminalState(self,node, player):
		#check if time is up 
		#then force this to be a terminal node
		
		if time.time() - self.start_time >= 10:
			#print("over 10", player)
			#if (node.depth == 1):
			#	print("terminal node",node.my_move)
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
		if did_i_win != 3: 
			return True

		return False

	#utility function
	#The initiator
	#he will decide to break stalemates to enter the war
	def utility(self, node, player):

		did_i_win = node.board.checkWin(player)
		based_off_black = 1
		if(self.max_player == "black"):
			based_off_black = 1
		else:
			based_off_black = -1
		#when black runs ai
		#max player is black and wins
		if did_i_win == 2 and self.max_player == "black":
			node.v = self.MAX * based_off_black
			return node.v
		#min player is white and wins
		elif did_i_win == 1 and self.min_player == "white":
			node.v = self.MIN * based_off_black
			return node.v
		#when white runs ai
		#max player is white and wins
		elif did_i_win == 1 and self.max_player == "white":
			node.v = self.MAX * based_off_black
			return node.v 
		#min player is black and wins
		elif did_i_win == 2 and self.min_player == "black":
			node.v = self.MIN * based_off_black
			return node.v
		#it is a draw
		elif did_i_win == 0:
			node.v = 0
			return node.v
		#else we hit a cut off so we evaluate that node as a leaf node
		else:
			opp_to_my_castle = 1.0
			me_to_opp_castle = 1.0

			total_piece = len(node.board.black_pieces) + len(node.board.white_pieces)

			#total distance to castle
			white_to_black_castle_avg = node.board.averageDistToOppCastle("white")
			black_to_white_castle_avg = node.board.averageDistToOppCastle("black")
			#values for black and white
			#i base white and black values off the opponent
			value_black = based_off_black * self.MAX / ((black_to_white_castle_avg * total_piece * len(node.board.black_pieces)))
			value_white = based_off_black * self.MAX / ((white_to_black_castle_avg * 50 * len(node.board.white_pieces)))

			node.v = value_white + value_black

			return node.v		

	#utility 2 and 3
	#if flip_flop == False: the Trapper
	#he sets up traps to then have blood shed
	#if flip_flop == : the Defender
	#he basically blockades and protects his castle with his life
	def utility2(self, node, player, flip_flop):
		did_i_win = node.board.checkWin(player)
		based_off_black = 1
		if(self.max_player == "black" and flip_flop):
			based_off_black = -1
		else:
			based_off_black = 1
		#max player and player is same
		if(did_i_win == 2):
			node.v = self.MAX * based_off_black
			return node.v
		elif(did_i_win == 1):
			node.v = self.MIN * based_off_black
			return node.v
		elif(did_i_win == 0):
			node.v = 0
			return 0
		else:
			if (node.board.isCastleOccupide("black")):
				node.v = self.MAX * based_off_black
				return node.v
			elif (node.board.isCastleOccupide("white")):
				node.v = self.MIN * based_off_black
				return node.v

			to_return = 0

			#pieces left on board
			#+5 for mine 
			#-8 for his
			white_pieces = len(node.board.white_pieces)
			black_pieces = len(node.board.black_pieces)
			if self.max_player == "black":
				to_return += (5*black_pieces) - (8*white_pieces)
			else: 
				to_return += (5*white_pieces) - (8*black_pieces)

			#how close we are to the opponent castle
			#if distance is less than 7 [roughly half the board] optimize for it and move toward the opp castle
			#if oppoentn is less than 5 penalize for it, dont go for a move that pushes me closer to opp castle
			white_dist_to_black_castle = node.board.minDistToOppCastle(player)
			black_dist_to_white_castle = node.board.minDistToOppCastle(player)
			if self.max_player == "black":
				if white_dist_to_black_castle < 5:
					to_return -= random.uniform(100.0,180.0)
				if black_dist_to_white_castle < 8: 
					to_return += random.uniform(200.0, 250.0)
			else:
				if black_dist_to_white_castle < 5:
					to_return -= random.uniform(100.0,180.0)
				if white_dist_to_black_castle < 8: 
					to_return += random.uniform(200.0, 250.0)

			white_dist_to_black_piece = node.board.minDistToOpp("white", self.max_player)
			black_dist_to_white_piece = node.board.minDistToOpp("black", self.max_player)

			to_return += white_dist_to_black_piece + black_dist_to_white_piece 

			node.v = to_return
			return node.v

	def applyAction(self, node, piece, move_to, player):
		self.nodes += 1
		#make clone
		temp_node = node.clone()
		#more depth
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
		#if node.depth == 0:
		#	print("applyAction",temp_node.my_move)
		#tell my child, I am the MAN
		temp_node.parent = node
		return temp_node
