import argparse
import xmltodict
import csv
#import json
import xlsxwriter

parser = argparse.ArgumentParser(description='process volumes details into CSV')
parser.add_argument('-s', '--source', help='path of file to parse')
parser.add_argument('-d', '--dest', help='path of processed file. extension .xlsx will be added')
args = parser.parse_args()

dest = str(args.dest) + '.xlsx'

with open (args.source, 'r') as f:
    xmlstring = f.read()

out = open('tempname.csv', 'w')

xmldict = xmltodict.parse(xmlstring)

workbook = xlsxwriter.Workbook(dest)
worksheet = workbook.add_worksheet('sis_status-l')

fieldnames = [
    {'header': 'vol'},
    {'header': 'vs'},
    {'header': 'path'},
    {'header': 'logical_data_size'},
    {'header': 'logical_data_pcent'},
    {'header': 'state'},
    {'header': 'bg_compr'},
    {'header': 'inline_compr'},
    {'header': 'compression_type'},
    {'header': 'inline_dedupe'},
    {'header': 'data_compaction'},
    {'header': 'type'},
    {'header': 'sched'},
    {'header': 'policy'}
]
csvfieldnames = []
for fieldnamesrow in fieldnames:
    csvfieldnames.append( fieldnamesrow['header'] )


w = csv.DictWriter(out, extrasaction='ignore', delimiter=',', fieldnames=csvfieldnames)

for row in xmldict['T_SIS']['asup:ROW'] :
    w.writerow(row)

out.close()

data =[]
with open ('tempname.csv', 'r') as csvread:
    rows = csvread.readlines()

for row in rows:
    data.append(row.split(','))

rowcount = len(data) - 1
fieldcount = len(fieldnames) - 1

worksheet.add_table(0, 0, rowcount, fieldcount, {'data': data, 'columns': fieldnames})

workbook.close()
