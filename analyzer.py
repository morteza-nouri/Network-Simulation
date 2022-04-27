class Analyzer:
    n_received_packets = 0
    n_sent_packets = 0
    n_received_bytes = 0
    sent_time = dict()
    received_time = dict()
    delay = dict()
    total_delay = 0
    sim_duration = 0
    def __init__(self, filename):
        self.filename = filename
    
    def throughput(self):
        return (self.n_received_bytes) / self.sim_duration
    
    def packet_transfer_ratio(self):
        return self.n_received_packets / self.n_sent_packets
    
    def avg_end_to_end_delay(self):
        return self.total_delay / self.n_received_packets
            
    def parser(self):
        trace_file = open(self.filename, 'r')

        for line in trace_file.readlines():
            line = line.strip().split()[:8]
            if line[0] == 's' and line[3] == 'AGT' and line[6] == 'cbr':
                self.n_sent_packets += 1
                self.sent_time[int(line[5])] = float(line[1])
            elif line[0] == 'r' and line[3] == 'AGT' and line[6] == 'cbr':
                self.n_received_packets += 1
                self.n_received_bytes += int(line[7])
                self.received_time[int(line[5])] = float(line[1])
                self.delay[int(line[5])] = self.received_time[int(line[5])] - self.sent_time[int(line[5])]
                self.total_delay += self.delay[int(line[5])]
            else:
                pass
        self.sim_duration = float(line[1]) - self.sent_time[0]


analyzer = Analyzer('outFiles/WLan.tr')
analyzer.parser()
print(analyzer.n_sent_packets, analyzer.n_received_packets)
print(analyzer.packet_transfer_ratio(), analyzer.avg_end_to_end_delay(), analyzer.throughput())