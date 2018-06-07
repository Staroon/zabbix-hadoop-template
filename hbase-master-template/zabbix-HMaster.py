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
        Loading JSON URL which we recieved

    :param url:
    :return:
    """
    # Server URL to get JSON information
    return json.load(urllib.urlopen(url))


def json_processing(server_name, listen_port):

    namenode_dict = {}

    server_json = load_url_as_dictionary(
        get_url(server_name, listen_port, "service=HBase,*,sub=Server"))
    jvm_json = load_url_as_dictionary(
        get_url(server_name, listen_port, "service=HBase,name=JvmMetrics"))
    ipc_json = load_url_as_dictionary(
        get_url(server_name, listen_port, "service=HBase,*,sub=IPC"))

    # Server
    isActiveMaster = str(server_json['beans'][0]['tag.isActiveMaster'])
    namenode_dict['isActive'] = isActiveMaster
    startTimeStamp = float(
        str(server_json['beans'][0]['masterStartTime'])[:10])
    startTimeArray = time.localtime(startTimeStamp)
    namenode_dict['startTime'] = time.strftime(
        '%Y-%m-%d %H:%M:%S', startTimeArray)
    if "true" == isActiveMaster:
        activeTimeStamp = float(
            str(server_json['beans'][0]['masterActiveTime'])[:10])
        activeTimeArray = time.localtime(activeTimeStamp)
        namenode_dict['activeTime'] = time.strftime(
            '%Y-%m-%d %H:%M:%S', activeTimeArray)
        namenode_dict['regionServers'] = server_json['beans'][0]['numRegionServers']
        namenode_dict['deadRegionServers'] = server_json['beans'][0]['numDeadRegionServers']

        # JvmMetrics
        namenode_dict['non_heap_mem_used'] = jvm_json['beans'][0]['MemNonHeapUsedM']
        namenode_dict['committed_non_heap_mem'] = jvm_json['beans'][0]['MemNonHeapCommittedM']
        namenode_dict['heap_mem_used'] = jvm_json['beans'][0]['MemHeapUsedM']
        namenode_dict['committed_heap_mem'] = jvm_json['beans'][0]['MemHeapCommittedM']
        namenode_dict['max_heap_mem'] = jvm_json['beans'][0]['MemHeapMaxM']
        namenode_dict['gcCount'] = jvm_json['beans'][0]['GcCount']
        namenode_dict['gcTimeMillis'] = jvm_json['beans'][0]['GcTimeMillis']
        namenode_dict['threadsRunnable'] = jvm_json['beans'][0]['ThreadsRunnable']
        namenode_dict['threadsBlocked'] = jvm_json['beans'][0]['ThreadsBlocked']
        namenode_dict['threadsWaiting'] = jvm_json['beans'][0]['ThreadsWaiting']

        # IPC
        namenode_dict['receivedBytes'] = ipc_json['beans'][0]['receivedBytes']
        namenode_dict['sentBytes'] = ipc_json['beans'][0]['sentBytes']

    if "false" == isActiveMaster:
        # JvmMetrics
        namenode_dict['non_heap_mem_used'] = jvm_json['beans'][0]['MemNonHeapUsedM']
        namenode_dict['committed_non_heap_mem'] = jvm_json['beans'][0]['MemNonHeapCommittedM']
        namenode_dict['heap_mem_used'] = jvm_json['beans'][0]['MemHeapUsedM']
        namenode_dict['committed_heap_mem'] = jvm_json['beans'][0]['MemHeapCommittedM']
        namenode_dict['max_heap_mem'] = jvm_json['beans'][0]['MemHeapMaxM']
        namenode_dict['gcCount'] = jvm_json['beans'][0]['GcCount']
        namenode_dict['gcTimeMillis'] = jvm_json['beans'][0]['GcTimeMillis']
        namenode_dict['threadsRunnable'] = jvm_json['beans'][0]['ThreadsRunnable']
        namenode_dict['threadsBlocked'] = jvm_json['beans'][0]['ThreadsBlocked']
        namenode_dict['threadsWaiting'] = jvm_json['beans'][0]['ThreadsWaiting']

    return namenode_dict


def write_data_to_file(json, file_path, name_in_zabbix):
    txt_file = open(file_path, 'w+')
    for keys in json:
        txt_file.writelines(name_in_zabbix + ' ' +
                            str(keys) + ' ' + str(json[keys]) + '\n')


def usage():
    print '''
            Usage: $SCRIPT_NAME <HBaseMaster_host> <port> <file_path> <zabbix_server_name>
    '''


if __name__ == '__main__':

    if len(sys.argv) == 5:

        hmaster_host = sys.argv[1]
        hmaster_listen_port = sys.argv[2]
        file_path = sys.argv[3]
        name_in_zabbix = sys.argv[4]

        json_processed = json_processing(hmaster_host, hmaster_listen_port)
        write_data_to_file(json_processed, file_path, name_in_zabbix)

    else:
        usage()
