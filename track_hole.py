#! /usr/bin/env python

import SimpleITK as sitk
import find_ellipse


def track_hole(seed, radius, slices, first_z=0, debugFlag=False):
    """ Track a hole through a series of images.

    I assume the slice images are binary with 1 for the
    background and 0 for the hole.
    """

    all_ellipses = []

    z = 0
    s = seed

    # loop through all the background images
    for b in slices:

        # skip slices before the first_z slice we picked our seeds on
        if z < first_z:
            z = z + 1
            continue
        # invert the background image to get the hole label image
        label_img = 1 - b
        center, axes = find_ellipse.find_ellipse(label_img, s, radius,
                                                 debugFlag)

        if center is None:
            print("Failed on seed", seed, "Z=", z)
            try:
                sitk.Show(label_img)
            except BaseException:
                print("No show")
            break

        # add Z coord for 3d ellipse
        cz = [center[0], center[1], z]
        axis1 = [axes[0], axes[1], 0]
        axis2 = [axes[2], axes[3], 0]
        ellipse = [cz, axis1, axis2]
        all_ellipses.append(ellipse)
        print(cz)

        # set this ellipse center as the seed for the next Z image
        s = center
        z = z + 1

    return all_ellipses
