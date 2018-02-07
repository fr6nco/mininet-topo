#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSSwitch, RemoteController
from mininet.link import TCLink, Intf
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from functools import partial

class SingleSwitchTopo(Topo):
	"Single switch topology"
	def build(self):
		hosts = [ self.addHost('client', ip='10.10.0.2'), self.addHost('server', ip='10.10.0.1')]
		s1 = self.addSwitch('s1')

		rr = self.addHost('rr', ip='10.10.0.4')
		mgsw = self.addSwitch('s2')
		self.addLink(rr, mgsw)

		for h in hosts:
			self.addLink(h, s1)

def setup():
	"Start Network"
	topo = SingleSwitchTopo()
	OVSSwitch13 = partial(OVSSwitch, protocols='OpenFlow13')
	net = Mininet(topo=topo, ipBase='10.10.0.0/24', switch=OVSSwitch13, controller=RemoteController('c0', ip='192.168.56.1'), autoSetMacs=True, xterms=True)

	for h in net.hosts:
		info('Disabling IPV6 for ' + str(h))
		h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
		h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
		h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")

	for sw in net.switches:
		if sw.name == 's2':
			_intf = Intf('enp0s9', node=sw)

	net.start()
	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	setup()


