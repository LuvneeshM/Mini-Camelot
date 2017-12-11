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

	def alphaBetaSearch(self, board, player, max_depth, start_time):

		self.depth = 0
		self.nodes = 0
		self.prune_in_max = 0
		self.prune_in_min = 0
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

		raise
		
		
	def maxValue(self, node, alpha, beta, player):
		if self.terminalState(node, player):
			return self.utility3(node, player)
		
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
						v = max(v, self.minValue(self.applyAction(node,piece,move_to, "white"), alpha, beta,"black" ))

						node.v = v
						
						if v > beta[0]:
							#pruning
							self.prune_in_max += 1
							return v
						alpha[0] = max(alpha[0],v)
			if v == float("-inf"):
				print("We fked up maxValue")
				raise
		

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
			if v == float("-inf"):
				print("We fked up maxValue")
				raise
		
		return v					
	
	def minValue(self, node, alpha, beta, player):
		if self.terminalState(node, player):
			#print(node.player)
			#print(player)
			#input()
			return self.utility3(node,player)

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
			if v == float("-inf"):
				print("We fked up minValue")
				raise
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
			if v == float("-inf") or v == float("inf"):
				print("We fked up minValue")
				raise
		
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
	def utility(self, node, player):

		did_i_win = node.board.checkWin(player)

		#when black runs ai
		#max player is black and wins
		if did_i_win == 2 and self.max_player == "black":
			node.v = self.MAX
			return self.MAX
		#min player is white and wins
		elif did_i_win == 1 and self.min_player == "white":
			node.v = self.MIN
			return self.MIN
		#when white runs ai
		#max player is white and wins
		elif did_i_win == 1 and self.max_player == "white":
			node.v = self.MAX
			return 1000
		#min player is black and wins
		elif did_i_win == 2 and self.min_player == "black":
			node.v = self.MIN
			return -1000
		#it is a draw
		elif did_i_win == 0:
			node.v = 0
			return 0
		#else we hit a cut off so we evaluate that node as a leaf node
		else:
			opp_to_my_castle = 1.0
			me_to_opp_castle = 1.0

			INF = 1000

			total_piece = len(node.board.black_pieces) + len(node.board.white_pieces)

			if (player == "white"):
				for i in node.board.white_pieces:
					me_to_opp_castle += ((4.0 - float(i[0]))**2  +(13-float(i[1]))**2 )**0.5 				
				val_me = len(node.board.white_pieces)*(INF/(me_to_opp_castle*15))

				for j in node.board.black_pieces:
					opp_to_my_castle += ((4.0 - float(j[0]))**2 + (float(j[1]))**2 )**0.5
				val_opp = INF/(opp_to_my_castle * 100 * len(node.board.black_pieces))

				node.v = (val_me+val_opp)

				return val_me + val_opp

			if(player == "black"):
				for i in node.board.black_pieces:
					me_to_opp_castle += ((4.0 - float(i[0]))**2 + (float(i[1]))**2 )**0.5 
				
				val_me = len(node.board.black_pieces)*(INF/(me_to_opp_castle*total_piece))

				for j in node.board.white_pieces:
					opp_to_my_castle += ((4.0 - float(j[0]))**2 + (8-float(j[1]))**2 )**0.5
				val_opp = INF/(opp_to_my_castle * 100 * len(node.board.white_pieces))


				#if (node.depth == 1):
				#	print("utility node", node.my_move)
				node.v = (val_me+val_opp)

				return val_me + val_opp
		

	#utility 2
	def utility2(self, node, player):
		did_i_win = node.board.checkWin(player)
		based_off_black = 1
		if(self.max_player == "black"):
			based_off_black = 1
		else:
			based_off_black = -1
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
				if black_dist_to_white_castle < 7: 
					to_return += random.uniform(150.0, 200.0)
			else:
				if black_dist_to_white_castle < 5:
					to_return -= random.uniform(100.0,180.0)
				if white_dist_to_black_castle < 7: 
					to_return += random.uniform(150.0, 200.0)

			white_dist_to_black_piece = node.board.minDistToOpp("white", self.max_player)
			black_dist_to_white_piece = node.board.minDistToOpp("black", self.max_player)

			to_return += white_dist_to_black_piece + black_dist_to_white_piece 

			node.v = to_return
			return node.v

	#utility 3
	def utility3(self, node, player):
		did_i_win = node.board.checkWin(player)
		based_off_black = 1
		if(self.max_player == "black"):
			based_off_black = 1
		else:
			based_off_black = -1
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

		white_pieces = len(node.board.white_pieces)
		black_pieces = len(node.board.black_pieces)

		to_return += 1 + (27*black_pieces * based_off_black) - (27*white_pieces * based_off_black)
		to_return -= based_off_black * 2*(3**(6-node.board.minDistToOpp(player, self.max_player)))
		to_return += based_off_black * 2*(3**(7-node.board.averageDistToOppCastle(player)))

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
