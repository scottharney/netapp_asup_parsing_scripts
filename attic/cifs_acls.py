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

fieldnames = ['vserver', 'share', 'user_or_group', 'user_group_type', 'permission', 'winsid', 'access_mask' ]
w = csv.DictWriter(out, fieldnames=fieldnames, restval='none', extrasaction='ignore', delimiter='|')
w.writeheader()
for row in xmldict['T_CIFS_SHARE_ACL']['asup:ROW'] :
    w.writerow(row)

out.close()
