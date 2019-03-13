import re
import ipaddr
import requests

http_proxy = "applicationwebproxy.nomura.com:80"
https_proxy = "applicationwebproxy.nomura.com:8080"

proxyDict = {
    "http": http_proxy,
    "https": https_proxy
}

GATEWAY = '172.17.0.1'
APNIC_LATEST = 'http://ftp.apnic.net/stats/apnic/delegated-apnic-latest'


def print_debug(hosts, range):
    print('mask {}'.format(hosts.netmask))
    print('range {}'.format(range))
    print(('noh {}'.format(hosts.numhosts)))
    print("route {} {} {}".format(hosts.network, hosts.netmask, "net_gateway"))


def assembly_route_add_command(hosts, commands):
    commands.append("route add -net {} netmask {} gw {}".format(hosts.network, hosts.netmask, GATEWAY))
    return commands


def assembly_route_del_command(hosts, commands):
    commands.append("route del -net {} netmask {} gw {}".format(hosts.network, hosts.netmask, GATEWAY))
    return commands


def write_to_files(commands, filename):
    with open(filename, 'a') as the_file:
        for command in commands:
            the_file.write(command + '\n')


def calculate_ip_range(count):
    binaryFields4 = "{0:b}".format(int(count))
    return 32 - (len(binaryFields4) - 1)


def download_file(url):
    local_file_name = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=False, proxies=proxyDict) as r:
        with open(local_file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_file_name


def __main__():
    file_name = download_file(APNIC_LATEST)
    apnic = open(file_name, 'r')
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
