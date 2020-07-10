#! /usr/bin/env python

import SimpleITK as sitk


def draw_ellipses(img, ellipses):
    """ Draw the ellipse centers on the hole volume.
    """
    dot_img = img * 0
    print(dot_img)

    # for each ellipse center, set the pixel in the volume
    for e in ellipses:
        print(e)
        c = e[0]
        x = int(c[0] + 0.5)
        y = int(c[1] + 0.5)
        z = c[2]
        print(x, y, z)

        dot_img[x, y, z] = 255

    # dilate the centers to make them bigger
    dot_img = sitk.GrayscaleDilate(dot_img, [3, 3, 3])

    img2 = img * 255

    # overlay the dot volume over the input volume
    inv_dot = img2 - dot_img
    result = sitk.Compose(dot_img + img2, inv_dot, inv_dot)
    return result
