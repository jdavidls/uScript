from .syntax_tree import Node
from .location import Location

class Unary(Node):
	__slots__ = ('location', 'value', 'annotations')
	def __init__(self, value, location=Location()):
		self.location = location
		self.value = value
		self.annotations = []
	def visit(self, visitor):
		self.value = yield self.value


class Binary(Node):
	__slots__ = ('location', 'lvalue', 'rvalue', 'annotations')
	def __init__(self, lvalue, rvalue, location=Location()):
		self.location = location
		self.lvalue = lvalue
		self.rvalue = rvalue
		self.annotations = []
	def visit(self, visitor):
		self.lvalue = yield self.lvalue
		self.rvalue = yield self.rvalue

class Nary(Node, list):
	__slots__ = ('location', 'annotations')
	def visit(self, visitor):
		for idx in range(len(self)):
			self[idx] = yield self[idx]



class Block(Nary):
	def __str__(self):
		return '[...]'


class Tuple(Nary):
	def __str__(self):
		return '(' + ', '.join(str(i) for i in self) + ')'

class Sequence(Nary):
	def __str__(self):
		return '[' + ', '.join(str(i) for i in self) + ']'



# 	Primary
class Local(Unary):
	def __str__(self):
		return str(self.value)

class Global(Unary):
	def __str__(self):
		return '.{0.value}'.format(self)

# postfix
class Property(Binary):
	def __str__(self):
		return '{0.lvalue}.{0.rvalue}'.format(self)

class Subscript(Binary):
	def __str__(self):
		return '{0.lvalue}{0.rvalue}'.format(self)



class With(Binary):
	def __str__(self):
		return '{0.lvalue} {0.rvalue}'.format(self)

class Pair(Binary):
	def __str__(self):
		return '{0.lvalue} : {0.rvalue}'.format(self)

# prefix

class Negative(Unary):
	('-', Unary)
	def __str__(self):
		return '-{0.value}'.format(self)

class Positive(Unary):
	('+', Unary)
	def __str__(self):
		return '+{0.value}'.format(self)

class Absolute(Unary):
	('+-', Unary)
	def __str__(self):
		return '+-{0.value}'.format(self)

class Not(Unary):
	('!', Unary)
	def __str__(self):
		return '!{0.value}'.format(self)


# 	Arithmetic 3
class Pow(Binary):
	def __str__(self):
		return '{0.lvalue} -^ {0.rvalue}'.format(self)

class Root(Binary):
	def __str__(self):
		return '{0.lvalue} -/ {0.rvalue}'.format(self)

class Logarithm(Binary):
	def __str__(self):
		return '{0.lvalue} -* {0.rvalue}'.format(self)



# 	Arithmetic 2
class Multiplication(Binary):
	def __str__(self):
		return '{0.lvalue} * {0.rvalue}'.format(self)

class Division(Binary):
	def __str__(self):
		return '{0.lvalue} / {0.rvalue}'.format(self)

class Modulo(Binary):
	def __str__(self):
		return '{0.lvalue} % {0.rvalue}'.format(self)


# 	Arithmetic 1

class Addition(Binary):
	def __str__(self):
		return '{0.lvalue} + {0.rvalue}'.format(self)

class Substraction(Binary):
	def __str__(self):
		return '{0.lvalue} - {0.rvalue}'.format(self)


# 	Push

class PushLeft(Binary):
	def __str__(self):
		return '{0.lvalue} << {0.rvalue}'.format(self)

class PushRight(Binary):
	def __str__(self):
		return '{0.lvalue} >> {0.rvalue}'.format(self)


# 	Bit Arithmetic

class And(Binary):
	def __str__(self):
		return '{0.lvalue} & {0.rvalue}'.format(self)

class Or(Binary):
	def __str__(self):
		return '{0.lvalue} | {0.rvalue}'.format(self)

class Xor(Binary):
	def __str__(self):
		return '{0.lvalue} ^ {0.rvalue}'.format(self)

# 	Comparison
class LessThan(Binary):
	def __str__(self):
		return '{0.lvalue} < {0.rvalue}'.format(self)

class LessEqual(Binary):
	def __str__(self):
		return '{0.lvalue} <= {0.rvalue}'.format(self)

class GreaterThan(Binary):
	def __str__(self):
		return '{0.lvalue} > {0.rvalue}'.format(self)

class GreaterEqual(Binary):
	def __str__(self):
		return '{0.lvalue} >= {0.rvalue}'.format(self)

class Equality(Binary):
	def __str__(self):
		return '{0.lvalue} == {0.rvalue}'.format(self)

class Inequality(Binary):
	def __str__(self):
		return '{0.lvalue} != {0.rvalue}'.format(self)

# 	control flow

class Then(Binary):
	def __str__(self):
		return '{0.lvalue} && {0.rvalue}'.format(self)

class Otherwise(Binary):
	def __str__(self):
		return '{0.lvalue} || {0.rvalue}'.format(self)

# Logic
class Logic(Unary):
	def __str__(self):
		return '{0.value}?'.format(self)



# assignment
class Assignment(Binary):
	def __init__(self, *args, operator=None):
		super().__init__(*args)
		self.operator = operator
	def __str__(self, operator=None):
		return '{0.lvalue} || {0.rvalue}'.format(self)



