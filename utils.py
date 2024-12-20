import re
import json
import pprint

def filter_by_list(text: str) -> list[int]:
    numeros = re.findall(r'\d+', text)
    return [int(num) for num in numeros if 1 <= int(num) <= 9]

def convert_response(response_text: str) -> json:
    json_convert = response_text.strip("(```)")
    json_convert = json_convert.replace('json\n', '', 1).replace('json', '', 1).replace('```','')
    return json.loads(json_convert)