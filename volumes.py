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

fieldnames = ['vol', 'vs', 'aggr', 'state', 'type', 'styleEx', 'security_style', 'policy', 'size', 'avail', 'total', 'used', 'pcnt_used', 'files', 'files_used', 'maxdir_size', 'space_guarantee', 'is_space_guarantee_en', 'lang', 'j_path', 'j_path_src', 'parent', 'j_actv', 'snapdir_access', 'snap_policy', 'exp_avail_size', 'over_provisioned_size', 'snap_rsrv_avail_size', 'pcnt_snap_space', 'atime_update', 'clone_vol', 'is_encrypted', 'hya_eligibility', 'hya_wc_ineligibility' ]
w = csv.DictWriter(out, fieldnames=fieldnames, restval='none', extrasaction='ignore', delimiter='|')
w.writeheader()
for row in xmldict['T_VOLUME']['asup:ROW'] :
    w.writerow(row)

out.close()
