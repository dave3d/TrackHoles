#! /usr/bin/env python

import sys, math

def write_results(all_ellipses, out_name=None):
    """ Write the results out """

    if len(out_name) == 0:
        outfile = sys.stdout
    else:
        outfile = open(out_name, 'w')

    print("Centers", file=outfile)
    for e in all_ellipses:
        center = e[0]
        print("%8.2f %8.2f %8.2f" % (center[0], center[1], center[2]), file=outfile)

    print("Inter Hole Distance", file=outfile)
    distances=[]

    # this assumes that there are 2 seeds points resulting in pairs of ellipses
    n = int(len(all_ellipses)/2)

    for i in range(n):
        e1 = all_ellipses[i]
        e2 = all_ellipses[i+n]
        dx = e1[0][0]-e2[0][0]
        dy = e1[0][1]-e2[0][1]
        d = math.sqrt(dx*dx + dy*dy)
        distances.append(d)
        print("%8.2f" % (d), file=outfile)

    # change in distance through Z
    print("Change in IHD through Z", file=outfile)
    dd_dz = []
    for i in range(n-1):
        dz = distances[i+1]-distances[i]
        dd_dz.append(dz)
        print("%8.2f" % (dz), file=outfile)

    if outfile != sys.stdout:
        outfile.close()
