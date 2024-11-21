import re

def filter_by_list(text: str) -> list[int]:
    numeros = re.findall(r'\d+', text)
    return [int(num) for num in numeros if 1 <= int(num) <= 9]
