from scapy.packet import Packet

from netmon_proc.metrics.leafmetric import LeafMetric
from netmon_proc.netinfo import MAC_ADDRS


class RxPacketsMetric(LeafMetric):
    def __init__(self):
        super().__init__("Received")
        self._unit = "packets"

    def __iadd__(self, packet: Packet):
        if packet.src not in MAC_ADDRS:
            self._value += 1
        return self

    def __add__(self, packet: Packet):
        new_metric = RxPacketsMetric()
        if packet.src not in MAC_ADDRS:
            new_metric._value = self._value + 1
        return new_metric
