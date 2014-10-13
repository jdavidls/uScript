'''

'''
import inspect, multimethods

__all__ = 'Dispatcher', 'dispatch',

class DispatchNode:
	__slots__ = 'map', 'solution', 'next'
	def __init__(self):
		self.map = {}
		self.solution = None
		self.next = None

def resolution_matrix(elements):
	return tuple((element,) + type(element).__mro__ for element in elements)

class Dispatcher:
	'''
	Function and method dispatcher
	'''
	__slots__ = 'root',

	def __init__(self):
		'''
		'''
		self.root = DispatchNode()

	def add(self, item):
		'''
		'''

		# callable signature
		signature = inspect.signature(item)
		domain = tuple(object if parameter.annotation is inspect._empty else parameter.annotation for parameter in signature.parameters.values())
		# codomain = (object,) if signature.return_annotation is inspect._empty else (signature.return_annotation,)

		node = self.root

		for element in domain:
			if not element in node.map:
				node.map[element] = DispatchNode()
				node = node.map[element]
			else:
				node = node.map[element]

			if node.next is None:
				node.next = DispatchNode()

			node = node.next

		node.solution = item

	def __get__(self, obj, type=None):
		'''
		'''
		if obj is None:
			return self
		from functools import partial

		return partial(Dispatcher.__call__, self, obj)

	def __call__(self, *argument):
		'''
		'''
		item = self.__getitem__(argument)

		result = item(*argument)

		return result

	def __getitem__(self, argument):
		'''
		'''
		if type(argument) is not tuple:
			argument = (argument,)

		rmatrix = resolution_matrix(argument)

		backstack = []
		X = len(rmatrix)
		x, y = 0, 0
		node = self.root

		while True:  # x < X:

			if x == X:
				break

			Y = len(rmatrix[x])

			while True:  # y < Y:
				if y == Y:
					try:
						node, x, y = backstack.pop()
					except IndexError:
						raise KeyError(''.format())

					break

				v = rmatrix[x][y]

				if v in node.map:
					backstack.append((node, x, y + 1))
					node = node.map[v].next

					assert node  # dispatch map corrupted

					x += 1
					y = 0
					break

				y += 1

		return node.solution


def dispatch(item):
	'''
	Python decorator for uScript functions/methods

	:param item: Callable item
	:type item: callable.
	:returns:  Dispatcher -- the dispatcher instance for callable item .
	'''
	frame = inspect.currentframe()
	try:
		dispatcher = frame.f_back.f_locals[item.__name__]
	except KeyError:
		dispatcher = Dispatcher()
	finally:
		del frame

	dispatcher.add(item)

	return dispatcher



