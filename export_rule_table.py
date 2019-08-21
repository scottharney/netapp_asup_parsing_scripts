import argparse
import xmltodict
import csv
import json


parser = argparse.ArgumentParser(description='process export rule table  into CSV')
parser.add_argument('-s', '--source', help='path of file to parse')
parser.add_argument('-d', '--dest', help='path of processed file. extension .csv will be added')
args = parser.parse_args()

dest = str(args.dest) + '.csv'

with open (args.source, 'r') as f:
    xmlstring = f.read()

out = open(dest, 'w')

xmldict = xmltodict.parse(xmlstring)

fieldnames = ['vserver', 'ruleindex', 'policyname', 'clientmatch', 'protocol', 'rorule', 'rwrule', 'allow_suid', 'superuser', 'allow_dev', 'ntfs_unix_security_ops', 'chown_mode' ]
w = csv.DictWriter(out, fieldnames=fieldnames, restval='none', extrasaction='ignore', delimiter='|')
w.writeheader()
for row in xmldict['T_EXPORT_POL_RULE']['asup:ROW'] :
    row['protocol'] = json.dumps(row['protocol'])
    row['rorule'] = json.dumps(row['rorule'])
    row['rwrule'] = json.dumps(row['rwrule'])
    row['superuser'] = json.dumps(row['superuser'])
    w.writerow(row)

out.close()
