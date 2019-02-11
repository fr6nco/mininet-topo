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
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s4 = self.addSwitch('s4')
		s5 = self.addSwitch('s5')

		self.addLink(s1, s2)
		self.addLink(s1, s3)
		self.addLink(s3, s4)
		self.addLink(s2, s4)
		self.addLink(s5, s1)
		self.addLink(s5, s2)

		mgsw = self.addSwitch('s66766') #DPID used for the Management switch

		self.addLink(mgsw, s2) # connect mgsw to core switch
		self.addLink(mgsw, s1) # connect mgsw to core switch
		self.addLink(mgsw, s5) # connect mgsw to core switch

def setup():
	"Start Network"
	topo = SingleSwitchTopo()
	OVSSwitch13 = partial(OVSSwitch, protocols='OpenFlow13')
	net = Mininet(topo=topo, ipBase='10.11.0.0/24', switch=OVSSwitch13, controller=RemoteController('c0', ip='10.9.1.11'), autoSetMacs=True, xterms=False)

	for h in net.hosts:
		info('Disabling IPV6 for ' + str(h) + '\n')
		h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
		h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
		h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
		h.cmd("echo ''")

		if str(h) in ['server', 'server2']:
			h.cmd('/usr/sbin/lighttpd -D -f /etc/lighttpd/lighttpd.conf &')
			info(str(h) + " is running a webserver now, You can connect at http://" + h.IP() + "/\n")

	for sw in net.switches:
		if sw.name == 's5':
			_intf = Intf('eth1', node=sw)
		if sw.name == 's66766':
			_intf = Intf('eth2', node=sw)
		if sw.name == 's2':
			_intf = Intf('eth3', node=sw)
		if sw.name == 's4':
			_intf = Intf('eth4', node=sw)
		if sw.name == 's1':
			_intf = Intf('eth5', node=sw)
		if sw.name == 's3':
			_intf = Intf('eth6', node=sw)

	net.start()
	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	setup()


