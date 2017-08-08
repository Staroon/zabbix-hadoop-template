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

    URL = "http://"+server_name+":"+str(listen_port)+"/jmx?qry=Hadoop:service=ResourceManager,name=QueueMetrics,q0=root,q1=default"
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

    yarn_dict = {}
    yarn_dict['apps-submitted'] = json_dict['beans'][0]['AppsSubmitted']
    yarn_dict['apps-pending'] = json_dict['beans'][0]['AppsPending']
    yarn_dict['apps-running'] = json_dict['beans'][0]['AppsRunning']
    yarn_dict['apps-completed'] = json_dict['beans'][0]['AppsCompleted']
    yarn_dict['apps-failed'] = json_dict['beans'][0]['AppsFailed']
    yarn_dict['apps-killed'] = json_dict['beans'][0]['AppsKilled']

    return yarn_dict

def write_data_to_file(json, file_path, name_in_zabbix):
    txt_file = open(file_path, 'w+')
    for keys in json:
        txt_file.writelines(name_in_zabbix +' '+ str(keys) +' '+ str(json[keys]) + '\n')

def usage():
    print '''
            Usage: $SCRIPT_NAME <YarnRM_host> <YarnRM_port> <file_path> <name_in_zabbix>
    '''

if __name__ == '__main__':

    if len(sys.argv) == 5:

        yarn_hostname = sys.argv[1]
        yarn_listen_port = sys.argv[2]
        file_path = sys.argv[3]
        nodename_in_zabbix = sys.argv[4]

        url = get_url(yarn_hostname, yarn_listen_port)
        json_as_dictionary = load_url_as_dictionary(url)
        json_processed = json_processing(json_as_dictionary)
        write_data_to_file(json_processed, file_path, nodename_in_zabbix)

    else:
        usage()

