
class Location:
	__slots__ = ('start_line', 'start_offset', 'end_line', 'end_offset')
	def __init__(self, *locator):
		if len(locator) is 0:
			self.start_line = self.end_line = None
			self.start_offset = self.end_offset = None
		elif len(locator) is 1:
			self.start_line = self.end_line = locator[0]
			self.start_offset = self.end_offset = None
		elif len(locator) is 2:
			self.start_line = self.end_line = locator[0]
			self.start_offset = self.end_offset = locator[1]
		elif len(locator) is 3:
			self.start_line = self.end_line = locator[0]
			self.start_offset = locator[1]
			self.end_offset = locator[2]
		elif len(locator) is 4:
			self.start_line = locator[0]
			self.start_offset = locator[1]
			self.end_line = locator[2]
			self.end_offset = locator[3]
		else:
			raise ValueError('invalid argument length')

	def __str__(self):
		if self.start_line is None:
			return "unknow location"
		elif self.start_line == self.end_line:
			if self.start_offset is None:
				return "line {0.start_line}".format(self)
			elif self.start_offset == self.end_offset:
				return "line {0.start_line} offset {0.start_offset}".format(self)
			else:
				return "line {0.start_line} offset {0.start_offset}..{0.end_offset}".format(self)
		else:
			return "line {0.start_line} offset {0.start_offset} .. line {0.end_line} offset {0.end_offset}".format(self)
