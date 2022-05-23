import tkinter
from model import Model
from view import View

class Controller():
    def __init__(self) -> None:
        # We create a root window 
        self.window = tkinter.Tk()
        self.window.configure(bg='#B95D49')
        self.window.geometry('300x300')
        self.window.resizable(False, False)
        self.window.title('Tkinter MVC Demo')

        # We set up the view
        self.view  = View(self.window)
        self.view.tcp_button.bind('<Button>', self.action_tcp)
        self.view.udp_button.bind('<Button>', self.action_udp)
        self.view.all_button.bind('<Button>', self.action_all)
        
        # We set up the model
        self.model = Model()

    def run(self):
        self.window.mainloop()

    def action_tcp(self, event):
        timeout = int( self.view.entry_tcp.get() )
        frame, rtt_mean, throughput_mean, jitter_mean, bandwidth = self.model.capture_tcp(timeout)
        self.view.show_dataframe_tcp(frame, rtt_mean, throughput_mean, jitter_mean, bandwidth)

    def action_udp(self, event):
        timeout = int( self.view.entry_udp.get() )
        frame, jitter_mean, bandwidth = self.model.capture_udp(timeout)
        self.view.show_dataframe_udp(frame, jitter_mean, bandwidth)

    def action_all(self, event):
        timeout = int( self.view.entry_all.get() )
        frame   = self.model.capture_all(timeout)
        self.view.show_dataframe_all(frame)

app = Controller()
app.run()