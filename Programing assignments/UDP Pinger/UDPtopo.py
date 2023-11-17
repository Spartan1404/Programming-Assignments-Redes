from mininet.topo import Topo

class MyTopo(Topo):
    
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1)
        self.addLink(s1, h2)

topos = {
    'first_topo': ( lambda: MyTopo() )
}
