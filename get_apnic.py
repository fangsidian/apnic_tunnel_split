import re
import ipaddr


def print_debug(hosts, range):
    print('mask {}'.format(hosts.netmask))
    print('range {}'.format(range))
    print(('noh {}'.format(hosts.numhosts)))
    print("route {} {} {}".format(hosts.network, hosts.netmask, "net_gateway"))


def assembly_route_add_command(hosts, commands):
    commands.append("route add {} {} {}".format(hosts.network, hosts.netmask, "192.168.1.1"))
    return commands


def assembly_route_del_command(hosts, commands):
    commands.append("route delete {} {}".format(hosts.network, hosts.netmask))
    return commands


def write_to_files(commands, filename):
    with open(filename, 'a') as the_file:
        for command in commands:
            the_file.write(command + '\n')


def calculate_ip_range(count):
    binaryFields4 = "{0:b}".format(int(count))
    return 32 - (len(binaryFields4) - 1)


def __main__():
    apnic = open("test.data", 'r')
    lines = apnic.readlines()
    add_commands = []
    del_commands = []
    for raw_rule in lines:
        raw_rule = raw_rule.strip()
        match = re.search('CN\|ipv4.*allocated', raw_rule)
        if match is not None:
            fields = raw_rule.split('|')
            range = calculate_ip_range(fields[4])
            hosts = ipaddr.IPv4Network('{}/{}'.format(fields[3], range))
            print_debug(hosts, range)
            add_commands = assembly_route_add_command(hosts, add_commands)
            del_commands = assembly_route_del_command(hosts, del_commands)
    write_to_files(add_commands, 'route_add.txt')
    write_to_files(del_commands, 'route_del.txt')


__main__()
