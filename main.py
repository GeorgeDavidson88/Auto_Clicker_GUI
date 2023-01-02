import os
import random
import threading
import time
from tkinter import PhotoImage, StringVar

import customtkinter
import pynput

exit_threads = threading.Event()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x300")
        self.resizable(0, 0)

        self.title("Auto Clicker")
        self.iconphoto(False, PhotoImage(
            file=os.path.join("icon", "icon.png")))

        self.left_hotkey = StringVar(self, "'x'")
        self.right_hotkey = StringVar(self, "Key.ctrl_l")

        self.delay = StringVar(self, f"Click Delay (0.06)")
        self.offset = StringVar(self, f"Random Offset (0.04)")

        self.top_frame = customtkinter.CTkFrame(master=self)
        self.top_frame.place(anchor="n", x=250, y=10,
                             width=480, height=120)

        self.delay_lable = customtkinter.CTkLabel(
            master=self.top_frame, textvariable=self.delay)
        self.delay_lable.place(anchor="n", x=240, y=10)

        self.delay_slider = customtkinter.CTkSlider(
            master=self.top_frame, from_=10, to=1000, command=lambda delay: self.delay.set(f"Click Delay ({round(delay / 1000, 2)})"))
        self.delay_slider.place(
            anchor="n", x=240, y=40, width=460, height=20)
        self.delay_slider.set(60)

        self.offset_lable = customtkinter.CTkLabel(
            master=self.top_frame, textvariable=self.offset)
        self.offset_lable.place(anchor="n", x=240, y=60)

        self.offset_slider = customtkinter.CTkSlider(
            master=self.top_frame, from_=0, to=1000, command=lambda delay: self.offset.set(f"Random Offset ({round(delay / 1000, 2)})"))
        self.offset_slider.place(
            anchor="n", x=240, y=90, width=460, height=20)
        self.offset_slider.set(40)

        self.middle_frame_top = customtkinter.CTkFrame(master=self)
        self.middle_frame_top.place(anchor="center", x=250,
                                    y=175, width=480, height=70)

        self.left_main_button_frame = customtkinter.CTkFrame(
            master=self.middle_frame_top)
        self.left_main_button_frame.place(
            anchor="w", x=10, y=35, width=225, height=50)

        self.left_button_frame = customtkinter.CTkFrame(
            master=self.left_main_button_frame)
        self.left_button_frame.place(
            anchor="w", x=10, y=25, width=97.5, height=30)

        self.left_button_lable = customtkinter.CTkLabel(
            master=self.left_button_frame, text="Hotkey")
        self.left_button_lable.place(
            anchor="center", x=48.75, y=15, width=97.5, height=20)

        self.left_hotkey_entry = customtkinter.CTkEntry(
            master=self.left_main_button_frame, textvariable=self.left_hotkey)
        self.left_hotkey_entry.place(
            anchor="e", x=215, y=25, width=97.5, height=30)

        self.left_main_mouse_button_frame = customtkinter.CTkFrame(
            master=self.middle_frame_top)
        self.left_main_mouse_button_frame.place(
            anchor="e", x=470, y=35, width=225, height=50)

        self.left_mouse_button_frame = customtkinter.CTkFrame(
            master=self.left_main_mouse_button_frame)
        self.left_mouse_button_frame.place(
            anchor="w", x=10, y=25, width=97.5, height=30)

        self.left_mouse_button_lable = customtkinter.CTkLabel(
            master=self.left_mouse_button_frame, text="Mouse Button")
        self.left_mouse_button_lable.place(
            anchor="center", x=48.75, y=15, width=97.5, height=20)

        self.left_button_label = customtkinter.CTkLabel(
            master=self.left_main_mouse_button_frame, text="Left")
        self.left_button_label.place(
            anchor="e", x=215, y=25, width=97.5, height=30)

        self.middle_frame_bottom = customtkinter.CTkFrame(master=self)
        self.middle_frame_bottom.place(anchor="center", x=250,
                                       y=255, width=480, height=70)

        self.right_main_button_frame = customtkinter.CTkFrame(
            master=self.middle_frame_bottom)
        self.right_main_button_frame.place(
            anchor="w", x=10, y=35, width=225, height=50)

        self.right_button_frame = customtkinter.CTkFrame(
            master=self.right_main_button_frame)
        self.right_button_frame.place(
            anchor="w", x=10, y=25, width=97.5, height=30)

        self.right_button_lable = customtkinter.CTkLabel(
            master=self.right_button_frame, text="Hotkey")
        self.right_button_lable.place(
            anchor="center", x=48.75, y=15, width=97.5, height=20)

        self.right_hotkey_entry = customtkinter.CTkEntry(
            master=self.right_main_button_frame, textvariable=self.right_hotkey)
        self.right_hotkey_entry.place(
            anchor="e", x=215, y=25, width=97.5, height=30)

        self.right_main_mouse_button_frame = customtkinter.CTkFrame(
            master=self.middle_frame_bottom)
        self.right_main_mouse_button_frame.place(
            anchor="e", x=470, y=35, width=225, height=50)

        self.right_mouse_button_frame = customtkinter.CTkFrame(
            master=self.right_main_mouse_button_frame)
        self.right_mouse_button_frame.place(
            anchor="w", x=10, y=25, width=97.5, height=30)

        self.right_mouse_button_lable = customtkinter.CTkLabel(
            master=self.right_mouse_button_frame, text="Mouse Button")
        self.right_mouse_button_lable.place(
            anchor="center", x=48.75, y=15, width=97.5, height=20)

        self.right_button_label = customtkinter.CTkLabel(
            master=self.right_main_mouse_button_frame, text="right")
        self.right_button_label.place(
            anchor="e", x=215, y=25, width=97.5, height=30)

    def mainloop(self):
        return super().mainloop()


class Clicker:
    def __init__(self):
        self.left_clicking = False
        self.right_clicking = False

    def calculate_delay(self, app):
        subtracted_offset = round(
            (float(app.delay.get()[13:-1]) - float(app.offset.get()[15:-1])) * 1000)
        added_offset = round(
            (float(app.delay.get()[13:-1]) + float(app.offset.get()[15:-1])) * 1000)

        if subtracted_offset < 0.01:
            subtracted_offset = 0.01

        if subtracted_offset > added_offset:
            subtracted_offset = added_offset

        return random.randint(round(subtracted_offset), round(added_offset)) / 1000

    def left_clicker(self, app):
        while not exit_threads.is_set():
            if self.left_clicking:
                pynput.mouse.Controller().click(pynput.mouse.Button.left)

                time.sleep(self.calculate_delay(app))

            else:
                time.sleep(0.1)

    def right_clicker(self, app):
        while not exit_threads.is_set():
            if self.right_clicking:
                pynput.mouse.Controller().click(pynput.mouse.Button.right)

                time.sleep(self.calculate_delay(app))

            else:
                time.sleep(0.1)

    def on_press(self, key, app):
        if exit_threads.is_set():
            return False

        if str(key) == app.left_hotkey.get():
            self.left_clicking = not self.left_clicking

        if str(key) == app.right_hotkey.get():
            self.right_clicking = not self.right_clicking


def keyboard_listener(app, clicker):
    with pynput.keyboard.Listener(on_press=lambda key: clicker.on_press(key, app)) as keyboard_listener:
        keyboard_listener.join()


def main():
    app = App()
    clicker = Clicker()

    left_clicker_thred = threading.Thread(
        target=clicker.left_clicker, args=(app,))
    left_clicker_thred.start()

    right_clicker_thred = threading.Thread(
        target=clicker.right_clicker, args=(app,))
    right_clicker_thred.start()

    keyboard_listener_thred = threading.Thread(
        target=keyboard_listener, args=(app, clicker))
    keyboard_listener_thred.start()

    app.mainloop()

    exit_threads.set()
    pynput.keyboard.Controller().press(pynput.keyboard.Key.esc)
    pynput.keyboard.Controller().release(pynput.keyboard.Key.esc)


if __name__ == "__main__":
    main()
