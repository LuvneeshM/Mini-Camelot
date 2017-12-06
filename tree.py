import random
import copy
from board import Board

class State:
	def __init__(self):
		#copy of the  game_board
		#self.list_of_possible_moves = self.board.possible_moves_to_make
		self.move_to_make_board = None

class Node:
	def __init__(self):
		#state
		self.board = None
		#List<Node> childarray
		self.child_array = []
		#(tuple_1, tuple_2)
		self.my_move = None
		#my parent
		self.parent = None
		#depth of that node
		self.depth = 0
		#what am i
		self.player = None
		#my v
		self.v = None

	def clone(self):
		temp_deep = Node()

		temp_deep.board = self.board.clone()
		temp_deep.parent = self.parent
		temp_deep.depth = self.depth
		temp_deep.player = self.player
		return temp_deep

class Tree:
	def __init__(self):
		self.root = Node()