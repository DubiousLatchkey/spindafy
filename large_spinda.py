from PIL import Image
from spinda_optimizer import evolve
import json, PIL.ImageOps
from spindafy import SpindaConfig
import numpy as np

# this is definitely not the best way of doing this!
def to_spindas(filename, pop, n_generations, invert = False):
    with Image.open(filename) as target:
        target = target.convert("RGB")
        if invert: target = PIL.ImageOps.invert(target)

        num_x = int((target.size[0]+10)/25)
        num_y = int((target.size[1]+13)/20)

        print(f"Size: {num_x} * {num_y}")

        img = Image.new("RGBA", (39 + num_x * 25, 44 + num_y * 20))
        pids = []

        for y in range(num_y):
            pids += [[]]
            for x in range(num_x):
                print(f"Subimage {x}|{y}")
                sub_target = target.crop((
                    x*25, y*20,
                    x*25+35,
                    y*20+33
                ))
                (_, best_spinda) = evolve(sub_target, pop, n_generations)
                spinmage = best_spinda.render_pattern()
                img.paste(
                    spinmage,
                    (x * 25, y * 20),
                    spinmage
                )
                pids[y] += [best_spinda.get_personality()]

        return (img, pids)
    

def getAverageBrightness(image):
    return np.asarray(image).mean()

def approximate_to_spindas(filename, invert = False):
    with Image.open(filename) as target:
        target = target.convert("L")
        if invert: target = PIL.ImageOps.invert(target)

        num_x = int((target.size[0]+10)/25)
        num_y = int((target.size[1]+13)/20)

        print(f"Size: {num_x} * {num_y}")

        img = Image.new("RGBA", (39 + num_x * 25, 44 + num_y * 20))
        pids = []

        for y in range(num_y):
            pids += [[]]
            for x in range(num_x):
                print(f"Subimage {x}|{y}")
                sub_target = target.crop((
                    x*25, y*20,
                    x*25+35,
                    y*20+33
                ))

                # Divide spinda into 4 quadrants (numbered in PID order)
                quadrant4 = sub_target.crop((0, 0 , 16, 16))
                quadrant3 = sub_target.crop((16, 0, sub_target.size[0], 16))
                quadrant2 = sub_target.crop((0, 16, 16, sub_target.size[1]))
                quadrant1 = sub_target.crop((16, 16, sub_target.size[0], sub_target.size[1]))
                
                # Find average brightnesses
                averageBrightnesses = [getAverageBrightness(quadrant1), getAverageBrightness(quadrant2), 
                                       getAverageBrightness(quadrant3), getAverageBrightness(quadrant4)]

                # In each quadrant, if too bright, default to position where dot doesn't show, otherwise place in middle
                whiteThreshold = 128
                PID1 = 0x99000000 if averageBrightnesses[0] < whiteThreshold else 0xFF000000
                PID2 = 0x008A0000 if averageBrightnesses[1] < whiteThreshold else 0x00F00000
                PID3 = 0x0000D600 if averageBrightnesses[2] < whiteThreshold else 0x00000000
                PID4 = 0x000000CB if averageBrightnesses[2] < whiteThreshold else 0x000000F0

                PID = PID1 | PID2 | PID3 | PID4
                spinda = SpindaConfig.from_personality(PID)


                spinmage = spinda.render_pattern()
                img.paste(
                    spinmage,
                    (x * 25, y * 20),
                    spinmage
                )
                pids[y] += [spinda.get_personality()]

        return (img, pids)
                
           
if __name__ == "__main__":
    # (img, pids) = to_spindas("doom/test.png", 100, 10)
    # img.resize((img.size[0]*10, img.size[1]*10), Image.Resampling.NEAREST).show()
    # img.save("doom/test_res.png")
    # with open("doom/test.json", "w") as f:
    #     json.dump(pids, f)
    (img, pids) = approximate_to_spindas("doom/test.png", True)
    img.resize((img.size[0]*10, img.size[1]*10), Image.Resampling.NEAREST).show()
    img.save("doom/test_res.png")