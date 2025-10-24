import queue
import socket
import threading
import time
import tkinter
from datetime import datetime

import pygame

from time_frame import TimeFrame


class TimeTravelApp:
    def __init__(self, master):
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

        self.pres_time_thread = threading.Thread(target=self.update_present_time, daemon=True)
        self.pres_time_thread.start()
        self.start_udp_server()

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
            # self.last_depart_frame.clock_font.configure(size=new_label_size)

            self.dest_frame.time_type_font.configure(size=new_frame_size)
            self.present_time_frame.time_type_font.configure(size=new_frame_size)
            # self.last_depart_frame.time_type_font.configure(size=new_frame_size)

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
        while True:
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
                    self.run_scenario(1)
        # self.master.after(100, self.process_udp_messages)

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
