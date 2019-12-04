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

fieldnames = ['vserver', 'smpolicy_name', 'smpolicy_type', 'smpolicy_comment', 'smpolicy_create_snapshot', 'smpolicy_is_net_compression_enabled', 'sm_replication_mode', 'smpolicy_rpo', 'smpolicy_keep', 'smpolicy_schedule']
w = csv.DictWriter(out, fieldnames=fieldnames, restval='none', extrasaction='ignore', delimiter='|')
w.writeheader()
for row in xmldict['T_SNAPMIRROR_POLICY']['asup:ROW'] :
    row['smpolicy_keep'] = json.dumps(row['smpolicy_keep'])
    row['smpolicy_schedule'] = json.dumps(row['smpolicy_schedule'])
    w.writerow(row)

out.close()
