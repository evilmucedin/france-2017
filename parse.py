#!/usr/bin/env python

import os
import re
import sys

def str2int(s):
    s1 = ""
    for ch in s:
        if ch >= '0' and ch <= '9':
            s1 += ch
    return int(s1)

groups = [0]*101
lePenGroups = [0.0]*101
lePenCountGroups = [0.0]*101
countGroups = [0.0]*101
votedGroups = [0]*10
communes = 0

folder = "wget/elections.interieur.gouv.fr"

fnames = []
for _, _, filenames in os.walk(folder):
    fnames += filenames

def getName(filename):
    return filename.replace(".html", "")

leaves = []
for i in xrange(len(fnames)):
    if i + 1 == len(fnames) or not getName(fnames[i + 1]).startswith(getName(fnames[i])):
        if fnames[i] != "FE.html":
            leaves.append(fnames[i])

raw = True
if raw:
    print("Voters\tVoted\tLe Pen\tMacron\tFilename")

for f in leaves:
    communes += 1
    data = open(folder + '/' + f).read()
    mAll = re.findall(
    """<td style="text-align:left">Inscrits</td>
<td style="text-align:right">([\d ]+)</td>""", data)
    if 1 == len(mAll):
        cAll = str2int(mAll[0])
        mVoted = re.findall(
        """<td style="text-align:left">Votants</td>
<td style="text-align:right">([\d ]+)</td>""", data)
        if 1 == len(mVoted):
            cVoted = str2int(mVoted[0])
            if 0 != cVoted:
                turnout = float(cVoted)/float(cAll)
                mLePen = re.findall(
"""<td style="text-align:left">Mme Marine LE PEN</td>
<td style="text-align:right">([\d ]+)</td>""", 
data)
                mMacron = re.findall(
"""<td style="text-align:left">M. Emmanuel MACRON</td>
<td style="text-align:right">([\d ]+)</td>""",
data)
                cLePen = str2int(mLePen[0])
                cMacron = str2int(mMacron[0])
                if raw:
                    print("%d\t%d\t%d\t%d\t%s" % (cAll, cVoted, cLePen, cMacron, f))
                cLePen = cMacron
                lePen = float(cLePen)/cVoted
                # print("%f\t%f" % (turnout, lePen))
                group = int(turnout*100)
                if False:
                    if group == 80:
                        print("%s\t%f\t%f" % (f, turnout, cAll))
                groups[group] += 1
                lePenGroups[group] += lePen
                lePenCountGroups[group] += cLePen
                countGroups[group] += cAll
                votedGroups[cAll % 10] += 1

print >>sys.stderr, "Communes = %d" % communes

if True and not raw:
    for i in xrange(101):
        if 0 != groups[i]:
            print "%f\t%f\t%f\t%f\t%f" % (i, lePenGroups[i]/groups[i], groups[i], lePenCountGroups[i], countGroups[i])

if False:
    for i in xrange(10):
        print i, votedGroups[i]
