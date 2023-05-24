

from m5.params import *
from m5.proxy import *

from m5.objects.Network import RubyNetwork
from m5.objects.BasicRouter import BasicRouter

class BooksimNetwork(RubyNetwork):
    type = 'BooksimNetwork'
    cxx_header = 'mem/ruby/network/booksim/BooksimNetwork.hh'
    cxx_class = 'gem5::ruby::booksim::BooksimNetwork'
    booksim_config = Param.String("111", "Booksim's configuration file")
    booksim_speedup = Param.UInt32(1,"Booksim Network Clock")


class NetworkSwitch(BasicRouter):
    type = 'NetworkSwitch'
    cxx_header = 'mem/ruby/network/booksim/NetworkSwitch.hh'
    cxx_class = 'gem5::ruby::booksim::NetworkSwitch'
    virt_nets = Param.Int(Parent.number_of_virtual_networks,
                          "number of virtual networks")
    