from numpy import random as probability
from tkinter import Tk, Label, Button, Scale, LabelFrame, ttk, IntVar, DoubleVar, VERTICAL, HORIZONTAL
from random import randint, random


def random_event(probability: float):
    "The probability is a number indicating a percentage [probability%]"
    return (random() < (probability / 100))


class Queue:
    """Follow the principle of FIFO, First In First Out. Can be used as a Buffer."""

    def __init__(self, size: int = float("inf"), value=[]):
        self.content = [value] if isinstance(value, int | float) else value
        self.__removed = None
        self.__count = {"loss": 0, "success": 0}  # Success/Fail
        self.size = size

    def __repr__(self):
        return (f"Queue({self.content})")

    def add(self, element: any, **kwargs):
        """
        Will add an element to the first position.
        \nOptional Arguments:
        \n\tlog: bool -> Print in the terminal when there is a packet loss.
        """
        if (self.space_remaining() > element.size):
            self.content = [element] + self.content
            self.__count["success"] += 1
        else:
            self.__count["loss"] += 1
            if kwargs.get("log") is True:
                print(f"\033[91mError:The Queue is full and {element} is lost.\033[0m")

    def remove(self):
        """Will remove the last element of the Queue and store that value.\n\n Can also only return the last removed object."""
        if (self.length() > 0):    # Cannot remove anything from an empty list
            self.__removed = (self.content)[-1]
            self.content = (self.content)[:-1]
            return (self.__removed)

    def remove_all(self):
        """Will remove all last element of the Queue."""
        self.content = []

    def transmit_packets(self, max_speed: int, **kwargs):
        if self.length() > 0:
            remaining = max_speed
            for packet in self.content:
                if packet.size == 0:
                    continue
                else:
                    to_remove = min(packet.size, remaining)
                    packet.size -= to_remove
                    remaining -= to_remove

            self.content = [packet for packet in self.content if packet.size > 0]   # Remove empty packets

    def length(self):
        """Get the length of the Queue."""
        return (len(self.content))

    def space_remaining(self) -> int:
        """Return the amount of space available"""
        return (self.size - sum([packet.size for packet in self.content]))

    def space_occupied(self) -> int:
        """Return the amount of space available"""
        return sum([packet.size for packet in self.content])

    def is_empty(self):
        """Checks if the Queue is empty or not."""
        return (False if self.content else True)

    @property
    def removed(self):
        """Use to get the last removed value."""
        return (self.__removed)

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

    def generate_packets(self, size: int = 100, rate_lambda: float = 0):
        if not self.packets:
            self.packets = [Packet(self.id, value) for value in probability.poisson(rate_lambda, size)]

    def send_packets(self, queue: Queue, amount: int = 1, log: bool = False):
        """The amount determines the number of cycles before creating new packets"""
        if self.packets:
            for packet in self.packets[:amount]:
                queue.add(packet, log=False)
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

    def __init__(self, master, grid_pos: tuple, size: int, index: int, clients: Client, display_size: int = 200):
        self.master = master
        self.grid_pos = grid_pos
        self.display_size = display_size
        self.clients = clients

        self.Frame = LabelFrame(self.master, text=f"Buffer {index}", background="#FFFF00")
        self.Frame.grid(row=grid_pos[0], column=grid_pos[1], padx=grid_pos[2], pady=grid_pos[3])
        self.buffer = Queue(size)
        self.progbarvalue = DoubleVar()
        self.rate_lambda = DoubleVar()
        self.link_speed = IntVar(value=1)  # bits/s

        self.ProgressBar = ttk.Progressbar(self.Frame, orient=VERTICAL, length=self.display_size, variable=self.progbarvalue, style="red.Horizontal.TProgressbar")
        self.ProgressBar.grid(row=0, column=0, padx=grid_pos[2], pady=grid_pos[3])
        self.ProgressBar.config(maximum=self.buffer.size)

        self.occupation_label = Label(self.Frame, text="Occupied: N/A")
        self.occupation_label.grid(row=0, column=2, padx=grid_pos[2], pady=grid_pos[3])

        self.loss_label = Label(self.Frame, text="Loss: N/A")
        self.loss_label.grid(row=1, column=2, padx=grid_pos[2], pady=grid_pos[3])

        self.remaining_packets = Label(self.Frame, text="Packets left: N/A")
        self.remaining_packets.grid(row=2, column=2, padx=grid_pos[2], pady=grid_pos[3])

        self.lambda_scale = Scale(self.Frame, from_=0, to=100, orient=HORIZONTAL, variable=self.rate_lambda, resolution=0.1)
        self.lambda_scale.config(length=self.display_size // 2)
        self.lambda_scale.grid(row=3, column=3)

        self.link_speed_scale = Scale(self.Frame, from_=1, to=1000, orient=HORIZONTAL, variable=self.link_speed)
        self.link_speed_scale.config(length=self.display_size // 2)
        self.link_speed_scale.grid(row=2, column=3)

    def update(self):

        # Clients
        self.clients.generate_packets(6, self.lambda_gen)
        self.clients.send_packets(self.buffer, 2, False)

        # Void of packets
        self.buffer.transmit_packets(int(self.link_speed.get()), log=True)    # Void packets over time based on the link speed

        # Updating widgets
        self.loss_label.configure(text=f"Loss: {self.buffer.ratio * 100:05.2f}%")
        self.occupation_label.configure(text=f"Occupied: {self.buffer.space_occupied()}/{self.buffer.size}")
        self.remaining_packets.configure(text=f"Packets left: {len(self.clients.packets)}")
        self.progbarvalue.set(self.buffer.space_occupied() - 0.001)

    @property
    def lambda_gen(self):
        return float(self.rate_lambda.get())


def main_loop():
    """What makes the window dynamic. Each loop is referred as a tick."""

    for BUFFER in BUFFERS:
        BUFFER.update()

    main_window.update()
    main_window.after(func=main_loop, ms=1000)


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

    BUFFERS = [Buffer(main_window, (0, i, 10, 10), 3000, i, Client()) for i in range(3)]

    # Add any additional configuration or widgets here

    # Run the Tkinter event loop
    main_loop()
    main_window.mainloop()
