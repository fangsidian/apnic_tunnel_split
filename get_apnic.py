import re
import ipaddr


apnic = open("test.data", 'r')
lines = apnic.readlines()

commands =  []
for raw_rule in lines:
    raw_rule = raw_rule.strip()
    match = re.search('CN\|ipv4.*allocated', raw_rule)
    if match is not None:
        print(raw_rule)
        fields = raw_rule.split('|')
        binaryFields4="{0:b}".format(int(fields[4]))
        range = 32 - (len(binaryFields4)-1)
        mask = ipaddr.IPv4Network('{}/{}'.format(fields[3],range))
        print('mask {}'.format(mask.netmask))
        print ('range {}'.format(range))
        print(('noh {}'.format(mask.numhosts)))
        commands.append("route {} {} {}".format(mask.network,mask.netmask,"net_gateway"))
        print("route {} {} {}".format(mask.network,mask.netmask,"net_gateway"))

with open('tunnel_splt.txt', 'a') as the_file:
    for command in commands:
        the_file.write(command+'\n')


