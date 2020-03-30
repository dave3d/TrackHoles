#! /usr/bin/env python

import SimpleITK as sitk

def compute_extents(img, center, radius):
    """ Compute the extents of a region in index space given its center and radius in physical space """
    # corners in physical space
    mincorner = [center[0]-radius, center[1]-radius]
    maxcorner = [center[0]+radius, center[1]+radius]

    minindex = list(img.TransformPhysicalPointToIndex(mincorner))
    maxindex = list(img.TransformPhysicalPointToIndex(maxcorner))
    size = img.GetSize()
    for i in range(2):
        if minindex[i]<0:
            minindex[i]=0
        if maxindex[i] >= size[i]:
            maxindex[i]=size[i]-1
    return minindex, maxindex

def find_ellipse(img, center, radius, debug=False):
    """ Find an ellipse given an approximate center and radius in physical space """
    minindex, maxindex = compute_extents(img, center, radius)

    cropped = img[minindex[0]:maxindex[0], minindex[1]:maxindex[1]]
    components = sitk.ConnectedComponent(cropped,cropped)
    if debug:
        #sitk.Show(img)
        sitk.Show(components)
    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(components)
    if stats.GetNumberOfLabels() == 0:
        print("Uh-oh: no labels")
        print (minindex, maxindex)
        try:
            sitk.Show(components)
        except:
            print("No show")
        return None, None
    c = stats.GetCentroid(1)
    axes = stats.GetPrincipalAxes(1)
    moments = stats.GetPrincipalMoments(1)
    #print("Center:", c)
    #print("Axes:", axes)
    return c, axes

