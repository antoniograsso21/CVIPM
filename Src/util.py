import cv2 as cv
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import math


class Util:

    @staticmethod
    def from_fits_to_mat(fits_file_name):
        """Return numpy matrix from fits file fits_file_name"""
        file = fits.open(fits_file_name)
        matrix = np.array(file[0].data, np.float64)
        file.close()
        return matrix

    @staticmethod
    def from_pix_to_wcs(pixel_coord, wcs):
        """Return world coordinates for the given pixel coordinates pixel_coord"""
        return wcs.all_pix2world(pixel_coord[0], pixel_coord[1], 0)

    @staticmethod
    def kernel_size(sigma):
        """Determine kernel size according to sigma"""
        size = int(sigma * 6)
        if size >= 5:
            if size % 2 == 0:
                size += 1
            return size, size
        else:
            return 5, 5

    @staticmethod
    def distance4(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def neigh4(p):
        return [
            (p[0] - 1, p[1]),
            (p[0], p[1] - 1),
            (p[0] + 1, p[1]),
            (p[0], p[1] + 1)
        ]

    @staticmethod
    def distance8(a, b):
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

    @staticmethod
    def neigh8(p):
        return [
            (p[0] - 1, p[1] - 1),
            (p[0] - 1, p[1]),
            (p[0] - 1, p[1] + 1),
            (p[0], p[1] - 1),
            (p[0], p[1] + 1),
            (p[0] + 1, p[1] - 1),
            (p[0] + 1, p[1]),
            (p[0] + 1, p[1] + 1)
        ]

    @staticmethod
    def local_maxima(img):
        maxima = []
        for i in range(1, len(img) - 1):
            for j in range(1, len(img[i]) - 1):
                is_max = True
                for p in Util.neigh8((i, j)):
                    if img[p[0]][p[1]] >= img[i][j]:
                        is_max = False
                if is_max:
                    maxima.append(((i, j), img[i][j]))
        return maxima

