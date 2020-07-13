#! /usr/bin/env python

import unittest

import SimpleITK as sitk
import segment


class TestSegment(unittest.TestCase):

    def test_segmentBackground(self):
        print("\nTesting segmentBackground")
        img = sitk.GaussianSource(sitk.sitkUInt16, [100, 100], [20, 25],
                                  [50, 50], 60000)

        img2 = segment.segmentBackground(img)
        components = sitk.ConnectedComponent(img2, img2)
        # sitk.Show(components)

        stats = sitk.LabelShapeStatisticsImageFilter()
        stats.Execute(components)

        print("# labels = ", stats.GetNumberOfLabels())

        c = stats.GetCentroid(1)
        axes = stats.GetPrincipalAxes(1)
        moments = stats.GetPrincipalMoments(1)
        npix = stats.GetNumberOfPixels(1)
        print("Center:", c)
        print("Axes:", axes)
        print("Moments:", moments)
        print("# pixels:", npix)

        self.assertEqual(c, (50.0, 50.0))
        self.assertEqual(axes, (1.0, 0.0, 0.0, 1.0))
        self.assertAlmostEqual(moments[0], 371.119403)
        self.assertAlmostEqual(moments[1], 587.553116769)
        self.assertEqual(npix, 2278)

    def test_segmentSeriesBackgrounds(self):
        """ Only tests if segmentSeriesBackgrounds handles no list.

        Kind of a dumb test, really.
        """

        x = segment.segmentSeriesBackgrounds(None)

        self.assertEqual(len(x), 0)


if __name__ == "__main__":
    unittest.main()
