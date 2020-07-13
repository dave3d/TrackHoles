#! /usr/bin/env python

import math
import os
import unittest

import SimpleITK as sitk
import draw_ellipses
import track_hole


class TestTrackHole(unittest.TestCase):

    def test_track_hole(self):
        print("\nTesting track_hole")

        slices = []
        seed = []
        centers = []

        for z in range(0, 400):
            zf = float(z)
            xsize = 40. + 10.0 * math.cos(zf / 8.0)
            ysize = 50. - 10.0 * math.sin(zf / 10.0)
            xpos = 200.0 + zf / 5.0
            ypos = 300.0 - zf / 6.0

            zslice = sitk.BinaryThreshold(sitk.GaussianSource(
                sitk.sitkUInt8, [512, 512], sigma=[xsize, ysize],
                mean=[xpos, ypos]), 200, 255, 0, 1)

            centers.append([xpos, ypos])

            if len(seed) == 0:
                seed = [xpos - 5, ypos + 6]
            slices.append(zslice)

        radius = 100
        ellipses = track_hole.track_hole(seed, radius, slices)
        # print(ellipses)
        img = sitk.JoinSeries(slices)
        result = draw_ellipses.draw_ellipses(img, ellipses)

        if "SITK_SHOW" in os.environ:
            sitk.Show(result)

        count = 0
        fail_count = 0
        for e, c in zip(ellipses, centers):
            ce = e[0]
            dx = c[0] - ce[0]
            dy = c[1] - ce[1]
            d = math.sqrt(dx * dx + dy * dy)
            if d > .5:
                print("\nBad center", count, round(d, 3))
                print(c)
                print(e)
                fail_count = fail_count + 1
            count = count + 1
        if fail_count:
            print("%d center errors total", fail_count)
            self.fail()


if __name__ == "__main__":
    unittest.main()
