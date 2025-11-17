import queue
import random
import socket
import threading
import time
import tkinter
from datetime import datetime

import pygame

from time_frame import TimeFrame


class TimeTravelApp:
    def __init__(self, master):
        self.no_signal_thread = None
        self.static_thread = None
        self.pres_time_thread = None
        self.static_thread_event = threading.Event()
        self.no_signal_thread_event = threading.Event()
        self.pres_time_thread_event = threading.Event()
        pygame.mixer.init()
        self.sound_effect = pygame.mixer.Sound("time-machine.wav")
        self.main_frame_bg = "#36454F"
        self.dest_fg = "#FF0000"
        self.pres_time_fg = "lime green"
        self.last_dep_fg = "#fff374"
        self.master = master
        self.master.bind('<Configure>', self.on_resize)
        self.master.bind('<Escape>', self.exit_fullscreen)
        self.master.bind('<F5>', self.enter_fullscreen)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        master.title("Time Travel App")
        self.destination_time = datetime.now()
        self.last_departure_time = datetime.now()
        self.present_time = datetime.now()

        self.message_queue = queue.Queue()

        self.main_frame = tkinter.Frame(master, background=self.main_frame_bg)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        # self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.grid(sticky=tkinter.NSEW)

        self.dest_frame = TimeFrame(self.main_frame, "Destination: ", self.dest_fg, row=0, col=0)
        self.present_time_frame = TimeFrame(self.main_frame, "Present: Cedar Rapids, IA", self.pres_time_fg, row=1,
                                            col=0)
        # self.last_depart_frame = TimeFrame(self.main_frame, "Last Departure Time", self.last_dep_fg, row=2, col=0)
        self.pres_time_thread_event.clear()
        self.start_pres_time_thread()
        self.start_udp_server()

        self.color_no_sig_canvas = tkinter.Canvas(self.master, bg="grey", highlightthickness=0)
        self.static_canvas = tkinter.Canvas(self.master, bg="grey", highlightthickness=0)

    def on_resize(self, event):
        frame_width = self.present_time_frame.month_day_frame.winfo_width()
        frame_height = self.present_time_frame.month_day_frame.winfo_height()
        if event.widget == self.master:
            new_label_size = int(min(frame_width / 2.5, frame_height / 2.5))
            new_era_label_size = int(min(frame_width / 2.5, frame_width / 2.5))
            new_frame_size = int(min(event.width / 20, event.height / 20))

            self.dest_frame.clock_font.configure(size=new_label_size)
            self.dest_frame.era_font.configure(size=new_era_label_size)
            self.present_time_frame.clock_font.configure(size=new_label_size)
            self.present_time_frame.era_font.configure(size=new_era_label_size)

            self.dest_frame.time_type_font.configure(size=new_frame_size)
            self.present_time_frame.time_type_font.configure(size=new_frame_size)

    def start_udp_server(self):
        self.udp_ip = "0.0.0.0"
        self.udp_port = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))
        print(f"listening on {self.udp_ip}:{self.udp_port}")

        self.udp_thread = threading.Thread(target=self.receive_udp_data, daemon=True)
        self.udp_thread.start()

        self.process_thread = threading.Thread(target=self.process_udp_messages, daemon=True)
        self.process_thread.start()

    def create_color_static(self):
        # Set the window size (common TV aspect ratio)
        self.master.update_idletasks()
        window_height = self.master.winfo_height()
        self.master.update_idletasks()
        window_width = self.master.winfo_width()

        # SMPTE color bar colors (hex codes)
        # The top bars (75% luminance)
        colors_top = ["#FFFFFF", "#FFFF00", "#00FFFF", "#00FF00", "#FF00FF", "#FF0000", "#0000FF"]
        # The bottom bars (pluge pulse area)
        colors_bottom = ["#0000FF", "#FFFFFF", "#00FFFF", "#FFFFFF", "#00FFFF", "#FFFFFF", "#0000FF"]  # Simplified

        num_bars = len(colors_top)
        bar_width = window_width / num_bars
        top_height = window_height * 0.75
        bottom_height = window_height * 0.25

        # Draw top color bars
        for i, color in enumerate(colors_top):
            x1 = i * bar_width
            x2 = (i + 1) * bar_width
            self.color_no_sig_canvas.create_rectangle(x1, 0, x2, top_height, fill=color, outline="")

        # Draw bottom color bars (simplified representation)
        for i, color in enumerate(colors_bottom):
            x1 = i * bar_width
            x2 = (i + 1) * bar_width
            self.color_no_sig_canvas.create_rectangle(x1, window_height, x2, bottom_height, fill=color, outline="")

    def create_static(self):
        """Generates a frame of random black and white static."""
        # Create a blank image
        height = self.static_canvas.winfo_height()
        width = self.static_canvas.winfo_width()
        image = tkinter.PhotoImage(width=width, height=height)

        # Generate random pixels
        pixels = []
        for y in range(height):
            row = "{"
            for x in range(width):
                # Randomly choose black or white color
                color = "#000000" if random.randint(0, 1) == 0 else "#FFFFFF"
                row += color + " "
            row = row.strip() + "}"
            pixels.append(row)

        # Put the generated pixels into the image
        image.put(" ".join(pixels), (0, 0))

        # Update the canvas with the new image
        self.static_canvas.delete("all")  # Clear previous image if any
        self.static_canvas.create_image(0, 0, anchor=tkinter.NW, image=image)

        # Must keep a reference to the image to prevent it from being garbage collected
        self.static_canvas.image = image

        num_lines = random.randint(1, 25)
        canvas_width = width
        canvas_height = height

        # Calculate even spacing
        # We use num_lines + 1 for the number of intervals to ensure lines are inside
        # and evenly spaced relative to the edges.
        spacing = canvas_width / (num_lines + 1)

        for i in range(1, num_lines + 1):
            x_position = i * spacing
            # Draw a vertical line from (x_position, 0) to (x_position, canvas_height)
            self.static_canvas.create_line(x_position, 0, x_position, canvas_height, fill="black", width=2)

    def run_static(self):
        while not self.static_thread_event.is_set():
            # Schedule the next frame generation (e.g., every 50ms for animation)
            self.create_static()
            time.sleep(0.05)

    def run_no_signal(self):
        while not self.no_signal_thread_event.is_set():
            # Schedule the next frame generation (e.g., every 50ms for animation)
            self.create_color_static()
            sleep_time = random.uniform(1, 3)
            time.sleep(sleep_time)

    def run_scenario(self, scenario_num):
        # 1. Set Destination Year to 10 seconds
        # 2. Countdown from 10
        # 3. Set Destination Time
        month_dict = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN", 7: "JUL", 8: "AUG", 9: "SEP",
                      10: "OCT", 11: "NOV", 12: "DEC"}
        scenario_date = datetime(1, 12, 25, 17, 22, 0)
        location = "Bethlehem"
        year = str(scenario_date.year)
        year = year
        month = str(month_dict[int(scenario_date.month)])
        day = scenario_date.strftime("%d").replace("1", " 1")
        hour = scenario_date.strftime("%I").replace("1", " 1")
        minute = scenario_date.strftime("%M").replace("1", " 1")
        am_pm_indicator = scenario_date.strftime('%p')
        time_string = f"{month} {day}, {year} BC {hour}:{minute} {am_pm_indicator}"
        time_and_place = f"{location} ({time_string})"
        self.dest_frame.time_field_label["text"] = f"Desination: {time_and_place}"
        self.dest_frame.year_label["text"] = "----"
        self.dest_frame.month_label["text"] = "---"
        self.dest_frame.day_label["text"] = "--"
        self.dest_frame.era_label["text"] = "--"
        self.dest_frame.hour_label["text"] = "--"
        self.dest_frame.min_label["text"] = "--"

        self.dest_frame.am_label.configure(image=self.dest_frame.black_circle)
        self.dest_frame.am_label.image = self.dest_frame.black_circle
        self.dest_frame.pm_label.configure(image=self.dest_frame.black_circle)
        self.dest_frame.pm_label.image = self.dest_frame.black_circle

        sound_thread = threading.Thread(target=self.sound_effect.play, daemon=True)
        sound_thread.start()
        time.sleep(1)
        for x in range(10, -1, -1):
            self.dest_frame.year_label["text"] = "0" * (4 - len(str(x))) + str(x).replace("1", " 1")
            time.sleep(1)
        time.sleep(2)
        self.dest_frame.set_time(scenario_date, "BC")

    def update_present_time(self):
        while not self.pres_time_thread_event.is_set():
            # Create a timestamp (current date and time)
            self.present_time = datetime.now()
            self.present_time_frame.set_time(self.present_time)

    def receive_udp_data(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = data.decode('utf-8')
                self.message_queue.put(message)
            except Exception as e:
                print(f"Error receiving UDP data: {e}")
                break

    def process_udp_messages(self):
        while True:
            if self.message_queue.not_empty:
                message = self.message_queue.get()
                if message == "1":
                    print("Running scenario 1")
                    self.start_pres_time_thread()
                    self.stop_no_signal_thread()
                    self.stop_static_thread()
                    self.run_scenario(1)
                elif message == "2":
                    self.stop_pres_time_thread()
                    self.stop_no_signal_thread()
                    self.start_static_thread()
                elif message == "3":
                    self.stop_pres_time_thread()
                    self.stop_static_thread()
                    self.start_no_signal_thread()
                elif message == "4":
                    self.clear_static()
                    self.start_pres_time_thread()

    def clear_static(self):
        self.stop_no_signal_thread()
        self.stop_static_thread()

    def start_pres_time_thread(self):
        if self.pres_time_thread is None or not self.pres_time_thread.is_alive():
            print(f"Present Time: {self.pres_time_thread}")
            self.pres_time_thread_event.clear()
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.pres_time_thread = threading.Thread(target=self.update_present_time, daemon=True)
            self.pres_time_thread.start()

    def stop_pres_time_thread(self):
        self.pres_time_thread_event.set()
        if self.pres_time_thread:
            self.pres_time_thread.join()

    def start_static_thread(self):
        self.static_thread_event.clear()
        self.static_canvas.grid(row=0, column=0, sticky="nsew")
        self.static_thread = threading.Thread(target=self.run_static, daemon=True)
        self.static_thread.start()

    def stop_static_thread(self):
        self.static_thread_event.set()
        self.static_canvas.grid_forget()
        if self.static_thread:
            self.static_thread.join()

    def start_no_signal_thread(self):
        self.no_signal_thread_event.clear()
        self.color_no_sig_canvas.grid(row=0, column=0, sticky="nsew")
        self.no_signal_thread = threading.Thread(target=self.run_no_signal, daemon=True)
        self.no_signal_thread.start()

    def stop_no_signal_thread(self):
        self.no_signal_thread_event.set()
        self.color_no_sig_canvas.grid_forget()
        if self.no_signal_thread:
            self.no_signal_thread.join()

    def update_gui(self, message):
        self.dest_text.set(f"Received: {message}")
        print(f"GUI Updated with: {message}")

    def enter_fullscreen(self, event):
        self.master.attributes('-fullscreen', True)
        # self.on_resize(event)

    def exit_fullscreen(self, event):
        self.master.attributes('-fullscreen', False)
        # self.on_resize(event)


def main():
    root = tkinter.Tk()
    display = root

    app = TimeTravelApp(display)
    root.mainloop()


if __name__ == "__main__":
    main()
