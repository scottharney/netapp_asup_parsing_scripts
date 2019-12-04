#!/usr/bin/env python3
import json
import sys

if len(sys.argv) == 2 :
    with open(sys.argv[1]) as f:
        data = json.load(f)
else:
    print(sys.argv[0] + " needs a filename to parse")
    exit ( 1 )


print ("vol|vserver|aggr|size|used|pcnt_used|space_guarantee|", end="")
print ("is_space_guarantee_en|security_style|state|", end="")
print ("policy|j_path|j_actv|parent|clone_vol")
for row in data['T_VOLUME']['asup:ROW']:
    print(row['vol'] + "|" + row['vs'] + "|", end="")
    print(row['aggr'] + "|", end="")
    print(row['size'] + "|" + row['used'] + "|" + row['files_used'] + "|", end="")
    print(row['pcnt_used'] + "|" + row['space_guarantee'] + "|", end="")
    print(row['is_space_guarantee_en'] + "|", end="")
    if 'security_style' in row:
        print(row['security_style'] + "|", end="")
    else:
        print ("|", end="")
    if 'state' in row:
        print(row['state'] + "|", end="")
    else:
        print ("|", end="")
    if 'policy' in row:
        print(row['policy'] + "|", end="")
    else:
        print ("|", end="")
    if 'j_path' in row:
        print(row['j_path'] + "|", end="")
    else:
        print ("|", end="")
    if 'j_actv' in row:
        print(row['j_actv'] + "|", end="")
    else:
        print ("|", end="")
    if 'parent' in row:
        print(row['parent'] + "|", end="")
    else:
        print ("|", end="")
    if 'clone_vol' in row:
        print(row['clone_vol'] + "|", end="")
    print ()
