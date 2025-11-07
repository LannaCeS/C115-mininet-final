#!/usr/bin/python

from __future__ import print_function
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import Controller


class NetworkTopo( Topo ):
    # Builds network topology
    def build(self, **_opts):

        s1 = self.addSwitch('s1', failMode='standalone')
        s2 = self.addSwitch('s2', failMode='standalone')
        s3 = self.addSwitch('s3', failMode='standalone')

        # Adding hosts
        h1 = self.addHost('h1',ip='192.168.0.1/28',mac='00:00:00:00:00:01')
        h2 = self.addHost('h2',ip='192.168.0.2/28',mac='00:00:00:00:00:02')
        h3 = self.addHost('h3',ip='192.168.0.3/28',mac='00:00:00:00:00:03')
        h4 = self.addHost('h4',ip='192.168.0.4/28',mac='00:00:00:00:00:04')
        h5 = self.addHost('h5',ip='192.168.0.5/28',mac='00:00:00:00:00:05')
        
        # Connecting hosts to switches
        for d, s in [(h1, s1), (h2, s1), (h3,s2), (h4,s3), (h5,s3)]:
            self.addLink(d, s)

        #Connecting switches
        self.addLink(s1, s2)
        self.addLink(s2, s3)




def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo, controller=None)
    #net.addController('c0')
    net.start()
    CLI( net, script="nodes.sh")
    h1 = net.get('h1')

    print(h1.cmd('sudo ovs-ofctl del-flows s1'))
    print(h1.cmd('sudo ovs-ofctl dump-flows s1'))
    print(h1.cmd('sudo ovs-ofctl del-flows s2'))
    print(h1.cmd('sudo ovs-ofctl dump-flows s2'))
    print(h1.cmd('sudo ovs-ofctl del-flows s3'))
    print(h1.cmd('sudo ovs-ofctl dump-flows s3'))
    #print(h1.cmd('sudo mn --custom topo-3s-5h.py --topo mytopo'))


    #h1 e h2
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02,actions=output:2')
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01,actions=output:1')

    #h1 e h3
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:03,actions=output:3')
    net['s2'].cmd('sudo ovs-ofctl add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:03,actions=output:1')
    net['s2'].cmd('sudo ovs-ofctl add-flow s2 dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:01,actions=output:2')
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:01,actions=output:1')

    #h1 e h4
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,actions=output:3')
    net['s2'].cmd('sudo ovs-ofctl add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,actions=output:3')
    net['s3'].cmd('sudo ovs-ofctl add-flow s3 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,actions=output:1')
    net['s3'].cmd('sudo ovs-ofctl add-flow s3 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,actions=output:3')
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,actions=output:1')
    net['s2'].cmd('sudo ovs-ofctl add-flow s2 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,actions=output:2')
 
    #h4 e h5
    net['s3'].cmd('sudo ovs-ofctl add-flow s3 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:05,actions=output:2')
    net['s3'].cmd('sudo ovs-ofctl add-flow s3 dl_src=00:00:00:00:00:05,dl_dst=00:00:00:00:00:04,actions=output:1')


    net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_type=0x806,nw_proto=1,action=flood')
    net['s2'].cmd('sudo ovs-ofctl add-flow s2 dl_type=0x806,nw_proto=1,action=flood')
    net['s3'].cmd('sudo ovs-ofctl add-flow s3 dl_type=0x806,nw_proto=1,action=flood')

    print(h1.cmd('sudo ovs-ofctl dump-flows s1'))
    print(h1.cmd('sudo ovs-ofctl dump-flows s2'))
    print(h1.cmd('sudo ovs-ofctl dump-flows s3'))


    CLI( net, script="ping.sh")

    net.stop()
if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
