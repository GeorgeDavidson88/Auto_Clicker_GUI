import os
import threading
import time
from tkinter import PhotoImage, StringVar

import customtkinter
import pynput

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

exit_threads = threading.Event()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x345")
        self.resizable(0, 0)

        self.title("Auto Clicker")
        self.iconphoto(True, PhotoImage(
            file=os.path.join("graphics", "icon.png")))

        self.hotkey = StringVar(self, "Key.f6")

        self.number_validate_register = self.register(self.number_validate)

        self.clicking = False

        self.top_frame = customtkinter.CTkFrame(master=self)
        self.top_frame.place(anchor="n", relx=0.5, rely=0.02,
                             relwidth=0.96, relheight=0.35)

        self.hrs_label = customtkinter.CTkLabel(
            master=self.top_frame, text="Hours")
        self.hrs_label.place(anchor="nw", relx=0.025,
                             rely=0.025, relwidth=0.20, relheight=0.25)

        self.hrs_entry = customtkinter.CTkEntry(
            master=self.top_frame)
        self.hrs_entry.place(anchor="nw", relx=0.025,
                             rely=0.2, relwidth=0.20, relheight=0.25)

        self.hrs_entry.configure(validate="key", validatecommand=(
            self.number_validate_register, "%P"))

        self.mins_label = customtkinter.CTkLabel(
            master=self.top_frame, text="Minutes")
        self.mins_label.place(anchor="nw", relx=0.275,
                              rely=0.025, relwidth=0.2, relheight=0.25)

        self.mins_entry = customtkinter.CTkEntry(
            master=self.top_frame)
        self.mins_entry.place(anchor="nw", relx=0.275,
                              rely=0.2, relwidth=0.2, relheight=0.25)

        self.mins_entry.configure(validate="key", validatecommand=(
            self.number_validate_register, "%P"))

        self.secs_lable = customtkinter.CTkLabel(
            master=self.top_frame, text="Seconds")
        self.secs_lable.place(anchor="nw", relx=0.525,
                              rely=0.025, relwidth=0.2, relheight=0.25)

        self.secs_entry = customtkinter.CTkEntry(
            master=self.top_frame)
        self.secs_entry.place(anchor="nw", relx=0.525,
                              rely=0.2, relwidth=0.2, relheight=0.25)

        self.secs_entry.configure(validate="key", validatecommand=(
            self.number_validate_register, "%P"))

        self.mils_lable = customtkinter.CTkLabel(
            master=self.top_frame, text="Milliseconds")
        self.mils_lable.place(anchor="nw", relx=0.775,
                              rely=0.025, relwidth=0.2, relheight=0.25)

        self.mils_entry = customtkinter.CTkEntry(
            master=self.top_frame)
        self.mils_entry.place(anchor="nw", relx=0.775,
                              rely=0.2, relwidth=0.2, relheight=0.25)

        self.mils_entry.configure(validate="key", validatecommand=(
            self.number_validate_register, "%P"))

        self.random_checkbox = customtkinter.CTkCheckBox(
            master=self.top_frame, text="Random Offset In Milliseconds")
        self.random_checkbox.place(anchor="nw", relx=0.025, rely=0.65)

        self.random_offset_entry = customtkinter.CTkEntry(
            master=self.top_frame)
        self.random_offset_entry.place(anchor="nw", relx=0.525,
                                       rely=0.6, relwidth=0.45, relheight=0.25)

        self.random_offset_entry.configure(validate="key", validatecommand=(
            self.number_validate_register, "%P"))

        self.middle_frame = customtkinter.CTkFrame(master=self)
        self.middle_frame.place(anchor="n", relx=0.5,
                                rely=0.4, relwidth=0.96, relheight=0.12)

        self.mouse_button_optionmenu = customtkinter.CTkOptionMenu(master=self.middle_frame, values=[
                                                                   "Mouse Button Left", "Mouse Button Right"], command=lambda button: print(button),)
        self.mouse_button_optionmenu.place(
            anchor="nw", relx=0.03, rely=0.1, relwidth=0.46, relheight=0.8)

        self.mode_optionmenu = customtkinter.CTkOptionMenu(master=self.middle_frame, values=[
                                                           "Toggle", "Hold"], command=lambda mode: print(mode),)
        self.mode_optionmenu.place(
            anchor="ne", relx=0.97, rely=0.1, relwidth=0.46, relheight=0.8)

        self.bottom_frame = customtkinter.CTkFrame(master=self)
        self.bottom_frame.place(anchor="n", relx=0.5,
                                rely=0.55, relwidth=0.96, relheight=0.42)

        self.main_hotkey_frame = customtkinter.CTkFrame(
            master=self.bottom_frame)
        self.main_hotkey_frame.place(
            anchor="nw", relx=0.03, rely=0.05, relwidth=0.46, relheight=0.4)

        self.hotkey_frame = customtkinter.CTkFrame(
            master=self.main_hotkey_frame)
        self.hotkey_frame.place(anchor="w", relx=0.05,
                                rely=0.5, relwidth=0.4, relheight=0.56)

        self.hotkey_lable = customtkinter.CTkLabel(
            master=self.hotkey_frame, text="Hotkey")
        self.hotkey_lable.place(anchor="center", relx=0.5,
                                rely=0.5, relwidth=0.5, relheight=0.6)

        self.hotkey_entry = customtkinter.CTkEntry(
            master=self.main_hotkey_frame, textvariable=self.hotkey)
        self.hotkey_entry.place(anchor="e", relx=0.93,
                                rely=0.5, relwidth=0.44, relheight=0.56)

        self.theme_optionmenu = customtkinter.CTkOptionMenu(master=self.bottom_frame, values=[
                                                            "Dark", "Light"], command=lambda theme: customtkinter.set_appearance_mode(theme))
        self.theme_optionmenu.place(
            anchor="ne", relx=0.97, rely=0.05, relwidth=0.46, relheight=0.4)

        self.start_button = customtkinter.CTkButton(
            master=self.bottom_frame, text="Start", command=self.start_clicking)
        self.start_button.place(anchor="sw", relx=0.03,
                                rely=0.95, relwidth=0.46, relheight=0.4)

        self.stop_button = customtkinter.CTkButton(
            master=self.bottom_frame, text="Stop", command=self.stop_clicking)
        self.stop_button.place(anchor="se", relx=0.97,
                               rely=0.95, relwidth=0.46, relheight=0.4)

    def number_validate(self, input):
        try:
            if input == "" or int(input):
                return True

        except:
            return False

    def clicker(self):
        while True:
            if exit_threads.is_set():
                break

            if self.clicking:
                pynput.mouse.Controller().click(pynput.mouse.Button.left, 1)
                
            time.sleep(0.01)

    def toggle_event(self, key):
        if exit_threads.is_set():
            return False

        key = str(key)
        hotkey = str(self.hotkey.get())

        if key == hotkey:
            self.clicking = not self.clicking

    def listener(self):
        with pynput.keyboard.Listener(on_press=self.toggle_event) as listener:
            listener.join()

    def start_clicking(self):
        self.clicking = True

    def stop_clicking(self):
        self.clicking = False

    def mainloop(self):
        click_thred = threading.Thread(target=self.clicker)
        click_thred.start()

        listener_thred = threading.Thread(target=self.listener)
        listener_thred.start()

        return super().mainloop()


def main():
    app = App()
    app.mainloop()

    exit_threads.set()
    pynput.keyboard.Controller().press(pynput.keyboard.Key.esc)


if __name__ == "__main__":
    main()
