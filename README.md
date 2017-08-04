# zabbix-template
用于监控Hadoop集群的Zabbix模版

## 说明
- 目前支持监控HDFS、NameNode、YARN ResourceManager、Hive、Zookeeper的运行数据。
- 在CentOS7，Zabbix3.2.6，Hadoop2.7.3， Hive1.2.1， Zookeeper3.4.10下测试成功。
- 项目是参照:[zubayr/zabbix_hadoop_monitoring](https://github.com/zubayr/zabbix_hadoop_monitoring)和[zabbix_mikoomi_templates](https://code.google.com/archive/p/mikoomi/)构建的，特别感谢这两个项目的开发者！！！前面的是使用python脚本抓取的数据，后面的是使用linux shell抓取的数据。
- 我这里是使用python脚本来解析抽取数据的，linux shell和python都是现学现用，肯定会有不完善的地方...

## 图片预览 ##
![](http://or0h1cjna.bkt.clouddn.com/git/zabbix-template/zabbix1.png)
HDFS监控项：
![](http://or0h1cjna.bkt.clouddn.com/git/zabbix-template/zabbix2.png)
NameNode监控项：
![](http://or0h1cjna.bkt.clouddn.com/git/zabbix-template/zabbix3.png)