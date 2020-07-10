#! /usr/bin/env python

import glob

import SimpleITK as sitk


def process_slice(img, bin_amount, crop):
    img2 = img[crop[0]:crop[2], crop[1]:crop[3]]
    img3 = sitk.BinShrink(img2, [bin_amount, bin_amount])
    return img3


def load_slices(name_string):
    file_names = glob.glob(name_string)
    file_names.sort()
    print(file_names[0])
    print("  ...")
    print(file_names[len(file_names) - 1])
    print(len(file_names), "files")

    # Read the header of the first image to get image size
    reader = sitk.ImageFileReader()
    reader.SetFileName(file_names[0])
    reader.ReadImageInformation()
    size = reader.GetSize()
    bin_amount = int(size[0] / 1000 + 0.5)
    print("Image width =", size[0])
    print("Binning by", bin_amount)

    # Read the first image to compute the crop box
    first_slice = reader.Execute()
    non_black = (first_slice > 0)
    lblstats = sitk.LabelShapeStatisticsImageFilter()
    lblstats.Execute(non_black)
    bounding_box = lblstats.GetBoundingBox(1)
    print(bounding_box)

    # images are shrunk to less than 1000x1000
    slices = [process_slice(first_slice, bin_amount, bounding_box)]
    n = len(file_names)
    # n = 40

    for i in range(1, n):
        try:
            slices.append(process_slice(sitk.ReadImage(file_names[i]),
                                        bin_amount, bounding_box))
            print(i, end=' ')
        except BaseException:
            print("\nError: couldn't read file", file_names[i])
            break

    print("Loaded files:", file_names)
    return slices
