#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSSwitch, RemoteController
from mininet.link import TCLink, Intf
from mininet.util import dumpNodeConnections, waitListening
from mininet.log import setLogLevel, info, output, warn
from mininet.cli import CLI
from functools import partial

class SingleSwitchTopo(Topo):
	"Single switch topology"
	def build(self):
		client = self.addHost('client', ip='10.10.0.1') 
		server = self.addHost('server', ip='10.10.0.2')
		dns = self.addHost('dns', ip='10.10.0.100')
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')

		self.addLink(client, s1)
		self.addLink(server, s2)
		self.addLink(dns, s1)
		self.addLink(s1, s2)

		mgsw = self.addSwitch('s66766') #DPID used for the Management switch

		self.addLink(mgsw, s2) # connect mgsw to core switch
		self.addLink(mgsw, s1) # connect mgsw to core switch

def setup():
	"Start Network"
	topo = SingleSwitchTopo()
	OVSSwitch13 = partial(OVSSwitch, protocols='OpenFlow13')
	net = Mininet(topo=topo, ipBase='10.10.0.0/24', switch=OVSSwitch13, controller=RemoteController('c0', ip='192.168.56.1'), autoSetMacs=True, xterms=False)

	for h in net.hosts:
		info('Disabling IPV6 for ' + str(h) + '\n')
		h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
		h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
		h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
		h.cmd("echo ''")

		if str(h) in ['rr', 'server']:
			h.cmd('python -m SimpleHTTPServer 80 &')
			info("Request Router is running a webserver now, You can connect at http://" + h.IP() + "/\n")

		if str(h) in ['dns']:
			h.cmd('/usr/sbin/named -f -u bind &')
			info("dns server started on dns node " + h.IP() + "\n")


	for sw in net.switches:
		if sw.name == 's66766':
			_intf = Intf('enp0s9', node=sw)

	net.start()
	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	setup()


