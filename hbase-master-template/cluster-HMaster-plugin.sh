#!/usr/bin/sh

#--------------------------------------------------------------------------------------------
# Expecting the following arguments in order -
# <host> = hostname/ip-address of HBase Master.
#        This is made available as a macro in host configuration.
# <port> = Port # on which the hbase master metrics are available (default = 16010)
#        This is made available as a macro in host configuration.
# <name_in_zabbix> = Name by which the HBase Master is configured in Zabbix.
#        This is made available as a macro in host configuration.
#--------------------------------------------------------------------------------------------

COMMAND_LINE="$0 $*" 
export SCRIPT_NAME="$0"

usage() {
   echo "Usage: $SCRIPT_NAME <host> <port> <name_in_zabbix>"
}

if [ $# -ne 3 ]
then
    usage ;
    exit ;
fi


#--------------------------------------------------------------------------------------------
# First 2 parameters are required for connecting to HBase Master
# The 3th parameter NAME_IN_ZABBIX is required to be sent back to Zabbix to identify the 
# Zabbix host/entity for which these metrics are destined.
#--------------------------------------------------------------------------------------------
export HBASE_HOST=$1
export METRICS_PORT=$2
export NAME_IN_ZABBIX=$3

#--------------------------------------------------------------------------------------------
# Set the data output file and the log fle from zabbix_sender
#--------------------------------------------------------------------------------------------
export DATA_FILE="/tmp/${NAME_IN_ZABBIX}_HBaseMaster.txt"
export BAK_DATA_FILE="/tmp/${NAME_IN_ZABBIX}_HBaseMaster_bak.txt"
export LOG_FILE="/tmp/${NAME_IN_ZABBIX}.log"


#--------------------------------------------------------------------------------------------
# Use python to get the metrics data from HBase Master and use screen-scraping to extract
# metrics. 
# The final result of screen scraping is a file containing data in the following format -
# <NAME_IN_ZABBIX> <METRIC_NAME> <METRIC_VALUE>
#--------------------------------------------------------------------------------------------

python `dirname $0`/zabbix-HMaster.py $HBASE_HOST $METRICS_PORT $DATA_FILE $NAME_IN_ZABBIX

#--------------------------------------------------------------------------------------------
# Check the size of $DATA_FILE. If it is not empty, use zabbix_sender to send data to Zabbix.
#--------------------------------------------------------------------------------------------
if [[ -s $DATA_FILE ]]
then
   zabbix_sender -vv -z 127.0.0.1 -i $DATA_FILE 2>>$LOG_FILE 1>>$LOG_FILE
   echo  -e "Successfully executed $COMMAND_LINE" >>$LOG_FILE
   mv $DATA_FILE $BAK_DATA_FILE
   echo "OK"
else
   echo "Error in executing $COMMAND_LINE" >> $LOG_FILE
   echo "ERROR"
fi
