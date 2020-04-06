#! /usr/bin/env python

import SimpleITK as sitk
import unittest

import find_ellipse

class TestFindEllipse(unittest.TestCase):
    def test_compute_extents(self):
        print ("\nTesting compute_extents")
        img = sitk.Image(100,100,sitk.sitkUInt8)
        img.SetOrigin([1,1])
        img.SetSpacing([2,1])
        #print(img)
        center = [100,50]
        radius = 20
        imin, imax = find_ellipse.compute_extents(img, center, radius)
        print(imin, imax)
        self.assertEqual(imin, [40, 29])
        self.assertEqual(imax, [60, 69])


    def test_find_ellipse(self):
        print ("\nTesting find_ellipse")
        blob = sitk.GaussianSource(sitk.sitkUInt8, [512,512], [30,50], [200, 300])
        bblob = sitk.BinaryThreshold(blob, 200, 255)
        #sitk.Show(bblob)
        center, axes = find_ellipse.find_ellipse(bblob, [180,310], 80)
        print(center, axes)
        self.assertEqual(center, (200.0,300.0))
        self.assertEqual(axes,(1.0,0.0,0.0,1.0))

if __name__ == "__main__":
    unittest.main()
