import argparse
import xmltodict
import csv
#import json
import xlsxwriter

parser = argparse.ArgumentParser(
    description='process asup details into xlsx tabs and tables')
parser.add_argument(
    '-s', '--source', help='path of directory containing files to parse')
parser.add_argument(
    '-d', '--dest', help='path of processed file. extension .xlsx will be added')
args = parser.parse_args()
dest = str(args.dest) + '.xlsx'


def get_csvfieldnames(fieldnames):
    csvfieldnames = []
    for fieldnamesrow in fieldnames:
        csvfieldnames.append(fieldnamesrow['header'])

    return(csvfieldnames)


def start_xml_import(filename, t_val):
    with open(filename, 'r') as f:
        xmlstring = f.read()

    out = open('tempname.csv', 'w')
    xmldict = xmltodict.parse(xmlstring, force_list='interface')
    w = csv.DictWriter(out, extrasaction='ignore', delimiter='|',
                       fieldnames=csvfieldnames, dialect=csv.QUOTE_NONE)

    row = {}
    for row in xmldict[t_val]['asup:ROW']:
        if not isinstance(row, dict):
            print ('DEBUG' + str(row))
            # w.writerow(row)
            continue
        if 'symlink_properties' in row.keys():
            if row['symlink_properties'] is not None:
                for v in row['symlink_properties'].values():
                    for odict_values in v.values():
                        row['symlink_properties'] = odict_values
        if 'share_properties' in row.keys():
            if row['share_properties'] is not None:
                for v in row['share_properties'].values():
                    for odict_values in v.values():
                        row['share_properties'] = odict_values
        if 'wins_servers' in row.keys():
            if row['wins_servers'] is not None:
                for v in row['wins_servers'].values():
                    for odict_values in v.values():
                        row['wins_servers'] = odict_values
        if 'netbios_alias' in row.keys():
            if row['netbios_alias'] is not None:
                for v in row['netbios_alias'].values():
                    for odict_values in v.values():
                        row['netbios_alias'] = odict_values
        if 'protocol' in row.keys():
            if row['protocol'] is not None:
                for v in row['protocol'].values():
                    for odict_values in v.values():
                        row['protocol'] = odict_values
        if 'rorule' in row.keys():
            if row['rorule'] is not None:
                for v in row['rorule'].values():
                    for odict_values in v.values():
                        row['rorule'] = odict_values
        if 'rwrule' in row.keys():
            if row['rwrule'] is not None:
                for v in row['rwrule'].values():
                    for odict_values in v.values():
                        row['rwrule'] = odict_values
        if 'superuser' in row.keys():
            if row['superuser'] is not None:
                for v in row['superuser'].values():
                    for odict_values in v.values():
                        row['superuser'] = odict_values
        if 'allowed_protocols' in row.keys():
            if row['allowed_protocols'] is not None:
                for v in row['allowed_protocols'].values():
                    for odict_values in v.values():
                        row['allowed_protocols'] = odict_values
        w.writerow(row)

    out.close()

    return(xmldict)


workbook = xlsxwriter.Workbook(dest, {'strings_to_numbers': True})
number_format = workbook.add_format({'num_format': '#,##0'})
tabs = ['volume', 'vserver-info', 'sis_status_l', 'cifs_server_byname', 'cifs-server-option',
        'cifs_share_byname', 'cifs-share-acl', 'export_rule_table', 'snapmirror-destination']
tabsdetails = {'sis_status_l':
               {'fieldnames': [
                   {'header': 'vol'},
                   {'header': 'vs'},
                   {'header': 'path'},
                   {'header': 'logical_data_size',
                    'total_function': 'sum', 'format': number_format},
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
               ],
                   't_val': 'T_SIS'},
               'cifs_server_byname':
               {'fieldnames': [
                   {'header': 'name'},
                   {'header': 'vserver'},
                   {'header': 'domain'},
                   {'header': 'domain_workgroup'},
                   {'header': 'workgroup'},
                   {'header': 'default_site'},
                   {'header': 'realm'},
                   {'header': 'auth_style'},
                   {'header': 'admin_status'},
                   {'header': 'netbios_alias'}
               ],
                   't_val': 'T_CIFS_SERVER'},
               'cifs_share_byname':
               {'fieldnames': [
                   {'header': 'cifs_server'},
                   {'header': 'vserver'},
                   {'header': 'share_name'},
                   {'header': 'symlink_properties'},
                   {'header': 'share_properties'},
                   {'header': 'path'},
                   {'header': 'file_umask'},
                   {'header': 'dir_umask'},
                   {'header': 'is_validation_enabled'},
                   {'header': 'VscanFileopProfile'},
                   {'header': 'offline_caching'}
               ],
                   't_val': 'T_CIFS_SHARE'},
               'snapmirror-destination':
               {'fieldnames': [
                   {'header': 'source_path'},
                   {'header': 'destination_path'},
                   {'header': 'relationship_id'},
                   {'header': 'type'},
                   {'header': 'status'},
                   {'header': 'transfer_progress'},
                   {'header': 'transfer_last_updated'},
                   {'header': 'source_volume_node'}
               ],
                   't_val': 'T_SNAPMIRROR_DESTINATION'},
               'cifs-share-acl':
               {'fieldnames': [
                   {'header': 'vserver'},
                   {'header': 'share'},
                   {'header': 'user_or_group'},
                   {'header': 'user_group_type'},
                   {'header': 'permission'},
                   {'header': 'winsid'},
                   {'header': 'access_mask'}
               ],
                   't_val': 'T_CIFS_SHARE_ACL'},
               'cifs-server-option':
               {'fieldnames': [
                   {'header': 'vserver'},
                   {'header': 'default_unix_user'},
                   {'header': 'default_unix_group'},
                   {'header': 'wins_servers'},
                   {'header': 'read_grant_exec'},
                   {'header': 'smb1_enabled'},
                   {'header': 'smb2_enabled'},
                   {'header': 'smb3_enabled'},
                   {'header': 'smb31_enabled'},
                   {'header': 'is_referral_enabled'},
                   {'header': 'shadowcopy_enabled'},
                   {'header': 'restrict_anonymous'},
                   {'header': 'is_local_admin_users_mapped_to_root_enabled'},
                   {'header': 'is_unix_nt_acl_enabled'},
                   {'header': 'is_unix_extensions_enabled'},
                   {'header': 'is_netbios_over_tcp_enabled'},
                   {'header': 'is_nbns_enabled'},
               ],
                   't_val': 'T_CIFS_SERVER_OPTIONS'},
               'vserver-info':
               {'fieldnames': [
                   {'header': 'vserver'},
                   {'header': 'rootvolume'},
                   {'header': 'language'},
                   {'header': 'type'},
                   {'header': 'aggregate'},
                   {'header': 'allowed_protocols'},
                   {'header': 'aggr_list'},
                   {'header': 'max_volumes'},
                   {'header': 'antivirus_on_access_policy'},
                   {'header': 'quota_policy'},
                   {'header': 'ipspace_name'},
                   {'header': 'admin_state'},
                   {'header': 'operational_state'},
                   {'header': 'ldap_client'}
               ],
                   't_val': 'T_VSERV'},
               'export_rule_table':
               {'fieldnames': [
                   {'header': 'vserver'},
                   {'header': 'ruleindex'},
                   {'header': 'policyname'},
                   {'header': 'clientmatch'},
                   {'header': 'protocol'},
                   {'header': 'rorule'},
                   {'header': 'rwrule'},
                   {'header': 'allow_suid'},
                   {'header': 'superuser'},
                   {'header': 'allow_dev'},
                   {'header': 'ntfs_unix_security_ops'},
                   {'header': 'chown_mode'}
               ],
                   't_val': 'T_EXPORT_POL_RULE'},
               'volume':
               {'fieldnames': [
                   {'header': 'vol'},
                   {'header': 'vs'},
                   {'header': 'aggr'},
                   {'header': 'state'},
                   {'header': 'type'},
                   {'header': 'styleEx'},
                   {'header': 'security_style'},
                   {'header': 'policy'},
                   {'header': 'size', 'total_function': 'sum',
                    'format': number_format},
                   {'header': 'avail', 'total_function': 'sum',
                    'format': number_format},
                   {'header': 'total', 'total_function': 'sum',
                    'format': number_format},
                   {'header': 'used', 'total_function': 'sum',
                    'format': number_format},
                   {'header': 'pcnt_used'},
                   {'header': 'files', 'format': number_format},
                   {'header': 'files_used', 'total_function': 'sum',
                    'format': number_format},
                   {'header': 'maxdir_size', 'format': number_format},
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
                   {'header': 'over_provisioned_size',
                    'total_function': 'sum', 'format': number_format},
                   {'header': 'snap_rsrv_avail_size',
                    'total_function': 'sum', 'format': number_format},
                   {'header': 'pcnt_snap_space'},
                   {'header': 'atime_update'},
                   {'header': 'clone_vol'},
                   {'header': 'is_encrypted'},
                   {'header': 'hya_eligibility'},
                   {'header': 'hya_wc_ineligibility'}
               ],
                   't_val': 'T_VOLUME'}
               }


for tab in tabs:
    myfile = args.source + '/' + tab + '.xml'
    fieldnames = tabsdetails[tab]['fieldnames']
    t_val = tabsdetails[tab]['t_val']
    csvfieldnames = get_csvfieldnames(fieldnames)
    xmldict = start_xml_import(myfile, t_val)
    worksheet = workbook.add_worksheet(tab)

    data = []
    with open('tempname.csv', 'r') as csvread:
        #rows = csv.DictReader(csvread, delimiter='|', quoting=csv.QUOTE_NONE)
        # print ( rows)
        rows = csvread.readlines()

    for row in rows:
        data.append(row.split('|'))

    rowcount = len(data) - 1
    fieldcount = len(fieldnames) - 1

    worksheet.add_table(0, 0, rowcount, fieldcount, {
                        'data': data, 'columns': fieldnames, 'total_row': True})


workbook.close()
