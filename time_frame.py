import time
import tkinter
from tkinter import font

from PIL import Image, ImageTk


class TimeFrame:
    def __init__(self, parent, time_type_title, digit_fg_color="lime green", row=0, col=0):
        self.clock_font = font.Font(family="Digital-7", size=12)
        self.time_type_font = font.Font(family="Arial", size=16)
        self.era_font = font.Font(family="Consolas", size=12)
        self.am_pm_font = font.Font(family="Arial", size=24)
        self.time_type_title = time_type_title
        self.digit_fg_color = digit_fg_color
        self.main_frame_bg = "#36454F"
        self.time_frame_bg = "black"
        self.clock_section_padx = 24
        self.clock_ipad = 8

        green_photo = Image.open("lime-green.png")
        self.green_circle = ImageTk.PhotoImage(green_photo)

        black_photo = Image.open("black-cir.png")
        self.black_circle = ImageTk.PhotoImage(black_photo)

        self.time_type_frame = tkinter.Frame(parent, background=self.main_frame_bg)
        self.time_type_frame.rowconfigure(0, weight=1)
        self.time_type_frame.rowconfigure(1, weight=1)
        self.time_type_frame.columnconfigure(0, weight=1)
        self.time_type_frame.grid(row=row, column=col, sticky=tkinter.NSEW, pady=12)

        self.time_field_frame = self.build_time_frame(self.time_type_frame, label_txt_color=self.digit_fg_color)
        self.time_field_frame.grid(row=1, column=0, sticky=tkinter.NSEW)

        # self.time_field_text = tkinter.StringVar()
        # self.time_field_text.set(self.time_type_title)
        self.time_field_label = tkinter.Label(self.time_type_frame, text=self.time_type_title, font=self.time_type_font, background=self.main_frame_bg, foreground='white')
        self.time_field_label.grid(row=0, column=0, sticky=tkinter.EW)

    def set_time(self, datestamp, era="AD"):
        print(f"setting time: {datestamp.year}:{datestamp.month}:{datestamp.day}:{datestamp.hour}:{datestamp.minute}")
        month_dict = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5:  "MAY", 6: "JUN", 7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"}
        time.sleep(1)
        year = str(datestamp.year)
        self.year_label["text"] = "0"*(4-len(year)) + year.replace("1", " 1")
        self.month_label["text"] = str(month_dict[int(datestamp.month)])
        self.day_label["text"] = datestamp.strftime("%d").replace("1", " 1")
        self.hour_label["text"] = datestamp.strftime("%I").replace("1", " 1")
        self.min_label["text"] = datestamp.strftime("%M").replace("1", " 1")
        am_pm_indicator = datestamp.strftime('%p')

        self.era_label["text"] = era

        if am_pm_indicator == "AM":
            self.am_label.configure(image=self.green_circle)
            self.am_label.image = self.green_circle
            self.pm_label.configure(image=self.black_circle)
            self.pm_label.image = self.black_circle
        else:
            self.am_label.configure(image=self.black_circle)
            self.am_label.image = self.black_circle
            self.pm_label.configure(image=self.green_circle)
            self.pm_label.image = self.green_circle

    def build_time_frame(self, parent, label_txt_color="lime green"):
        time_frame = tkinter.Frame(parent, background=self.main_frame_bg)
        time_frame.rowconfigure(0, weight=1)
        time_frame.columnconfigure(0, weight=1, uniform="equal_width")
        time_frame.columnconfigure(1, weight=1)
        time_frame.columnconfigure(2, weight=1, uniform="equal_width")

        month_day_frame = tkinter.Frame(time_frame, background=self.main_frame_bg)
        month_day_frame.rowconfigure(0, weight=1)
        month_day_frame.columnconfigure(0, weight=1)
        month_day_frame.columnconfigure(1, weight=1)
        # month_day_frame.columnconfigure(2, weight=1)
        # month_day_frame.columnconfigure(3, weight=1)
        month_day_frame.grid(row=0, column=0, sticky=tkinter.NSEW, padx=self.clock_section_padx)

        self.month_label = tkinter.Label(month_day_frame, text="---", font=self.clock_font,
                                    background=self.time_frame_bg, foreground=label_txt_color)
        self.month_label.grid(row=0, column=0, padx=self.clock_section_padx, ipadx=self.clock_ipad,
                         ipady=self.clock_ipad, sticky=tkinter.NSEW)

        self.day_label = tkinter.Label(month_day_frame, text="--", font=self.clock_font,
                                  background=self.time_frame_bg, foreground=label_txt_color)
        self.day_label.grid(row=0, column=1, padx=self.clock_section_padx, ipadx=self.clock_ipad, ipady=self.clock_ipad, sticky=tkinter.NSEW)

        year_frame = tkinter.Frame(time_frame, background=self.main_frame_bg)
        year_frame.rowconfigure(0, weight=1)
        year_frame.columnconfigure(0, weight=1, uniform="equal_width")
        year_frame.columnconfigure(1, weight=1)
        # year_frame.columnconfigure(2, weight=1)
        # year_frame.columnconfigure(3, weight=1)
        year_frame.grid(row=0, column=1, sticky=tkinter.NSEW, padx=self.clock_section_padx)

        self.year_label = tkinter.Label(year_frame, text="----", font=self.clock_font,
                                   background=self.time_frame_bg, foreground=label_txt_color)
        self.year_label.grid(row=0, column=0, padx=self.clock_section_padx, ipadx=self.clock_ipad,
                        ipady=self.clock_ipad, sticky=tkinter.NSEW)

        self.era_label = tkinter.Label(year_frame, text="--", font=self.clock_font,
                                   background=self.time_frame_bg, foreground=label_txt_color)
        self.era_label.grid(row=0, column=1, padx=self.clock_section_padx, ipadx=self.clock_ipad,
                        ipady=self.clock_ipad, sticky=tkinter.NSEW)

        hour_min_frame = tkinter.Frame(time_frame, background=self.main_frame_bg)
        hour_min_frame.rowconfigure(0, weight=1)
        hour_min_frame.columnconfigure(0, weight=1)
        hour_min_frame.columnconfigure(1, weight=1)
        hour_min_frame.columnconfigure(2, weight=1)
        hour_min_frame.columnconfigure(3, weight=1)
        hour_min_frame.grid(row=0, column=2, sticky=tkinter.NSEW, padx=self.clock_section_padx)

        am_pm_frame = tkinter.Frame(hour_min_frame)
        am_pm_frame.rowconfigure(0, weight=1)
        am_pm_frame.rowconfigure(1, weight=1)
        am_pm_frame.columnconfigure(0, weight=1)
        am_pm_frame.grid(row=0, column=0, sticky=tkinter.EW)

        am_label_frame = tkinter.LabelFrame(am_pm_frame, text="AM", font=self.am_pm_font, labelanchor=tkinter.N,
                                            borderwidth=0, background=self.main_frame_bg, foreground="red")
        am_label_frame.rowconfigure(0, weight=1)
        am_label_frame.columnconfigure(0, weight=1)
        am_label_frame.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.am_label = tkinter.Label(am_label_frame, image=self.black_circle, background=self.main_frame_bg)
        self.am_label.grid(row=0, column=0, sticky=tkinter.EW)
        self.am_label.image = self.black_circle

        pm_label_frame = tkinter.LabelFrame(am_pm_frame, text="PM", font=self.am_pm_font, labelanchor=tkinter.N,
                                            borderwidth=0, background=self.main_frame_bg, foreground="red")
        pm_label_frame.rowconfigure(0, weight=1)
        pm_label_frame.columnconfigure(0, weight=1)
        pm_label_frame.grid(row=1, column=0, sticky=tkinter.NSEW)

        self.pm_label = tkinter.Label(pm_label_frame, image=self.black_circle, background=self.main_frame_bg)
        self.pm_label.grid(row=0, column=0, sticky=tkinter.EW)
        self.pm_label.image = self.black_circle

        self.hour_label = tkinter.Label(hour_min_frame, text="--", font=self.clock_font,
                                   background=self.time_frame_bg, foreground=label_txt_color)
        self.hour_label.grid(row=0, column=1, sticky="nsew", ipadx=self.clock_ipad, ipady=self.clock_ipad)

        colon_var = tkinter.StringVar()
        colon_var.set(":")
        colon_label = tkinter.Label(hour_min_frame, textvariable=colon_var, font=self.clock_font,
                                    background=self.main_frame_bg, foreground=label_txt_color)
        colon_label.grid(row=0, column=2, sticky=tkinter.EW, ipadx=self.clock_ipad, ipady=self.clock_ipad)

        self.min_label = tkinter.Label(hour_min_frame, text="--", font=self.clock_font,
                                  background=self.time_frame_bg, foreground=label_txt_color)
        self.min_label.grid(row=0, column=3, sticky="nsew", ipadx=self.clock_ipad, ipady=self.clock_ipad)

        return time_frame
