import argparse
import xmltodict
import csv
import json


parser = argparse.ArgumentParser(description='process cifs share file into CSV')
parser.add_argument('-s', '--source', help='path of file to parse')
parser.add_argument('-d', '--dest', help='path of processed file. extension .csv will be added')
args = parser.parse_args()

dest = str(args.dest) + '.csv'

with open (args.source, 'r') as f:
    xmlstring = f.read()

out = open(dest, 'w')

xmldict = xmltodict.parse(xmlstring)

fieldnames = ['v', 'n', 'e', 's', 'c', 'l']
w = csv.DictWriter(out, fieldnames=fieldnames, restval='none', extrasaction='ignore', delimiter='|')
w.writeheader()
for row in xmldict['T_SNAPSHOT_POLICY']['asup:ROW'] :
    row['e'] = json.dumps(row['e'])
    row['s'] = json.dumps(row['s'])
    row['c'] = json.dumps(row['c'])
    row['l'] = json.dumps(row['l'])
    w.writerow(row)

out.close()
