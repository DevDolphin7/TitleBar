pip install titlebarctk

Create a custom title bar for a windows app developed with custom tkinter.

--------------------------------------------------
import titlebarctk as tb
import customtkinter as ctk

def save_like_this():
    print("Saving file")
    
def change_text():
    window_frame.titlebar_text_variable.set("Goodbye, World!")

root = ctk.CTk()

window_frame = tb.TitleBar(root,
                           height = 20,
                           non_maximised_width=1600,
                           non_maximised_height=900,
                           save_function=save_like_this,
                           title="Eat my dolphin shorts",
                           font=("helvetica", 20),
                           fg_color=["#ffffff", "#000000"],
                           start_fullscreen=False,
                           icon_path="path_to_icon.ico",
                           text_variable="Hello, World!")

window_frame.pack(side="top", fill="x")

root.after(2000, change_text)

root.mainloop()
--------------------------------------------------

Windows 10
Python 3

Install requires:
 - pywin32 306, url: https://pypi.org/project/pywin32/
 - screeninfo 0.8.1, url: https://pypi.org/project/screeninfo/
 - PIL 10.2.0, url: https://pypi.org/project/pillow/
 - customtkinter 0.3, url: https://pypi.org/project/customtkinter/0.3/, url: https://customtkinter.tomschimansky.com/

--------------------------------------------------

GitHub url: https://github.com/DevDolphin7/TitleBar
PyPI url: https://pypi.org/project/titlebarctk/
Get in contact: DevDolphin7@outlook.com
