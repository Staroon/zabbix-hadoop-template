#!/usr/bin/sh

#--------------------------------------------------------------------------------------------
# Expecting the following arguments in order -
# <host> = hostname/ip-address of Hadoop cluster NameNode server.
#        This is made available as a macro in host configuration.
# <port> = Port # on which the NameNode metrics are available (default = 50070)
#        This is made available as a macro in host configuration.
# <name_in_zabbix> = Name by which the Hadoop NameNode is configured in Zabbix.
#        This is made available as a macro in host configuration.
# <monitor_type> is the parameter (NN or DFS) you want to monitor.
#--------------------------------------------------------------------------------------------

COMMAND_LINE="$0 $*" 
export SCRIPT_NAME="$0"

usage() {
   echo "Usage: $SCRIPT_NAME <host> <port> <name_in_zabbix> <monitor_type>"
}

if [ $# -ne 4 ]
then
    usage ;
    exit ;
fi


#--------------------------------------------------------------------------------------------
# First 2 parameters are required for connecting to Hadoop NameNode
# The 3th parameter HADOOP_NAME_IN_ZABBIX is required to be sent back to Zabbix to identify the 
# Zabbix host/entity for which these metrics are destined.
# The 4th parameter MONITOR_TYPE is to specify the type to monitoring(NN or DFS)
#--------------------------------------------------------------------------------------------
export CLUSTER_HOST=$1
export METRICS_PORT=$2
export HADOOP_NAME_IN_ZABBIX=$3
export MONITOR_TYPE=$4

#--------------------------------------------------------------------------------------------
# Set the data output file and the log fle from zabbix_sender
#--------------------------------------------------------------------------------------------
export DATA_FILE="/tmp/${HADOOP_NAME_IN_ZABBIX}_${MONITOR_TYPE}.txt"
export BAK_DATA_FILE="/tmp/${HADOOP_NAME_IN_ZABBIX}_${MONITOR_TYPE}_bak.txt"
export LOG_FILE="/tmp/${HADOOP_NAME_IN_ZABBIX}.log"


#--------------------------------------------------------------------------------------------
# Use python to get the metrics data from Hadoop NameNode and use screen-scraping to extract
# metrics. 
# The final result of screen scraping is a file containing data in the following format -
# <HADOOP_NAME_IN_ZABBIX> <METRIC_NAME> <METRIC_VALUE>
#--------------------------------------------------------------------------------------------

python `dirname $0`/zabbix_hadoop_nn_mikoomi.py $CLUSTER_HOST $METRICS_PORT $DATA_FILE $HADOOP_NAME_IN_ZABBIX $MONITOR_TYPE

#--------------------------------------------------------------------------------------------
# Check the size of $DATA_FILE. If it is not empty, use zabbix_sender to send data to Zabbix.
#--------------------------------------------------------------------------------------------
if [[ -s $DATA_FILE ]]
then
   zabbix_sender -vv -z 127.0.0.1 -i $DATA_FILE 2>>$LOG_FILE 1>>$LOG_FILE
   echo  -e "Successfully executed $COMMAND_LINE" >>$LOG_FILE
   mv $DATA_FILE $BAK_DATA_FILE
else
   echo "Error in executing $COMMAND_LINE" >> $LOG_FILE
fi
