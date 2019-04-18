#!/usr/bin/python


### Linear topology where clients are on the one end and service engines are on the other end.

import sys
import math

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSSwitch, RemoteController
from mininet.link import TCLink, Intf
from mininet.util import dumpNodeConnections, waitListening, irange
from mininet.log import setLogLevel, info, output, warn
from mininet.cli import CLI
from functools import partial

class CustomLinearTopo(Topo):

    def __init__(self, switchcount):
        self.switchcount = switchcount
        super(CustomLinearTopo, self).__init__()

    """
    Linear topology
    """
    def build(self):

        # build switches
        switches = [ self.addSwitch( 's%s' % s )
                     for s in irange( 1, self.switchcount ) ]

        # Wire up switches
        last = None
        for switch in switches:
            if last:
                self.addLink( last, switch )
            last = switch

def setup(count):
    "Start Network"
    topo = CustomLinearTopo(count)
    OVSSwitch13 = partial(OVSSwitch, protocols='OpenFlow13')
    net = Mininet(topo=topo, ipBase='10.11.0.0/24', switch=OVSSwitch13, controller=RemoteController('c0', ip='10.9.1.11'), autoSetMacs=True, xterms=False)

    for sw in net.switches:
        print sw.name
        ## Clients
        if sw.name == 's1':
            print 'attaching clients on eth5 and 6'
            _intf = Intf('eth5', node=sw)
            _intf = Intf('eth6', node=sw)
        
        ## Surrogates
        if sw.name == 's%s' % str(count):
            print 'attaching surrogates on eth3 and 4'
            _intf = Intf('eth3', node=sw)
            _intf = Intf('eth4', node=sw)

        if count % 2 == 0:
            if sw.name == 's%s' % str(int(count / 2)):
                print 'attaching services on eth1 and 2'
                _intf = Intf('eth1', node=sw)
                _intf = Intf('eth2', node=sw)
        else:
            if sw.name == 's%s' % str(int(math.ceil(count / 2.0))):
                print 'attaching services on eth1 and 2'
                _intf = Intf('eth1', node=sw)
                _intf = Intf('eth2', node=sw)


    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')

    if len(sys.argv) < 2:
        print "Integer as arguemnt required"
        exit(1)

    try:
        print "Starting Topo with " + str(int(sys.argv[1])) + " switches"
    except ValueError:
        print "argument must be integer"

    setup(int(sys.argv[1]))


