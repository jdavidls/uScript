from uscript.source.syntax_tree import Visitor

class FileSystemInjector(Visitor):
	def preRoot(self, root):
		self.preModule(root)

	def preModule(self, module):
		# scan directories

		for dir in module.source_dirs:
			for entry in dir.iterdir():
				identifier = entry.stem

				if identifier.startswith('.'):
					continue

				if entry.is_dir():
					submod = module
					for identifier in identifier.split('.'):
						submod = submod.module(identifier)
					submod.addSourceDir(entry)

		for dir in module.source_dirs:
			for entry in dir.iterdir():
				identifier = entry.stem

				if identifier.startswith('.'):
					continue

				if entry.is_file():
					if entry.suffix in ('.u', '.µ'):
						submod = module
						for identifier in identifier.split('.'):
							submod = submod.module(identifier)
						submod.addUnit(entry)

					# manage another file extension

					else:
						print('ignored', entry)
