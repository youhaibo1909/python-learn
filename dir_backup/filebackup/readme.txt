1.测试项目可行：<2018.11.09>
  client   -->   server
1> linux         linux
2> windows7      linux
3> linux         windows7
4> windows7      windows7

2.目前测试有线网带宽
	60Mbit/s  70GB的文件大概2.6小时
	在一个pc上同时开启两个发送端，另一个pc上同时两个接收端，速度能达到80Mbit/s
	
	修改带宽（之前只能达到7Mbit/s,修改后提升将近10倍）:
		单次传输1448byte，1448字tcp的最大有效载荷
		每传输5*1448byte，服务器返回一个数字0。我的饿windows7 的tcp发送缓存区为8k，5*1448 = 7240小于8k


3.服务端有md5sum校验。
	在传输一个文件开始发送文件大小，名称，md5校验码给服务端，服务端接收完成数据后，校验md5值：
	如果不匹配：
		返回客户端数据字1
	匹配：
		返回客户端数据字0
	客户端处理，记录传输结果，然后继续下一个文件传输。
		
4.只要指定一个目录
	备份目录下的所有文件以及文件夹，一层一层的文件夹遍历，直到完成所有文件的遍历。到拷贝到服务端指定的目录。
	1>.多层次目录,多文件测试可行。
	2>.大文件测试，可行。
	
5.实现增量备份（基于文件为单位）
    1>.如果传输中断开，下一次再传输，以前已经传输的不再传输。
    
6.更新重传
    1>.目录下如果存文件内容更新，此文件会重传。
	
	
注意：
 	1>linux->linux中如果目录有中文,在字符串前面添加‘u’字符
 	 'from_dir':u'/root/玥/filebackup/from_dir', #linux path
 	2>注意windows与linux的路径不同
 		windows：  
 			'from_dir':'G:\\iso\\centos', #windows
 		linux:
 			'from_dir':'/root/linux_socket/filebackup/from_dir', #linux path
 			
 	