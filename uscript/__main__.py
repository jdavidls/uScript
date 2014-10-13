from uscript.model.root import Root
from uscript import settings

if __name__ == '__main__':
	root = Root()
	root.addSourceDir(settings.runtime_path)
	root()
