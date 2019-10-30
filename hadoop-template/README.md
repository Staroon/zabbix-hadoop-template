# zabbix-hadoop-template
用于监控HDFS的Zabbix模板。

## 说明
- 支持监控HDFS、NameNode的运行数据。
- 在CentOS7，Zabbix3.2.6，Hadoop2.7.3下测试成功。

## 使用方法
在zabbix前端导入`Template Cluster Hadoop.xml`模板文件，链接该模板到Hadoop主机上，并根据实际情况在`继承以及主机宏`这里修改三个宏参数：
> {$HADOOP_NAMENODE_HOST} NameNode主机ip或者hostname   
> {$HADOOP_NAMENODE_METRICS_PORT} NameNode Web UI端口，默认为`50070`   
> {$ZABBIX_NAME} Zabbix前端创建当前主机时设置的主机名   

然后上传剩余的两个脚本文件到Zabbix Server主机上存放Zabbix外部脚本的文件夹（默认为`/usr/local/share/zabbix/externalscripts/`）中，并使用`chmod +x`赋予脚本文件可执行权限。

完成！

## 当前支持的监控项目
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
- NameNode（9项）
  - Hadoop版本`hadoop_version`
  - NameNode启动时间`start_time`
  - NameNode状态`namenode_state`
  - 堆内存使用量`heap_memory_used`
  - 非堆内存使用量`non_heap_memory_used`
  - 总内存使用量`all_memory_used`
  - 提交的堆内存大小`heap_memory`
  - 提交的非堆内存大小`commited_non_heap_memory`
  - 最大堆内存大小`max_heap_memory`

## 当前支持的触发器项目
- Hadoop集群总可用存储空间已不足20%
- 主机{HOSTNAME}上的NameNode刚刚被重启过
- 副本不足的Block个数有增加
- 在过去的2分钟内未获取到主机[{HOSTNAME}]上NameNode的任何数据，请检查数据采集器的日志或者查看该主机NameNode运行状态
- 当前处于Active状态的NameNode主机为: {HOSTNAME}
- 有一个或多个节点变为Decommissioning状态
- 有一个或多个节点变为Live状态或者重启了
- 有一个或多个节点处于Dead状态
- 集群中出现了可用存储空间不足20%的节点
- 集群中处于Live状态的节点数量发生了变化

## 图片预览 
HDFS监控项：
![](https://blogfiles-1254091060.cos.ap-shanghai.myqcloud.com/git/zabbix-template/zabbix2.png)
NameNode监控项：
![](https://blogfiles-1254091060.cos.ap-shanghai.myqcloud.com/git/zabbix-template/zabbix3.png)