# apnic_tunnel_split

1) dynamically fetch the latest CHINA IP from APNIC
2) by default, export as ip-net tool (route)



TODO
1) add support for ip route tool



# DNSmasq
将某个域名提交给指定的dns服务器解析，在Additional DNSMasq Options中填写

-server=/.google.com/208.67.222.222#443
-server=/.google.com.hk/208.67.222.222#443
 

如果Additional DNSMasq Options里的内容太多，也可指定一个目录来读取这些配置信息

conf-dir=/opt/etc/dnsmasq.d
