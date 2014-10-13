from .source.syntax_tree import *
from .source.expression import Block




class Unit(Node):
	def __init__(self, parent, filename):
		self.parent = parent
		self.filename = filename

class Module(Node):
	def __init__(self, parent, identifier):
		self.parent = parent
		self.identifier = identifier
		self.source_dirs = []

		# childs
		self.modules = {}
		self.units = []

		self.declarations = {}


	def addSourceDir(self, path, name=None):
		'''
		Los directorios de codigo son tratados como capas, el compilador realiza
		los pasos de interpretacion y evaluacion de capa en capa:

		Capa 0: (builtins, backend, etc)
		Capa 1:	Libreria base
		Capa <application>: Nivel de ususario

		Esto es importante para solventar los conflictos, cada capa debe implementar todo lo necesario
		para la correcta ejecucion de la siguiente capa a nivel declarativo.

		Pasos de evaluacion:
			1 - extrae declaraciones simples <id>:...=...
			2 - paso semantico para Identificadores lvalues <Id> .. LeftIndentifiers


		'''
		from pathlib import Path
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


	def declare(self, name, invariant):
		if name in self.declarations:
			raise NameError('{} has already declared'.format(name))
		print('declare', name, 'as', invariant)
		self.declarations[name] = invariant


