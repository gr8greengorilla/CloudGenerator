from PIL import Image, ImageDraw, ImageOps
import random
import threading
import math

IMAGE_SIZE = (3456, 2160)
#IMAGE_SIZE = (int(3456/4), int(2160/4))
NUM_POINTS = 650
POINT_RANGE = 350
STRENGTH = .5
THREADS = 8

def GenerateImage():
    image = Image.new("RGB", IMAGE_SIZE)
    draw = ImageDraw.Draw(image)

    randompoints = [(int(random.random() * IMAGE_SIZE[0]), int(random.random() * IMAGE_SIZE[1])) for x in range(NUM_POINTS)]
    print("start")
    threads = [threading.Thread(target=generateQuadrant, args=(x, randompoints, draw, x == 0)) for x in range(THREADS)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    image.save("output.png")

def generateQuadrant(index, randompoints, draw, verbose):
    for i in range(int(IMAGE_SIZE[0] / THREADS)):
        i = i + int(IMAGE_SIZE[0] / THREADS * index)
        if verbose:
            print(f"{i}/{IMAGE_SIZE[0] / THREADS * (index + 1)}")
        for j in range(IMAGE_SIZE[1]):

            distanceFromPoints = [((a[0] - i) ** 2 + (a[1] - j) ** 2) ** .5 for a in randompoints]
            distance = min(distanceFromPoints)

            concentration = int((distance / POINT_RANGE) * STRENGTH * 255)

            draw.point((i, j), fill=(concentration, 0, 0))
    print(f"Thread {index} has completed")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    GenerateImage()

