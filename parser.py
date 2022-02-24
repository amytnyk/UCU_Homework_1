from typing import Dict, Tuple, Optional, List
import pytesseract
import cv2


def get_location(place: str) -> Optional[Dict[str, float]]:
    pass


def parse_place_info(data: str) -> Tuple[str, Dict]:
    data = data[data.index(')') + 1:]
    name = data[data.index(' ') + 1:data.index(',')]
    place_info = { "name": name }
    if (location := get_location(name)) is not None:
        place_info["location"] = location
    return data[data.index(','):], place_info


def parse_churches_info(data: str) -> Tuple[str, List]:
    churches_data = data[:data.index('\nНадає')]
    churches = []
    for church_str in churches_data.split(')'):
        church = {}
        for idx, info in enumerate(list(map(lambda x: x.strip().replace('\n', ' '), filter(len, church_str.split(','))))):
            if info.startswith("в прил."):
                church["location"] = info[info.index("в прил.") + 7:]
            elif info.startswith("мур.") or info.startswith("збуд.") or info.startswith("дер."):
                church["type"] = "дер" if info[:info.index(".")] == "дер" else "мур"
                church["year"] = info[info.index(".") + 1:]
            elif info.startswith("відн.") or info.startswith("відновл."):
                church["recovered"] = info[info.index('.') + 1:]
            elif idx <= 1 and len(info) > 2:
                if "в. " in info:
                    church["location"] = info[info.index('в. ') + 3:]
                    info = info[:info.index('в. ')]
                church["name"] = info[info.index(' ') + 1:]
 
        churches.append({key.strip(): val.strip() for key, val in church.items()})
    
    return data[data.index('\n\n') + 2:], churches


def parse(data: str):
    data, place_info = parse_place_info(data)
    data, churches = parse_churches_info(data)
    return place_info, churches



print(parse(image_to_text("image.jpeg")))
