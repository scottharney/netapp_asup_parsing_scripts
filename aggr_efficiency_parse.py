#!/usr/bin/env python3
import xmltodict
import csv
import json

with open ('~/Downloads/aggr-efficiency.xml', 'r') as f:
    xmlstring = f.read()

out = open('~/Downloads/aggr_efficiency.csv', 'w')

xmldict = xmltodict.parse(xmlstring)

fieldnames = ['aggr', 'node', 'tlu', 'tpu', 'vlu', 'vpu', 'vdrser' ]
w = csv.DictWriter(out, fieldnames=fieldnames, restval='none', extrasaction='ignore', delimiter='|')
w.writeheader()
for row in xmldict['T_AGGR_EFFICIENCY']['asup:ROW'] :
    w.writerow(row)

out.close()
