import random
import copy
from board import Board

class State:
	def __init__(self):
		#copy of the  game_board
		self.list_of_possible_moves = self.board.possible_moves_to_make
		self.move_to_make_board = None

class Node:
	def __init__(self):
		#state
		self.board = None
		#List<Node> childarray
		self.childArray = []
		#(tuple_1, tuple_2)
		self.my_move = None
		#my parent
		self.parent = None
		#depth of that node
		self.depth = 0

	def clone(self):
		temp_deep = Node()

		temp_deep.board = self.board.clone()
		temp_deep.childArray = copy.deepcopy(self.childArray)
		temp_deep.my_move = copy.deepcopy(self.my_move)
		temp_deep.parent = self.parent
		temp_deep.depth = self.depth

		return temp_deep

class Tree:
	def __init__(self):
		self.root = Node()