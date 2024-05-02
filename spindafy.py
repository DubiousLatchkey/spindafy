from PIL import Image, ImageChops, ImageDraw
from random import randint
import numpy as np

class SpindaConfig:
    sprite_base = Image.open("res/spinda_base.png")
    sprite_mask = Image.open("res/spinda_mask.png")
    spot_masks = [
        Image.open("res/spots/spot_1.png"),
        Image.open("res/spots/spot_2.png"),
        Image.open("res/spots/spot_3.png"),
        Image.open("res/spots/spot_4.png")
    ]
    spot_offsets = [
        (8, 6),
        (32, 7),
        (14, 24),
        (26, 25)
    ]
    def __init__(self):
        self.spots = [
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0)
        ]

    def __str__(self):
        return f"<SpindaConfig> {self.spots}"
    
    @staticmethod
    def from_personality(pers):
        self = SpindaConfig()
        self.spots[0] = (pers & 0x0000000f, (pers & 0x000000f0) >> 4)
        self.spots[1] = ((pers & 0x00000f00) >> 8, (pers & 0x0000f000) >> 12)
        self.spots[2] = ((pers & 0x000f0000) >> 16, (pers & 0x00f00000) >> 20)
        self.spots[3] = ((pers & 0x0f000000) >> 24, (pers & 0xf0000000) >> 28)
        return self
    
    @staticmethod
    def random():
        return SpindaConfig.from_personality(randint(0, 0x100000000))

    def get_personality(self):
        pers = 0x00000000
        for i, spot in enumerate(self.spots):
            pers = pers | (spot[0] << i*8) | (spot[1] << i*8+4)
        return pers

    def render_pattern(self, only_pattern = False, crop = False):
        # Prepare a result image with the same size as base and bg either black or transparent
        size = self.sprite_base.size
        img = Image.new('RGBA', size, (0, 0, 0, 255 if only_pattern else 0))

        # When wanting an actual spinda, start by pasting in the base sprite
        if not only_pattern:
            img.paste(self.sprite_base, (0, 0))

        for index in range(4):
            # Calculate the top-left coordinate for the spot image
            position = (self.spot_offsets[index][0] + self.spots[index][0],
                        self.spot_offsets[index][1] + self.spots[index][1])

            # Create a full-size image for the full spot at the desired position,
            #   as composite operation requires same-sized images
            spot_full = Image.new('RGBA', size, (0, 0, 0, 0))
            spot_full.paste(self.spot_masks[index], position, mask=self.spot_masks[index])

            # Create temporary mask by combining mask and spot mask
            temp_mask = Image.new('RGBA', size, (0, 0, 0, 0))
            temp_mask.paste(self.sprite_mask, (0, 0), mask=spot_full)

            if only_pattern:
                # Composite the white spot onto the masked area
                temp_mask = Image.composite(spot_full, temp_mask, temp_mask)

            # Composite the new mask with the current result
            img = Image.composite(temp_mask, img, temp_mask)

        if crop:
            img = img.crop((17, 15, 52, 48))

        return img

    def get_difference(self, target):
        # Validate the mode will match the type used in the next step
        if target.mode != "RGB":
            target = target.convert("RGB")
        # Compare the resulting images by the total average pixel difference
        result = self.render_pattern(only_pattern=True, crop=True).convert("RGB")
        diff = ImageChops.difference(target, result)
        total_diff = 0
        for n, (r, g, b) in diff.getcolors():  # gives a list of counter and RGB values in the image
            total_diff += n*((r+g+b)/3)
        return total_diff

if __name__ == "__main__":
    PID0000 = 0xFFF000F0
    PID0001 = 0xFFF000CB
    PID0010 = 0xFFF0D6F0
    PID0011 = 0xFFF0D6CB
    PID0100 = 0xFF8A00F0 
    PID0101 = 0xFF8A00CB
    PID0110 = 0xFF8AD6F0
    PID0111 = 0xFF8AD6CB
    PID1000 = 0x99F000F0
    PID1001 = 0x99F000CB
    PID1010 = 0x99F0D6F0
    PID1011 = 0x99F0D6CB
    PID1100 = 0x998A00F0
    PID1101 = 0x998A00CB
    PID1110 = 0x998AD6F0
    PID1111 = 0x998AD6CB

    spin = SpindaConfig.from_personality(PID0000)
    spin.render_pattern().save("0000.png")
    spin = SpindaConfig.from_personality(PID0001)
    spin.render_pattern().save("0001.png")
    spin = SpindaConfig.from_personality(PID0010)
    spin.render_pattern().save("0010.png")
    spin = SpindaConfig.from_personality(PID0011)
    spin.render_pattern().save("0011.png")
    spin = SpindaConfig.from_personality(PID0100)
    spin.render_pattern().save("0100.png")
    spin = SpindaConfig.from_personality(PID0101)
    spin.render_pattern().save("0101.png")
    spin = SpindaConfig.from_personality(PID0110)
    spin.render_pattern().save("0110.png")
    spin = SpindaConfig.from_personality(PID0111)
    spin.render_pattern().save("0111.png")

    spin = SpindaConfig.from_personality(PID1000)
    spin.render_pattern().save("1000.png")
    spin = SpindaConfig.from_personality(PID1001)
    spin.render_pattern().save("1001.png")
    spin = SpindaConfig.from_personality(PID1010)
    spin.render_pattern().save("1010.png")
    spin = SpindaConfig.from_personality(PID1011)
    spin.render_pattern().save("1011.png")
    spin = SpindaConfig.from_personality(PID1100)
    spin.render_pattern().save("1100.png")
    spin = SpindaConfig.from_personality(PID1101)
    spin.render_pattern().save("1101.png")
    spin = SpindaConfig.from_personality(PID1110)
    spin.render_pattern().save("1110.png")
    spin = SpindaConfig.from_personality(PID1111)
    spin.render_pattern().save("1111.png")
    #print(hex(spin.get_personality()))