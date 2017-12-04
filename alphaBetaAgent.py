from tree import *
from board import Board
import time
import copy
import math

class AlpaBetaAgent:


	def alphaBetaSearch(self, board):
		alpha = float("inf")
		beta = float("-inf")

		tree = Tree()
		self.rootNode = tree.root
		self.board = board		

		v = self.maxValue(rootNode, alpha, beta)

	def maxValue(self, rootNode, alpha, beta):
		pass