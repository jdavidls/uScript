from pathlib import Path

def visit_map(map):
	for key in map:
		map[key] = yield map[key]

def visit_seq(seq):
	for idx in range(len(seq)):
		seq[idx] = yield seq[idx]


class Visitor:
	def __init__(self, root):
		self.root = root
		self.methods_by_type = {}

	def __call__(self, entity):
		entity_type = type(entity)

		# pre and post visitor method
		if entity_type in self.methods_by_type:
			preorder, postorder = self.methods_by_type[entity_type]
		else:
			preorder = postorder = lambda _: _

			for cls in reversed(entity_type.__mro__):
				preorder = getattr(self, 'pre' + cls.__name__, preorder)
				postorder = getattr(self, 'post' + cls.__name__, postorder)
			self.methods_by_type[entity_type] = (preorder, postorder)


		entity = preorder(entity) or entity

		# visit child entities
		visitor = entity.visit(self)

		try:
			child = next(visitor)
			while True:
				child = self(child)
				child = visitor.send(child)
		except StopIteration:
			pass

		return postorder(entity) or entity


class Entity:
	def visit(self, visitor):
		return
		yield


class Unit(Entity):
	def __init__(self, parent, filename):
		self.parent = parent
		self.filename = filename
		#self.

class InteractiveUnit(Entity):
	def __init__(self, parent):
		self.parent = parent

class Module(Entity):
	def __init__(self, parent, identifier):
		self.parent = parent
		self.identifier = identifier
		self.source_dirs = []

		# childs
		self.modules = {}
		self.units = []


	def addSourceDir(self, path):
		if isinstance(path, str):
			path = Path(path)
		self.source_dirs.append(path)

	def module(self, identifier):
		if not identifier in self.modules:
			self.modules[identifier] = Module(self, identifier)
		return self.modules[identifier]

	def addUnit(self, filename):
		self.units.append(Unit(self, filename.resolve()))

	def visit(self, visitor):
		yield from visit_map(self.modules)
		yield from visit_seq(self.units)


class Root(Module):
	from uscript.processing.filesystem import FileSystemInjector
	from uscript.processing.sourcecode import SourceCodeProcessor

	def __init__(self):
		Module.__init__(self, None, 'root')

		self.units.append(InteractiveUnit(self))

		self.file_system_injector = self.FileSystemInjector(self)
		self.source_code_processor = self.SourceCodeProcessor(self)


	def __call__(self):
		''
		self.file_system_injector(self)
		self.source_code_processor(self)

