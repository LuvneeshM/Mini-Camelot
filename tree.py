import random
import copy


class Node:
	def __init__(self):
		#List<Node> childarray
		self.childArray = []
		#(tuple_1, tuple_2)
		self.my_move = None
		#my parent
		self.parent = None
		#game board
		self.board = None

class Tree:
	def __init__(self):
		self.root = Node()