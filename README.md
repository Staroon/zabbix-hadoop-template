# zabbix-hadoop-template
Zabbix上的Hadoop监控模板。

## 说明 ##
- 目前仅支持监控HDFS状态和NameNode的运行数据。
- 在CentOS7，Zabbix3.2.6，Hadoop2.7.3下测试成功。
- 项目是参照:[zubayr/zabbix_hadoop_monitoring](https://github.com/zubayr/zabbix_hadoop_monitoring)和[zabbix_mikoomi_templates](https://code.google.com/archive/p/mikoomi/)构建的，特别感谢这两个项目的开发者！！！前面的是使用python脚本抓取的数据，后面的是使用linux shell抓取的数据。
- 我这里是使用python脚本来解析抽取数据的，linux shell和python都是现学现用，可能会有Bug...

## 使用方法 ##
在zabbix前端导入`/hadoop-mikoomi-template/`目录下的`Template Hadoop.xml`模板文件，链接该模板到Hadoop主机上，并添加三个宏参数：
- {$HADOOP_NAMENODE_HOST}
- {$HADOOP_NAMENODE_METRICS_PORT}
- {$ZABBIX_NAME}

> `$HADOOP_NAMENODE_HOST`是要监控的主机hostname，需要在Zabbix Server主机上的hosts文件中配置该hostname； 
> `$HADOOP_NAMENODE_METRICS_PORT`是NameNode WebUI的端口，通常是`50070`； 
> `$ZABBIX_NAME`是在Zabbix前端配置的要监控的主机名。

然后上传`/hadoop-mikoomi-template/`目录下剩余的三个脚本文件到Zabbix Server主机上存放Zabbix外部脚本的文件夹（默认为`/usr/local/share/zabbix/externalscripts/`）中，并使用`chmod +x`赋予三个脚本可执行权限。

完成！

## 当前支持的监控项目 ##
- HDFS（24项）
  - Blocks总数`blocks`
  - 副本不足的Block个数`under_replicated_blocks`
  - 文件及文件夹总数量`files_and_directorys`
  - 集群总配置容量`configured_capacity`
  - DFS已使用的容量`dfs_used`
  - DFS已使用的容量占总配置容量的百分比`dfs_used_persent`
  - 非DFS已使用的容量`non_dfs_used`
  - DFS可用的剩余容量`dfs_remaining`
  - DFS可用的剩余容量占总配置容量的百分比`dfs_remaining_persent`
  - 单节点最大的可用容量`max_remaining`
  - 单节点最大的可用容量百分比`max_remaining_persent`
  - 单节点最小的可用容量`min_remaining`
  - 单节点最小的可用容量百分比`min_remaining_persent`
  - 具有最大可用容量的DataNode主机名`max_remaining_nodename`
  - 具有最大的可用容量百分比的DataNode主机名`max_remaining_persent_nodename`
  - 具有最小可用容量的DataNode主机名`min_remaining_nodename`
  - 具有最小的可用容量百分比的DataNode主机名`min_remaining_persent_nodename`
  - 各DataNode节点已使用空间百分比的中位数`median_datanodes_usages`
  - 各DataNode节点已使用空间百分比的标准差`stdDev_datanodes_usages`
  - 处于Dead状态的DataNode节点数`dead_nodes`
  - 处于Live状态的DataNode节点数`live_nodes`
  - 处于Decommissing状态的节点数`decommissioning_nodes`
  - 最大的DataNode节点空间使用量(%)`max_datanodes_usages`
  - 最小的DataNode节点空间使用量(%)`min_datanodes_usages`
- NameNode（10项）
  - Hadoop版本`hadoop_version`
  - NameNode启动时间`start_time`
  - NameNode状态`namenode_state`
  - 主机连通性检查`agent.ping`
  - 堆内存使用量`heap_memory_used`
  - 非堆内存使用量`non_heap_memory_used`
  - 总内存使用量`all_memory_used`
  - 提交的堆内存大小`heap_memory`
  - 提交的非堆内存大小`commited_non_heap_memory`
  - 最大堆内存大小`max_heap_memory`

## 图片预览 ##
![](http://or0h1cjna.bkt.clouddn.com/git/zabbix-template/zabbix1.png)
HDFS监控项：
![](http://or0h1cjna.bkt.clouddn.com/git/zabbix-template/zabbix2.png)
NameNode监控项：
![](http://or0h1cjna.bkt.clouddn.com/git/zabbix-template/zabbix3.png)

## TODO ##
- Yarn ResourceManager
- Hive
- Hbase