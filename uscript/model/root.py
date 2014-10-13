from .module import Module, Unit

#class InteractiveUnit(Unit):	...


class Root(Module):
	from uscript.process import FileSystemInjector
	from uscript.process import SyntacticProcessor, SemanticProcessor

	def __init__(self):
		Module.__init__(self, None, 'root')

		#self.units.append(InteractiveUnit(self))

		self.file_system_injector = self.FileSystemInjector()
		self.syntactic_processor = self.SyntacticProcessor()
		self.semantic_processor = self.SemanticProcessor()

	def __call__(self):
		''
		self.file_system_injector(self)
		self.syntactic_processor(self)
		self.semantic_processor(self)

