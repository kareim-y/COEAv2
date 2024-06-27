import tkinter as tk
from tkinter import messagebox, StringVar
from datetime import datetime
import subprocess
from PIL import Image, ImageTk
from model_inputs import ModelInputs
import pickle


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
    
def open_formations_list():
    subprocess.run(["open", "runfiles/list_of_producing_formations.txt"]) 

def open_graph_list(list_directory):
    subprocess.run(["open", list_directory]) 

def toggle_state(checkbox_var, *items):
    state = tk.NORMAL if checkbox_var.get() else tk.DISABLED
    for item in items:
        item.config(state=state)

def submit_data():
    # global inputs_instance  # Refer to the module-level variable
    # Check for main variable states
    project_name = project_name_entry.get()
    drilled_after = drilled_after_entry.get()
    drilled_before = drilled_before_entry.get()
    provinces = provinces_entry.get()
    formations = formations_entry.get()
    horizontal = horizontal_entry.get()
    min_gor = min_gor_entry.get()
    max_gor = max_gor_entry.get()
    # start_date = start_date_entry.get()
    # end_date = end_date_entry.get()

    # Get checkbox states
    prod_data_checkbox = prod_data_checkbox_entry.get()
    inject_data_checkbox = inject_data_checkbox_entry.get()
    fluid_data_checkbox = fluid_data_checkbox_entry.get()
    fluid_boxplot = fluid_boxplot_entry.get()
    pressure_DST_data_checkbox = pressure_DST_data_checkbox_entry.get()
    pressure_plot = pressure_plot_entry.get()
    pressure_gradient = pressure_gradient_entry.get()
    HF_water_checkbox = HF_water_checkbox_entry.get()
    water_plot = water_plot_entry.get()
    facility_data_checkbox = facility_data_checkbox_entry.get()
    facility_gas_prod = facility_gas_prod_entry.get()
    facility_print_AB = facility_print_AB_entry.get()
    facility_print_BC = facility_print_BC_entry.get()
    OPGEE_distribution_checkbox = OPGEE_dsitribution_entry.get()
    OPGEE_export_checkbox = OPGEE_export_entry.get()

    # get other inputs
    prod_startdate = prod_startdate_entry.get()
    prod_enddate = prod_enddate_entry.get()
    prod_graph = prod_graph_entry.get()
    prod_graph2 = prod_graph_entry2.get()

    inject_startdate = inject_startdate_entry.get()
    inject_enddate = inject_enddate_entry.get()
    inject_graph = inject_graph_entry.get()

    facility_startdate = facility_startdate_entry.get()
    facility_enddate = facility_enddate_entry.get()

    min_welltime = min_welltime_entry.get()
    min_wellprod = min_wellprod_entry.get()

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
        project_name, drilled_after, drilled_before, provinces, formations, horizontal,
        min_gor, max_gor, 
        prod_data_checkbox = prod_data_checkbox,
        prod_startdate = prod_startdate,
        prod_enddate = prod_enddate,
        prod_graph = prod_graph,
        prod_graph2 = prod_graph2,

        inject_data_checkbox = inject_data_checkbox, 
        inject_startdate = inject_startdate,
        inject_enddate = inject_enddate,
        inject_graph = inject_graph,

        fluid_data_checkbox = fluid_data_checkbox,
        fluid_boxplot = fluid_boxplot,

        pressure_DST_data_checkbox = pressure_DST_data_checkbox, 
        pressure_plot = pressure_plot,
        pressure_gradient = pressure_gradient,

        HF_water_checkbox = HF_water_checkbox, 
        water_plot = water_plot,

        facility_data_checkbox = facility_data_checkbox, 
        facility_startdate = facility_startdate,
        facility_enddate = facility_enddate,
        facility_gas_prod = facility_gas_prod,
        facility_print_AB = facility_print_AB,
        facility_print_BC = facility_print_BC,

        OPGEE_distribution_checkbox = OPGEE_distribution_checkbox, 
        OPGEE_export_checkbox = OPGEE_export_checkbox,
        min_welltime = min_welltime,
        min_wellprod = min_wellprod
        # , start_date, end_date
    )

    # Display the stored data for verification
    messagebox.showinfo("Model Inputs", str(inputs_instance))

    with open('model_input_instance.pkl', 'wb') as f:
        pickle.dump(inputs_instance, f)

    subprocess.run(["python", "Canadian_Oilfield_Environmental_Assessor.py"])
    

app = tk.Tk()
app.title("Canadian Oilfield Environmental Assessment Model")

# Creates a canvas and a scrollbar
canvas = tk.Canvas(app)
scrollbar = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Configure the scrollbar
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Load the image
image_path = "schulich-engineering.png" 
original_image = Image.open(image_path)
resized_image = original_image.resize((383, 150), Image.LANCZOS) # Resize image
photo = ImageTk.PhotoImage(resized_image)

image_label = tk.Label(scrollable_frame, image=photo)
image_label.grid(row=0, column=0, columnspan=3)

tk.Label(scrollable_frame, text="==========================================================\n\
Welcome to the Canadian Oilfield Environmental Assessor (COEA)\n\
==========================================================\n\
Data is available for wells drilled over the period Jan 2005 to Dec 2019\n\
1 - Available Data For Analysis:\n\
2 - General Well Data (AB,BC,SK)\n\
3 - Production Data (AB,BC,SK)\n\
4 - Injection Data (AB,BC,SK)\n\
5 - Hydraulic Fracturing Data (AB,BC)\n\
6 - Drill String Test (DST) Data (AB,BC,SK)\n\
7 - Oil Compositional Data (AB,BC,SK)\n\
8 - Gas Compositional Data (AB,BC,SK)\n\
9 - Facility Volumetric Data (AB,BC,SK)\n\
10 - Induced Seismicity (AB,BC)\n", font='Helvetica 16 bold').grid(row=1, column = 0, columnspan=3)

# Input Descriptions
tk.Label(scrollable_frame, text= "________________________________________________________________________________________________________________________________").grid(row=2, columnspan=3, sticky='w')
tk.Label(scrollable_frame, text="Enter Project Name", font='Helvetica 14 bold', justify='left').grid(row=3, sticky='w')
tk.Label(scrollable_frame, text="Enter a Drilled After Date (DD/MM/YYYY):", font='Helvetica 14 bold', justify='left').grid(row=4, sticky='w')
tk.Label(scrollable_frame, text="Enter a Drilled Before Date (DD/MM/YYYY):", font='Helvetica 14 bold', justify='left').grid(row=5, sticky='w')
tk.Label(scrollable_frame, text="Enter provinces of interest separate by a comma (,)\n(AB,BC and SK available):", font='Helvetica 14 bold', justify='left').grid(row=6, sticky='w')
tk.Label(scrollable_frame, text='Enter formations of Interest (separate by , )\nClick "Search" for a complete list of formations:', font='Helvetica 14 bold', justify='left').grid(row=7, sticky='w')
tk.Label(scrollable_frame, text="Horizontal Well? (True, False or Both):", font='Helvetica 14 bold', justify='left').grid(row=8, sticky='w')
tk.Label(scrollable_frame, text="Enter a Minimum First 12 month Ave GOR (m3/m3):", font='Helvetica 14 bold', justify='left').grid(row=9, sticky='w')
tk.Label(scrollable_frame, text="Enter a Maximum First 12 month Ave GOR (m3/m3):", font='Helvetica 14 bold', justify='left').grid(row=10, sticky='w')
tk.Label(scrollable_frame, text= "________________________________________________________________________________________________________________________________").grid(row=11, columnspan=3, sticky='w')
tk.Label(scrollable_frame, text= "________________________________________________________________________________________________________________________________").grid(row=18, columnspan=3, sticky='w')
tk.Label(scrollable_frame, text= "________________________________________________________________________________________________________________________________").grid(row=23, columnspan=3, sticky='w')
tk.Label(scrollable_frame, text= "________________________________________________________________________________________________________________________________").grid(row=26, columnspan=3, sticky='w')
tk.Label(scrollable_frame, text= "________________________________________________________________________________________________________________________________").grid(row=30, columnspan=3, sticky='w')
tk.Label(scrollable_frame, text= "________________________________________________________________________________________________________________________________").grid(row=33, columnspan=3, sticky='w')
tk.Label(scrollable_frame, text= "________________________________________________________________________________________________________________________________").grid(row=41, columnspan=3, sticky='w')

prod_graph_label = tk.Label(scrollable_frame, text="Choose graphs To display from the \"First Year Production Trend Analysis\"\nTo view available graphs click \"Graphs Available\" button to the right", state=tk.DISABLED, justify='left')
prod_graph_label.grid(row=13, sticky='w')
prod_assess_label = tk.Label(scrollable_frame, text="The available data set contains monthly production data for wells between Jan-2005 and Dec-2019\nFor OPGEE field assessment, adjust start date to be first drill year", state=tk.DISABLED, justify='left')
prod_assess_label.grid(row=14, sticky='w')
prod_startdate_label = tk.Label(scrollable_frame, text="Enter the Start Date (YYYY-MM)", state=tk.DISABLED, justify='left')
prod_startdate_label.grid(row=15, sticky='w')
prod_enddate_label = tk.Label(scrollable_frame, text="Enter the End Date (YYYY-MM)", state=tk.DISABLED, justify='left')
prod_enddate_label.grid(row=16, sticky='w')
prod_graph_label2 = tk.Label(scrollable_frame, text="Choose Graphs To Display from production analysis\nTo view available graphs click \"Graphs Available\" button to the right", state=tk.DISABLED, justify='left')
prod_graph_label2.grid(row=17, sticky='w')

inject_graph_label = tk.Label(scrollable_frame, text="Choose Graphs To Display from injection analysis\nTo View available graphs click \"Graphs Available\" button to the right", state=tk.DISABLED, justify='left')
inject_graph_label.grid(row=20, sticky='w')
inject_startdate_label = tk.Label(scrollable_frame, text="Enter the Start Date (YYYY-MM)", state=tk.DISABLED, justify='left')
inject_startdate_label.grid(row=21, sticky='w')
inject_enddate_label = tk.Label(scrollable_frame, text="Enter the End Date (YYYY-MM)", state=tk.DISABLED, justify='left')
inject_enddate_label.grid(row=22, sticky='w')

facility_info_label = tk.Label(scrollable_frame, text="Monthly Facility Data is Available from 2014-01 to 2019-12\nEnter The Date Range For Assessment (5-10 seconds per month)", state=tk.DISABLED, justify='left')
facility_info_label.grid(row=35, sticky='w')
facility_startdate_label = tk.Label(scrollable_frame, text="Enter the Start Date (YYYY-MM)", state=tk.DISABLED, justify='left')
facility_startdate_label.grid(row=36, sticky='w')
facility_enddate_label = tk.Label(scrollable_frame, text="Enter the End Date (YYYY-MM)", state=tk.DISABLED, justify='left')
facility_enddate_label.grid(row=37, sticky='w')

opgee_export_label = tk.Label(scrollable_frame, text="NOTE: Exclude wells to reduce/remove calculation issues in OPGEE\nOil production must be greater than 0 bbl/day for OPGEE to run", state=tk.DISABLED, justify='left')
opgee_export_label.grid(row=44, sticky='w')
min_welltime_label = tk.Label(scrollable_frame, text="Minimum well producing time (years)", state=tk.DISABLED, justify='left')
min_welltime_label.grid(row=45, sticky='w')
min_wellprod_label = tk.Label(scrollable_frame, text="Minimum oil production (bbl/day)", state=tk.DISABLED, justify='left')
min_wellprod_label.grid(row=46, sticky='w')

# tk.Label(app, text="Enter the Start Date (YYYY-MM):").grid(row=8)
# tk.Label(app, text="Enter the End Date (YYYY-MM):").grid(row=9)

# Checkboxes
prod_data_checkbox_entry = tk.BooleanVar()
inject_data_checkbox_entry = tk.BooleanVar()

fluid_data_checkbox_entry = tk.BooleanVar()
fluid_boxplot_entry = tk.BooleanVar()

pressure_DST_data_checkbox_entry = tk.BooleanVar()
pressure_plot_entry = tk.BooleanVar()
pressure_gradient_entry = tk.BooleanVar()

HF_water_checkbox_entry = tk.BooleanVar()
water_plot_entry = tk.BooleanVar()

facility_data_checkbox_entry = tk.BooleanVar()
facility_gas_prod_entry = tk.BooleanVar()
facility_print_AB_entry = tk.BooleanVar()
facility_print_BC_entry = tk.BooleanVar()

OPGEE_dsitribution_entry = tk.BooleanVar()
OPGEE_export_entry = tk.BooleanVar()

tk.Checkbutton(scrollable_frame, text="Production Data", font='Helvetica 14 bold', variable = prod_data_checkbox_entry,
            command=lambda: toggle_state(prod_data_checkbox_entry, prod_graph_label, prod_graph_label2, prod_assess_label, prod_graph_entry, 
                            prod_graph_entry2, prod_graph_button, prod_graph_button2, prod_startdate_label,  
                            prod_enddate_label, prod_startdate_entry, prod_enddate_entry)).grid(row=12, column=0, sticky='W')

tk.Checkbutton(scrollable_frame, text="Injection Data", font='Helvetica 14 bold', variable = inject_data_checkbox_entry, 
            command=lambda: toggle_state(inject_data_checkbox_entry, inject_graph_label, inject_startdate_label, inject_enddate_label,
                                        inject_graph_button, inject_graph_entry, inject_startdate_entry, inject_enddate_entry)).grid(row=19, column=0, sticky='W')

tk.Checkbutton(scrollable_frame, text="Fluid Data", font='Helvetica 14 bold', variable = fluid_data_checkbox_entry, 
            command=lambda: toggle_state(fluid_data_checkbox_entry, fluid_boxplot_checkbox)).grid(row=24, column=0, sticky='W')
fluid_boxplot_checkbox = tk.Checkbutton(scrollable_frame, text="Plot API BoxPlot", variable = fluid_boxplot_entry, state=tk.DISABLED)
fluid_boxplot_checkbox.grid(row=25, column=0, sticky='W')

tk.Checkbutton(scrollable_frame, text="Pressure/DST Data", font='Helvetica 14 bold', variable = pressure_DST_data_checkbox_entry,
            command=lambda: toggle_state(pressure_DST_data_checkbox_entry, pressure_plot_checkbox, pressure_gradient_checkbox)).grid(row=27, column=0, sticky='W')
pressure_plot_checkbox = tk.Checkbutton(scrollable_frame, text="Plot \"Max Pressure (psi)\"", variable = pressure_plot_entry, state=tk.DISABLED)
pressure_plot_checkbox.grid(row=28, column=0, sticky='W')
pressure_gradient_checkbox = tk.Checkbutton(scrollable_frame, text="Would you like to use the calculated pressure gradient? If no, the default pressure gradient is assumed (0.45 psi/ft)", 
                                        variable = pressure_gradient_entry, justify='left', state=tk.DISABLED)
pressure_gradient_checkbox.grid(row=29, column=0, sticky='W', columnspan=2)

tk.Checkbutton(scrollable_frame, text="HF Water Data", font='Helvetica 14 bold', variable = HF_water_checkbox_entry,
            command=lambda: toggle_state(HF_water_checkbox_entry, water_plot_checkbox)).grid(row=31, column=0, sticky='W')
water_plot_checkbox = tk.Checkbutton(scrollable_frame, text="Plot Total Water Usage", variable = water_plot_entry, state=tk.DISABLED)
water_plot_checkbox.grid(row=32, column=0, sticky='W')

tk.Checkbutton(scrollable_frame, text="Facility Data", font='Helvetica 14 bold', variable = facility_data_checkbox_entry,
            command=lambda: toggle_state(facility_data_checkbox_entry, facility_info_label, facility_startdate_label, facility_enddate_label, 
                                        facility_startdate_entry, facility_enddate_entry, facility_gas_prod_checkbox, facility_print_AB_checkbox, facility_print_BC_checkbox,)).grid(row=34, column=0, sticky='W')
facility_gas_prod_checkbox = tk.Checkbutton(scrollable_frame, text="Would you like to include Gas Processing Plants", variable = facility_gas_prod_entry, state=tk.DISABLED)
facility_gas_prod_checkbox.grid(row=38, column=0, sticky='W')
facility_print_AB_checkbox = tk.Checkbutton(scrollable_frame, text="Would you like a print out of each AB facility", variable = facility_print_AB_entry, state=tk.DISABLED)
facility_print_AB_checkbox.grid(row=39, column=0, sticky='W')
facility_print_BC_checkbox = tk.Checkbutton(scrollable_frame, text="Would you like to print each single BC facility", variable = facility_print_BC_entry, state=tk.DISABLED)
facility_print_BC_checkbox.grid(row=40, column=0, sticky='W')

tk.Checkbutton(scrollable_frame, text="Plot OPGEE Distribution Parameters", font='Helvetica 14 bold', variable = OPGEE_dsitribution_entry,).grid(row=42, column=0, sticky='W')

tk.Checkbutton(scrollable_frame, text="Export to OPGEE", font='Helvetica 14 bold', variable = OPGEE_export_entry,
            command=lambda: toggle_state(OPGEE_export_entry, opgee_export_label, min_welltime_label, min_wellprod_label, min_welltime_entry,
                                        min_wellprod_entry)).grid(row=43, column=0, sticky='W')

# Input Boxes
project_name_entry = tk.Entry(scrollable_frame)
drilled_after_entry = tk.Entry(scrollable_frame)
drilled_before_entry = tk.Entry(scrollable_frame)

# Drop down menu set-up
provinces_entry = StringVar(scrollable_frame)
provinces_entry.set("AB")  # Set default value
province_options = ["AB","BC", "SK", "AB,BC", "AB,SK", "BC,SK", "AB,BC,SK"]

formations_entry = tk.Entry(scrollable_frame)
horizontal_entry = tk.Entry(scrollable_frame)
min_gor_entry = tk.Entry(scrollable_frame)
max_gor_entry = tk.Entry(scrollable_frame)

prod_graph_entry = tk.Entry(scrollable_frame, state=tk.DISABLED)
prod_graph_entry2 = tk.Entry(scrollable_frame, state=tk.DISABLED)
prod_startdate_entry = tk.Entry(scrollable_frame, state=tk.DISABLED)
prod_enddate_entry = tk.Entry(scrollable_frame, state=tk.DISABLED)

inject_graph_entry = tk.Entry(scrollable_frame, state=tk.DISABLED)
inject_startdate_entry = tk.Entry(scrollable_frame, state=tk.DISABLED)
inject_enddate_entry = tk.Entry(scrollable_frame, state=tk.DISABLED)
# start_date_entry = tk.Entry(app)
# end_date_entry = tk.Entry(app)

facility_startdate_entry = tk.Entry(scrollable_frame, state=tk.DISABLED)
facility_enddate_entry = tk.Entry(scrollable_frame, state=tk.DISABLED)

min_welltime_entry = tk.Entry(scrollable_frame, state=tk.DISABLED)
min_wellprod_entry = tk.Entry(scrollable_frame, state=tk.DISABLED)

project_name_entry.insert(0, "Test Project")
drilled_after_entry.insert(0, "01/05/2016")
drilled_before_entry.insert(0, "01/09/2016")
# provinces_entry.insert(0, "AB")
formations_entry.insert(0, "Cambrian,Kcard_ss,Dduvernay,Delk_pt,Dleduc")
horizontal_entry.insert(0, "Both")
min_gor_entry.insert(0, "100")
max_gor_entry.insert(0, "1000")
prod_graph_entry.insert(0, "5")
prod_graph_entry2.insert(0, "4")
prod_startdate_entry.insert(0, "2016-01")
prod_enddate_entry.insert(0, "2016-05")
inject_startdate_entry.insert(0, "2016-01")
inject_enddate_entry.insert(0, "2016-05")
inject_graph_entry.insert(0, "3")

project_name_entry.grid(row=3, column=1)
drilled_after_entry.grid(row=4, column=1)
drilled_before_entry.grid(row=5, column=1)

# provinces_entry.grid(row=6, column=1)
# Drop down menu layout
dropdown_menu = tk.OptionMenu(scrollable_frame, provinces_entry, *province_options)
dropdown_menu.config(width=16)
dropdown_menu.grid(row=6, column=1)

formations_entry.grid(row=7, column=1)
horizontal_entry.grid(row=8, column=1)
min_gor_entry.grid(row=9, column=1)
max_gor_entry.grid(row=10, column=1)

prod_graph_entry.grid(row=13, column=1)
prod_startdate_entry.grid(row= 15, column=1)
prod_enddate_entry.grid(row= 16, column=1)
prod_graph_entry2.grid(row=17, column=1)

inject_graph_entry.grid(row=20, column=1)
inject_startdate_entry.grid(row= 21, column=1)
inject_enddate_entry.grid(row=22, column=1)
# start_date_entry.grid(row=8, column=1)
# end_date_entry.grid(row=9, column=1)

facility_startdate_entry.grid(row= 36, column=1)
facility_enddate_entry.grid(row=37, column=1)

min_welltime_entry.grid(row= 45, column=1)
min_wellprod_entry.grid(row=46, column=1)


tk.Button(scrollable_frame, text='Search', command=open_formations_list).grid(row=7, column=2, padx=10)
tk.Button(scrollable_frame, text='Submit', command=submit_data).grid(row=47, column=1, pady=4)

prod_graph_button = tk.Button(scrollable_frame, text='Graphs Available', command=lambda: open_graph_list("graphing options/production_graph_list.txt"), state=tk.DISABLED)
prod_graph_button.grid(row=13, column=2, padx=10)
prod_graph_button2 = tk.Button(scrollable_frame, text='Graphs Available', command=lambda: open_graph_list("graphing options/production_graph_list2.txt"), state=tk.DISABLED)
prod_graph_button2.grid(row=17, column=2, padx=10)

inject_graph_button = tk.Button(scrollable_frame, text='Graphs Available', command=lambda: open_graph_list("graphing options/injection_graph_list.txt"), state=tk.DISABLED)
inject_graph_button.grid(row=20, column=2, padx=10)

app.mainloop()
