import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import subprocess
from PIL import Image, ImageTk
from model_inputs import ModelInputs, inputs_instance


def validate_date(date_text, format):
    try:
        datetime.strptime(date_text, format)
        return True
    except ValueError:
        return False

def validate_provinces(provinces):
    valid_provinces = {'AB', 'BC', 'SK'}
    input_provinces = set(provinces.split(','))
    return input_provinces.issubset(valid_provinces)

def validate_horizontal(horizontal):
    return horizontal in {'True', 'False', 'Both'}

def validate_gor(gor_text):
    try:
        value = float(gor_text)
        return value >= 0
    except ValueError:
        return False

def validate_date_ym(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m')
        return True
    except ValueError:
        return False

def submit_data():
    global inputs_instance  # Refer to the module-level variable
    drilled_after = drilled_after_entry.get()
    drilled_before = drilled_before_entry.get()
    provinces = provinces_entry.get()
    formations = formations_entry.get()
    horizontal = horizontal_entry.get()
    min_gor = min_gor_entry.get()
    max_gor = max_gor_entry.get()
    # start_date = start_date_entry.get()
    # end_date = end_date_entry.get()

    if not validate_date(drilled_after, '%d/%m/%Y'):
        messagebox.showerror("Input Error", "Drilled After Date is not in the correct format (DD/MM/YYYY).")
        return
    if not validate_date(drilled_before, '%d/%m/%Y'):
        messagebox.showerror("Input Error", "Drilled Before Date is not in the correct format (DD/MM/YYYY).")
        return
    if not validate_provinces(provinces):
        messagebox.showerror("Input Error", "Provinces of Interest must be AB, BC, and/or SK.")
        return
    if not validate_horizontal(horizontal):
        messagebox.showerror("Input Error", 'Horizontal Well must be "True", "False", or "Both".')
        return
    if not validate_gor(min_gor):
        messagebox.showerror("Input Error", "Minimum First 12 month Ave GOR must be a non-negative number.")
        return
    if not validate_gor(max_gor):
        messagebox.showerror("Input Error", "Maximum First 12 month Ave GOR must be a non-negative number.")
        return
    # if not validate_date_ym(start_date):
    #     messagebox.showerror("Input Error", "Start Date is not in the correct format (YYYY-MM).")
    #     return
    # if not validate_date_ym(end_date):
    #     messagebox.showerror("Input Error", "End Date is not in the correct format (YYYY-MM).")
    #     return

    # Create an instance of ModelInputs and store the data
    inputs_instance = ModelInputs(
        drilled_after, drilled_before, provinces, formations, horizontal,
        min_gor, max_gor
        # , start_date, end_date
    )

    # Display the stored data for verification
    messagebox.showinfo("Model Inputs", str(inputs_instance))

def open_formations_list():
    subprocess.run(["open", "runfiles/list_of_producing_formations.txt"])

app = tk.Tk()
app.title("Canadian Oilfield Environmental Assessment Model")

# Load the image
image_path = "schulich-engineering.png" 
original_image = Image.open(image_path)
resized_image = original_image.resize((255, 100), Image.LANCZOS) # Resize image
photo = ImageTk.PhotoImage(resized_image)

image_label = tk.Label(app, image=photo)
image_label.grid(row=0, column=0, columnspan=3)

tk.Label(app, text="Enter a Drilled After Date (DD/MM/YYYY):").grid(row=1)
tk.Label(app, text="Enter a Drilled Before Date (DD/MM/YYYY):").grid(row=2)
tk.Label(app, text="Enter provinces of interest separate by a comma (,)\n(AB,BC and SK available):").grid(row=3)
tk.Label(app, text='Enter formations of Interest (separate by , )\nClick "Search" for a complete list of formations:').grid(row=4)
tk.Label(app, text="Horizontal Well? (True, False or Both):").grid(row=5)
tk.Label(app, text="Enter a Minimum First 12 month Ave GOR (m3/m3):").grid(row=6)
tk.Label(app, text="Enter a Maximum First 12 month Ave GOR (m3/m3):").grid(row=7)
# tk.Label(app, text="Enter the Start Date (YYYY-MM):").grid(row=8)
# tk.Label(app, text="Enter the End Date (YYYY-MM):").grid(row=9)

drilled_after_entry = tk.Entry(app)
drilled_before_entry = tk.Entry(app)
provinces_entry = tk.Entry(app)
formations_entry = tk.Entry(app)
horizontal_entry = tk.Entry(app)
min_gor_entry = tk.Entry(app)
max_gor_entry = tk.Entry(app)
# start_date_entry = tk.Entry(app)
# end_date_entry = tk.Entry(app)

drilled_after_entry.insert(0, "01/05/2016")
drilled_before_entry.insert(0, "01/09/2016")
provinces_entry.insert(0, "AB")
formations_entry.insert(0, "Cambrian,Kcard_ss,Dduvernay,Delk_pt,Dleduc")
horizontal_entry.insert(0, "Both")
min_gor_entry.insert(0, "100")
max_gor_entry.insert(0, "1000")

drilled_after_entry.grid(row=1, column=1)
drilled_before_entry.grid(row=2, column=1)
provinces_entry.grid(row=3, column=1)
formations_entry.grid(row=4, column=1)
horizontal_entry.grid(row=5, column=1)
min_gor_entry.grid(row=6, column=1)
max_gor_entry.grid(row=7, column=1)
# start_date_entry.grid(row=8, column=1)
# end_date_entry.grid(row=9, column=1)

tk.Button(app, text='Search', command=open_formations_list).grid(row=4, column=2, padx=10)
tk.Button(app, text='Submit', command=submit_data).grid(row=10, column=1, pady=4)

app.mainloop()
