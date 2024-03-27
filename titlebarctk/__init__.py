import io
import customtkinter as ctk
from ctypes import windll
from win32api import GetMonitorInfo, MonitorFromPoint
from screeninfo import get_monitors
from PIL import Image
from .dat import dat_main as data_main

__version__ = "0.1.2"

class TitleBar(ctk.CTkFrame):
    """Creates titlebar_text_variable that can be updated.
        Parameters:
        - root (CTk() object): pass root as an argument.
        - height (int, optional): Define the height of the titlebar.
        - non_maximised_width (int, optional): Define the width of the window when not maximised.
        - non_maximised_height (int, optional): Define the height of the window when not maximised.
        - title (str, optional): Define the title text to appear in the middle of the TitleBar.
        - text_variable (str, optional): Define a variable text parameter that apears on the left of the TitleBar.
        - fg_color (list, optional): Define in hex values [light, dark] colours (see custom tkinter documentation).
        - start_fullscreen (bool, optional): Define if to start in full screen.
        - icon_path (str, optional): Define the path to a .ico file, appears on the left of the TitleBar.
        - font (tuple, optional): Define (font as str, size as int) for TitleBar text (see custom tkinter documentation).
        - save_function (function, optional): Define what happens when the save button is pressed, otherwise omit save button."""

    def __init__(self, root, height=20, non_maximised_width=480, non_maximised_height=480, title="", text_variable="",
                 fg_color=["#ddf5ff", "#051419"], start_fullscreen=False, icon_path="", font=None, save_function=None) -> None:
        # Load CTk Frame
        super().__init__(root)

        # Class variables
        self.root = root
        self.dat = data_main.Data()
        self.monitors = monitors_information()
        
        # Class user inputs
        self._height = height
        self._non_maximised_width = non_maximised_width
        self._non_maximised_height = non_maximised_height
        self._title = title
        self._text_variable = text_variable
        self._fg_color = fg_color
        self._start_fullscreen = start_fullscreen
        self._icon_path = icon_path
        self._font = font
        self._create_save_button = False
        self._save_function = save_function
        if self._save_function != None: self._create_save_button = True
        self.check_user_input_types()
        
        # Show icon on windows taskbar
        self._GWL_EXSTYLE = -20
        self._WS_EX_APPWINDOW = 0x00040000
        self._WS_EX_TOOLWINDOW = 0x00000080
        self.set_appwindow()
        
        # Light & Dark colour scheme
        self.configure(fg_color=self._fg_color)

        # Create title bar       
        self.create_window_buttons()
        self.create_window_labels()
        self.position_window() 
        self.pack_widgets()
        
        # Bring user attention to software
        self.root.attributes("-topmost", True)
        self.root.attributes("-topmost", False)
        self.focus()


    def check_user_input_types(self):
        user_variables = {"height": [self._height, int],
                          "non_maximised_width": [self._non_maximised_width, int],
                          "non_maximised_height": [self._non_maximised_height, int],
                          "title": [self._title, str],
                          "text variable": [self._text_variable, str],
                          "fg_color": [self._fg_color, list],
                          "start_fullscreen": [self._start_fullscreen, bool],
                          "icon_path": [self._icon_path, str]}
        
        if self._font != None: user_variables["font"] = [self._font, tuple]
        
        for name, var_list in user_variables.items():
            if type(var_list[0]) == var_list[1]: continue
            else:
                raise TypeError(f"Variable {name} must be type {var_list[1]}, type {type(var_list[0])} was given.")
            
        if self._save_function == None: pass
        elif callable(self._save_function): pass
        else: raise TypeError(f"Variable save_function should contain the function to save the application, type {type(self._save_function)} was given.")


    def position_window(self) -> None:
        """Set the window to be in the middle of screen"""
        for properties_dict in self.monitors.values():
            if properties_dict["primary"] == True:
                self.window_width = properties_dict["x_rng"][1] - properties_dict["x_rng"][0]
                self.window_height = properties_dict["y_rng"][1] - properties_dict["y_rng"][0]

        self.define_current_monitor()

        if self._start_fullscreen:
            for _ in range(2): self.maximise()
        else:
            self.maximise()


    def create_window_buttons(self) -> None:
        self.window_buttons = {"close": {"image": "ExitClose", "command": self.exit_software},
                               "maximise": {"image": "FullScreen", "command": self.maximise},
                               "minimise": {"image": "Minimise", "command": self.minimise},
                               "save": {"image": "Save", "command": self.save}}
        
        if self._create_save_button == False: del self.window_buttons["save"]

        for button_id, properties_dict in self.window_buttons.items():
            image_data = self.dat.data(properties_dict["image"])
            image = ctk.CTkImage(load_image(image_data), size=[self._height,self._height])
            self.window_buttons[button_id] = ctk.CTkButton(self, image=image, text="", command=properties_dict["command"], fg_color=self._fg_color,
                                                           width=self._height, border_width=0, height=self._height)


    def create_window_labels(self) -> None:
        self.titlebar_text_variable = ctk.StringVar(value=self._text_variable)
        self.window_labels = {}
        
        if self._icon_path != "":
            self.window_labels["icon"] =  {"text": None, "text var": None, "image": self._icon_path, "size w,h": [self._height, self._height], "font": None}
        
        self.window_labels["status"] = {"text": None, "text var": self.titlebar_text_variable, "image": None, "size h,w": None, "font": self._font}
        self.window_labels["title"] =  {"text": self._title, "text var": None, "image": None, "size h,w": None, "font": self._font}

        for label_id, properties_dict in self.window_labels.items():
            if type(properties_dict["image"]) == str:
                properties_dict["image"] = ctk.CTkImage(load_image(self._icon_path), size=properties_dict["size w,h"])
            self.window_labels[label_id] = ctk.CTkLabel(self, height=self._height, image=properties_dict["image"], text=properties_dict["text"],
                                                        textvariable=properties_dict["text var"], font=properties_dict["font"])


    def pack_widgets(self) -> None:
        for button in self.window_buttons.values():
            button.pack(side="right")

        for name, label_widget in self.window_labels.items():
            if name != "title": label_widget.pack(side="left", padx=5)
            else: label_widget.pack(fill="x", anchor="center", pady=5)


    def configure_binds(self, label, bind=True) -> None:
        """use "all labels" to bind or "minimised" to unbind"""
        if label == "all labels" and bind:
            for widget in self.window_labels.values():
                widget.bind("<ButtonPress-1>", self.start_move_window)
                widget.bind("<ButtonRelease-1>", self.stop_move_window)
                widget.bind("<B1-Motion>", self.do_move_window)

        elif label == "all labels" and not bind:
            for widget in self.window_labels.values():
                widget.unbind("<ButtonPress-1>")
                widget.unbind("<ButtonRelease-1>")
                widget.unbind("<B1-Motion>")
        
        elif label == "minimised" and bind:
            self.root.bind('<FocusIn>', self.set_appwindow)

        elif label == "minimised" and not bind:
            self.root.unbind('<FocusIn>')

        else: raise ValueError(f"Unexpected value passed to configure_binds: label={label}, widget_id={widget}, bind={bind}")


    def exit_software(self) -> None:
        self.root.destroy()


    def maximise(self) -> None:
        if self.window_width == (self.monitor_area[2] - self.monitor_area[0]) and self.window_height == (self.monitor_area[3] - self.monitor_area[1]):
            self.root.geometry(f"{self._non_maximised_width}x{self._non_maximised_height}" \
                               f"+{int(self.monitor_area[0] + (self.window_width / 2) - (self._non_maximised_width / 2))}" \
                                f"+{int(self.monitor_area[1] + (self.window_height / 2) - (self._non_maximised_height / 2))}")
            self.window_width = self._non_maximised_width
            self.window_height = self._non_maximised_height
            self.root.resizable(True,True)
            self.configure_binds("all labels")
        else:
            self.window_width = self.monitor_area[2] - self.monitor_area[0]
            self.window_height = self.monitor_area[3] - self.monitor_area[1]
            self.root.geometry(f"{self.window_width}x{self.window_height}+{self.monitor_area[0]}+{self.monitor_area[1]}")
            self.root.resizable(False,False)
            self.configure_binds("all labels", bind=False)
        self.set_appwindow()

    
    def minimise(self) -> None:
        self.root.overrideredirect(False)
        self.root.wm_iconify()
        self.root.after(10, lambda: self.configure_binds("minimised"))

    
    def set_appwindow(self, *event) -> None:
        self.root.overrideredirect(True)
        hwnd = windll.user32.GetParent(self.root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, self._GWL_EXSTYLE)
        style = style & ~self._WS_EX_TOOLWINDOW
        style = style | self._WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, self._GWL_EXSTYLE, style)
        # re-assert the new window style
        self.root.wm_withdraw()
        self.configure_binds("minimised", bind=False)
        self.root.after(10, lambda: self.root.wm_deiconify())


    def save(self) -> None:
        self._save_function()


    def start_move_window(self, event) -> None:
        self.x = event.x
        self.y = event.y


    def stop_move_window(self, event) -> None:
        self.define_current_monitor()
        self.x = None
        self.y = None


    def do_move_window(self, event) -> None:
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    
    def define_current_monitor(self) -> None:
        for key, pixel_rng_dict in self.monitors.items():
            if (self.root.winfo_x() + (self.window_width / 2)) in range(pixel_rng_dict['x_rng'][0],pixel_rng_dict['x_rng'][1]):
                if self.root.winfo_y() in range(pixel_rng_dict['y_rng'][0],pixel_rng_dict['y_rng'][1]):
                    self.current_monitor = key
        
        self.monitor_area = (self.monitors[self.current_monitor]["x_rng"][0],
                             self.monitors[self.current_monitor]["y_rng"][0],
                             self.monitors[self.current_monitor]["x_rng"][1],
                             self.monitors[self.current_monitor]["y_rng"][1])

    
def load_image(image_bytes, resize=False, crop=False) -> object:
    """Load an image from bytes. Optionally resizes then / or crops. Parameters:
    - image_bytes (bytes): The bytes containing the image information. Uses PIL.Image
    - resize (list, optional): Expects integers [width,height]
    - crop (list, optional): Expects tuple of integers (left, top, right, bottom)"""
    if type(image_bytes) == str:
        if image_bytes[-4:] != ".ico": raise ValueError("Path provided should include .ico file type.")
        image = Image.open(image_bytes)
    else:
        b = bytearray(image_bytes)
        image = Image.open(io.BytesIO(b))
    if resize != False:
        image = image.resize((resize[0],resize[1]))
    if crop != False:
        image = image.crop(crop)
    return image


def monitors_information() -> dict:
    """Returns a dictionary of
    {monitor number:
        {"x_rng": [left-most pixel, right-most pixel],
         "y_rng": [top-most pixel, bottom-most pixel],
         "primary": bool}"""
    monitors = {}
    for count, m in enumerate(get_monitors()):
        monitor_info = GetMonitorInfo(MonitorFromPoint((m.x, m.y)))
        area = monitor_info.get("Work")
        monitors[count] = {"x_rng": [area[0], area[2]],
                           "y_rng": [area[1], area[3]],
                           "primary": m.is_primary}
    return monitors
