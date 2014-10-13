
class Method:
	'''
	un metodo representa un conjunto de funciones cuyo dominio y
	codominio estan contenidos respectivamente en el dominio y
	codominio del metodo, ej::


		addition: Numeric->Numeric

		addition(:Constant Natural, :Constant Natural):
			addition of contant values

		method(:Natural, :Natural) # funcion del

		Boolean: {0, 1}


	'''

class Tuple(list):
	'''
		un tuple es un conjunto de elementos
		los elementos de un tuple pueden estar nombrados
		el tuple puede estar tipado:
		los tipos de un tuple vienen determinados por los codominios de las funciones y metodos que los han retornado como valor

		El dominio solo acepta tuples que han sido retornados desde un metodo especifico

		Numeric: Any->Tuple

		Tuple Natural

	'''
	def __str__(self):
		return '(' + ', '.join(str(i) for i in self) + ')'



