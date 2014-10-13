
class Node:
	__slots__ = ()
	## ITER FOR TUPLES?? TUPLES WITH SLOTS??
	def visit(self, visitor):
		return
		yield

def visit_map(map):
	for key in map:
		map[key] = yield map[key]

def visit_seq(seq):
	for idx in range(len(seq)):
		seq[idx] = yield seq[idx]



def generator(func):
	"""
	Force to usea a function as a coroutine
	"""
	import inspect
	if inspect.isgeneratorfunction(func):
		return func
	else:
		def wrapper(*args, **kwds):
			return func(*args, **kwds)
			yield
	return wrapper


class Visitor:
	'''
	'''
	def __init__(self):
		self.methods_by_type = {}

	def __call__(self, node):
		node_type = type(node)

		# pre and post visitor method
		if node_type in self.methods_by_type:
			preorder, postorder = self.methods_by_type[node_type]
		else:
			preorder = postorder = lambda _:_

			for cls in reversed(node_type.__mro__):
				preorder = getattr(self, 'pre' + cls.__name__, preorder)
				postorder = getattr(self, 'post' + cls.__name__, postorder)
			self.methods_by_type[node_type] = (preorder, postorder)

		node = preorder(node) or node

		# if the node accept visits, visit child nodes
		if hasattr(node, 'visit'):
			visitor = node.visit(self)
			try:
				child = next(visitor)
				while True:
					child = self(child)
					child = visitor.send(child)
			except StopIteration:
				pass

		node = postorder(node) or node
		return node




class Covisitor:
	def __init__(self):
		self.methods_by_type = {}

	def __call__(self, node):
		node_type = type(node)

		# pre and post visitor method
		if node_type in self.methods_by_type:
			preorder, postorder = self.methods_by_type[node_type]
		else:
			preorder = postorder = lambda _:_

			for cls in reversed(node_type.__mro__):
				preorder = generator(getattr(self, 'pre' + cls.__name__, preorder))
				postorder = generator(getattr(self, 'post' + cls.__name__, postorder))
			self.methods_by_type[node_type] = (preorder, postorder)

		node = (yield from preorder(node)) or node

		# if the node accept visits, visit child nodes
		if hasattr(node, 'visit'):
			visitor = node.visit(self)
			try:
				child = next(visitor)
				while True:
					child = yield from self(child)
					child = visitor.send(child)
			except StopIteration:
				pass

		node = (yield from postorder(node)) or node
		return node


class Processor:
	def __call__(self, node):
		''
