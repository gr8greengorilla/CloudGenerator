from PIL import Image, ImageDraw, ImageOps
import random
import threading
import math

IMAGE_SIZE = (3456, 2160)
#IMAGE_SIZE = (300, 300)
CLOUD_SPAWN_RANGE = (230, 230)
POINT_RANGE = 500
STRENGTH = .5
THREADS = 8

def GenerateImage():
    image = Image.new("RGB", IMAGE_SIZE)
    draw = ImageDraw.Draw(image)

    numHorizontalSpaces = int(IMAGE_SIZE[0] / CLOUD_SPAWN_RANGE[0])
    numVerticalSpaces = int(IMAGE_SIZE[1] / CLOUD_SPAWN_RANGE[1])

    randompoints = []
    for y in range(0, numVerticalSpaces):
        for x in range(0, numHorizontalSpaces):
            randompoints.append((int(random.random() * CLOUD_SPAWN_RANGE[0] + CLOUD_SPAWN_RANGE[0] * x), int(random.random() * CLOUD_SPAWN_RANGE[1] + CLOUD_SPAWN_RANGE[1] * y)))

    #for x, y in randompoints:
    #    draw.ellipse([(x, y), (x+10, y+10)], fill=(255, 255, 255))

    for y in range(IMAGE_SIZE[1]):
        for x in range(IMAGE_SIZE[0]):
            distanceFromPoints = []

            if (y % 100 == 0):
                print(y)

            xGridPos = int(x / CLOUD_SPAWN_RANGE[0])
            yGridPos = int(y / CLOUD_SPAWN_RANGE[1])
            gridPosition = xGridPos + yGridPos * numHorizontalSpaces

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if xGridPos == 0 and i == -1:
                        continue
                    if xGridPos + 1 % numHorizontalSpaces == 0 and i == 1:
                        continue

                    if 0 <= gridPosition + i + numHorizontalSpaces * j < len(randompoints):
                        point = randompoints[gridPosition + i + numHorizontalSpaces * j]
                        distance = ((x - point[0]) ** 2 + (y - point[1]) ** 2) ** .5
                        distanceFromPoints.append(distance)

            bestDistance = min(distanceFromPoints)

            concentration = int(bestDistance / POINT_RANGE * STRENGTH * 255)
            draw.point((x, y), fill=(concentration, 0, 0))


    image.save("output.png")

def generateQuadrant(index, randompoints, draw, verbose):
    for i in range(int(IMAGE_SIZE[0] / THREADS)):
        i = i + int(IMAGE_SIZE[0] / THREADS * index)
        for j in range(IMAGE_SIZE[1]):

            distanceFromPoints = [((a[0] - i) ** 2 + (a[1] - j) ** 2) ** .5 for a in randompoints]
            distance = min(distanceFromPoints)

            concentration = int((distance / POINT_RANGE) * STRENGTH * 255)

            draw.point((i, j), fill=(concentration, 0, 0))
    print(f"Thread {index} has completed")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    GenerateImage()

