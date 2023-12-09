from typing import List, Dict
from collections import Counter

from utils import read_input


Layer = List[List[int]]
Image = List[Layer]

def parse_image(raw: str, width: int, height: int) -> Image:
    digits = [int(d) for d in raw]
    n_layers = len(raw) // width // height

    image = [
        [
            [
                digits[(i:=i+1 if c+r+l > 0 else 0)] for c in range(width)
            ] for r in range(height)
        ] for l in range(n_layers)
    ]

    return image


def count_colors(image: Image) -> List[Dict[int, int]]:
    return [
        Counter(x for row in l for x in row) for l in image
    ]


def one_by_two(image: Image) -> int:
    color_counts = count_colors(image)

    layer = min(color_counts, key=lambda cc: cc[0])
    return layer[1] * layer[2]


raw = "123456789012"

image = parse_image(raw, 3, 2)

assert image == [[[1,2,3], [4,5,6]], [[7,8,9], [0,1,2]]]


RAW = read_input(day=8, part=1)[0]

IMAGE = parse_image(RAW, 25, 6)
print(one_by_two(IMAGE))


def stack_layers(top_layer: Layer, bottom_layer: Layer) -> Layer:
    output_layer = [
        [
            None for _ in range(len(top_layer[0]))
        ] for _ in range(len(top_layer))
    ]


    for i in range(len(top_layer)):
        for j in range(len(top_layer[0])):
            if top_layer[i][j] == 2:
                output_layer[i][j] = bottom_layer[i][j]
            else:
                output_layer[i][j] = top_layer[i][j]

    return output_layer


def decode_image(image: Image) -> Layer:
    output_layer = image[0]

    for layer in image[1:]:
        output_layer = stack_layers(output_layer, layer)

    return output_layer



raw2 = "0222112222120000"

image2 = parse_image(raw2, 2, 2)

assert decode_image(image2) == [[0,1], [1, 0]]



decoded = decode_image(IMAGE)


print("\n".join(["".join("#" if x else " " for x in row) for row in decoded]))
