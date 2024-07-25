import numpy as np


class Noise:
    def __init__(self, height, width, velr, velc, color):
        """
        Initialize the Noise class with the frame dimensions and velocity.

        :param height: Height of the frame
        :param width: Width of the frame
        :param velr: Velocity in the row direction
        :param velc: Velocity in the column direction
        """
        self.img = np.zeros((height, width))
        self.rr = np.array([], dtype=int)
        self.cc = np.array([], dtype=int)
        self.velr = velr
        self.velc = velc
        self.color = color

    def move(self):
        """
        Move the noise by updating its position based on its velocity.
        """
        if len(self.rr) > 0:
            self.rr = (self.rr + self.velr) % self.img.shape[0]
            self.cc = (self.cc + self.velc) % self.img.shape[1]

    def append(self, shapes):
        """
        Append the pixel coordinates of the given shapes to the noise.

        :param shapes: List of shapes to append to the noise
        """
        for shape in shapes:
            sq_rr, sq_cc = shape.getPixelCoordinates()
            sq_rr = sq_rr.astype(int)
            sq_cc = sq_cc.astype(int)
            self.img[sq_rr, sq_cc] = 1

        rr_list = []
        cc_list = []

        for i in range(self.img.shape[0]):
            for j in range(self.img.shape[1]):
                if self.img[i, j] == 1:
                    rr_list.append(i)
                    cc_list.append(j)

        self.rr = np.array(rr_list, dtype=int)
        self.cc = np.array(cc_list, dtype=int)

    def draw(self, frame):
        """
        Draw the noise on the given frame.

        :param frame: The frame on which to draw the noise
        :return: The frame with the noise drawn on it
        """
        frame[self.rr, self.cc, :] = self.color[:]

        return frame
