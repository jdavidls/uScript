


def unique(iterable, key=None):
	"List unique elements, preserving order. Remember all elements ever seen."
	from itertools import filterfalse
	seen = set()
	seen_add = seen.add
	if key is None:
		for element in filterfalse(seen.__contains__, iterable):
			seen_add(element)
			yield element
	else:
		for element in iterable:
			k = key(element)
			if k not in seen:
				seen_add(k)
				yield element


class MetaTuple:
	@classmethod
	def __prepare__(cls, name, bases, *args, **kwds):
		print(name, bases)
		return type.__prepare__(name)

	def __new__(cls, name, bases, dct, **kwds):
		''
		from itertools import chain



		dct['__slots__'] = unique(chain())
		return type(name, bases, dct)


class TupleObject(metaclass=MetaTuple):
	__slots__ = ()

	def __init__(self):
		''

	def __iter__(self):
		''

		# por defecto, itera sobre los slots, haciendo yield sobre ellos,
		#	cuando recibe new_value = yield self.value


