from procedure_data_tool.utils.docwriter import DocWriter 
import procedure_data_tool.utils.excelData as ex
import procedure_data_tool.utils.graph as gr
from procedure_data_tool.utils.valve3 import Valve3
from procedure_data_tool.utils.split import Split
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedStyle

import os

def process_route(route):
    route_with_dvi = []
    for element in route:
        element.setPosition(route)
        route_with_dvi.append(element)
        if type(element) == Valve3 or type(element) == Split:
            route_with_dvi.extend(element.getDVI())
    return route_with_dvi

def find_routes(source, destination, alts = 1):
    return components[source].routesTo(components[destination], alts)

def create_route_options():
    global route_s
    global route_d
    route_d = []
    try:
        alts = int(alternatives.get())
    except ValueError:
        messagebox.showwarning("Warning", "Valid number of alternatives not specified, showing shortest route available.")
    route_s= find_routes(source.get(), destination.get(), alts) 
    for route in route_s:
        route_d.append(process_route(route))
    refresh_listbox()

def refresh_listbox():
    listbox.delete(0, tk.END)
    for i in range(len(route_s)):
        listbox.insert(tk.END, f"Option {i+1}: {route_s[i][0].ein} to {route_s[i][-1].ein}. {len(route_s[i])} Components")

def preview_graph(event):
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        if index<len(route_s):
            gr.makeGraph(components, route_d[index], route_s[index], graphing_algorithm)

def make_doc():
    src = source.get()
    dst = destination.get()
    writer = DocWriter(src + " to " + dst + " draft procedure data:")
    filename = src +"_to_"+ dst + ".docx"
    writer.buildDocument(route_s[listbox_index], route_d[listbox_index], pits)
    try:
        writer.save(filename)
        os.system(f'start {filename}')
    except PermissionError as e:
        if e.errno == 13:
            messagebox.showerror("Error", f"The file '{filename}' might be open or in use. Please close the file and try again.")
        else:
            raise

def src_filter(*args):
    query = src_entry.get().lower() 
    src_dropdown['menu'].delete(0, tk.END)
    for node in displayed_nodes:
        if node:
            if (query in node.lower() and (components[node].in_tank or show_all.get())):
                src_dropdown['menu'].add_command(label=node, command=tk._setit(source, node))

def dst_filter(*args):
    query = dst_entry.get().lower() 
    dst_dropdown['menu'].delete(0, tk.END)
    for node in displayed_nodes:
        if node:
            if (query in node.lower() and (components[node].in_tank or show_all.get())):
                dst_dropdown['menu'].add_command(label=node, command=tk._setit(destination, node))

def browse_file(*args):
    filename = filedialog.askopenfilename(defaultextension="xlsx", title = "Select Procedure Data Excel file")
    return filename

def load_new_file(*args):
    new_file_path = None
    try:
        new_file_path = browse_file()
        if (new_file_path):
            header_message.set("Using data from: "+ new_file_path)
            components, pits =  ex.importComponents(new_file_path)
    except:
        messagebox.warning("Warning", "File not supported")
        return

def main():
    window = tk.Tk()
    window.title("Waste Transfer Procedure Tool")
    style = ThemedStyle(window)
    style.set_theme("breeze")
    global file_path
    file_path = '//hanford/data/sitedata/WasteTransferEng/Waste Transfer Engineering/1 Transfers/1C - Procedure Review Tools/MasterProcedureData.xlsx'
    global components
    global pits 
    try: 
        components, pits =  ex.importComponents(file_path)
    except Exception as e:
        filewarning ="Unable to find file at:\n\n" + file_path + "\n\n Please browse for Excel data file"
        messagebox.showwarning("Warning", filewarning)
        components, pits =  ex.importComponents(browse_file())
    
    global displayed_nodes 
    displayed_nodes = components.keys()
    
    def toggle_boolean(*args):
        src_filter()
        dst_filter()
    #######################################################################################################################
    row_index = 0
    current_dir = os.path.dirname(__file__)
    logo_path = os.path.join(current_dir, "utils", "WRPS-new-logo.png")
    logo = tk.PhotoImage(file=logo_path)
    logo_small = logo.subsample(12,12)
    logo_label = ttk.Label(window, image = logo_small)
    logo_label.grid(row= row_index, column = 0, sticky= "w", padx= 15)
    row_index += 1
    sep = tk.ttk.Separator(window, orient='horizontal')
    sep.grid(row = row_index, column = 4, sticky="e", columnspan = 4)
    row_index += 1
    #######################################################################################################################
    row_index += 1
    global header_message 
    header_message = tk.StringVar()
    header_message.set("Using data from: "+ file_path)
    label3 = ttk.Label(window, textvariable = header_message, wraplength=500, anchor="w", justify= "left")
    label3.grid(row = row_index, columnspan=3, rowspan=1, padx=15, pady=10,sticky = "w")
    file_button = ttk.Button(window, text= "Or use a different file", command=lambda: load_new_file())
    file_button.grid(row = row_index, column = 3, padx= 15, pady=10)
    row_index += 1
    sep = tk.ttk.Separator(window, orient='horizontal')
    sep.grid(row = row_index, column = 0,sticky="ew", columnspan = 4)
    row_index += 1
    #######################################################################################################################
    global show_all
    show_all = tk.BooleanVar(value=False)
    # checkbox = ttk.Checkbutton(window, text="Make all components available for selection (valves, nozzles, etc)", variable=show_all, command = toggle_boolean, anchor = "w")
    checkbox = ttk.Checkbutton(window, text="Make all components available for selection (valves, nozzles, etc)", variable=show_all, command = toggle_boolean)
    checkbox.grid(row=row_index, column=0, padx=15, sticky="w")

    row_index += 1
    #######################################################################################################################
    label0 = ttk.Label(window, text="1. Select source tank (eg. PUMP):")
    label0.grid(row=row_index, column= 0, pady = 2, padx=15,sticky = "w")
    global src_entry
    s = tk.StringVar(window, value= "AP01A-")
    src_entry = ttk.Entry(window, textvariable=s)
    src_entry.grid(row=row_index, column= 2, pady=5, padx=15, sticky="w")
    global source
    source = tk.StringVar(window)
    global src_dropdown
    src_dropdown = ttk.OptionMenu(window, source, *displayed_nodes)
    src_dropdown.grid(row=row_index, column= 3, pady=2, padx=15, sticky="w")

    row_index += 1
    #######################################################################################################################
    label1 = ttk.Label(window, text="2. Select receiving tank (eg. TKR):")
    label1.grid(row=row_index, column= 0, pady = 2, padx=15, sticky = "w")
    global dst_entry
    dst_entry = ttk.Entry(window)
    dst_entry.grid(row=row_index, column= 2, pady=15, padx=15, sticky="w")
    global destination
    destination = tk.StringVar(window)
    global dst_dropdown
    dst_dropdown = ttk.OptionMenu(window, destination, *displayed_nodes)
    dst_dropdown.grid(row=row_index, column= 3, pady=2, padx=15, sticky="w")

    row_index += 1
    #######################################################################################################################
    find_routes_button = ttk.Button(window, text="3. Generate route options", command=lambda: create_route_options())
    find_routes_button.grid(row=row_index, column= 0, padx=13, pady=10, sticky= "w")
    label2 = ttk.Label(window, text="Alternatives needed (optional):")
    label2.grid(row=row_index, column= 2, padx=6, sticky= 'e')
    global alternatives 
    alternatives = ttk.Entry(window, width= 7)
    alternatives.insert(0, "1") 
    alternatives.grid(row=row_index, column= 3, padx=15, sticky='w')

    row_index += 1
    sep = tk.ttk.Separator(window, orient='horizontal')
    sep.grid(row = row_index, column = 0,sticky="ew", columnspan = 4)

    row_index += 1
    #######################################################################################################################
    label3 = ttk.Label(window, text="4. Click on a route option to preview graph")
    label3.grid(row=row_index, column= 0, padx=15, sticky= "w")
    global listbox
    global listbox_index
    listbox_index = 0
    listbox = tk.Listbox(window, height=4)
    listbox.grid(row=row_index, column= 1, columnspan=5, sticky="we", padx=15, pady=15, rowspan=2)

    row_index +=1
    #######################################################################################################################
    global graphing_algorithm 
    graphing_algorithm = tk.StringVar(window)
    graphing_algorithm.set(value="Zig-zag")
    label4 = ttk.Label(window, text="Graph style (optional): ")
    label4.grid(row=row_index, column= 0, padx=18, sticky= "w")
    algorithm_dropdown = ttk.OptionMenu(window, graphing_algorithm, "Zig-zag", "Pyramid", "Arch")
    algorithm_dropdown.grid(row=row_index, column= 0, columnspan=1, padx=20 )
    
    row_index += 1
    #######################################################################################################################
    make_document_button = ttk.Button(window, text="5. Generate procedure development doc", command=lambda: make_doc())
    make_document_button.grid(row=row_index, column= 0, padx = 13, pady=15, sticky="w")
    
    listbox.bind("<<ListboxSelect>>", preview_graph)
    src_entry.bind("<KeyRelease>", src_filter)
    dst_entry.bind("<KeyRelease>", dst_filter)
    src_filter()
    dst_filter()
    source.set(value="AP03A-PUMP")
    destination.set(value="AY01A-TKR-D")

    window.mainloop()

if __name__== '__main__':   
    main()
