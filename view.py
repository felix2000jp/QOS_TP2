import tkinter
import pandastable
import pandas as pd
import matplotlib.pyplot as plt
from pyparsing import col

class View:
    def __init__(self, parent) -> None:
        self.window = parent
        
        # Capture only TCP packets option
        self.entry_tcp = tkinter.Entry(master=self.window, width=20)
        self.entry_tcp.place(x=80, y=25)
        self.tcp_button = tkinter.Button(master=self.window, text='Capture TCP', bg='#884A3D', fg='white')
        self.tcp_button.place(x=100, y=45)

        self.entry_udp = tkinter.Entry(master=self.window, width=20)
        self.entry_udp.place(x=80, y=120)
        self.udp_button = tkinter.Button(master=self.window, text='Capture UDP', bg='#884A3D', fg='white')
        self.udp_button.place(x=100, y=140)

        self.entry_all = tkinter.Entry(master=self.window, width=20)
        self.entry_all.place(x=80, y=215)
        self.all_button = tkinter.Button(master=self.window, text='Capture All', bg='#884A3D', fg='white')
        self.all_button.place(x=100, y=235)


    def show_dataframe_tcp(self, frame, rtt_mean, throughput_mean, jitter_mean, bandwidth):
        table_window = tkinter.Toplevel(self.window)
        table_window.resizable(False, False)
        table_window.title('TCP Capture')

        data = pandastable.Table(parent=table_window, dataframe=frame, showtoolbar=False, showstatusbar=False)
        data.show()

        data_window = tkinter.Toplevel(self.window)
        data_window.configure(bg='#B95D49')
        data_window.geometry('300x500')
        data_window.resizable(True, True)
        data_window.title('TCP Capture')

        # Average Values
        def rtt_plot():
            frame['RTT'].interpolate(method='linear').plot()
            plt.show()
        
        def jitter_plot():
            frame['Jitter'].plot()
            plt.show()

        def throughput_plot():
            frame['Length'].plot()
            plt.show()

        # Figures
        rtt_button = tkinter.Button(master=data_window, text=f'Average RTT: {rtt_mean}', command=rtt_plot, width = 35, height=5)
        rtt_button.grid(padx=15, pady=15)

        jitter_button = tkinter.Button(master=data_window, text=f'Average Jitter: {jitter_mean}', command=jitter_plot, width = 35, height=5)
        jitter_button.grid(padx=15, pady=15)

        throughput_button = tkinter.Button(master=data_window, text=f'Average Legnth: {throughput_mean}', command=throughput_plot, width = 35, height=5)
        throughput_button.grid(padx=15, pady=15)

        bandwidth_label = tkinter.Label(master=data_window, text=f'Bandwidth: {bandwidth}', width = 35, height=5)
        bandwidth_label.grid(padx=15, pady=15)


    def show_dataframe_udp(self, frame, jitter_mean, bandwidth):
        table_window = tkinter.Toplevel(self.window)
        table_window.resizable(False, False)
        table_window.title('TCP Capture')

        data = pandastable.Table(parent=table_window, dataframe=frame, showtoolbar=False, showstatusbar=False)
        data.show()

        data_window = tkinter.Toplevel(self.window)
        data_window.configure(bg='#B95D49')
        data_window.geometry('300x300')
        data_window.resizable(True, True)
        data_window.title('TCP Capture')

        # Average Values        
        def jitter_plot():
            frame['Jitter'].interpolate(method='linear').plot()
            plt.show()

        # Figures
        jitter_button = tkinter.Button(master=data_window, text=f'Average Jitter: {jitter_mean}', command=jitter_plot, width = 35, height=5)
        jitter_button.grid(padx=15, pady=15)

        bandwidth_label = tkinter.Label(master=data_window, text=f'Average Throughput: {bandwidth}', width = 35, height=5)
        bandwidth_label.grid(padx=15, pady=15)

    
    def show_dataframe_all(self, frame):
        table_window = tkinter.Toplevel(self.window)
        table_window.resizable(False, False)
        table_window.title('TCP Capture')

        data = pandastable.Table(parent=table_window, dataframe=frame, showtoolbar=False, showstatusbar=False)
        data.show()