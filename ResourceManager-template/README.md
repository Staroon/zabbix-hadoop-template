# zabbix-yarn-template
Zabbix上的YARN ResourceManager监控模板。

## 说明
- 支持监控YARN上的Application信息。
- 在CentOS7，Zabbix3.2.6，Hadoop2.7.3下测试成功。
- ResourceManager进程重启或者处于Active状态的ResourceManager主机切换后数据会归零

## 使用方法
在zabbix前端导入`Template Cluster YARN ResourceManager.xml`模板文件，链接该模板到ResourceManager主机上，并根据实际情况在`继承以及主机宏`这里修改三个宏参数：
> {$HADOOP_YARN_HOST} ResourceManager主机ip或者hostname   
> {$HADOOP_YARN_METRICS_PORT} ResourceManager Web UI的端口，默认是`8088`   
> {$ZABBIX_NAME} Zabbix前端创建当前主机时设置的主机名   

然后上传剩余的两个脚本文件到Zabbix Server主机上存放Zabbix外部脚本的文件夹（默认为`/usr/local/share/zabbix/externalscripts/`）中，并使用`chmod +x`赋予脚本文件可执行权限。

完成！

## 当前支持的监控项目(6项)
- 已经提交的任务数量
- 等待处理的任务数量
- 正在运行的任务数量
- 运行完成的任务数量
- 运行失败的任务数量
- 被KILL掉的任务数量

## 当前支持的触发器项目
- 在过去的2分钟内未获取到主机[{HOSTNAME}]上ResourceManager的任何数据，请检查数据采集器的日志或者查看该主机Yarn运行状态
- 有一个或者多个任务执行失败
- 当前有正在执行的任务

