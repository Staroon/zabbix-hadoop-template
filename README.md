# zabbix-template
用于监控Hadoop集群的Zabbix模版

## 说明
- 目前支持监控HDFS、NameNode, YARN ResourceManager, Hive, Zookeeper, HBase Master.
- 在CentOS7，Zabbix3.2.6, Hadoop2.7.3, Hive1.2.1,  Zookeeper3.4.10, HBase1.2.6下测试通过。
- 部分监控项是参照:[zubayr/zabbix_hadoop_monitoring](https://github.com/zubayr/zabbix_hadoop_monitoring)和[zabbix_mikoomi_templates](https://code.google.com/archive/p/mikoomi/)构建的，特别感谢这两个项目的开发者！！！
- 对于不同Haopp版本的集群有很大几率不适用，提供的脚本只是一个思路参考。
