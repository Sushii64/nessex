# NESSEX - The NES Sprite EXtractor
Yes. I did name it NES Sex.

No, it was not intentional.

Yes, I'm keeping the name because it's funny.

Created by [Sushii64](https://github.com/Sushii64) :3

## Usage
Requirements:

- Python 3
- Pillow

Install Python from your system's package manager or [their website](https://python.org)

Install Pillow with `pip`:
```bash
pip install Pillow
# Or
python3 -m pip install Pillow
```

Next, use your terminal to use the program.

```bash
# Windows
python main.py "path\to\your\rom.nes"

# Linux
python3 ./main.py "/path/to/your/rom.nes"

# Either for macOS, I don't use it so I forgot which one it was LMAO
```

**Note**: Use `clean` instead of a file path and it will clean up the generated content

**Note**: I don't believe all games work! Please create an [issue](https://github.com/Sushii64/nessex/issues) if a game doesn't work, and I'll work on fixing that!

To be fair though I only tried a few games and only 1 broke, it was probably just a bad ROM

## How it works
NES ROMs are structured to contain various types of data, with the first 16 bytes serving as a header that includes information about the ROM's layout. This header specifies the sizes of the PRG-ROM (Program ROM) and CHR-ROM (Character ROM), which contain the game code and graphics data, respectively.

To extract the CHR-ROM, the program first calculates the size of the PRG-ROM. Each PRG-ROM bank is 16 KB, and the size is determined using the byte at position 4 in the header. This is done with the line:
```python
prg_rom_size = 16 * 1024 * rom_data[4]
```
Here, `rom_data[4]` gives the number of PRG-ROM banks, which is multiplied by 16 KB to get the total size of the PRG-ROM.

Next, the program determines the starting point of the CHR-ROM by adding the size of the PRG-ROM to the fixed header size (16 bytes):
```python
chr_rom_start = 16 + prg_rom_size
```
This calculation skips over the header and PRG-ROM to reach the CHR-ROM.

Finally, the program extracts the CHR-ROM data starting from the calculated position:
```python
chr_data = rom_data[chr_rom_start:]
```
This line reads the CHR-ROM data, which contains the graphics used in the game. The extracted data can then be processed to isolate individual sprites.

shoutouts to copilot for taking like 12 tries to get this section right because I didn't want to write it LMAO
