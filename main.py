from PIL import Image, ImageDraw
import random

IMAGE_SIZE = (3456, 2160)
#IMAGE_SIZE = (300, 300)
CLOUD_SPAWN_RANGE = (230, 230)
POINT_RANGE = 500
STRENGTH = .5

def GenerateImage():
    # Create the image to be edited.
    image = Image.new("RGB", IMAGE_SIZE)
    draw = ImageDraw.Draw(image)

    # Calculate the number of cells in the image
    numHorizontalSpaces = int(IMAGE_SIZE[0] / CLOUD_SPAWN_RANGE[0])
    numVerticalSpaces = int(IMAGE_SIZE[1] / CLOUD_SPAWN_RANGE[1])

    # Create on random point per cell and add it to an array
    randompoints = []
    for y in range(0, numVerticalSpaces):
        for x in range(0, numHorizontalSpaces):
            randompoints.append((int(random.random() * CLOUD_SPAWN_RANGE[0] + CLOUD_SPAWN_RANGE[0] * x), int(random.random() * CLOUD_SPAWN_RANGE[1] + CLOUD_SPAWN_RANGE[1] * y)))

    # Loop over every image pixel left to right top to down
    for y in range(IMAGE_SIZE[1]):

        # Calculate the y cell of the pixel
        yGridPos = int(y / CLOUD_SPAWN_RANGE[1])

        for x in range(IMAGE_SIZE[0]):

            # Calculate the cell that the pixel is located in
            # Stores the index of the randompoint of the cell in gridPosition
            distanceFromPoints = []
            xGridPos = int(x / CLOUD_SPAWN_RANGE[0])
            gridPosition = xGridPos + yGridPos * numHorizontalSpaces

            # Find the indexes of the surrounding cells
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # Prevent the search for the shortest distance from considering cells across the image
                    if xGridPos == 0 and i == -1:
                        continue
                    if xGridPos + 1 % numHorizontalSpaces == 0 and i == 1:
                        continue

                    # If the cell index is in range, caluclate the distance to the random point
                    # in that cell and add it to a list
                    potentialCellIndex = gridPosition + i + numHorizontalSpaces * j
                    if 0 <= potentialCellIndex < len(randompoints):
                        point = randompoints[potentialCellIndex]
                        distance = ((x - point[0]) ** 2 + (y - point[1]) ** 2) ** .5
                        distanceFromPoints.append(distance)

            # Get the smallest distance from the list
            bestDistance = min(distanceFromPoints)

            # Make the pixel color concentration inversely scale with the distance to the point
            concentration = int(bestDistance / POINT_RANGE * STRENGTH * 255)
            draw.point((x, y), fill=(concentration, 0, 0))

    # Output image
    image.save("output.png")

if __name__ == '__main__':
    GenerateImage()

