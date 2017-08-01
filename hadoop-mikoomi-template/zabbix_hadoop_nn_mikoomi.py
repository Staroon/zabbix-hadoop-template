__author__ = 'ssj'

import json
import urllib
import logging
import sys
import time

# ---------------------------------
# Generate URL
# ---------------------------------
# This function converts the servername to URL which we need to query.
def get_url(server_name, listen_port):
    """
        Generating URL to get the information
        from namenode/namenode

    :param server_name:
    :param listen_port:
    :return:
    """

    if listen_port < 0:
        print ("Invalid Port")
        exit()

    if not server_name:
        print("Pass valid Hostname")
        exit()

    URL = "http://"+server_name+":"+str(listen_port)+"/jmx?qry=Hadoop:*"
    return URL


# ---------------------------------
# Load URL
# ---------------------------------
def load_url_as_dictionary(url):
    """
        Loading JSON URL which we recieved from
        namenode/namenode

    :param url:
    :return:
    """
    # Server URL to get JSON information
    return json.load(urllib.urlopen(url))


def json_processing(json_dict, monitor_type):

    TB = 1024 * 1024 * 1024 * 1024
    GB = 1024 * 1024 * 1024
    MB = 1024 * 1024
    KB = 1024

    namenode_dict = {}

    if "NN" == monitor_type:
        # JvmMetrics
        namenode_dict['heap_memory_used'] = json_dict['beans'][0]['MemHeapUsedM']
        namenode_dict['heap_memory'] = json_dict['beans'][0]['MemHeapCommittedM']
        namenode_dict['max_heap_memory'] = json_dict['beans'][0]['MemHeapMaxM']
        namenode_dict['non_heap_memory_used'] = json_dict['beans'][0]['MemNonHeapUsedM']
        namenode_dict['commited_non_heap_memory'] = json_dict['beans'][0]['MemNonHeapCommittedM']
        namenode_dict['all_memory_used'] = float(json_dict['beans'][0]['MemHeapUsedM']) + float(json_dict['beans'][0]['MemNonHeapUsedM'])
    
        # NameNodeStatus
        namenode_dict['namenode_state'] = json_dict['beans'][2]['State']

        # FSNamesystemState
        timeStamp = float(str(json_dict['beans'][9]['BlockDeletionStartTime'])[:10])
        timeArray = time.localtime(timeStamp)
        namenode_dict['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)

        # NameNodeInfo
        namenode_dict['hadoop_version'] = str(json_dict['beans'][4]['Version']).split(',')[0]

        return namenode_dict

    if "DFS" == monitor_type:
        # FSNamesystemState
        namenode_dict['live_nodes'] = json_dict['beans'][9]['NumLiveDataNodes']
        namenode_dict['dead_nodes'] = json_dict['beans'][9]['NumDeadDataNodes']
        namenode_dict['decommissioning_nodes'] = json_dict['beans'][9]['NumDecommissioningDataNodes']
        namenode_dict['under_replicated_blocks'] = json_dict['beans'][9]['UnderReplicatedBlocks']

        # NameNodeInfo
        namenode_dict['files_and_directorys'] = json_dict['beans'][4]['TotalFiles']
        namenode_dict['blocks'] = json_dict['beans'][4]['TotalBlocks']
        namenode_dict['configured_capacity'] = min_value_display(float(json_dict['beans'][4]['Total']) / GB)
        namenode_dict['dfs_used'] = min_value_display(float(json_dict['beans'][4]['Used']) / GB)
        namenode_dict['dfs_used_persent'] = min_value_display(float(json_dict['beans'][4]['PercentUsed']))
        namenode_dict['non_dfs_used'] = min_value_display(float(json_dict['beans'][4]['NonDfsUsedSpace']) / GB)
        namenode_dict['dfs_remaining'] = min_value_display(float(json_dict['beans'][4]['Free']) / GB)
        namenode_dict['dfs_remaining_persent'] = min_value_display(float(json_dict['beans'][4]['PercentRemaining']))
        datanodes_usages = json.loads(json_dict['beans'][4]['NodeUsage'])
        namenode_dict['min_datanodes_usages'] = datanodes_usages['nodeUsage']['min']
        namenode_dict['median_datanodes_usages'] = datanodes_usages['nodeUsage']['median']
        namenode_dict['max_datanodes_usages'] = datanodes_usages['nodeUsage']['max']
        namenode_dict['stdDev_datanodes_usages'] = datanodes_usages['nodeUsage']['stdDev']
        live_nodes =  json.loads(json_dict['beans'][4]['LiveNodes'])

        HIGH_CONST = 99999
        LOW_CONST = -99999

        max_node_remaining = LOW_CONST
        min_node_remaining = HIGH_CONST

        max_node_remaining_persent = LOW_CONST
        min_node_remaining_persent = HIGH_CONST

        for live_node_in_list in live_nodes:
            live_node_name = live_node_in_list
            capacity = float(live_nodes[live_node_in_list]['capacity']) / GB

            node_remaining = float(min_value_display(float(live_nodes[live_node_in_list]['remaining']) / GB))
            node_remaining_persent = node_remaining / capacity * 100

            if node_remaining > max_node_remaining:
                max_node_remaining = node_remaining
                namenode_dict['max_remaining'] = max_node_remaining
                namenode_dict['max_remaining_nodename'] = live_node_name

            if node_remaining < min_node_remaining:
                min_node_remaining = node_remaining
                namenode_dict['min_remaining'] = min_node_remaining
                namenode_dict['min_remaining_nodename'] = live_node_name

            if node_remaining_persent > max_node_remaining_persent:
                max_node_remaining_persent = node_remaining_persent
                namenode_dict['max_remaining_persent'] = max_node_remaining_persent
                namenode_dict['max_remaining_persent_nodename'] = live_node_name

            if node_remaining_persent < min_node_remaining_persent:
                min_node_remaining_persent = node_remaining_persent
                namenode_dict['min_remaining_persent'] = min_node_remaining_persent
                namenode_dict['min_remaining_persent_nodename'] = live_node_name
        return namenode_dict
    else:
        print '''
                The <monitor_type> is NN or DFS.
        '''

def write_data_to_file(json, file_path, hadoop_name_in_zabbix):
    txt_file = open(file_path, 'w+')
    for keys in json:
        txt_file.writelines(hadoop_name_in_zabbix +' '+ str(keys) +' '+ str(json[keys]) + '\n')

def usage():
    print '''
            Usage: $SCRIPT_NAME <hadoop_host> <hadoop_port> <file_path> <zabbix_server_name> <monitor_type>
    '''

def min_value_display(x):
    return '{0:.2f}'.format(x)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) == 6:

        namenode_name = sys.argv[1]
        namenode_listen_port = sys.argv[2]
        file_path = sys.argv[3]
        nodename_in_zabbix = sys.argv[4]
        monitor_type=sys.argv[5]

        url = get_url(namenode_name, namenode_listen_port)
        json_as_dictionary = load_url_as_dictionary(url)
        json_processed = json_processing(json_as_dictionary, monitor_type)
        write_data_to_file(json_processed, file_path, nodename_in_zabbix)

    else:
        usage()

