# TODO:
#   - explanation comments on every line
#   - NES colour palette so it doesnt look like Bad
#   - works for more games
#   - make the spritesheet look all nice with all the sprites fully pieced together
#       - idk how I'd do that considering how the sheet is laid out
#       - maybe even add labels??
#           - depending on something in the file????? 
#           - is that even . possible

###############################################################
# NESSEX - The Nintendo Entertainment System Sprite EXtractor #
#     Developed and poorly named by Sushii64 on github :3     #
###############################################################
import os
import math
import sys
from PIL import Image

nsx_location = os.path.dirname(os.path.abspath(__file__))

def convert_bytes(bytes, suffix="bytes"):
    for unit in ("", "kilo", "mega", "giga", "tera", "peta", "exa", "zetta"):
        if abs(bytes) < 1024.0:
            return f"{bytes:3.1f} {unit}{suffix}"
        bytes /= 1024.0
    return f"{bytes:.1f} yotta{suffix}"

def testfor_removedir(dir: str):
    if os.path.exists(dir):
        for root, dirs, files in os.walk(dir):
            for file in files:
                os.remove(os.path.join(nsx_location + "/" + dir + "/" + file))
        os.removedirs(dir)

def testfor_removefile(file: str):
    if os.path.exists(file):
        os.remove(os.path.join(nsx_location + "/" + file))

def extract_sprites(chr_data):
    sprites = []
    for i in range(0, len(chr_data), 16):  # Each sprite is 16 bytes
        sprite = [0] * 64  # 8x8 sprite
        for row in range(8):
            byte1 = chr_data[i + row]
            byte2 = chr_data[i + row + 8]
            for col in range(8):
                color = ((byte1 >> (7 - col)) & 1) + (((byte2 >> (7 - col)) & 1) << 1)
                sprite[row * 8 + col] = color
        sprites.append(sprite)
    return sprites

def clean_exports():
    testfor_removedir("sprites")
    testfor_removefile("spritesheet_actual.png")
    testfor_removefile("spritesheet_big.png")

def save_sprites(sprites, output_dir='sprites'):
    clean_exports()
    try:
        os.mkdir("sprites")
    except FileExistsError:
        pass
    for i, sprite in enumerate(sprites):
        image = Image.new('RGB', (8, 8))
        pixels = image.load()
        for y in range(8):
            for x in range(8):
                color = sprite[y * 8 + x]
                pixels[x, y] = (color * 85, color * 85, color * 85)
        image.save(f'{output_dir}/sprite_{i}.png')

def read_rom(file_path):
    with open(file_path, 'rb') as rom:
        return rom.read(), os.path.basename(file_path), convert_bytes(os.path.getsize(file_path))
        
def create_spritesheet(sprites, sprites_per_row=None):
    num_sprites = len(sprites)
    if sprites_per_row is None:
        sprites_per_row = math.ceil(math.sqrt(num_sprites))

    sheet_width = sprites_per_row * 8
    sheet_height = math.ceil(num_sprites / sprites_per_row) * 8
    spritesheet = Image.new('RGB', (sheet_width, sheet_height))

    x, y = 0, 0
    for sprite in sprites:
        image = Image.new('RGB', (8, 8))
        pixels = image.load()
        for row in range(8):
            for col in range(8):
                color = sprite[row * 8 + col]
                pixels[col, row] = (color * 85, color * 85, color * 85)

        spritesheet.paste(image, (x * 8, y * 8))
        x += 1
        if x >= sprites_per_row:
            x = 0
            y += 1

    return spritesheet

def blow_up(image, scale_factor=4):
    blown_up_image = image.resize((image.width * scale_factor, image.height * scale_factor), Image.NEAREST)
    return blown_up_image

def cli():
    if len(sys.argv) > 1:
        if sys.argv[1]:
            if sys.argv[1] == "clean": 
                print("cleaning up...")
                clean_exports()
                return
            else:
                rom_path = sys.argv[1]
    else: 
        print("Usage:")
        print("\npython3 nessex.py [file_path]")
        return
    rom_data, rom_filename, rom_size = read_rom(rom_path)

    print(f"extracting sprites from {rom_filename}...")

    prg_rom_size = 16 * 1024 * rom_data[4]  # 16KB per bank
    chr_rom_start = 16 + prg_rom_size  # Skip the 16-byte header and PRG-ROM
    chr_data = rom_data[chr_rom_start:] # Get the CHR-ROM data

    sprites = extract_sprites(chr_data)
    save_sprites(sprites)

    spritesheet = create_spritesheet(sprites)
    spritesheet.save('spritesheet_actual.png')

    big_spritesheet = blow_up(spritesheet, 8)
    big_spritesheet.save('spritesheet_big.png')

    print(f"\n\"{rom_filename}\"\n{len(sprites)} sprites\n{rom_size}\n")

if __name__ == "__main__":
    cli()