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
        Loading JSON URL which we recieved

    :param url:
    :return:
    """
    # Server URL to get JSON information
    return json.load(urllib.urlopen(url))


def json_processing(json_dict):

    namenode_dict = {}

    # Server
    isActiveMaster = str(json_dict['beans'][0]['tag.isActiveMaster'])
    namenode_dict['isActive'] = isActiveMaster
    startTimeStamp = float(str(json_dict['beans'][0]['masterStartTime'])[:10])
    startTimeArray = time.localtime(startTimeStamp)
    namenode_dict['startTime'] = time.strftime('%Y-%m-%d %H:%M:%S', startTimeArray)
    if "true" == isActiveMaster:
        activeTimeStamp = float(str(json_dict['beans'][0]['masterActiveTime'])[:10])
        activeTimeArray = time.localtime(activeTimeStamp)
        namenode_dict['activeTime'] = time.strftime('%Y-%m-%d %H:%M:%S', activeTimeArray)
        namenode_dict['regionServers'] = json_dict['beans'][0]['numRegionServers']
        namenode_dict['deadRegionServers'] = json_dict['beans'][0]['numDeadRegionServers']

        # JvmMetrics
        namenode_dict['non_heap_mem_used'] = json_dict['beans'][3]['MemNonHeapUsedM']
        namenode_dict['committed_non_heap_mem'] = json_dict['beans'][3]['MemNonHeapCommittedM']
        namenode_dict['heap_mem_used'] = json_dict['beans'][3]['MemHeapUsedM']
        namenode_dict['committed_heap_mem'] = json_dict['beans'][3]['MemHeapCommittedM']
        namenode_dict['max_heap_mem'] = json_dict['beans'][3]['MemHeapMaxM']
        namenode_dict['gcCount'] = json_dict['beans'][3]['GcCount']
        namenode_dict['gcTimeMillis'] = json_dict['beans'][3]['GcTimeMillis']
        namenode_dict['threadsRunnable'] = json_dict['beans'][3]['ThreadsRunnable']
        namenode_dict['threadsBlocked'] = json_dict['beans'][3]['ThreadsBlocked']
        namenode_dict['threadsWaiting'] = json_dict['beans'][3]['ThreadsWaiting']

        # IPC
        namenode_dict['receivedBytes'] = json_dict['beans'][4]['receivedBytes']
        namenode_dict['sentBytes'] = json_dict['beans'][4]['sentBytes']

    if "false" == isActiveMaster:
        # JvmMetrics
        namenode_dict['non_heap_mem_used'] = json_dict['beans'][1]['MemNonHeapUsedM']
        namenode_dict['committed_non_heap_mem'] = json_dict['beans'][1]['MemNonHeapCommittedM']
        namenode_dict['heap_mem_used'] = json_dict['beans'][1]['MemHeapUsedM']
        namenode_dict['committed_heap_mem'] = json_dict['beans'][1]['MemHeapCommittedM']
        namenode_dict['max_heap_mem'] = json_dict['beans'][1]['MemHeapMaxM']
        namenode_dict['gcCount'] = json_dict['beans'][1]['GcCount']
        namenode_dict['gcTimeMillis'] = json_dict['beans'][1]['GcTimeMillis']
        namenode_dict['threadsRunnable'] = json_dict['beans'][1]['ThreadsRunnable']
        namenode_dict['threadsBlocked'] = json_dict['beans'][1]['ThreadsBlocked']
        namenode_dict['threadsWaiting'] = json_dict['beans'][1]['ThreadsWaiting']

    return namenode_dict

def write_data_to_file(json, file_path, name_in_zabbix):
    txt_file = open(file_path, 'w+')
    for keys in json:
        txt_file.writelines(name_in_zabbix +' '+ str(keys) +' '+ str(json[keys]) + '\n')

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

        url = get_url(hmaster_host, hmaster_listen_port)
        json_as_dictionary = load_url_as_dictionary(url)
        json_processed = json_processing(json_as_dictionary)
        write_data_to_file(json_processed, file_path, name_in_zabbix)

    else:
        usage()
