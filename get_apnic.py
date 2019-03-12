import re
import ipaddr


def print_debug(hosts, range):
    print('mask {}'.format(hosts.netmask))
    print('range {}'.format(range))
    print(('noh {}'.format(hosts.numhosts)))
    print("route {} {} {}".format(hosts.network, hosts.netmask, "net_gateway"))


def assembly_net_tools_command(hosts, commands):
    commands.append("route {} {} {}".format(hosts.network, hosts.netmask, "net_gateway"))


def write_to_files(commands):
    with open('tunnel_splt.txt', 'a') as the_file:
        the_file.write('max-routes 10000\n')
        the_file.write('route-nopull\n\n')
        for command in commands:
            the_file.write(command + '\n')


def calculate_ip_range(count):
    binaryFields4 = "{0:b}".format(int(count))
    return 32 - (len(binaryFields4) - 1)


def __main__():
    apnic = open("test.data", 'r')
    lines = apnic.readlines()
    commands = []
    for raw_rule in lines:
        raw_rule = raw_rule.strip()
        match = re.search('CN\|ipv4.*allocated', raw_rule)
        if match is not None:
            fields = raw_rule.split('|')
            range = calculate_ip_range(fields[4])
            hosts = ipaddr.IPv4Network('{}/{}'.format(fields[3], range))
            print_debug(hosts, range)
            assembly_net_tools_command(hosts, commands)
    write_to_files(commands)


__main__()
