from numpy import random as probability
from tkinter import Tk, Label, Button, LabelFrame, ttk, DoubleVar, VERTICAL
from random import randint, random


def random_event(probability: float):
    "The probability is a number indicating a percentage [probability%]"
    return (random() < (probability / 100))


class Queue:
    """Follow the principle of FIFO, First In First Out. Can be used as a Buffer."""

    def __init__(self, size: int = float("inf"), value=[]):
        self.__content = [value] if isinstance(value, int | float) else value
        self.__removed = None
        self.__count = {"loss": 0, "success": 0}  # Success/Fail
        self.size = size

    def __repr__(self):
        return (f"Queue({self.__content})")

    def add(self, element: any, log: bool = False):
        """Will add an element to the first position."""
        if (self.length() < self.size):
            self.__content = [element] + self.__content
            self.__count["success"] += 1
        else:
            self.__count["loss"] += 1
            if log:
                print(f"\033[91mError:The Queue is full and {element} is lost.\033[0m")

    def remove(self):
        """Will remove the last element of the Queue and store that value.\n\n Can also only return the last removed object."""
        if self.length() > 0:
            self.__removed = (self.__content)[-1]
            self.__content = (self.__content)[:-1]
            return (self.__removed)

    def remove_all(self):
        """Will remove all last element of the Queue."""
        self.__content = []

    def length(self):
        """Get the length of the Queue."""
        return (len(self.__content))

    def is_empty(self):
        """Checks if the Queue is empty or not."""
        return (False if self.__content else True)

    @property
    def removed(self):
        """Use to get the last removed value."""
        return (self.__removed)

    @property
    def content(self):
        """Use to get the content of the queue."""
        return (self.__content)

    @property
    def counter(self):
        return (self.__count)

    @property
    def ratio(self):
        """Return the percentage of loss."""
        return (self.__count["loss"] / max(1, sum(self.__count.values())))


class Client:
    """A Source of packets, that can send information to a Buffer."""

    def __init__(self):
        self.id = id(self)
        self.packets = None

    def __repr__(self) -> str:
        return (f"Client(ID={self.id})")

    def generate_packets(self, size: int = 100, rate_lambda: float = .1):
        if not self.packets:
            self.packets = [Packet(self.id, value) for value in probability.poisson(rate_lambda, size)]

    def send_packets(self, queue: Queue, amount: int = 1, log: bool = False):
        if self.packets:
            for packet in self.packets[:amount]:
                if packet.size > 0:
                    queue.add(packet, log)
                self.packets.pop(0)
        else:
            print(f"\033[91mError: No packets to send. Generate packets first using {self.__class__.__name__}.generate_packets(size, rate_lambda)\033[0m")


class Packet:
    """Represent a Packet of data. Must be given a source id and it's content."""

    def __init__(self, source: int, size: int):
        self.source = source
        self.size = size

    def __repr__(self) -> str:
        return (f"Packet(Source:{self.source}, Size:{self.size})")


def test_queue():
    """Scenario to test the class Queue"""
    fifo0 = Queue()
    for i in range(10):
        fifo0.add(i)
    print(fifo0)
    while not fifo0.is_empty():
        fifo0.remove()
        print(fifo0.removed)


def test_client():
    """Scenario to test the class Client and Packet"""
    client0, queue0 = Client(), Queue(50)   # Init
    print(id(client0))  # Proof that the packet source can be used to identify the client
    client0.send_packets(queue0)    # To test without any packets
    client0.generate_packets()      # Generating packets
    client0.send_packets(queue0, 99)    # Sending all but one packet
    print(queue0, queue0.length())  # Check that the queue is not empty
    print()
    print(f"There is {len(client0.packets)} packets remaining")     # How many packets left to send
    client0.send_packets(queue0, len(client0.packets))  # Sending last packet
    print(f"There is {len(client0.packets)} packets remaining")
    print(f"Packet loss: {queue0.ratio * 100:.3f}% based on {queue0.counter}")

# Question 4+


class Buffer:
    """"""

    def __init__(self, master, grid_pos: tuple, size: int, index: int, display_size: int = 200):
        self.master = master
        self.grid_pos = grid_pos
        self.display_size = display_size

        self.Frame = LabelFrame(self.master, text=f"Buffer {index}", background="#FFFF00")
        self.Frame.grid(row=grid_pos[0], column=grid_pos[1], padx=grid_pos[2], pady=grid_pos[3])
        self.buffer = Queue(size)
        self.progbarvalue = DoubleVar()

        self.ProgressBar = ttk.Progressbar(self.Frame, orient=VERTICAL, length=self.display_size, variable=self.progbarvalue, style="red.Horizontal.TProgressbar")
        self.ProgressBar.grid(row=0, column=0, padx=grid_pos[2], pady=grid_pos[3])
        self.ProgressBar.config(maximum=self.buffer.size)

        self.loss_label = Label(self.Frame, text="Loss: N/A")
        self.loss_label.grid(row=0, column=2, padx=grid_pos[2], pady=grid_pos[3])

    def update(self):
        (self.progbarvalue).set(self.buffer.length() - 0.001)
        self.loss_label.configure(text=f"Loss: {self.buffer.ratio * 100:05.2f}%")


def main_loop():
    """What makes the window dynamic. Each loop is referred as a tick."""

    for BUFFER in BUFFERS:
        BUFFER.buffer.remove() if randint(0, 1) else 0
        BUFFER.buffer.remove_all() if random_event(.1) else 0
        client_test.generate_packets(50, 0.6)
        client_test.send_packets(BUFFER.buffer, 2, False)
        BUFFER.update()

    main_window.update()
    main_window.after(func=main_loop, ms=25)


if __name__ == "__main__":
    # test_client()
    # Create a Tkinter window
    main_window = Tk()
    main_window.title("Simulateur d'un lien réseau")
    main_window.configure(bg="#2C3E50")
    main_window.state("zoomed")
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

    client_test = Client()
    BUFFERS = [Buffer(main_window, (0, i, 10, 10), 100, i) for i in range(5)]

    # Add any additional configuration or widgets here

    #clear_queue = Button(main_window, text="Clear", command=lambda: BUFFER.buffer.remove_all()).grid(row=1, column=2, padx=10, pady=10)

    # Run the Tkinter event loop
    main_loop()
    main_window.mainloop()
