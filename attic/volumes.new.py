import argparse
import xmltodict
import csv
#import json
import xlsxwriter


parser = argparse.ArgumentParser(description='process volumes details into CSV')
parser.add_argument('-s', '--source', help='path of file to parse')
parser.add_argument('-d', '--dest', help='path of processed file. extension .csv will be added')
args = parser.parse_args()

dest = str(args.dest) + '.xlsx'

with open (args.source, 'r') as f:
    xmlstring = f.read()

out = open('tempvols.csv', 'a')

xmldict = xmltodict.parse(xmlstring)

workbook = xlsxwriter.Workbook(dest)
worksheet = workbook.add_worksheet('volumes')

#fieldnames = ['vol', 'vs', 'aggr', 'state', 'type', 'styleEx', 'security_style', 'policy', 'size', 'avail', 'total', 'used', 'pcnt_used', 'files', 'files_used', 'maxdir_size', 'space_guarantee', 'is_space_guarantee_en', 'lang', 'j_path', 'j_path_src', 'parent', 'j_actv', 'snapdir_access', 'snap_policy', 'exp_avail_size', 'over_provisioned_size', 'snap_rsrv_avail_size', 'pcnt_snap_space', 'atime_update', 'clone_vol', 'is_encrypted', 'hya_eligibility', 'hya_wc_ineligibility' ]
fieldnames = [
    {'header': 'vol'},
    {'header': 'vs'},
    {'header': 'aggr'},
    {'header': 'state'},
    {'header': 'type'},
    {'header': 'styleEx'},
    {'header': 'security_style'},
    {'header': 'policy'},
    {'header': 'size'},
    {'header': 'avail'},
    {'header': 'total'},
    {'header': 'used'},
    {'header': 'pcnt_used'},
    {'header': 'files'},
    {'header': 'files_used'},
    {'header': 'maxdir_size'},
    {'header': 'space_guarantee'},
    {'header': 'is_space_guarantee_on'},
    {'header': 'lang'},
    {'header': 'j_path'},
    {'header': 'j_path_src'},
    {'header': 'parent'},
    {'header': 'j_actv'},
    {'header': 'snapdir_access'},
    {'header': 'snap_policy'},
    {'header': 'exp_avail_size'},
    {'header': 'over_provisioned_size'},
    {'header': 'snap_rsrv_avail_size'},
    {'header': 'pcnt_snap_space'},
    {'header': 'atime_update'},
    {'header': 'clone_vol'},
    {'header': 'is_encrypted'},
    {'header': 'hya_eligibility'},
    {'header': 'hya_wc_ineligibility'}
]
csvfieldnames = []
for fieldnamesrow in fieldnames:
    csvfieldnames.append( fieldnamesrow['header'] )

w = csv.DictWriter(out, extrasaction='ignore', delimiter=',', fieldnames=csvfieldnames)

for row in xmldict['T_VOLUME']['asup:ROW'] :
    w.writerow(row)

out.close()

data =[]
with open ('tempvols.csv', 'r') as csvread:
    rows = csvread.readlines()

for row in rows:
    data.append(row.split(','))

rowcount = len(data) - 1
fieldcount = len(fieldnames) - 1

worksheet.add_table(0, 0, rowcount, fieldcount, {'data': data, 'columns': fieldnames})

workbook.close()
