from .syntax_tree import Covisitor

class ASTPrinter(Covisitor):
	def __init__(self):
		super().__init__()
		self.level = 0

	def preNode(self, node):
		yield from self.print(node)
		self.level += 1

	def postNode(self, node):
		self.level -= 1

	def print(self, node):
		yield ('\u2502 ' * (self.level) + '\u251c\u2500\u252e\u2501', node.__class__.__name__, str(node))
