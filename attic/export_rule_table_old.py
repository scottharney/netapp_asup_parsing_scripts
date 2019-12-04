import json

with open('export_rule_table.json') as f:
    data = json.load(f)


print "vsverver,rulindex,export-policy,clientmatch,protocols"
for row in data['T_EXPORT_POL_RULE']['asup:ROW']:
    print(row['vserver']) + "," + row['ruleindex'] + ",",
    print(row['clientmatch']) + "," + (row['policyname']) + ",",
    if 'protocol' in row:
        for li in range(len(row['protocol']['asup:list'])):
            if isinstance(row['protocol']['asup:list']['asup:li'], list):
                print "(",
                print ' '.join(row['protocol']['asup:list']['asup:li']),
                print ")"
            else:
                print "(",
                print (row['protocol']['asup:list']['asup:li']),
                print ")"
