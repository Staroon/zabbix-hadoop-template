# zabbix-zookeeper-template
用于监控Zookeeper集群的Zabbix模版

## 说明
- 支持监控Zookeeper的运行数据。
- 在CentOS7，Zabbix3.2.6，Zookeeper3.4.10下测试通过。

## 使用方法
在zabbix前端导入`Template Cluster Zookeeper.xml`模板文件，链接该模板到监控主机上，并根据实际情况在`继承以及主机宏`这里修改宏参数：
> {$ZK_PORT} 默认为`2181`

然后上传**userparameter_zkstat.conf**文件到Zookeeper主机上存放Zabbix-agentd自定义参数的文件夹中。

完成！

## 当前支持的监控项目(18项)
- Zookeeper[2181]端口监听状态
- zk_version
- zk_znode_count
- zk_watch_count
- zk_followers
- zk_synced_followers
- zk_min_latency
- zk_max_latency
- zk_avg_latency
- zk_server_state
- zk_packets_sent
- zk_packets_received
- zk_outstanding_requests
- zk_open_file_descriptor_count
- zk_max_file_descriptor_count
- zk_ephemerals_count
- zk_num_alive_connections

## 当前支持的触发器项目
- Zookeeper[2181]端口未处于监听状态

## 图片预览
![](http://or0h1cjna.bkt.clouddn.com/git/zabbix-template/zookeeper.png)
