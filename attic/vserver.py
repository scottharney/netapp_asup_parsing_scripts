import argparse
import xmltodict
import csv
import json


parser = argparse.ArgumentParser(description='process vserver info into CSV')
parser.add_argument('-s', '--source', help='path of file to parse')
parser.add_argument('-d', '--dest', help='path of processed file. extension .csv will be added')
args = parser.parse_args()

dest = str(args.dest) + '.csv'

with open (args.source, 'r') as f:
    xmlstring = f.read()

out = open(dest, 'w')

xmldict = xmltodict.parse(xmlstring)

fieldnames = ['vserver', 'rootvolume', 'language', 'volume_security_style', 'aggregate', 'allowed_protocols', 'aggr_list', 'type', 'max_volumes', 'antivirus_on_access_policy', 'quota_policy', 'ipspace_name', 'admin_state', 'operational_state', 'nisdomain', 'ldap_client' ]
w = csv.DictWriter(out, fieldnames=fieldnames, restval='none', extrasaction='ignore', delimiter='|')
w.writeheader()
for row in xmldict['T_VOLUME']['asup:ROW'] :
    row['aggr_list'] = json.dumps(row['aggr_list'])
    row['allowed_protocols'] = json.dumps(row['allowed_protocols'])
    row['nisdomain'] = json.dumps(row['nisdomain'])
    row['ldap_client'] = json.dumps(row['ldap_client'])
    w.writerow(row)

out.close()
