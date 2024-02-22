pip install TitleBarCTk
see https://pypi.org/project/TitleBarCTk/0.1.0/

This script creates a title bar for Windows with an icon on the taskbar. It requires:
 - pywin32 306, url: https://pypi.org/project/pywin32/
 - screeninfo 0.8.1, url: https://pypi.org/project/screeninfo/
 - PIL 10.2.0, url: https://pypi.org/project/pillow/
 - customtkinter 0.3, url: https://pypi.org/project/customtkinter/0.3/, url: https://customtkinter.tomschimansky.com/

Example script below:
import TitleBarCTk as tb
import customtkinter as ctk

def save_like_this():
    print("Saving file")
    
def change_text():
    window_frame.titlebar_text_variable.set("Goodbye, World!")

root = ctk.CTk()

window_frame = tb.WindowFrame(root,
                           height = 20,
                           non_maximised_width=1600,
                           non_maximised_height=900,
                           save_function=save_like_this,
                           title="Eat my dolphin shorts",
                           fg_color=["#ffffff", "#000000"],
                           start_fullscreen=False,
                           font=("helvetica", 20),
                           icon_path="path_to_icon.ico",
                           text_variable="Hello, World!")

window_frame.pack(side="top", fill="x")

root.after(2000, change_text)

root.mainloop()