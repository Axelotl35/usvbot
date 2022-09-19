
def read(file: str) -> str:
	with open (file, "r", encoding="UTF-8") as f:
		return f.read()