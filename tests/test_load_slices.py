#! /usr/bin/env python

import SimpleITK as sitk
import unittest

import load_slices

class TestLoadSlices(unittest.TestCase):
    def test_process_slice(self):
        print ("\nTesting process_slice")
        img = sitk.Image(100,100,sitk.sitkUInt8)

        img2 = load_slices.process_slice(img, 2, [1,1,98,98])

        print(img2.GetSize())
        print(img2.GetSpacing())
        print(img2.GetOrigin())
        self.assertEqual(img2.GetSize(), (48,48))
        self.assertEqual(img2.GetSpacing(), (2,2))
        self.assertEqual(img2.GetOrigin(), (1.5,1.5))

    def test_load_slices(self):
        print ("\nTesting load_slices")
        name_string = "sample/slice.00?.tif"

        slices = load_slices.load_slices(name_string)
        self.assertEqual(len(slices), 10)
        print(type(slices[0]))
        for s in slices:
            self.assertIs(type(s), sitk.Image)

if __name__ == "__main__":
    unittest.main()
