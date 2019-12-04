import argparse
import xmltodict
import csv
import json


parser = argparse.ArgumentParser(description='process volumes details into CSV')
parser.add_argument('-s', '--source', help='path of file to parse')
parser.add_argument('-d', '--dest', help='path of processed file. extension .csv will be added')
args = parser.parse_args()

dest = str(args.dest) + '.csv'

with open (args.source, 'r') as f:
    xmlstring = f.read()

out = open(dest, 'w')

xmldict = xmltodict.parse(xmlstring)

fieldnames = ['vol', 'vs', 'path', 'logical_data_size', 'logical_data_pcent','state', 'bg_compr', 'inline_compr', 'compression_type', 'inline_dedupe', 'data_compaction', 'type', 'sched', 'policy']
w = csv.DictWriter(out, fieldnames=fieldnames, restval='none', extrasaction='ignore', delimiter='|')
w.writeheader()
for row in xmldict['T_SIS']['asup:ROW'] :
    w.writerow(row)

out.close()
