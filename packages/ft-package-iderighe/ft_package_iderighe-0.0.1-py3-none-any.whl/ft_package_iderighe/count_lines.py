def count_lines_in_file(filepath: str) -> int:
	"""
	Count the number of lines in a file.
	"""
	# return sum(1 for _ in open(filepath)) => ATTENTION pas bonne pratique (car on n'est pas sur que le fichier sera correctement fermé si une exception est levée)
	with open(filepath, 'r') as file:
		return sum(1 for _ in file)