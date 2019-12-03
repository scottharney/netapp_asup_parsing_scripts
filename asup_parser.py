import argparse
import xmltodict
import csv
import xlsxwriter

parser = argparse.ArgumentParser(
    description='process asup details into xlsx tabs and tables')
parser.add_argument(
    '-s', '--source', help='path of directory containing files to parse')
parser.add_argument(
    '-d', '--dest',
    help='path of processed file. extension .xlsx will be added')
args = parser.parse_args()
dest = str(args.dest) + '.xlsx'


def get_csvfieldnames(fieldnames):
    csvfieldnames = []
    for fieldnamesrow in fieldnames:
        csvfieldnames.append(fieldnamesrow['header'])

    return(csvfieldnames)


def start_xml_import(filename, t_val, csvfilename):
    with open(filename, 'r') as f:
        xmlstring = f.read()

    out = open(csvfilename, 'w')
    xmldict = xmltodict.parse(xmlstring)
    w = csv.DictWriter(out, extrasaction='ignore', delimiter='|',
                       fieldnames=csvfieldnames, dialect=csv.QUOTE_NONE)

    for row in xmldict[t_val]['asup:ROW']:

        # fix weird parsing issue
        if not isinstance(row, dict):
            row = xmldict[t_val]['asup:ROW']

        # if values of a key is a further ordered dict with an embedded list
        # flatten out and extract the list as the content of that item
        for curkey in row.keys():
            if isinstance(row[curkey], dict):
                for v in row[curkey].values():
                    for odict_values in v.values():
                        if isinstance(odict_values, list):
                            row[curkey] = ', '.join(odict_values)
                        else:
                            row[curkey] = odict_values

        w.writerow(row)

    out.close()

    return(xmldict)


workbook = xlsxwriter.Workbook(dest, {'strings_to_numbers': True})
number_format = workbook.add_format({'num_format': '#,##0'})

tabs = ['volume',
        'vserver-info',
        'aggr-info',
        'aggr-efficiency',
        'sis_status_l',
        'export_rule_table',
        'nfs_servers_byname',
        'cifs_server_byname',
        'cifs-server-option',
        'cifs_share_byname',
        'cifs-share-acl',
        'snapmirror',
        'snapmirror-destination',
        'fpolicy-policy',
        'fpolicy-event',
        'fpolicy-server-status',
        'snapmirror-policy',
        'broadcast-domain',
        'ipspaces',
        'ifgrps',
        'network-interface',
        'network-ports',
        'network-routes',
        'dns',
        'licenses'
        ]

tabsdetails = {'sis_status_l':
               {'fieldnames': [
                   {'header': 'vol',
                    'total_function': 'count'},
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
               'broadcast-domain':
               {'fieldnames': [
                   {'header': 'broadcast_domain_name',
                    'total_function': 'count'},
                   {'header': 'broadcast_domain_ipspace_name'},
                   {'header': 'broadcast_domain_id'},
                   {'header': 'broadcast_domain_mtu'},
                   {'header': 'broadcast_domain_ports'}
               ],
                   't_val': 'T_BROADCAST_DOMAIN'},
               'ifgrps':
               {'fieldnames': [
                   {'header': 'ifgrp-name',
                    'total_function': 'count'},
                   {'header': 'node'},
                   {'header': 'distr-func'},
                   {'header': 'lacp'},
                   {'header': 'mac'},
                   {'header': 'activeports'},
                   {'header': 'ports'},
                   {'header': 'up-ports'},
                   {'header': 'down-ports'}
               ],
                   't_val': 'T_IFGRP'},
               'network-interface':
               {'fieldnames': [
                   {'header': 'vif',
                    'total_function': 'count'},
                   {'header': 'vserver'},
                   {'header': 'role'},
                   {'header': 'data_protocol'},
                   {'header': 'address'},
                   {'header': 'inetmask'},
                   {'header': 'home_node'},
                   {'header': 'home_port'},
                   {'header': 'curr_node'},
                   {'header': 'curr_port'},
                   {'header': 'status_oper'},
                   {'header': 'status_admin'},
                   {'header': 'failover_policy'},
                   {'header': 'failover_group'},
                   {'header': 'failover_targets'},
                   {'header': 'firewall_policy'},
                   {'header': 'auto_revert'},
                   {'header': 'is_home'},
               ],
                   't_val': 'T_VIF'},
               'network-ports':
               {'fieldnames': [
                   {'header': 'port',
                    'total_function': 'count'},
                   {'header': 'node'},
                   {'header': 'role'},
                   {'header': 'link'},
                   {'header': 'mtu'},
                   {'header': 'mtu-admin'},
                   {'header': 'autonegotiate_admin'},
                   {'header': 'autonegotiate_oper'},
                   {'header': 'duplex_admin'},
                   {'header': 'duplex_oper'},
                   {'header': 'flowcontrol_admin'},
                   {'header': 'flowcontrol_oper'},
                   {'header': 'ifgrp'},
                   {'header': 'ifgrp-status'},
                   {'header': 'mac'},
                   {'header': 'up-admin'},
                   {'header': 'type'},
                   {'header': 'speed-actual'},
                   {'header': 'remote-device-id'},
                   {'header': 'ipspace'},
                   {'header': 'broadcast-domain'},
                   {'header': 'health-status'},
                   {'header': 'degraded-reason'}
               ],
                   't_val': 'T_PORT'},
               'network-routes':
               {'fieldnames': [
                   {'header': 'route-vserver',
                    'total_function': 'count'},
                   {'header': 'route-destination'},
                   {'header': 'route-gateway'},
                   {'header': 'route-metric'},
               ],
                   't_val': 'T_ROUTES'},
               'fpolicy-policy':
               {'fieldnames': [
                   {'header': 'Vserver',
                    'total_function': 'count'},
                   {'header': 'PolicyName'},
                   {'header': 'EventsToMonitor'},
                   {'header': 'FPolicyEngine'}
               ],
                   't_val': 'T_FPOLICY_POLICY'},
               'licenses':
               {'fieldnames': [
                   {'header': 'package',
                    'total_function': 'count'},
                   {'header': 'serialno'},
                   {'header': 'owner'},
                   {'header': 'descr'},
                   {'header': 'type'},
                   {'header': 'legacy'}
               ],
                   't_val': 'T_LIC_V2'},
               'fpolicy-event':
               {'fieldnames': [
                   {'header': 'Vserver',
                    'total_function': 'count'},
                   {'header': 'EventName'},
                   {'header': 'FileOperations'},
                   {'header': 'Filters'},
                   {'header': 'VolumeOperation'}
               ],
                   't_val': 'T_FPOLICY_EVENT'},
               'fpolicy-server-status':
               {'fieldnames': [
                   {'header': 'Vserver',
                    'total_function': 'count'},
                   {'header': 'Node'},
                   {'header': 'PolicyName'},
                   {'header': 'ServerStatus'},
                   {'header': 'ServerType'},
                   {'header': 'ConnectedSince'},
                   {'header': 'DisconnectedSince'},
                   {'header': 'DisconnectedReason'}
               ],
                   't_val': 'T_FPOLICY_SERVER_STATUS'},
               'dns':
               {'fieldnames': [
                   {'header': 'vserver',
                    'total_function': 'count'},
                   {'header': 'domains'},
                   {'header': 'nameservers'},
                   {'header': 'timeout'},
                   {'header': 'attempts'},
                   {'header': 'is-tld-query-enabled'}
               ],
                   't_val': 'T_DNS'},
               'ipspaces':
               {'fieldnames': [
                   {'header': 'ipspace_name',
                    'total_function': 'count'},
                   {'header': 'ipspace_id'},
                   {'header': 'ipspace_ports'}
               ],
                   't_val': 'T_IPSPACES'},
               'nfs_servers_byname':
               {'fieldnames': [
                   {'header': 'vserver',
                    'total_function': 'count'},
                   {'header': 'v2'},
                   {'header': 'v3'},
                   {'header': 'v4.0'},
                   {'header': 'v41'},
                   {'header': 'v4.1_pnfs'},
                   {'header': 'v4.1_referrals'},
                   {'header': 'v4.1_acl'},
                   {'header': 'v4.1_migration'},
                   {'header': 'v4.1_readDelegation'},
                   {'header': 'v4.1_writeDelegation'},
                   {'header': 'udp'},
                   {'header': 'tcp'},
                   {'header': 'chown_mode'},
                   {'header': 'mount_rootonly'},
                   {'header': 'nfs_rootonly'},
                   {'header': 'qtree_export'},
                   {'header': 'showmount'},
                   {'header': 'name-server-lookup-protocol'}
               ],
                   't_val': 'T_VSERV_NFS'},
               'cifs_server_byname':
               {'fieldnames': [
                   {'header': 'name',
                    'total_function': 'count'},
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
                   {'header': 'cifs_server',
                    'total_function': 'count'},
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
               'snapmirror-policy':
               {'fieldnames': [
                   {'header': 'vserver',
                    'total_function': 'count'},
                   {'header': 'smpolicy_name'},
                   {'header': 'smpolicy_type'},
                   {'header': 'smpolicy_comment'},
                   {'header': 'smpolicy_transferpriority'},
                   {'header': 'smpolicy_ignore_atime'},
                   {'header': 'smpolicy_is_net_compression_enabled'},
                   {'header': 'smpolicy_restart'},
                   {'header': 'smpolicy_snapmirrorlabel'},
                   {'header': 'smpolicy_keep'},
                   {'header': 'smpolicy_preserve'},
                   {'header': 'smpolicy_warn'},
                   {'header': 'smpolicy_schedule'},
                   {'header': 'smpolicy_prefix'}
               ],
                   't_val': 'T_SNAPMIRROR_POLICY'},
               'snapmirror':
               {'fieldnames': [
                   {'header': 'vserver',
                    'total_function': 'count'},
                   {'header': 'source_path'},
                   {'header': 'destination_path'},
                   {'header': 'schedule'},
                   {'header': 'type'},
                   {'header': 'policy'},
                   {'header': 'policy_type'},
                   {'header': 'throttle'},
                   {'header': 'state'},
                   {'header': 'status'},
                   {'header': 'healthy'},
                   {'header': 'identity_preserve'},
                   {'header': 'lag_time'}
               ],
                   't_val': 'T_SNAPMIRROR'},
               'snapmirror-destination':
               {'fieldnames': [
                   {'header': 'source_path',
                    'total_function': 'count'},
                   {'header': 'destination_path'},
                   {'header': 'source_volume_node'},
                   {'header': 'type'},
                   {'header': 'status'},
                   {'header': 'transfer_progress',
                    'format': number_format},
                   {'header': 'progress_last_updated'}
               ],
                   't_val': 'T_SNAPMIRROR_DESTINATION'},
               'cifs-share-acl':
               {'fieldnames': [
                   {'header': 'vserver',
                    'total_function': 'count'},
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
                   {'header': 'vserver',
                    'total_function': 'count'},
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
                   {'header': 'vserver',
                    'total_function': 'count'},
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
                   {'header': 'vserver',
                    'total_function': 'count'},
                   {'header': 'ruleindex'},
                   {'header': 'policyname'},
                   {'header': 'protocol'},
                   {'header': 'clientmatch'},
                   {'header': 'rorule'},
                   {'header': 'rwrule'},
                   {'header': 'anon'},
                   {'header': 'allow_suid'},
                   {'header': 'superuser'},
                   {'header': 'allow_dev'},
                   {'header': 'ntfs_unix_security_ops'},
                   {'header': 'chown_mode'}
               ],
                   't_val': 'T_EXPORT_POL_RULE'},
               'aggr-efficiency':
               {'fieldnames': [
                   {'header': 'aggr',
                    'total_function': 'count'},
                   {'header': 'node'},
                   {'header': 'tlu',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'tpu',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'vlu',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'vpu',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'alu',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'apu',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'tser'},
                   {'header': 'tdrer'},
                   {'header': 'vdrser'},
                   {'header': 'adrser'}
               ],
                   't_val': 'T_AGGR_EFFICIENCY'},
               'aggr-info':
               {'fieldnames': [
                   {'header': 'name',
                    'total_function': 'count'},
                   {'header': 'node'},
                   {'header': 'home_name'},
                   {'header': 'is_home'},
                   {'header': 'cluster'},
                   {'header': 'storage_type'},
                   {'header': 'diskcount'},
                   {'header': 'raidtype'},
                   {'header': 'raidstatus'},
                   {'header': 'ha_policy'},
                   {'header': 'hybrid_enabled'},
                   {'header': 'hybrid'},
                   {'header': 'hybrid_cache_size'},
                   {'header': 'size',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'available_size',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'physical_used',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'maxraidsize',
                    'format': number_format},
                   {'header': 'percent_used'},
                   {'header': 'phyisical_used_percent'},
                   {'header': 'plex_count',
                    'format': number_format},
                   {'header': 'volcount',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'volcount_not_online',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'volcount_quiesced',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'root'},
                   {'header': 'plexes'},
                   {'header': 'raidgroups'},
                   {'header': 'snapmirrored'},
                   {'header': 'is_encrypted'},
                   {'header': 'sis_space_saved',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'data_compaction_space_saved',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'composite'},
                   {'header': 'composite_capacity_tier_used',
                    'format': number_format,
                    'total_function': 'sum'},
                   {'header': 'effective_disk_type'},
                   {'header': 'is_flash_pool_caching_enabled'},
                   {'header': 'is_snaplock'}
               ],
                   't_val': 'T_AGGR_INFO'},
               'volume':
               {'fieldnames': [
                   {'header': 'vol',
                    'total_function': 'count'},
                   {'header': 'vs'},
                   {'header': 'aggr'},
                   {'header': 'state'},
                   {'header': 'type'},
                   {'header': 'styleEx'},
                   {'header': 'security_style'},
                   {'header': 'policy'},
                   {'header': 'size',
                    'total_function': 'sum',
                    'format': number_format},
                   {'header': 'avail',
                    'total_function': 'sum',
                    'format': number_format},
                   {'header': 'total',
                    'total_function': 'sum',
                    'format': number_format},
                   {'header': 'used',
                    'total_function': 'sum',
                    'format': number_format},
                   {'header': 'pcnt_used'},
                   {'header': 'files',
                    'format': number_format},
                   {'header': 'files_used',
                    'total_function': 'sum',
                    'format': number_format},
                   {'header': 'maxdir_size',
                    'format': number_format},
                   {'header': 'space_guarantee'},
                   {'header': 'is_space_guarantee_en'},
                   {'header': 'lang'},
                   {'header': 'j_path'},
                   {'header': 'j_path_src'},
                   {'header': 'parent'},
                   {'header': 'j_actv'},
                   {'header': 'snapdir_access'},
                   {'header': 'snap_policy'},
                   {'header': 'exp_avail_size',
                    'format': number_format},
                   {'header': 'over_provisioned_size',
                    'total_function': 'sum',
                    'format': number_format},
                   {'header': 'snap_rsrv_avail_size',
                    'total_function': 'sum',
                    'format': number_format},
                   {'header': 'pcnt_snap_space'},
                   {'header': 'atime_update'},
                   {'header': 'clone_vol'},
                   {'header': 'is_encrypted'},
                   {'header': 'is_rdonly'},
                   {'header': 'vsroot'},
                   {'header': 'blk_type'},
                   {'header': 'tiering_policy'},
                   {'header': 'tiering_min_cooling_days'},
                   {'header': 'sl_type'},
                   {'header': 'hya_eligibility'},
                   {'header': 'hya_wc_ineligibility'}
               ],
                   't_val': 'T_VOLUME'}
               }


for tab in tabs:
    myfile = args.source + '/' + tab + '.xml'
    fieldnames = tabsdetails[tab]['fieldnames']
    t_val = tabsdetails[tab]['t_val']
    csvfilename = tab + '.csv'
    csvfieldnames = get_csvfieldnames(fieldnames)
    xmldict = start_xml_import(myfile, t_val, csvfilename)
    worksheet = workbook.add_worksheet(tab)

    data = []
    with open(csvfilename, 'r') as csvread:
        rows = csvread.readlines()

        for row in rows:
            data.append(row.split('|'))

    csvread.close()
    rowcount = len(data) + 1
    fieldcount = len(fieldnames) - 1

    worksheet.add_table(0, 0, rowcount, fieldcount, {
        'data': data,
        'columns': fieldnames,
        'total_row': True,
        'name': str(t_val)})


workbook.close()
