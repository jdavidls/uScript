from .source.module import Module, Unit

#class InteractiveUnit(Unit):	...


class Root(Module):
	from uscript.process.file_system import FileSystemInjector
	from uscript.process.source_code import SourceCodeProcessor

	def __init__(self):
		Module.__init__(self, None, 'root')

		#self.units.append(InteractiveUnit(self))

		self.file_system_injector = self.FileSystemInjector()
		self.source_code_processor = self.SourceCodeProcessor()


	def __call__(self):
		''
		self.file_system_injector(self)
		self.source_code_processor(self)

