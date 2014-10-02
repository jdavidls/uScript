from uscript.source.lexicon import *
from uscript.source.expression import *

__all__ = ('Parser', )

with_tokens = (Identifier, Constant, Begin, OpenBracket, OpenParenthesis, OpenCurly)

class Parser:
	def __init__(self):
		self.token_stream = None
		self.current_line = 0
		self.token = None
		self.token_stack = []
		self.escape_stack = []
		self.error_stack = []

	def popToken(self):
		while True:
			if self.token_stack:
				self.token = token = self.token_stack.pop()
			else:
				try:
					self.token = token = next(self.token_stream)
				except StopIteration:
					self.token = token = None
			if isinstance(token, Escape):
				self.escape_stack.append(token)
			else:
				break
		return token

	def pushToken(self, token):
		self.token_stack.append(self.token)
		self.token = token


	def __call__(self, token_stream):
		self.token_stream = token_stream
		self.current_line = 0
		self.token = next(token_stream)
		self.finish = False

		return self.parseExpression()

	def parseExpression(self):
		forward = self.parseSwitch
		expr = forward()

		token = self.token
		if isinstance(token, Equal):
			equal, token = token, self.popToken()
			expr = Assignment(expr, self.parseExpression())	# a = b

		return expr



	def parseSwitch(self):
		forward = self.parseOtherwise
		expr = forward()

		token = self.token
		if isinstance(token, Question):
			question, token = token, self.popToken()
			expr = Logic(expr)	# a?

			while True:
				if isinstance(token, with_tokens):
					expr = With(expr, self.parseSwitch()) # a? ...
					continue
				break

		elif isinstance(token, Colon):
			colon, token = token, self.popToken()
			expr = Pair(expr, self.parseSwitch())	# a: ...

			'''
			while True:
				if isinstance(token, with_tokens):
					expr = With(expr, self.parseSwitch()) # a? ...
					continue
				break
			'''

		return expr



	def parseOtherwise(self):
		forward = self.parseThen

		expr = forward()

		while True:
			token = self.token
			if isinstance(token, Pipe):
				pipe, token = token, self.popToken()
				if isinstance(token, Pipe):
					self.popToken()
					expr = Otherwise(expr, forward())	# a || b
					continue
				self.pushToken(pipe)
			break
		return expr


	def parseThen(self):
		forward = self.parseComparison

		expr = forward()

		while True:
			token = self.token
			if isinstance(token, Ampersand):
				ampersand, token = token, self.popToken()
				if isinstance(token, Ampersand):
					self.popToken()
					expr = Then(expr, forward())	# a && b
					continue
				self.pushToken(ampersand)
			break
		return expr


	def parseComparison(self):
		forward = self.parseOr

		expr = forward()

		while True:
			token = self.token
			if isinstance(token, Less):
				less, token = token, self.popToken()
				if isinstance(token, Equal):
					self.popToken()
					expr = LessEqual(expr, forward())	# <=
					continue
				if isinstance(token, Greater):
					self.popToken()
					expr = Inequality(expr, forward())	# <>
					continue
				else:
					expr = LessThan(expr, forward())		# <
					continue
			elif isinstance(token, Greater):
				greater, token = token, self.popToken()
				if isinstance(token, Equal):
					self.popToken()
					expr = GreaterEqual(expr, forward())	# >=
					continue
				if isinstance(token, Less):
					self.popToken()
					expr = Inequality(expr, forward())	# ><
					continue
				else:
					expr = GreaterThan(expr, forward())	# >
					continue
			elif isinstance(token, Equal):
				equal, token = token, self.popToken()
				if isinstance(token, Equal):
					self.popToken()
					expr = Equality(expr, forward())		# ==
					continue
				else:
					self.pushToken(equal)
			break

		return expr


	def parseOr(self):
		forward = self.parseXor
		expr = forward()

		while True:
			token = self.token
			if isinstance(token, Pipe):
				pipe, token = token, self.popToken()
				if not isinstance(token, (Pipe, Equal)): # reject || |=
					expr = Or(expr, forward())		# a | b
					continue
				self.pushToken(pipe)
			break
		return expr

	def parseXor(self):
		forward = self.parseAnd
		expr = forward()

		while True:
			token = self.token
			if isinstance(token, Caret):
				caret, token = token, self.popToken()
				if not isinstance(token, (Caret, Equal)): # reject ^^ ^=
					expr = Xor(expr, forward())		# a ^ b
					continue
				self.pushToken(caret)
			break
		return expr

	def parseAnd(self):
		forward = self.parsePush
		expr = forward()

		while True:
			token = self.token
			if isinstance(token, Ampersand):
				ampersand, token = token, self.popToken()
				if not isinstance(token, (Ampersand, Equal)): # reject && &=
					expr = And(expr, forward())		# a & b
					continue
				self.pushToken(ampersand)
			break
		return expr

	def parsePush(self):
		forward = self.parseArithmetic
		expr = forward()
		while True:
			token = self.token
			if isinstance(token, Less):
				less, token = token, self.popToken()
				if isinstance(token, Less):
					self.popToken()
					expr = PushLeft(expr, forward())		# a << b
					continue
				self.pushToken(less)
			elif isinstance(token, Greater):
				greater, token = token, self.popToken()
				if isinstance(token, Greater):
					self.popToken()
					expr = PushRight(expr, forward())	# a >> b
					continue
					self.pushToken(greater)
			break
		return expr

	def parseArithmetic1(self):
		forward = self.parseArithmetic2
		expr = forward()

		while True:
			token = self.token
			if isinstance(token, Plus):
				self.popToken()
				expr = Addition(expr, forward())		# a + b
				continue
			elif isinstance(token, Slash):
				self.popToken()
				expr = Substraction(expr, forward())	# a - b
				continue
			break

		return expr

	parseArithmetic = parseArithmetic1

	def parseArithmetic2(self):
		forward = self.parseArithmetic3
		expr = forward()

		while True:
			token = self.token
			if isinstance(token, Asterisk):
				self.popToken()
				expr = Multiplication(expr, forward())	# a * b
				continue
			elif isinstance(token, Slash):
				self.popToken()
				expr = Division(expr, forward())	# a / b
				continue
			elif isinstance(token, Percent):
				self.popToken()
				expr = Modulo(expr, forward())	# a % b
				continue
			break

		return expr


	def parseArithmetic3(self):
		forward = self.parsePrefix
		expr = forward()
		while True:
			token = self.token
			if isinstance(token, Minus):
				minus, token = token, self.popToken()
				if isinstance(token, Caret):
					self.popToken()
					expr = Pow(expr, forward())	# a -^ a
					continue
				elif isinstance(token, Slash):
					self.popToken()
					expr = Root(expr, forward())	# a -/ a
					continue
				elif isinstance(token, Slash):
					self.popToken()
					expr = Logarithm(expr, forward())	# a -* a
					continue
				self.pushToken(minus)
			break
		return expr


	def parsePrefix(self):
		forward = self.parsePostfix
		token = self.token

		if isinstance(token, Minus):
			self.popToken()
			return Negative(forward())	# - a
		elif isinstance(token, Plus):
			self.popToken()
			return Positive(forward())	# + a
		elif isinstance(token, Exclamation):
			self.popToken()
			return Not(forward())		# ! a
		else:
			return forward()
	'''
	def parseResolutor(self):
		forward = self.parsePostfix
		expr = forward()

		while True:
			token = self.token
			if isinstance(token, resolutor_tokens):
				expr = Resolutor(expr, forward())
				continue
			break

		return expr
	'''
	def parsePostfix(self):
		forward = self.parsePrimary
		expr = forward()

		while True:
			token = self.token
			if isinstance(token, Dot):
				dot, token = token, self.popToken(),
				if isinstance(token, Identifier):
					self.popToken()
					expr = Property(expr, token, dot.location)		# a . b
					continue
				self.pushToken(dot)

			elif isinstance(token, with_tokens):
				expr = With(expr, forward())			# a b
				continue
			break
		return expr

	def parsePrimary(self):
		''
		token = self.token

		if isinstance(token, Identifier):
			self.popToken()
			return token							# a
			#return Local(token)				# a
		elif isinstance(token, Constant):
			self.popToken()
			return token							# K

		elif isinstance(token, Begin):
			begin, token = token, self.popToken()
			forward = self.parseExpression

			block = Block()
			while True:
				token = self.token

				if isinstance(token, Line):
					self.popToken()
					block.append(forward())
					continue
				elif isinstance(token, End):
					self.popToken()
				else:
					self.popToken()
					print('Unexpected', token)
				break
			return block

		elif isinstance(token, OpenParenthesis):
			open_parenthesis, token = token, self.popToken()
			tuple = Tuple()
			while not isinstance(token, CloseParenthesis):
				tuple.append(self.parseExpression())
				token = self.token
				if isinstance(token, Comma):
					token = self.popToken()
					continue
				break
			if not isinstance(token, CloseParenthesis):
				raise SyntaxError('Unexpected token {}'.format(token))
			self.popToken()
			return tuple # (...)

		elif isinstance(token, OpenBracket):
			open_parenthesis, token = token, self.popToken()
			sequence = Sequence()
			while not isinstance(token, CloseBracket):
				sequence.append(self.parseExpression())
				token = self.token
				if isinstance(token, Comma):
					token = self.popToken()
					continue
				break
			if not isinstance(token, CloseBracket):
				raise SyntaxError('Unexpected token {}'.format(token))
			self.popToken()
			return sequence

		'''
		elif isinstance(token, Dot):
			dot, token = token, self.popToken()
			if isinstance(token, Id):
				self.popToken()
				return Global(token)			# . a
			else:
				self.pushToken(dot)
		'''

		raise SyntaxError("Unexpected token {0} {0.__class__.__module__}".format(token))

