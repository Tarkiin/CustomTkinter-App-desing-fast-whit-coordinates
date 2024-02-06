import customtkinter as ctk
from tkinter import Tk, Toplevel

class DraggableElement:
    def __init__(self, master, element_type, text="", on_release_callback=None, **kwargs):
        self.master = master
        self.text = text  # Store text for later use
        if element_type == ctk.CTkTextbox:
            self.element = element_type(master, **kwargs)
        else:
            self.element = element_type(master, text=text, font=("Arial", 16, "bold"), **kwargs)
        self.element.bind("<Button-1>", self.start_drag)
        self.element.bind("<B1-Motion>", self.on_drag)
        self.element.pack(pady=10, padx=10)
        self.on_release_callback = on_release_callback

    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag(self, event):
        x = self.element.winfo_x() + (event.x - self.drag_start_x)
        y = self.element.winfo_y() + (event.y - self.drag_start_y)
        self.element.place(x=x, y=y)

    def stop_drag(self, event):
        if self.on_release_callback:
            self.on_release_callback(self)

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Draggable Elements App - TarkinSoft - 05/02/2024")
        self.geometry("800x600")
        self.draggable_elements = []

        self.add_draggable_element(ctk.CTkButton, "Button 1")
        self.add_draggable_element(ctk.CTkButton, "Button 2")
        self.add_draggable_element(ctk.CTkButton, "Button 3")
        self.add_draggable_element(ctk.CTkButton, "Button 4")
        self.add_draggable_element(ctk.CTkLabel, "Label 1", place_kwargs={"anchor": "center"})
        self.add_draggable_element(ctk.CTkLabel, "Label 2 mas largo", place_kwargs={"anchor": "center"})
        self.add_draggable_element(ctk.CTkTextbox, "", place_kwargs={"width": 200, "height": 100, "anchor": "nw"},
                                   element_kwargs={"wrap": "word"})

        print_button = ctk.CTkButton(self, text="Imprimir", font=("Arial", 16, "bold"), corner_radius=10, fg_color="#FF5733", command=self.print_element_positions)
        print_button.place(x=10, y=10)

    def add_draggable_element(self, element_type, text, place_kwargs={}, element_kwargs={}):
        if element_type == ctk.CTkTextbox:
            element_kwargs["width"] = 450  # Cambia el ancho a 400
            element_kwargs["height"] = 250  # Cambia la altura a 200
        element = DraggableElement(self, element_type, text, self.on_element_release, **element_kwargs)
        self.draggable_elements.append(element)

    def on_element_release(self, draggable_element):
        draggable_element.stop_drag(None)

    def print_element_positions(self):
        for element in self.draggable_elements:
            relx = element.element.winfo_x() / self.winfo_width()
            rely = element.element.winfo_y() / self.winfo_height()
            try:
                relwidth = element.element.winfo_width() / self.winfo_width()
                relheight = element.element.winfo_height() / self.winfo_height()
                print(f"{element.text if element.text else 'CTkTextbox'} position: relx={relx:.2f}, rely={rely:.2f}, relwidth={relwidth:.2f}, relheight={relheight:.2f}")
            except:
                print(f"{element.text} position: relx={relx:.2f}, rely={rely:.2f}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
