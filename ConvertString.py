import re


def get_image_size(image: str) -> tuple[int, int]:
    height = len(image.splitlines()[1:-1])
    width = 0
    for line in image.splitlines()[1:-1]:
        line_data = re.compile(r'"(.*)"').findall(line)[0]
        line_data = line_data.replace("\\\\", "\\")
        width = max(width, len(line_data))
    return (width, height)


def get_mask_color(mask: list[str], index: int, default: str):
    if index >= len(mask):
        char = default
    else:
        char = mask[index]

    if char == ' ':
        char = default

    color = -1
    if char == 'r' or char == 'R':
        color = 1
    if char == 'g' or char == 'G':
        color = 2
    if char == 'y' or char == 'Y':
        color = 3
    if char == 'b' or char == 'B':
        color = 4
    if char == 'm' or char == 'M':
        color = 5
    if char == 'c' or char == 'C':
        color = 6
    if char == 'w' or char == 'W':
        color = 7
    if char == 'p':  # gray
        color = 7 + 10
    if ord(char) >= ord('0') and ord(char) <= ord('9'):
        return ord(char) - ord('0')

    if f"{char}".upper() == char and color >= 0:
        return color + 10
    elif color >= 0:
        return color

    raise RuntimeError(":( " + char)


def format_image_init(default_color: str, image: str, mask: str) -> str:
    result = ""

    image_data = []
    for line in image.splitlines()[1:-1]:
        line_data = re.compile(r'"(.+)"').findall(line)[0]
        line_data = line_data.replace("\\\\", "\\")
        image_data.append(line_data)

    mask_data = []

    for line in mask.splitlines()[1:-1]:
        line_data = re.compile(r'"(.*)"').findall(line)[0]
        line_data = line_data.replace("\\\\", "\\")
        mask_data.append(line_data)

    for y, line in enumerate(image_data):
        for x, char in enumerate(line):
            mask_line = mask_data[y] if y < len(mask_data) else ""
            mask_color = get_mask_color(mask_line, x, default_color)
            if char == '?':
                char = '  '
            if mask_color != -1:
                result += f"      .setPixel({x}, {y}, {ord(char[0])}, {mask_color})" + "\n"

    return "      " + result.strip() + ";\n"


def process(lines: str):
    hunks = re.compile(r"String[\[\]]+ (\w+).+\{((.|\n)+?)\};").findall(lines)

    fields = []
    inits = []

    default_colors = {
        "castleImage": "p",  # gray
        "waterLineSegment": "b",
        "fishImage": "y",
        "sharkImage": "c",
        "shipImage": "y",
        "bigFishImage": "Y",
        "monsterImage": "g"
    }

    for hunk in hunks:
        (name, text, _) = hunk
        regex = re.compile(r"\{[^}]+\}")
        frames = regex.findall(text)

        with_mask: list[tuple[str, str]] = []
        i = 0
        while i < len(frames) - 1:
            with_mask.append((frames[i], frames[i+1]))
            i = i + 2

        fields.append(f"public Image[] {name} = new Image[{len(with_mask)}];")
        fields.append(f"public int {name}Count;")
        inits.append(f"{name}Count = {len(with_mask)};")
        for index, item in enumerate(with_mask):
            image, mask = item
            width, height = get_image_size(image)
            text = ""
            text = text + f"{name}[{index}] = new Image().init({width}, {height})\n"
            text = text + format_image_init(default_colors[name], image, mask)
            inits.append(text)

    print("class Images {\n")
    for field in fields:
        print("  " + field)

    print("\n  public Images init() {")

    for init in inits:
        print("    " + init)

    print("    return this;")
    print("  }")
    print("}")

    pass


if __name__ == '__main__':
    with open("input.txt", "r") as file:
        text = file.read()
    process(text)
