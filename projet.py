from numpy import random as probability
from tkinter import Tk, Label, Scale, LabelFrame, ttk, IntVar, DoubleVar, VERTICAL, HORIZONTAL
from random import randint
from collections.abc import Iterable


class Queue:
    """Follow the principle of FIFO, First In First Out.
    \nOptionnal Arguments:
    \n - size: int = ∞ -> Determines the maximum amount the Queue can hold.
    \n - content: any = [] -> The initial values to put inside the Queue.
    """

    def __init__(self, size: int = float("inf"), content: any = []):
        self.content = [content] if not isinstance(content, Iterable) else content
        self.__removed = None
        self.__count = {"loss": 0, "success": 0}
        self.size = size

    def __repr__(self):
        return (f"Queue({str(self.content)[1:-1]})")

    def __add__(self, value):
        """Add an element to the first position."""
        if isinstance(value, Packet):
            if (self.space_remaining() > value.size):
                self.content.append(value)
                self.__count["success"] += 1
            else:
                self.__count["loss"] += 1
        elif isinstance(value, Iterable):
            self.content += value
        return (self)

    def remove(self):
        """Remove the last element of the Queue and store that value.\n\n Can also only return the last removed object."""
        if (self.length() > 0):    # Cannot remove anything from an empty list
            self.__removed = (self.content)[-1]
            self.content = (self.content)[:-1]
            return (self.__removed)

    def remove_all(self):
        """Remove all last element of the Queue."""
        self.content = []

    def gargabe_collection(self):
        """Remove all packets that are empty."""
        self.content = [element for element in self.content if isinstance(element, Packet) and (element.size > 0)]

    def reset_ratio(self):
        """Reset the count to 0 loss and 0 success."""
        self.__count = {"loss": 0, "success": 0}

    def transmit_packets(self, max_speed: int):
        if (self.length() > 0):
            remaining = max_speed
            for packet in self.content:
                if (packet.size == 0):
                    continue
                else:
                    to_remove = min(packet.size, remaining)
                    packet.size -= to_remove
                    remaining -= to_remove

            self.gargabe_collection()

    def length(self):
        """Get the length of the Queue."""
        return (len(self.content))

    def space_remaining(self) -> int:
        """Return the amount of space available."""
        return (self.size - sum([packet.size for packet in self.content]))

    def space_occupied(self, **kwargs) -> int:
        """Return the amount of space available.
        \nOptionnal Arguments:
        \n - percentage: bool = False -> Will return the result in a percentage form [0;1].
        """
        if kwargs.get("percentage") is True:
            return (sum([packet.size for packet in self.content]) / self.size)
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
        """Return the percentage of loss [0;1]."""
        return (self.__count["loss"] / max(1, sum(self.__count.values())))


class Client:
    """A Source of packets, that can send information to a Buffer."""

    def __init__(self, master=None):
        self.id = id(self)
        self.packets = []

    def __repr__(self) -> str:
        return (f"Client(ID={self.id})")

    def generate_packets(self, size: int = 100, rate_lambda: float = 0):
        """Generate a numpy array containing values based on the λ chosen, the amount of values is given by the size
        \nThe larger the size the better the accuracy, but slower is the reaction time when λ changes.
        """
        if len(self.packets) <= 0:
            self.packets = [Packet(self.id, value) for value in probability.poisson(rate_lambda, size)]

    def send_packets(self, queue: Queue, amount: int = 1):
        """The amount determines the number of cycles before creating new packets"""
        for packet in self.packets[:amount]:
            queue += packet
            self.packets.pop(0)


class Packet:
    """Represent a Packet of data. Must be given a source id and it's content."""

    def __init__(self, source: int, size: int):
        self.source = source
        self.size = size

    def __repr__(self) -> str:
        return (f"Packet(Source:{self.source}, Size:{self.size})")

    def __add__(self, packet):
        self.size += packet.size
        return (self)


def test_queue():
    """Scenario to test the class Queue"""
    fifo0 = Queue(size=8)       # Creates a Queue with a size limit of 8
    for i in range(10):         # Attempt to fill the Queue with 10 elements
        fifo0 += Packet(0, i)   # Using the __add__ method
    print(fifo0, fifo0.length(), fifo0.space_occupied())                # Displaying using the __repr__ method
    while not fifo0.is_empty():
        fifo0.remove()
        print(fifo0.removed)
    print(fifo0)
    print(fifo0._Queue__count)
    print(f"The Queue has a loss ratio of: {fifo0.ratio * 100:.3f}%")
    print("Because the Queue can hold only 8 bits, we stop adding packets after the fourth packet (0+1+2+3 = 6 < 8, 0+1+2+3+4 = 10 > 8)")


def test_client(dummy_lambda):
    """Scenario to test the class Client and Packet"""
    client0, queue0 = Client(), Queue(500)       # Init
    print(f"The id of the Client is:{id(client0)}")  # Proof that the packet source can be used to identify the client

    client0.send_packets(queue0)                # To test without any packets
    client0.generate_packets(100, dummy_lambda)      # Generating packets with λ
    client0_packets = [packet.size for packet in client0.packets]
    print(client0_packets, sum(client0_packets), len(client0_packets))  # Packets generated with λ and the total amount
    client0.send_packets(queue0, 99)            # Sending all but one packet
    print("queue0:", queue0.length(), queue0.space_occupied())  # The queue can't receive all packets
    print(f"There is {len(client0.packets)} packets remaining")     # How many packets left to send
    client0.send_packets(queue0, 1)              # Sending last packet
    print(f"There is {len(client0.packets)} packets remaining")
    print(f"Packet loss: {queue0.ratio * 100:.3f}%")    # Since the queue can only hold 500 bits, the remaining packets were lost

# Question 4+


class Buffer:
    """LabelFrame with a progressbar associated with. Display stats such as:
    \n - Maximum Size
    \n - Packet loss
    \n - Link Speed
    \n - Number of packets left to process
    \nOptionnal Arguments:
    \n- row: int = 0 -> Same as reguler widgets.
    \n- column: int = 0 -> Same as reguler widgets.
    \n- rowspan: int = 1 -> Same as reguler widgets.
    \n- columnspan: int = 1 -> Same as reguler widgets.
    \n- padx: int = 0 -> Same as reguler widgets.
    \n- pady: int = 0 -> Same as reguler widgets.
    \n- sticky: str = "" -> Same as reguler widgets.
    \n- display_size: int = 100 -> Length of the progress bar associated.
    \n- size: int = 3000 -> Amount of points the buffer can accumulate.
    \n- name: str = "Buffer id" -> The name of the LabelFrame created.
    \n- link_speed: int = randint(1, 100) -> The speed at which the Buffer voids bits
    \n- independant: bool = False -> Define a Buffer with an independant λ.
    """

    def __init__(self, master, **kwargs):
        self.master = master
        self.row = kwargs.get("row", 0)
        self.column = kwargs.get("column", 0)
        self.rowspan = kwargs.get("rowspan", 1)
        self.columnspan = kwargs.get("columnspan", 1)
        self.padx = kwargs.get("padx", 0)
        self.pady = kwargs.get("pady", 0)
        self.sticky = kwargs.get("sticky", "")
        self.size = kwargs.get("size", 3000)
        self.display_size = kwargs.get("display_size", 100)
        self.name = kwargs.get("name", f"Buffer {id(self):02d}")
        self.independant = kwargs.get("independant", False)

        self.CL = Client()

        self.Frame = LabelFrame(self.master, text=f"{self.name}", background="#17202A", fg="#FFFFFF")
        self.Frame.grid(row=self.row, column=self.column, rowspan=self.rowspan, columnspan=self.columnspan, padx=self.padx, pady=self.pady, sticky=self.sticky)
        self.buffer = Queue(self.size)
        self.progbarvalue = DoubleVar()
        self.link_speed = IntVar(value=kwargs.get("link_speed", randint(1, int(self.size / 8))))  # bits/s

        #  self.Frame.grid_rowconfigure(0, weight=1)
        #  self.Frame.grid_rowconfigure(1, weight=1)

        self.ProgressBar = ttk.Progressbar(self.Frame, orient=VERTICAL, length=self.display_size, variable=self.progbarvalue, style="blue.Horizontal.TProgressbar")
        self.ProgressBar.grid(row=0, column=0, padx=5, pady=5, rowspan=int(self.display_size / 10), columnspan=1, sticky="nsw")
        self.ProgressBar.config(maximum=self.buffer.size)

        self.occupation_label = Label(self.Frame, text="Occupied: N/A", background="#CBAACB")
        self.occupation_label.grid(row=0, column=1, sticky="nwes", pady=0)

        self.loss_label = Label(self.Frame, text="Loss: N/A", background="#FFD54F", anchor="w")
        self.loss_label.grid(row=1, column=1, sticky="nwes")

        self.remaining_packets = Label(self.Frame, text="Packets left: N/A", background="#FFCCBC")
        self.remaining_packets.grid(row=2, column=1, sticky="nwes")

        self.link_speed_scale = Scale(self.Frame, from_=1, to=int(self.size / 3), orient=HORIZONTAL, variable=self.link_speed, label="Speed", background="#5DADE2")
        self.link_speed_scale.config(length=self.display_size // 2)
        self.link_speed_scale.grid(row=3, column=1, sticky="ew")

        if self.independant is True:
            self.lambda_scale = Scale(self.Frame, from_=0, to=self.buffer.size // 8, orient=HORIZONTAL, variable=public_lambda, resolution=1, label="λ", background="#58D68D")
            self.lambda_scale.config(length=self.display_size // 2)
            self.lambda_scale.grid(row=4, column=1, columnspan=2, sticky="ew")

    def update(self):

        # Clients
        if self.independant is False:
            if int(public_lambda.get()) > 0:
                self.CL.generate_packets(6, int(public_lambda.get()))
            for _ in range(2):
                self.CL.send_packets(self.buffer, 1)
                self.occupation_label.configure(text=f"Occupied:\n{self.buffer.space_occupied():04d}/{self.buffer.size}")
                self.remaining_packets.configure(text=f"Packets left: {len(self.CL.packets)}")

        # Void of packets
        self.buffer.transmit_packets(self.speed)    # Void packets over time based on the link speed

        # Updating widgets
        self.loss_label.configure(text=f"Loss: {self.buffer.ratio * 100:05.2f}%")
        self.progbarvalue.set(self.buffer.space_occupied() - 0.001)

    def receive_packets(self, packets):
        self.buffer += packets

    @property
    def speed(self):
        return int(self.link_speed.get())


def main_loop():
    """What makes the window dynamic. Each loop is referred as a tick."""

    for BUFFER in BUFFERS:
        BUFFER.update()

    main_window.update()
    main_window.after(func=main_loop, ms=1000)  # One loop per second


if __name__ == "__main__":

    # Test
    test_queue()
    print()
    test_client(10)

    # Create a Tkinter window
    main_window = Tk()
    main_window.title("Simulateur d'un lien réseau")
    main_window.configure(bg="#2C3E50")
    main_window.state("zoomed")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')

    public_lambda = DoubleVar()

    BUFFERS = [Buffer(main_window, row=i % 5, column=i // 5, padx=5, pady=5, size=3000, name=f"Buffer {i:02d}") for i in range(6)]
    BUFFERS += [Buffer(main_window, row=0, column=10, rowspan=100, padx=5, pady=5, sticky="nse", size=3000, display_size=200, name="Main Buffer", independant=True)]

    # Add any additional configuration or widgets here
    main_window.columnconfigure(10, weight=1)
    #main_window.rowconfigure(0, weight=1)

    # Run the Tkinter event loop
    main_loop()
    main_window.mainloop()
