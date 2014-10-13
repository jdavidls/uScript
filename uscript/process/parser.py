from uscript.model.source.lexicon import *
from uscript.model.source.expression import *

__all__ = ('Parser', )

primary_tokens = (Identifier, Constant, Begin, BracketOpen, ParenthesisOpen, CurlyOpen)

with_tokens = (Identifier, Constant, Begin, BracketOpen, ParenthesisOpen, CurlyOpen)

prefix_tokens = (Minus, Plus, Exclamation) + primary_tokens




class Parser:
	def __init__(self):
		self.token_stream = None
		self.current_line = 0
		self.token = None
		self.token_stack = []
		# self.escape_stack = []
		# self.error_stack = []

	def popToken(self):
		if self.token_stack:
			self.token = token = self.token_stack.pop()
		else:
			try:
				self.token = token = next(self.token_stream)
			except StopIteration:
				self.token = token = None
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



	def parseStatement(self):
		forward = self.parseExpression
		expr = forward()

		token = self.token
		if type(token) is Equal:
			equal, token = token, self.popToken()
			expr = Assignment(expr, self.parseStatement())	# a = b
		return expr


	def parseExpression(self):
		forward = self.parseSwitch
		expr = forward()
		return expr


	def parseSwitch(self):
		forward = self.parseLambda
		expr = forward()

		token = self.token

		if type(token) is Colon:
			colon, token = token, self.popToken()
			if type(token) in primary_tokens:
				expr = Pair(expr, self.parseExpression())	# a: ...
			else:
				expr = Pair(expr, None)	# a:


		'''
		if type(token) is Question:
			question, token = token, self.popToken()
			expr = Logic(expr)								# a?


		elif type(token) is Colon:
			colon, token = token, self.popToken()
			if type(token) in primary_tokens:
				expr = Pair(expr, self.parseExpression())	# a: ...
			else:
				expr = Pair(expr, None)	# a:


		while True:
			token = self.token
			if type(token) in primary_tokens:
				expr = With(expr, self.parseSwitch()) # ...
				continue
			break
		'''

		return expr

	def parseLambda(self):
		forward = self.parseOtherwise
		expr = forward()

		'''
		while True:
			token = self.token
			if type(token) in primary_tokens:
				expr = With(expr, self.parseLambda()) # ...
				continue
			break
		'''

		token = self.token
		while True:
			if type(token) is Minus:
				minus, token = token, self.popToken()
				if type(token) is Greater:
					self.popToken()
					expr = Lambda(expr, forward())		# a -> b
					continue
				self.pushToken(minus)
			break
		return expr



	def parseOtherwise(self):
		forward = self.parseThen

		expr = forward()

		while True:
			token = self.token
			if type(token) is Pipe:
				pipe, token = token, self.popToken()
				if type(token) is Pipe:
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
			if type(token) is Ampersand:
				ampersand, token = token, self.popToken()
				if type(token) is Ampersand:
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
			if type(token) is Less:
				less, token = token, self.popToken()
				if type(token) is Equal:
					self.popToken()
					expr = LessEqual(expr, forward())	# <=
					continue
				if type(token) is Greater:
					self.popToken()
					expr = Inequality(expr, forward())	# <>
					continue
				else:
					expr = LessThan(expr, forward())	# <
					continue
			elif type(token) is Greater:
				greater, token = token, self.popToken()
				if type(token) is Equal:
					self.popToken()
					expr = GreaterEqual(expr, forward())# >=
					continue
				if type(token) is Less:
					self.popToken()
					expr = Inequality(expr, forward())	# ><
					continue
				else:
					expr = GreaterThan(expr, forward())	# >
					continue
			elif type(token) is Equal:
				equal, token = token, self.popToken()
				if type(token) is Equal:
					self.popToken()
					expr = Equality(expr, forward())	# ==
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
			if type(token) is Pipe:
				pipe, token = token, self.popToken()
				if type(token) in prefix_tokens:
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
			if type(token) is Caret:
				caret, token = token, self.popToken()
				if type(token) in prefix_tokens:
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
			if type(token) is Ampersand:
				ampersand, token = token, self.popToken()
				if type(token) in prefix_tokens:
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
			if type(token) is Less:
				less, token = token, self.popToken()
				if type(token) is Less:
					self.popToken()
					expr = PushLeft(expr, forward())	# a << b
					continue
				self.pushToken(less)
			elif type(token) is Greater:
				greater, token = token, self.popToken()
				if type(token) is Greater:
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
			if type(token) is Plus:
				self.popToken()
				expr = Addition(expr, forward())		# a + b
				continue
			elif type(token) is Slash:
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
			if type(token) is Asterisk:
				self.popToken()
				expr = Multiplication(expr, forward())	# a * b
				continue
			elif type(token) is Slash:
				self.popToken()
				expr = Division(expr, forward())		# a / b
				continue
			elif type(token) is Percent:
				self.popToken()
				expr = Modulo(expr, forward())			# a % b
				continue
			break

		return expr


	def parseArithmetic3(self):
		forward = self.parsePrefix
		expr = forward()
		while True:
			token = self.token
			if type(token) is Minus:
				minus, token = token, self.popToken()
				if type(token) is Caret:
					self.popToken()
					expr = Pow(expr, forward())			# a -^ b
					continue
				elif type(token) is Slash:
					self.popToken()
					expr = Root(expr, forward())		# a -/ b
					continue
				elif type(token) is Slash:
					self.popToken()
					expr = Logarithm(expr, forward())	# a -* b
					continue
				self.pushToken(minus)
			break
		return expr


	def parsePrefix(self):
		forward = self.parsePostfix
		token = self.token

		if type(token) is Minus:
			self.popToken()
			expr =  Negative(forward())	# - a
		elif type(token) is Plus:
			self.popToken()
			expr = Positive(forward())	# + a
		elif type(token) is Exclamation:
			self.popToken()
			expr = Not(forward())		# ! a
		else:
			expr = forward()

		return expr

	def parsePostfix(self):
		forward = self.parsePrimary
		expr = forward()

		while True:
			token = self.token
			if type(token) is Dot:
				dot, token = token, self.popToken(),
				if type(token) is Identifier:
					self.popToken()
					expr = Property(expr, token, dot.location)		# a . b
					continue
				self.pushToken(dot)
			elif type(token) in primary_tokens:
				expr = With(expr, forward())			# a [preix] b
				continue


			'''
			elif type(token) is Minus:
				minus, token = token, self.popToken()
				if type(token) is Greater:
					self.popToken()
					expr = ArrowRight(expr, self.parseExpression())		# a -> b
					continue
				self.pushToken(minus)
			'''
			break

		return expr

	def parsePrimary(self):
		token = self.token

		if isinstance(token, (Identifier, Constant)):
			self.popToken()
			return token							# a
		elif type(token) is Begin:
			code_block = Block()
			for statement in self.parseBlock():
				code_block.append(statement)

			return code_block

		elif type(token) is ParenthesisOpen:
			return self.parseTuple()

		else:
			self.popToken()
			return Error("Unexpected token {0} {0.__class__.__module__}".format(token))

		assert(False)

	def parseBlock(self):

		forward = self.parseStatement

		begin, token = self.token, self.popToken()

		assert(type(begin) is Begin)

		while True:
			token = self.token
			if type(token) is End:
				self.popToken()
				return
			elif type(token) is Line:
				token = self.popToken()
				yield forward()
			else:
				print("ERROR code block unexpected token", repr(token))
				token = self.popToken()

	def parseTuple(self):
		forward = self.parseStatement
		parenthesis_open, token = self.token, self.popToken()

		assert(type(parenthesis_open) is ParenthesisOpen)

		tuple = Tuple()


		while True:
			if type(token) is ParenthesisClose:
				self.popToken()
				return tuple

			tuple.append(forward())	# try?

			token = self.token

			if type(token) is Comma:
				token = self.popToken()
