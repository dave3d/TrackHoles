#! /usr/bin/env python

import SimpleITK as sitk


def segmentBackground(img, thresholds=[15000, 36000]):
    """ Segment an image background.

    It does this by thesholding, applying a median filter,
    eroding, and selecting the largest connected component.

    A threshold range of [15000, 36000] seems to work well
    for these microscopy images, so that's the default.
    """

    thresh = sitk.Median(sitk.BinaryThreshold(img, thresholds[0],
                                              thresholds[1]), [2, 2])
    erode = sitk.BinaryErode(thresh, [1, 1])

    # selects the largest connected component
    connected = sitk.Cast(sitk.ConnectedComponent(erode), sitk.sitkUInt8) == 1
    return connected


def segmentSeriesBackgrounds(images, thresholds=[15000, 36000]):
    """ Segment the backgrounds of a series of images.

    It does this by thesholding, applying a median filter,
    eroding, and selecting the largest connected component.

    A threshold range of [15000, 36000] seems to work well
    for these microscopy images, so that's the default.
    """

    if not hasattr(images, '__iter__'):
        return []

    bg = []
    for i in images:
        bg.append(segmentBackground(i, thresholds))

    return bg
