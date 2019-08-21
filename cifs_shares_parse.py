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

fieldnames = ['cifs_server','vserver', 'share_name', 'symlink_properties', 'share_properties', 'path', 'file_umask', 'dir_umask', 'is_validation_enabled', 'VscanFileopProfile', 'offline_caching', ]
w = csv.DictWriter(out, fieldnames=fieldnames, restval='none', extrasaction='ignore', delimiter='|')
w.writeheader()
for row in xmldict['T_CIFS_SHARE']['asup:ROW'] :
    row['symlink_properties'] = json.dumps(row['symlink_properties'])
    row['share_properties'] = json.dumps(row['share_properties'])
    w.writerow(row)

out.close()
