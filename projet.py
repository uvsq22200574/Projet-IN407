from numpy import random as probability
from tkinter import Tk, Label, Scale, LabelFrame, Radiobutton, ttk, IntVar, DoubleVar, StringVar, VERTICAL, HORIZONTAL
from random import randint, choice
from collections.abc import Iterable


class Packet:
    """Represent a Packet of data. Must be given a source id and it's content."""

    def __init__(self, source: int, size: int, name: str = ""):
        self.source = source
        self.size = size
        self.name = name

    def __repr__(self) -> str:
        return (f"Packet(Source:{self.source}, Size:{self.size}, Name:{self.name})")

    def __add__(self, packet):
        self.size += packet.size
        return (self)


class Graph:
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
        self.independant = kwargs.get("independant", False)  # Can be replaced by a type [buffer;client]

        self.Frame = LabelFrame(self.master, text=f"{self.name}", background="#17202A", fg="#FFFFFF")
        self.Frame.grid(row=self.row, column=self.column, rowspan=self.rowspan, columnspan=self.columnspan, padx=self.padx, pady=self.pady, sticky=self.sticky)
        self.progbarvalue = DoubleVar()
        self.link_speed = IntVar(value=kwargs.get("link_speed", 0))  # bits/s

        self.ProgressBar = ttk.Progressbar(self.Frame, orient=VERTICAL, length=self.display_size, variable=self.progbarvalue, style="blue.Horizontal.TProgressbar")
        self.ProgressBar.grid(row=0, column=0, padx=5, pady=5, rowspan=int(self.display_size / 10), columnspan=1, sticky="nsw")

        self.occupation_label = Label(self.Frame, text="Occupied: N/A", background="#CBAACB")
        self.occupation_label.grid(row=0, column=1, sticky="nwes", pady=0)

        self.loss_label = Label(self.Frame, text="Loss: N/A", background="#FFD54F", anchor="w")
        self.loss_label.grid(row=1, column=1, sticky="nwes")

        self.remaining_packets = Label(self.Frame, text="Packets left: N/A", background="#FFCCBC")
        self.remaining_packets.grid(row=2, column=1, sticky="nwes")

        # Label qui affichera la taille du packet actuel à transmettre
        self.packet_label = Label(self.Frame, text="Current packet: N/A", background="#FFCCBC")
        self.packet_label.grid(row=5, column=1, sticky="nwes")

        # Label qui affichera le nom du packet actuel à transmettre
        self.packet_size_label = Label(self.Frame, text="Current packet size: N/A", background="#FFCCBC")
        self.packet_size_label.grid(row=6, column=1, sticky="nwes")

        if self.independant is True:
            self.link_speed_scale = Scale(self.Frame, from_=0, to=1, orient=HORIZONTAL, variable=self.link_speed, label="Speed", background="#5DADE2")
            self.link_speed_scale.config(length=self.display_size // 2)
            self.link_speed_scale.grid(row=3, column=1, sticky="ew")

            self.lambda_scale = Scale(self.Frame, from_=0, to=1, orient=HORIZONTAL, variable=public_lambda, resolution=1, label="λ", background="#58D68D")
            self.lambda_scale.config(length=self.display_size // 2)
            self.lambda_scale.grid(row=4, column=1, columnspan=2, sticky="ew")
        else:
            self.waited_label = Label(self.Frame, text="Waited: N/A", background="#FFCCBC")
            self.waited_label.grid(row=7, column=1, sticky="nwes")

    def receive_packets(self, packets):
        self.buffer += packets

    @property
    def speed(self):
        return int(self.link_speed.get())


class Buffer(Graph):
    """Follow the principle of FIFO, First In First Out. Use Graph docstring.
    \nOptionnal Arguments:
    \n - size: int = ∞ -> Determines the maximum amount the Buffer can hold.
    \n - content: any = [] -> The initial values to put inside the Buffer.
    \n - create_ui: bool = True -> Whether or not to create a GUI.
    """
    def __init__(self, master=None, size: int = float("inf"), content: any = None, **kwargs):
        self.ui = kwargs.get('create_ui', True)
        if self.ui is True:
            super().__init__(master, **kwargs)
        if content is None:
            content = []
        self.content = [content] if not isinstance(content, Iterable) else content
        self.__removed = None
        self.count = {"loss": 0, "success": 0}
        self.size = size
        if self.ui is True:
            self.ProgressBar.config(maximum=self.size)
            if self.independant is True:
                self.link_speed_scale.config(to=self.size / 3)
                self.lambda_scale.config(to=self.size // 50)
                self.strategy_0 = Radiobutton(self.Frame, variable=strategy_var, indicatoron=0, bg="#EC7063", activebackground="#58D68D", selectcolor="#58D68D", value="Random", text="Random")
                self.strategy_1 = Radiobutton(self.Frame, variable=strategy_var, indicatoron=0, bg="#EC7063", activebackground="#58D68D", selectcolor="#58D68D", value="Highest", text="Highest")
                self.strategy_2 = Radiobutton(self.Frame, variable=strategy_var, indicatoron=0, bg="#EC7063", activebackground="#58D68D", selectcolor="#58D68D", value="Round", text="Round")
                self.strategy_0.grid(row=7, column=1, sticky="ew")
                self.strategy_1.grid(row=8, column=1, sticky="ew")
                self.strategy_2.grid(row=9, column=1, sticky="ew")

    def __repr__(self):
        return (f"Buffer(occupied:{self.space_occupied()}/{self.size}, amount={len(self.content)})")

    def __add__(self, value):
        """Add an element to the first position."""
        if isinstance(value, Packet):
            if (self.space_remaining() > value.size):
                self.content.append(value)
                self.count["success"] += 1
            else:
                self.count["loss"] += 1
        elif isinstance(value, Iterable):
            self.content += value
        return (self)

    def remove(self):
        """Remove the last element of the Buffer and store that value.\n\n Can also only return the last removed object."""
        if (self.length() > 0):    # Cannot remove anything from an empty list
            self.__removed = (self.content)[-1]
            self.content = (self.content)[:-1]

    def remove_all(self):
        """Remove all last element of the Buffer."""
        self.content = []

    def gargabe_collection(self):
        """Remove all packets that are empty."""
        self.content = [element for element in self.content if isinstance(element, Packet) and (element.size > 0)]

    def reset_ratio(self):
        """Reset the count to 0 loss and 0 success."""
        self.count = {"loss": 0, "success": 0}

    def void_packets(self, max_speed: int):
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
        """Get the length of the Buffer."""
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
        """Checks if the Buffer is empty or not."""
        return (False if self.content else True)

    def update(self):

        # Updating widgets
        if self.ui is True:
            self.loss_label.configure(text=f"Loss: {self.ratio * 100:05.2f}%")
            self.progbarvalue.set(self.space_occupied() - 1)
            self.occupation_label.configure(text=f"Occupied:\n{self.space_occupied():04d}/{self.size}")

    @property
    def removed(self):
        """Use to get the last removed value."""
        return (self.__removed)

    @property
    def ratio(self):
        """Return the percentage of loss [0;1]."""
        return (self.count["loss"] / max(1, sum(self.count.values())))


class Source(Buffer):
    """A Source of packets, that can send information to a Buffer. Use Graph docstring.
    \nOptionnal Arguments:
    \n - create_ui: bool = True -> Whether or not to create a GUI.
    """

    def __init__(self, master=None, **kwargs):
        self.ui = kwargs.get("create_ui", True)
        self.id = id(self)
        self.waited = 0
        super().__init__(master, **kwargs)

    def __repr__(self) -> str:
        return (f"Client(ID={self.id}, occupied:{self.space_occupied()}/{self.size}, amount={len(self.content)})")

    def generate_packets(self, size: int = 4, rate_lambda: float = 0, log=False):
        """Generate a numpy array containing values based on the λ chosen, the amount of values is given by the size
        \nThe larger the size the better the accuracy, but slower is the reaction time when λ changes.
        """
        for value in probability.poisson(rate_lambda, size):
            if (self.space_occupied() + value) <= self.size:
                if value > 0:
                    self.content += [Packet(self.id, value, f"Packet {value:04d}")]
                    self.count["success"] += 1
            else:
                self.count["loss"] += 1

        self.update()
        if log is True:
            print(f"Generated packet size: {sum(packet.size for packet in self.content)} bits")
            print([packet.size for packet in self.content])

    def send_packets(self, buffer, amount: int = 1, packet: Packet = None):
        """The amount determines the number of cycles before creating new packets"""
        self.gargabe_collection()   # Don't send packets that are empty
        for i in range(amount):
            if packet is not None:
                buffer += packet  # Add the packet to the buffer
                buffer.update()
                if self.ui is True:
                    buffer.packet_label.configure(text=f"Current packet: {packet.source}")
                    buffer.packet_size_label.configure(text=f"Current packet size: {packet.size}")
            else:
                # Transmettre le prochain paquet de la liste de paquets du client
                if self.content:
                    next_packet = self.content.pop(0)
                    buffer += next_packet  # Add the packet to the buffer
                    buffer.update()
                    if self.ui is True:
                        buffer.packet_label.configure(text=f"Current packet: {next_packet.source}")
                        buffer.packet_size_label.configure(text=f"Current packet size: {next_packet.size}")

    def update(self):

        # Updating widgets
        if self.ui is True:
            self.loss_label.configure(text=f"Loss: {self.ratio * 100:05.2f}%")
            self.progbarvalue.set(self.space_occupied() - 1)
            self.occupation_label.configure(text=f"Occupied:\n{self.space_occupied():04d}/{self.size}")
            self.remaining_packets.configure(text=f"Packets left: {self.length()}")
            self.waited_label.configure(text=f"Waited: {self.waited}s")


def test_buffer():
    """Scenario to test the class Buffer"""
    buffer0 = Buffer(size=8, create_ui=False)       # Creates a Buffer with a size limit of 8
    for i in range(10):         # Attempt to fill the Buffer with 10 elements
        buffer0 += Packet(0, i)   # Using the __add__ method
    print(buffer0, buffer0.length(), buffer0.space_occupied())                # Displaying using the __repr__ method
    while not buffer0.is_empty():
        buffer0.remove()
        print(buffer0.removed)
    print(buffer0)
    print(buffer0.count)
    print(f"The Buffer has a loss ratio of: {buffer0.ratio * 100:.3f}%")
    print("Because the Buffer can hold only 8 bits, we stop adding packets after the fourth packet (0+1+2+3 = 6 < 8, 0+1+2+3+4 = 10 > 8)")


def test_client(dummy_lambda):
    """Scenario to test the class Source and Packet"""
    test_source0, test_buffer1 = Source(size=50, create_ui=False), Buffer(size=500, create_ui=False)

    print("source0:", test_source0)
    test_source0.send_packets(test_buffer1)                # To test without any packets
    print("source0:", test_source0)
    test_source0.generate_packets(10, dummy_lambda, True)      # Generating packets with λ
    print("source0:", test_source0)
    test_source0.send_packets(test_buffer1, 9)            # Sending all but one packet
    print("After sending 9 packets")
    print("source0:", test_source0)
    print("buffer1:", test_buffer1)
    print(f"There is {len(test_source0.content)} packets remaining")     # How many packets left to send
    test_source0.send_packets(test_buffer1, 1)              # Sending last packet
    print(f"There is {len(test_source0.content)} packets remaining")
    print("source0:", test_source0)
    print("buffer1:", test_buffer1)
    print(f"Source Packet loss: {test_source0.ratio * 100:.3f}%")
    print(f"Buffer Packet loss: {test_buffer1.ratio * 100:.3f}%")

# Question 4+


def main_loop():
    """What makes the simulation dynamic. Each loop is referred as a tick."""
    global tick
    tick += 1
    main_window.title(f"Simulateur d'un lien réseau tick #{tick}")
    source_choice = None

    match strategy_var.get():
        case "Random":
            candidats = [source.id for source in SOURCES if source.space_occupied() > 0]
            source_choice = choice(candidats) if len(candidats) > 0 else 0
        case "Highest":
            temp = 0
            for source in SOURCES:
                if source.space_occupied() > temp:
                    temp = source.space_occupied()
                    source_choice = source.id
        case "Round":
            source_choice = SOURCES[tick % len(SOURCES)].id

    for BUFFER in BUFFERS:
        BUFFER.update()
    for SOURCE in SOURCES:
        if (tick % 2 == 0):     # Every two ticks
            SOURCE.generate_packets(4, float(public_lambda.get()))
        if SOURCE.id == source_choice:
            SOURCE.send_packets(BUFFERS[0])
            SOURCE.waited = 0
            BUFFERS[0].update()
        else:
            if SOURCE.length() > 0:
                SOURCE.waited += 1
        SOURCE.update()

    # Call transmit_packets once per tick
    for BUFFER in BUFFERS:
        BUFFER.void_packets(BUFFER.speed)

    main_window.update()
    main_window.after(func=main_loop, ms=1000)  # One tick per second


if __name__ == "__main__":

    # Test (Q2)
    test_buffer()
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
    tick = 0
    strategy_var = StringVar(value="Random")

    SOURCES = [Source(main_window, row=i % 3, column=i // 3, padx=5, pady=5, size=10000, name=f"Client {i:02d}") for i in range(9)]
    BUFFERS = [Buffer(main_window, row=0, column=100, rowspan=100, padx=5, pady=5, sticky="nse", size=100000, display_size=200, name="Main Buffer", independant=True)]

    main_window.columnconfigure(10, weight=1)  # Make sure the main Buffer is at the right side

    main_loop()
    main_window.mainloop()
