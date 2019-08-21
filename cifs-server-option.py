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

fieldnames = ['vserver','default_unix_user', 'default_unix_group', 'wins_servers', 'read_grant_exec', 'smb1_enabled', 'smb2_enabled', 'smb3_enabled', 'smb31_enabled', 'copy_offload_enabled', 'is_referral_enabled', 'shadowcopy_enabled', 'restrict_anonymous','is_local_admin_users_mapped_to_root_enabled', 'is_unix_nt_acl_enabled', 'is_unix_extensions_enabled', 'is_netbios_over_tcp_enabled', 'is_nbns_enabled' ]
w = csv.DictWriter(out, fieldnames=fieldnames, restval='none', extrasaction='ignore', delimiter='|')
w.writeheader()
for row in xmldict['T_CIFS_SERVER_OPTIONS']['asup:ROW'] :
    row['wins_servers'] = json.dumps(row['wins_servers'])
    w.writerow(row)

out.close()
