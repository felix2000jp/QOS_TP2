import pyshark
import asyncio
import pandas as pd
import numpy as np

class Model():
    def capture_tcp(self, timeout):
        # This processes each packet captured
        def process(packet):
            try:                
                packet_version = packet.layers[1].version    
                layer_name     = packet.layers[2].layer_name # Transport Layer
                ip_src     = packet.layers[1].src
                ip_dst     = packet.layers[1].dst
                length     = float( packet.length )
                irtt       = float( packet.tcp.analysis_initial_rtt ) if hasattr(packet.tcp, 'analysis_initial_rtt') else np.NaN
                rtt        = float( packet.tcp.analysis_ack_rtt ) if hasattr(packet.tcp, 'analysis_ack_rtt') else np.NaN
                ack        = float( packet.tcp.ack )
                time       = packet.sniff_time 
                jitter     = 0 if len(packet_list) == 0 else (time - packet_list[len(packet_list) - 1][8]).total_seconds()
                throughput = (length) / 8 / rtt if rtt != np.NaN else np.NaN
                packet_list.append([packet_version, layer_name, ip_src, ip_dst, length, irtt, rtt, ack, time, jitter, throughput])
            except AttributeError:
                pass

        packet_list = []
        capture = pyshark.LiveCapture(interface='wlo1')
        try:
            capture.apply_on_packets(process, timeout=timeout)
        except asyncio.TimeoutError:
            pass

        df = pd.DataFrame(packet_list, columns=['Packet Version', 'Layer', 'Source', 'Destination', 'Length', 'iRTT', 'RTT', 'ACK', 'Time', 'Jitter', 'Throughput'])
        rtt_mean        = df['RTT'].mean()
        throughput_mean = df['Length'].mean()
        jitter_mean     = df['Jitter'].mean()
        bandwidth       = df['Length'].sum() / 8 / timeout
        return df, rtt_mean, throughput_mean, jitter_mean, bandwidth


    def capture_udp(self, timeout):
        # This processes each packet captured
        def process(packet):
            try:                
                packet_version = packet.layers[1].version    
                layer_name     = packet.udp.layer_name # Transport Layer
                ip_src     = packet.layers[1].src
                ip_dst     = packet.layers[1].dst
                length     = float( packet.length )
                time       = packet.sniff_time 
                jitter     = 0 if len(packet_list) == 0 else (time - packet_list[len(packet_list) - 1][5]).total_seconds()
                packet_list.append([packet_version, layer_name, ip_src, ip_dst, length, time, jitter])
            except AttributeError:
                pass

        packet_list = []
        capture = pyshark.LiveCapture(interface='wlo1')
        try:
            capture.apply_on_packets(process, timeout=timeout)
        except asyncio.TimeoutError:
            pass

        df = pd.DataFrame(packet_list, columns=['Packet Version', 'Layer', 'Source', 'Destination', 'Length', 'Time', 'Jitter'])
        jitter_mean     = df['Jitter'].mean()
        bandwidth       = df['Length'].sum() / timeout
        return df, jitter_mean, bandwidth


    def capture_all(self, timeout):
        # This processes each packet captured
        def process(packet):
            try:                
                packet_version = packet.layers[1].version    
                layer_name     = packet.layers[2].layer_name # Transport Layer
                ip_src     = packet.layers[1].src
                ip_dst     = packet.layers[1].dst
                length     = packet.length
                time       = packet.sniff_time 
                packet_list.append([packet_version, layer_name, ip_src, ip_dst, length, time])
            except AttributeError:
                pass

        packet_list = []
        capture = pyshark.LiveCapture(interface='wlo1')
        try:
            capture.apply_on_packets(process, timeout=timeout)
        except asyncio.TimeoutError:
            pass

        df = pd.DataFrame(packet_list, columns=['Packet Version', 'Layer', 'Source', 'Destination', 'Length', 'Time'])

        return df