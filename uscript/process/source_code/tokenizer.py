from uscript.source import lexicon
from uscript.source.lexicon import *

punctuation_marks = {
	# ascii punctuation
	'&': 'Ampersand',
	'*': 'Asterisk',
	'@': 'At',

	'^': 'Caret',
	':': 'Colon',
	',': 'Comma',

	'.': 'Dot',

	'=': 'Equal',
	'!': 'Exclamation',

	'>': 'Greater',

	'#': 'Hash',

	'<': 'Less',

	'-': 'Minus',

	'%': 'Percent',
	'|': 'Pipe',
	'+': 'Plus',

	'?': 'Question',

	';': 'Semicolon',
	'/': 'Slash',

	'(': 'OpenParenthesis',
	')': 'CloseParenthesis',

	'[': 'OpenBracket',
	']': 'CloseBracket',

	'{': 'OpenCurly',
	'}': 'CloseCurly',

	# '·': 'InterPoint',
	# '→': 'RightArrow',
	# '←': 'LeftArrow',
}

text_delimitiers = {
	'\'': '\'',
	'"': '"'
}

def scan_stream(line_stream):


	''
	line_number = 0
	level = 0
	escape_block = False


	yield Begin(line_number)

	for line in line_stream:
		line_number += 1

		# calcula la identacion de la linea
		line_level = len(line) - len(line.lstrip('\t'))

		# corrige el bloque y la identacion
		escape_block = line_level > level + 1

		if line_level > level and not escape_block:
			level += 1
			yield Begin(line_number)

		while(line_level < level):
			level -= 1
			yield End(line_number)

		# escanea la linea
		if escape_block:
			yield Escape(line[level+2:], line_number)
		else:
			if line.strip():
				yield Line(line_number)
				try:
					yield from scan_line(line, line_number)
				except SyntaxError as e:
					yield e

	# \for line in line_stream

	# cierra los bloques abiertos
	while(level):
		level -= 1
		yield End(line_number)

	# cierra el bloque global
	yield End(line_number)



def scan_line(line, line_number=0):
	offset = 0
	line_length = len(line)

	while offset < line_length:
		c = line[offset]
		start_offset = offset
		offset += 1

		# eat spaces
		if c.isspace():
			continue

		# parse id
		elif c.isalpha() or c == '_':
			while offset < line_length and line[offset].isidentifier():
				offset += 1

			yield Identifier(line[start_offset:offset], line_number, start_offset, offset)


		# parse decimal constant
		elif c.isdecimal():
			while offset < line_length and line[offset].isdecimal():
				offset += 1

			if offset < line_length and line[offset] is '.':
				offset += 1
				while offset < line_length and line[offset].isdecimal():
					offset += 1
				yield Constant(float(line[start_offset:offset]), line_number, start_offset, offset)
			else:
				yield Constant(int(line[start_offset:offset]), line_number, start_offset, offset)


		# parse text literal
		elif c in text_delimitiers:
			end_c = text_delimitiers[c]
			offset += 1

			if offset < line_length:
				while line[offset] != end_c:
					offset += 1

					if offset >= line_length:
						yield Error('unexpected EOL while parsing text literal', offset)
						return

				offset += 1

				text = line[start_offset+1:offset-1].encode().decode('unicode-escape')
				yield Constant(text, line_number, start_offset, offset)
			else:
				yield Error('unexpected EOL while parsing text literal', offset)
				return

		# punctuation
		elif c in punctuation_marks:
			yield getattr(lexicon, punctuation_marks[c])(line_number, start_offset, offset)

		# escape sequence
		elif c is '\\':
			yield Escape(line[offset:].strip(), line_number, start_offset, len(line))
			return
		else:
			# consume todos los caracteres inesperados y arroja Error
			yield Error(start_offset, 'unexpected chars')
