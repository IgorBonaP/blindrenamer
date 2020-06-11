import pathlib

def get_file_iterator(target:str, subtree:bool, ext=None):
	'''
	Return an iterator with the files present in path.
	Uses Path.glob() if subtree is True and Path.iterdir() otherwise.
	'''
	pattern = "*"

	if ext:
		pattern += ext

	if subtree:
		pattern = f"**/{pattern}"

	file_iterator = pathlib.Path(target).glob(pattern)
	return file_iterator

if __name__ in ("__main__", "__builtin__"):
	print(*get_file_iterator(r"test",  True, ext=".txt"))