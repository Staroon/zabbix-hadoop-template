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


def get_url(server_name, listen_port, topic_name):
    """
        Generating URL to get the information
        from namenode/namenode

    :param server_name:
    :param listen_port:
    :param topic_name:
    :return:
    """

    if listen_port < 0:
        print ("Invalid Port")
        exit()

    if not server_name:
        print("Pass valid Hostname")
        exit()

    if not topic_name:
        topic_name = "*"

    URL = "http://"+server_name+":" + \
        str(listen_port)+"/jmx?qry=Hadoop:"+topic_name
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


def json_processing(server_name, listen_port, monitor_type):

    namenode_dict = {}

    jvm_json = load_url_as_dictionary(
        get_url(server_name, listen_port, "service=NameNode,name=JvmMetrics"))
    nns_json = load_url_as_dictionary(
        get_url(server_name, listen_port, "service=NameNode,name=NameNodeStatus"))
    fsns_json = load_url_as_dictionary(
        get_url(server_name, listen_port, "service=NameNode,name=FSNamesystemState"))
    nninfo_json = load_url_as_dictionary(
        get_url(server_name, listen_port, "service=NameNode,name=NameNodeInfo"))

    if "NN" == monitor_type:
        # JvmMetrics
        namenode_dict['heap_memory_used'] = jvm_json['beans'][0]['MemHeapUsedM']
        namenode_dict['heap_memory'] = jvm_json['beans'][0]['MemHeapCommittedM']
        namenode_dict['max_heap_memory'] = jvm_json['beans'][0]['MemHeapMaxM']
        namenode_dict['non_heap_memory_used'] = jvm_json['beans'][0]['MemNonHeapUsedM']
        namenode_dict['commited_non_heap_memory'] = jvm_json['beans'][0]['MemNonHeapCommittedM']
        namenode_dict['all_memory_used'] = float(
            jvm_json['beans'][0]['MemHeapUsedM']) + float(jvm_json['beans'][0]['MemNonHeapUsedM'])

        # NameNodeStatus
        namenode_dict['namenode_state'] = nns_json['beans'][0]['State']

        # FSNamesystemState
        timeStamp = float(
            str(fsns_json['beans'][0]['BlockDeletionStartTime'])[:10])
        timeArray = time.localtime(timeStamp)
        namenode_dict['start_time'] = time.strftime(
            '%Y-%m-%d %H:%M:%S', timeArray)

        # NameNodeInfo
        namenode_dict['hadoop_version'] = str(
            nninfo_json['beans'][0]['Version']).split(',')[0]

        return namenode_dict

    if "DFS" == monitor_type:
        # FSNamesystemState
        namenode_dict['live_nodes'] = fsns_json['beans'][0]['NumLiveDataNodes']
        namenode_dict['dead_nodes'] = fsns_json['beans'][0]['NumDeadDataNodes']
        namenode_dict['decommissioning_nodes'] = fsns_json['beans'][0]['NumDecommissioningDataNodes']
        namenode_dict['under_replicated_blocks'] = fsns_json['beans'][0]['UnderReplicatedBlocks']

        # NameNodeInfo
        namenode_dict['files_and_directorys'] = nninfo_json['beans'][0]['TotalFiles']
        namenode_dict['blocks'] = nninfo_json['beans'][0]['TotalBlocks']
        namenode_dict['configured_capacity'] = nninfo_json['beans'][0]['Total']
        namenode_dict['dfs_used'] = nninfo_json['beans'][0]['Used']
        namenode_dict['dfs_used_persent'] = min_value_display(
            float(nninfo_json['beans'][0]['PercentUsed']))
        namenode_dict['non_dfs_used'] = nninfo_json['beans'][0]['NonDfsUsedSpace']
        namenode_dict['dfs_remaining'] = nninfo_json['beans'][0]['Free']
        namenode_dict['dfs_remaining_persent'] = min_value_display(
            float(nninfo_json['beans'][0]['PercentRemaining']))
        datanodes_usages = json.loads(nninfo_json['beans'][0]['NodeUsage'])
        namenode_dict['min_datanodes_usages'] = datanodes_usages['nodeUsage']['min']
        namenode_dict['median_datanodes_usages'] = datanodes_usages['nodeUsage']['median']
        namenode_dict['max_datanodes_usages'] = datanodes_usages['nodeUsage']['max']
        namenode_dict['stdDev_datanodes_usages'] = datanodes_usages['nodeUsage']['stdDev']
        live_nodes = json.loads(nninfo_json['beans'][0]['LiveNodes'])

        HIGH_CONST = 99999
        LOW_CONST = -99999
        GB = 1024 * 1024 * 1024

        max_node_remaining = LOW_CONST
        min_node_remaining = HIGH_CONST

        max_node_remaining_persent = LOW_CONST
        min_node_remaining_persent = HIGH_CONST

        for live_node_in_list in live_nodes:
            live_node_name = live_node_in_list
            capacity = float(live_nodes[live_node_in_list]['capacity']) / GB

            node_remaining = float(min_value_display(
                float(live_nodes[live_node_in_list]['remaining']) / GB))
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
        exit()


def write_data_to_file(json, file_path, hadoop_name_in_zabbix):
    txt_file = open(file_path, 'w+')
    for keys in json:
        txt_file.writelines(hadoop_name_in_zabbix + ' ' +
                            str(keys) + ' ' + str(json[keys]) + '\n')


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

        namenode_host = sys.argv[1]
        namenode_listen_port = sys.argv[2]
        file_path = sys.argv[3]
        nodename_in_zabbix = sys.argv[4]
        monitor_type = sys.argv[5]

        json_processed = json_processing(
            namenode_host, namenode_listen_port, monitor_type)
        write_data_to_file(json_processed, file_path, nodename_in_zabbix)

    else:
        usage()
