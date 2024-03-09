from tkinter import filedialog
from tkinter import ttk
from PIL import Image
import itertools
import tkinter

def generate_binary_data(message):
    
    binary_data = []
    
    for i in message:
        bin = format(ord(i), "08b")
        binary_data.append(bin)
    
    return binary_data

def decode(path, decode_input_window):
    
    image = Image.open(path)
    image_size = image.size
    width = image_size[0]
    height = image_size[1]
    
    is_end = False
    secret_message = ""
    ascii_binary = ""
    
    for x in range(0, width):
        for y in range(0, height):
    
            if is_end == True:
                break
    
            for color in image.getpixel((x, y)):
    
                if len(ascii_binary) == 8:
                    ascii = int(ascii_binary, 2)
                    character = chr(ascii)
                    secret_message += character
                    ascii_binary = ""
                    if color % 2 == 1:
                        is_end = True    
    
                else:
                    if color % 2 == 0:
                        ascii_binary += "0"
                    else:
                        ascii_binary += "1"
    
    decode_input_window.destroy()
    
    message_window = tkinter.Toplevel()
    message_window.title("Message")
    message_window.resizable("False", "False")
    message_window.geometry("+580+125")
    message_window.tk.call("wm", "iconphoto", message_window._w, icon_image)
    
    message_label = ttk.Label(message_window, text = "The Secret Message is", font = ("Times New Roman", 18))
    secret_message_label = ttk.Label(message_window, text = secret_message, font = ("Times New Roman", 18))
    
    message_label.pack(padx = 5, pady = 5)
    secret_message_label.pack(padx = 5, pady = 5)
    
    message_window.mainloop()

def decode_input():
    
    decode_input_window = tkinter.Toplevel()
    decode_input_window.title("Decode")
    decode_input_window.geometry("+580+125")
    decode_input_window.tk.call("wm", "iconphoto", decode_input_window._w, icon_image)
    decode_input_window.resizable("False", "False")
    
    source_label = ttk.Label(decode_input_window, text = "Select Image", font = ("Times New Roman", 18))
    source_name_label = ttk.Label(decode_input_window, text = "No Image Selected", font = ("Times New Roman", 18))
    select_image_button = ttk.Button(decode_input_window, image = select_pic, command = lambda: select_image(source_name_label, "decode"))
    decode_button = ttk.Button(decode_input_window, text = "Decode", command = lambda: decode(file_path, decode_input_window), style = "my.TButton")
    
    source_label.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    source_name_label.grid(row = 1, column = 0, padx = 5)
    select_image_button.grid(row = 1, column = 1, padx = 5)
    decode_button.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5)
    
    decode_input_window.mainloop()

def save_image(image, save_image_window):
    
    loc = filedialog.asksaveasfile() 
    image.save(loc.name)
    save_image_window.destroy()

def encode(message_entry, file_path, encode_input_window):
    
    image = Image.open(file_path)
    image_size = image.size
    width = image_size[0]
    height = image_size[1]

    message = message_entry.get()
    binary_data = generate_binary_data(message)
    num_encoded = 0
    bin_encoded = 0

    for x in range(0, width):
        for y in range(0, height):
    
            if num_encoded == len(binary_data):
                break
    
            pixel_value = image.getpixel((x, y))
            bin = binary_data[num_encoded]
            new_pixel_value = []
    
            for color in pixel_value:
                new_color = color
    
                if bin_encoded == 8:
                    num_encoded += 1
                    bin_encoded = 0
    
                    if color % 2 == 1:
                        new_color = color + 1
                    
                    if num_encoded == len(message):
                        if color % 2 == 0:
                            new_color = color - 1
                        else:
                            new_color = color
    
                else:
                    if color % 2 == 0 and bin[bin_encoded] == '1':
                        new_color = color - 1
                
                    if color % 2 == 1 and bin[bin_encoded] == '0':
                        new_color = color + 1
                    bin_encoded += 1
    
                new_pixel_value.append(new_color)
            image.putpixel((x, y), tuple(new_pixel_value))
    
    encode_input_window.destroy()
    
    save_image_window = tkinter.Toplevel()
    save_image_window.title("Save image")
    save_image_window.geometry("+490+175")
    save_image_window.resizable("False", "False")
    save_image_window.tk.call("wm", "iconphoto", save_image_window._w, icon_image)
    
    info_label = ttk.Label(save_image_window, text = "Message has been successfully encoded", font = ("Times New Roman", 16))
    save_button = ttk.Button(save_image_window, text = "Save encoded image", command = lambda: save_image(image, save_image_window), style = "my.TButton")
    
    info_label.pack(padx = 5, pady = 5)
    save_button.pack(padx = 5, pady = 5)
    
    save_image_window.mainloop()
    
def select_image(file_label, type):

    global file_path
    image_extensions = ["avif", "jpg", "jpeg", "png", "svg"]
    image_extensions_cases = []
    
    for extension in image_extensions:
        chars = ((char.lower(), char.upper()) for char in extension)
        for letters in itertools.product(*chars):
            image_extensions_cases.append('*.' + ''.join(letters))
    
    file_types = [('test files', image_extensions_cases), ('All files', '*'),]
    file_path = filedialog.askopenfilename(title = "Select image to " + type, filetypes = file_types)
    file_name = file_path.split("/")[-1]
    
    if file_name != "":
        file_label.config(text = file_name)

def encode_input():

    encode_input_window = tkinter.Toplevel()
    encode_input_window.title("Encode")
    encode_input_window.geometry("+440+125")
    encode_input_window.resizable("False", "False")
    encode_input_window.tk.call("wm", "iconphoto", encode_input_window._w, icon_image)
    
    message_label = ttk.Label(encode_input_window, text = " " * 2 + "Secret Message" + " " * 4, font = ("Times New Roman", 16))
    message_entry = ttk.Entry(encode_input_window, width = 25, font = ("Times New Roman", 16))
    source_label = ttk.Label(encode_input_window, text = "Select Image", font = ("Times New Roman", 16))
    source_name_label = ttk.Label(encode_input_window, text = "No Image Selected", font = ("Times New Roman", 16))
    select_image_button = ttk.Button(encode_input_window, image = select_pic, command = lambda: select_image(source_name_label, "encode"))
    encode_button = ttk.Button(encode_input_window, text = "Encode", command = lambda: encode(message_entry, file_path, encode_input_window), style = "my.TButton")
    
    message_label.grid(row = 0, column = 0)
    message_entry.grid(row = 0, column = 1, padx = 5, pady = 5, columnspan = 2)
    source_label.grid(row = 1, column = 0, pady = 5)
    source_name_label.grid(row = 1, column = 1, pady = 5)
    select_image_button.grid(row = 1, column = 2, pady = 5)
    encode_button.grid(row = 2, column = 1, pady = 5)
    
    encode_input_window.mainloop()

def my_info():
    
    info_window = tkinter.Toplevel()
    info_window.geometry("+240+370")
    info_window.title("Credit")
    info_window.resizable("False", "False")
    info_window.tk.call("wm", "iconphoto", info_window._w, icon_image)

    ttk.Label(info_window, text = "SUNNY KUMAR", font = ("Times New Roman", 22)).pack(padx = 10)
    ttk.Label(info_window, text = "B Tech in CSE", font = ("Times New Roman", 20)).pack(padx = 10)
    ttk.Label(info_window, text = "Chandigarh University", font = ("Times New Roman", 18)).pack(padx = 10)
    ttk.Label(info_window, text = "2021-2025", font = ("Times New Roman", 16)).pack(padx = 10)
    
    info_window.mainloop()

window = tkinter.Tk()

icon_image = tkinter.PhotoImage(file = "Icon.png")
select_pic = tkinter.PhotoImage(file = "Add Image.png")
style = ttk.Style()
style.configure("my.TButton", font = ("Times New Roman", 18))

window.title("Image Steganography")
window.resizable("False", "False")
window.geometry("+530+360")
window.call("wm", "iconphoto", window._w, icon_image)

my_info_button = ttk.Button(window, text = "Credit", command = my_info, style = "my.TButton")
encode_button = ttk.Button(window, command = encode_input, style = "my.TButton")
decode_button = ttk.Button(window, command = decode_input, style = "my.TButton")
exit_button = ttk.Button(window, text = "Exit", command = window.destroy, style = "my.TButton")

encode_button["text"] = "Encode  message  into  image"
decode_button["text"] = "Decode  message  from  image"

my_info_button.pack(padx = 5)
encode_button.pack(padx = 5)
decode_button.pack(padx = 5)
exit_button.pack(padx = 5)

window.mainloop()