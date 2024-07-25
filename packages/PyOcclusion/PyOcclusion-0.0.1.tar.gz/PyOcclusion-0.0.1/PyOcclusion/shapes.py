from skimage import draw
import numpy as np


class Shape:
    def __init__(self, r, c, height, width, velr, velc, color):
        """
        Initialize the Shape class with position, frame dimensions, velocity, and color.

        :param r: Initial row position
        :param c: Initial column position
        :param height: Height of the frame
        :param width: Width of the frame
        :param velr: Velocity in row direction
        :param velc: Velocity in column direction
        :param color: Color of the shape
        """
        self.r = r
        self.c = c
        self.frameHeight = height
        self.frameWidth = width
        self.velr = velr
        self.velc = velc
        self.num_pixels = 0
        self.color = color

    def move(self):
        """
        Move the shape by updating its position based on its velocity.
        """
        self.r += self.velr
        self.c += self.velc


class Square(Shape):
    def __init__(self, r, c, height, width, velr, velc, sizer, sizec, color):
        """
        Initialize the Square class with additional parameters for size.

        :param r: Initial row position
        :param c: Initial column position
        :param height: Height of the frame
        :param width: Width of the frame
        :param velr: Velocity in row direction
        :param velc: Velocity in column direction
        :param sizer: Size of the square in the row direction
        :param sizec: Size of the square in the column direction
        :param color: Color of the square
        """
        super().__init__(r, c, height, width, velr, velc, color)
        self.sizec = sizec
        self.sizer = sizer

    def draw(self, frame):
        """
        Draw the square on the given frame.

        :param frame: The frame on which to draw the square
        :return: The frame with the square drawn on it
        """
        rr, cc = draw.rectangle((self.r, self.c), extent=(self.sizer, self.sizec))

        rr = rr % self.frameHeight
        cc = cc % self.frameWidth

        frame[rr, cc, 0] = self.color[0]
        frame[rr, cc, 1] = self.color[1]
        frame[rr, cc, 2] = self.color[2]

        return frame

    def getPixelCoordinates(self):
        """
        Get the pixel coordinates of the square.

        :return: Row and column coordinates of the square
        """
        rr, cc = draw.rectangle((self.r, self.c), extent=(self.sizer, self.sizec))

        rr = rr % self.frameHeight
        cc = cc % self.frameWidth

        return rr, cc


class Drop(Shape):
    def __init__(self, r, c, height, width, velr, velc, radius, length, color):
        """
        Initialize the Drop class with additional parameters for radius and length.

        :param r: Initial row position
        :param c: Initial column position
        :param height: Height of the frame
        :param width: Width of the frame
        :param velr: Velocity in row direction
        :param velc: Velocity in column direction
        :param radius: Radius of the drop
        :param length: Length of the drop
        :param color: Color of the drop
        """
        super().__init__(r, c, height, width, velr, velc, color)
        self.length = length
        self.radius = radius

    def generateVerticies(self, r_start, c_start, r_end, radius):
        """
        Generate the vertices of the drop shape.

        :param r_start: Starting row position
        :param c_start: Starting column position
        :param r_end: Ending row position
        :param radius: Radius of the drop
        :return: Lists of row and column vertices
        """
        rows = []
        rows.append(r_start)
        columns = []
        columns.append(c_start)
        for i in range(-1 * radius, radius + 1, 1):
            column = c_start + i
            row = r_end + np.sqrt(radius ** 2 - i ** 2)
            rows.append(row)
            columns.append(column)

        rows.append(r_start)
        columns.append(c_start)
        return rows, columns

    def draw(self, frame):
        """
        Draw the drop on the given frame.

        :param frame: The frame on which to draw the drop
        :return: The frame with the drop drawn on it
        """
        rows, columns = self.generateVerticies(self.r, self.c, self.r + self.length, self.radius)

        rr, cc = draw.polygon(rows, columns)

        rr = rr % self.frameHeight
        cc = cc % self.frameWidth

        image_shape = (self.frameHeight, self.frameWidth)
        img = np.zeros(image_shape)
        img[rr, cc] = 1
        self.num_pixels = np.sum(img)

        frame[rr, cc, :] = self.color

        return frame

    def getPixelCoordinates(self):
        """
        Get the pixel coordinates of the drop.

        :return: Row and column coordinates of the drop
        """
        rows, columns = self.generateVerticies(self.r, self.c, self.r + self.length, self.radius)

        rr, cc = draw.polygon(rows, columns)

        rr = rr % self.frameHeight
        cc = cc % self.frameWidth
        return rr, cc
