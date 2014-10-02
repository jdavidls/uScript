from .location import Location
from .syntax_tree import Node

class Terminal(Node):
	__slots__ = ('location', 'value', 'annotations')
	def __init__(self, value, *location):
		self.location = Location(*location)
		self.value = value
		self.annotations = []
	def __repr__(self):
		return "<{0.__class__.__name__} '{0.value}' at {0.location}>".format(self)
	def __str__(self):
		return str(self.value)
	def visit(self, visitor):
		self.value = yield self.value


class Error(Terminal): pass
class Escape(Terminal): pass
class Annotation(Terminal): pass
class Constant(Terminal): pass
class Identifier(Terminal): pass

class PunctuationMark:
	__slots__ = ('location')
	def __init__(self, *location):
		self.location = Location(*location)
	def __repr__(self):
		return "<{0.__class__.__name__} at {0.location}>".format(self)



class Begin(PunctuationMark): pass
class End(PunctuationMark): pass
class Line(PunctuationMark): pass

# re.sub(r"\t'.':\s'(\w+)',", r"class $1(PunctuationMark): pass")

class Ampersand(PunctuationMark): pass
class Asterisk(PunctuationMark): pass
class At(PunctuationMark): pass

class Caret(PunctuationMark): pass
class Colon(PunctuationMark): pass
class Comma(PunctuationMark): pass

class Dot(PunctuationMark): pass

class Equal(PunctuationMark): pass
class Exclamation(PunctuationMark): pass

class Greater(PunctuationMark): pass

class Hash(PunctuationMark): pass

class Less(PunctuationMark): pass

class Minus(PunctuationMark): pass

class Percent(PunctuationMark): pass
class Pipe(PunctuationMark): pass
class Plus(PunctuationMark): pass

class Question(PunctuationMark): pass

class Semicolon(PunctuationMark): pass
class Slash(PunctuationMark): pass

class OpenParenthesis(PunctuationMark): pass
class CloseParenthesis(PunctuationMark): pass

class OpenBracket(PunctuationMark): pass
class CloseBracket(PunctuationMark): pass

class OpenCurly(PunctuationMark): pass
class CloseCurly(PunctuationMark): pass


