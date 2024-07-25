import imageio
import os
import av
from shapes import *
from noise import Noise
import traceback


class VideoEditor:
    def __init__(self, velocity_r, velocity_c, side_h, side_w, num,
                 height=720, width=1280, noise_row=1, noise_col=1, shape='square', color=(0, 0, 0)):
        """
        Initialize the VideoEditor class with parameters for shape placement and video editing.

        :param velocity_r: Row velocity of shapes
        :param velocity_c: Column velocity of shapes
        :param side_h: Height of the shapes
        :param side_w: Width of the shapes
        :param num: Number of shapes
        :param height: Height of the video frame default 720
        :param width: Width of the video frame, default 1280
        :param noise_row: Noise factor for row placement, default 1
        :param noise_col: Noise factor for column placement, default 1
        :param shape: Shape type ('square' or 'drop'), default 'square
        :param color: Color of the shapes in the RGB format, default value is black or (0,0,0)
        """
        self.height = height
        self.width = width
        self.vel_r = velocity_r
        self.vel_c = velocity_c
        self.side_h = side_h
        self.side_w = side_w
        self.num = num
        self.noise_row = noise_row
        self.noise_col = noise_col
        self.color = color
        self.shape = shape
        self.shapes = self.placeShapes()

        self.noise = Noise(height, width, velocity_r, velocity_c, color)
        self.noise.append(self.shapes)

    def placeShapes(self):
        """
        Place shapes on the video frame based on the equally spaced grid.

        :return: List of placed shapes
        """
        num_on_x = int(np.sqrt(self.width * self.num / self.height))
        num_on_y = self.num // num_on_x
        col_gap = self.width / num_on_x
        row_gap = self.height / num_on_y

        shapesArr = []
        if self.shape == 'square':
            for col_i in range(num_on_x):
                for row_i in range(num_on_y):
                    shapesArr.append(Square(row_gap * row_i + row_gap / 2 * self.noise_row * np.random.rand(),
                                            col_gap * col_i + col_gap / 2 * self.noise_col * np.random.rand(),
                                            self.height, self.width, self.vel_r, self.vel_c,
                                            self.side_h, self.side_w, self.color))
        elif self.shape == 'drop':
            for col_i in range(num_on_x):
                for row_i in range(num_on_y):
                    shapesArr.append(Drop(row_gap * row_i + row_gap / 2 * self.noise_row * np.random.rand(),
                                          col_gap * col_i + col_gap / 2 * self.noise_col * np.random.rand(),
                                          self.height, self.width, self.vel_r, self.vel_c,
                                          self.side_h, self.side_w, self.color))

        print(f"displayed number of shapes: {num_on_x * num_on_y}")

        return shapesArr

    def calculateCoveredPixels(self):
        """
        Calculate the number of pixels covered by the shapes.

        :return: Total number of covered pixels
        """
        tempImgArray = np.zeros((self.height, self.width))
        for square in self.shapes:
            rr, cc = square.getPixelCoordinates()
            rr = rr.astype(int)
            cc = cc.astype(int)
            tempImgArray[rr, cc] = 1
        return np.sum(tempImgArray)

    def edit(self, filename, noisyname, fps=30, codec='libx264', bitrate='4000k'):
        """
        Edit a video by adding noise and shapes.

        :param filename: Input video file path
        :param noisyname: Output noisy video file path
        :param fps: Frames per second for the output video
        :param codec: Codec to be used for the output video
        :param bitrate: Bitrate for the output video
        """
        global container, writer
        isFirstFrame = True

        try:
            container = av.open(filename)
            stream = container.streams.video[0]
            writer = imageio.get_writer(noisyname, fps=fps, codec=codec, bitrate=bitrate)

            for frame in container.decode(stream):
                imgArray = frame.to_rgb().to_ndarray()

                self.noise.move()
                imgArray = self.noise.draw(imgArray)

                if isFirstFrame:
                    coveredPixels = self.calculateCoveredPixels()
                    print(
                        f"Pixels covered: {coveredPixels}, coverage percent: "
                        f"{coveredPixels / (self.height * self.width) * 100}%")

                isFirstFrame = False
                writer.append_data(imgArray)

        except av.AVError as e:
            print(f"An error occurred with the AV library: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print(traceback.format_exc())

        finally:
            container.close()
            writer.close()

    def editAll(self, directory, extension):
        """
        Edit all videos in a directory by adding noise and shapes.

        :param directory: Directory containing video files
        :param extension: Extension of video files to be processed
        """
        for filename in os.listdir(directory):
            if filename.endswith(extension):
                self.edit(os.path.join(directory, filename), "noisy_" + filename)
