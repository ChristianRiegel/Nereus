#############################################
# Program Nereus.py
# Nereus was the son of Pontus and Gaia and was believed to be the god of the fish.
# Open CSV data by selecting decimal sign and separator char,
# Plot different seaborn plot types
# Version 0.3
# January 21, 2023
#############################################
import tkinter.filedialog as fd
import tkinter as tk
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate

## Global variables
version = 'v0.4'
df_container = {'df':pd.DataFrame(), 'valid_file_read_in':False, 'df_numeric_columns':[], 'df_object_columns':[], 'separator':"", 'decimal':""}
gui_container = {'dict_explanation_text_en':{
    'Histogram':'A Histogram displays the distribution of a single variable X. Numeric values should be chosen. By selecting a column of discrete labels for data sets (e.g. Countries), distributions for all values in this set are drawn in different colours. The number of bins is automatically chosen unless specified.',
    'Countplot':'A Countplot displays the total count of each value in a data column X. Category values should be chosen. By selecting a column of discrete labels for data sets (e.g. Countries), distributions for all values in this set are drawn in different colours.',
    'Pairplot':'A Pairplot displays an NxN grid if the data contains N columns with numeric values.The grid then contains histograms on the diagonal and correlations plots on the off-diagonal spaces. No X-column or Y-column need to be specified. By selecting a column of discrete labels for data sets(e.g. Countries), distributions for all values in this set are drawn in different colours.',
    'Jointplot':'A Jointplot displays X-Y value pairs and in addition the projected distributions of both X and Y. By selecting a column of discrete labels for data sets (e.g. Countries), distributions for all values in this set are drawn in different colours.',
    'Boxplot':'A Boxplot displays the distribution of a variable Y horizontally. By selecting a column of discrete labels for X data sets (e.g. Countries), distributions for all values in this set are drawn. A second column of discrete labels can be selected as data sets.',
    'Lmplot':'An Lmplot displays the correlation between two variables X and Y. A linear correlation is calculated and added. By selecting a column of discrete labels for data sets (e.g. Countries), distributions for all values in this set are drawn in different colours.',
    'Violinplot':'A Violinplot displays the distribution of a variable Y horizontally. By selecting a column of discrete labels for X data sets (e.g. Countries), distributions for all values in this set are drawn. A second column of discrete labels can be selected as data sets.'}}

def plot_selected():
    global gui_container
    global df_container

    plot_type = var_plottype.get()
    x_header_name = gui_container['var_column_x'].get()
    y_header_name = gui_container['var_column_y'].get()
    hue_column  = gui_container['var_column_hue'].get()

    n_bins = 'auto'
    if gui_container['entry_bins'].get().isdigit():
        if int(gui_container['entry_bins'].get()) > 0:
            n_bins = int(gui_container['entry_bins'].get())

    if (x_header_name == 'None' and plot_type in ['Boxplot','Violinplot']):
        x_header_name = None
        pass
    elif plot_type in ['Pairplot']:
        pass
    elif x_header_name not in df_container['df'].columns.values:
        print_to_terminal("X Column "+x_header_name+" not found in data.")
        return
    if y_header_name not in df_container['df'].columns.values:
        print_to_terminal("Y Column "+y_header_name+" not found in data.")
        return

    if(hue_column== "None"):
        hue_column = None
    elif(hue_column not in df_container['df'].columns.values):
        print_to_terminal("Hue Column "+hue_column+" not found in data.")

    # Debug, later to be added in plot window
    gui_container['bool_common_norm'] = False
    gui_container['bool_normalise'] = False
    gui_container['statistic_type'] = ['count','frequency','probability','percent','percent'][0]
    gui_container['bool_normalise'] = True
    if(plot_type=='Selection'):
        pass
    elif(plot_type=='Histogram'):
        sns.histplot(data=df_container['df'], x=x_header_name, bins=n_bins, hue=hue_column, palette="bright",
        stat=gui_container['statistic_type'], common_norm=gui_container['bool_common_norm'], cumulative=gui_container['bool_normalise'])
    elif(plot_type=='Countplot'):
        sns.histplot(data=df_container['df'], x=x_header_name,hue=hue_column, palette="bright")
    elif(plot_type=='Pairplot'):
        g = sns.pairplot(data = df_container['df'], hue=hue_column, palette="bright")
        g.map_upper(plt.scatter)
        g.map_lower(sns.kdeplot)
    elif(plot_type=='Jointplot'):
        sns.jointplot(data=df_container['df'], x=x_header_name, y=y_header_name, hue=hue_column, palette="bright")
    elif(plot_type=='Boxplot'):
        sns.boxplot(data=df_container['df'], x=x_header_name, y=y_header_name, hue=hue_column, palette="bright")
    elif(plot_type=='Lmplot'):
        sns.lmplot(data=df_container['df'], x=x_header_name, y=y_header_name, hue=hue_column, palette="bright")
    elif(plot_type=='Violinplot'):
        sns.violinplot(data=df_container['df'], x=x_header_name, y=y_header_name, hue=hue_column, palette="bright")
    plt.show()

def prepare_child_window():
    global gui_container
    global df_container

    plot_type_label = var_plottype.get()

    gui_container['child_window'] = tk.Toplevel(gui_container['window'])
    gui_container['child_window'].title(plot_type_label+' window')
    gui_container['child_window'].geometry('355x180')
    gui_container['child_window'].geometry('+600+0')
    gui_container['child_window'].grab_set()
    y_position = 10

    gui_container['array_df_headers']            = df_container['df'].columns.values
    gui_container['array_df_headers_numeric']    = df_container['df_numeric_columns']
    gui_container['array_df_headers_and_None']         = ["None"]
    gui_container['array_df_headers_numeric_and_None'] = ["None"]

    for column in gui_container['array_df_headers']:
        gui_container['array_df_headers_and_None'].append(column)
    for column in gui_container['array_df_headers_numeric']:
        gui_container['array_df_headers_numeric_and_None'].append(column)

    gui_container['label_welcome'] = tk.Label(gui_container['child_window'], text = "Plot type: "+plot_type_label)
    gui_container['label_welcome'].place(x=5, y=y_position)
    y_position += 30

    gui_container['var_column_x'] = tk.StringVar()
    if(plot_type_label in ['Histogram','Countplot','Jointplot','Boxplot','Lmplot','Violinplot']):
        gui_container['label_x'] = tk.Label(gui_container['child_window'], text = "Select column as X coordinate:")
        gui_container['label_x'].place(x=5, y=y_position)
        if(plot_type_label in ['Boxplot','Violinplot']):
            gui_container['var_column_x'].set(gui_container['array_df_headers_and_None'][0])
            gui_container['optionmenu_x'] = tk.OptionMenu(gui_container['child_window'],gui_container['var_column_x'],*gui_container['array_df_headers_and_None'])
        elif(plot_type_label in ['Countplot']):
            gui_container['var_column_x'].set(gui_container['array_df_headers'][0])
            gui_container['optionmenu_x'] = tk.OptionMenu(gui_container['child_window'],gui_container['var_column_x'],*gui_container['array_df_headers'])
        else:
            gui_container['var_column_x'].set(gui_container['array_df_headers_numeric'][0])
            gui_container['optionmenu_x'] = tk.OptionMenu(gui_container['child_window'],gui_container['var_column_x'],*gui_container['array_df_headers_numeric'])
        gui_container['optionmenu_x'].place(x=205, y=y_position)
        y_position += 30

    gui_container['var_column_y'] = tk.StringVar()
    gui_container['var_column_y'].set(gui_container['array_df_headers_numeric'][0])
    if(plot_type_label in ['Jointplot','Boxplot','Lmplot','Violinplot']):
        gui_container['label_y'] = tk.Label(gui_container['child_window'], text = "Select column as Y coordinate:")
        gui_container['label_y'].place(x=5, y=y_position)
        gui_container['optionmenu_y'] = tk.OptionMenu(gui_container['child_window'],gui_container['var_column_y'],*gui_container['array_df_headers_numeric'])
        gui_container['optionmenu_y'].place(x=205, y=y_position)
        y_position += 30

    gui_container['var_column_hue'] = tk.StringVar()
    gui_container['var_column_hue'].set(gui_container['array_df_headers_and_None'][0])
    if(plot_type_label in ['Histogram','Countplot','Pairplot','Jointplot','Boxplot','Lmplot','Violinplot']):
        gui_container['label_hue'] = tk.Label(gui_container['child_window'], text = "Select column for data sets:")
        gui_container['label_hue'].place(x=5, y=y_position)
        gui_container['optionmenu_hue'] = tk.OptionMenu(gui_container['child_window'],gui_container['var_column_hue'],*gui_container['array_df_headers_and_None'])
        gui_container['optionmenu_hue'].place(x=205, y=y_position)
        y_position += 30

    gui_container['entry_bins'] = tk.Entry(gui_container['child_window'], width = 10)
    if(plot_type_label in ['Histogram']):
        gui_container['label_bins'] = tk.Label(gui_container['child_window'], text = "Number of bins (optional):")
        gui_container['label_bins'].place(x=5, y=y_position)
        gui_container['entry_bins'].place(x=205, y=y_position)
        y_position += 30

    gui_container['button_plot'] = tk.Button(gui_container['child_window'],text="Plot "+plot_type_label,command=plot_selected, height = 1, width = 15)
    gui_container['button_plot'].place(x=5, y=y_position)
    y_position += 30

    gui_container['textbox_explanation'] = tk.Message(gui_container['child_window'],anchor='nw', width=345,
    text=gui_container['dict_explanation_text_en'][plot_type_label])
    gui_container['textbox_explanation'].place(x=5,y=y_position)
    y_position +=120

    gui_container['child_window'].geometry('355x'+str(y_position))  # Height of window depends on amoount of content

def print_to_terminal(string,clear=False):
    global gui_container
    gui_container['textbox_terminal'].config(state='normal')
    if(clear):
        gui_container['textbox_terminal'].delete(1.0,'end')
    gui_container['textbox_terminal'].insert('end', string+'\n\n')
    gui_container['textbox_terminal'].config(state='disabled')

def click_button_select_file():
    global gui_container
    global df_container

    filename = fd.askopenfilename(title='Open a file',initialdir='.',filetypes=(('CSV', '*.csv'),('All files', '*.*')))
    df_container['selected_file'] = filename
    print_to_terminal("File "+filename+" selected.",True)

    gui_container['textbox_filepath'].config(state='normal')
    gui_container['textbox_filepath'].delete(1.0,'end')
    gui_container['textbox_filepath'].insert('end', filename)
    gui_container['textbox_filepath'].config(state='disabled')

def click_button_open_file():
    global gui_container
    global df_container

    df_container['df'] = None
    df_container['df_numeric_columns'] = []
    df_container['df_object_columns'] = []

    filename = df_container['selected_file']

    #filename = fd.askopenfilename(title='Open a file',initialdir='.',filetypes=(('CSV', '*.csv'),('All files', '*.*')))
    try:
        df_container['df'] = pd.read_csv(filename, sep=df_container['separator'], decimal=df_container['decimal'])
        print_to_terminal("File "+filename+" read in.",True)
        print_to_terminal("Here are the first ten rows as imported:",False)
        print_to_terminal(tabulate(df_container['df'].head(10),headers=list(df_container['df'].columns),showindex=False,tablefmt="presto"),False)
        for column in df_container['df'].columns.values:
            if df_container['df'][column].dtype.kind in 'biufcM':    # I include 'M' since DateTime should be plottable
                df_container['df_numeric_columns'].append(column)
            if df_container['df'][column].dtype.kind in 'biuOSUV':
                df_container['df_object_columns'].append(column)

        if len(df_container['df_numeric_columns']) <1:
            print_to_terminal("\nNo numerical data read in. Maybe try a different separator or decimal sign.")
            df_container['valid_file_read_in'] = False
        else:
            df_container['valid_file_read_in'] = True

    except:
       print_to_terminal("\nFile "+filename+" could not be read in.")
       df_container['valid_file_read_in'] = False

## Gui functions
def gui_init():
    global gui_container
    gui_container['radio_decimal_point'].invoke()
    gui_container['radio_separator_semicolon'].invoke()
    df_container['selected_file'] = ""

def click_button_open_plot_options():
    global df_container
    if df_container['valid_file_read_in']:
        prepare_child_window()
    else:
        print_to_terminal("\nNo numerical data read in. Maybe try a different separator or decimal sign.")

def click_button_exit():
    global gui_container
    gui_container['window'].quit()
    gui_container['window'].destroy()

def change_radio():
    global df_container
    df_container['decimal'] = var_decimal_sign.get()
    df_container['separator'] = var_separator_sign.get()

## Section defining the gui
gui_container['window'] = tk.Tk()
gui_container['window'].title('Window title')
gui_container['window'].geometry('580x750')

y_position = 5   # coordinate for vertical positioning
gui_container['message_instructions'] = tk.Message(gui_container['window'],anchor='nw', width = 580,
text="Welcome to Nereus, the CSV plotting tool!\n\nUsage:\n(1)\tSpecify decimal sign and separator below\n(2)\tSelect file\n(3)\tOpen selected file\n(4)\tThe first ten rows as imported are shown\n\tCorrect decimal sign or separator if necessary and repeat (3) and (4)\n(5)\tSelect plot type (default: Histogram)\n(6)\tOpen plot options\n(>6)\tRepeat steps 5 & 6 for the same file, if desired")
gui_container['message_instructions'].place(x=5,y=y_position)

gui_container['message_version'] = tk.Message(gui_container['window'],anchor='ne', width = 60, text=version)
gui_container['message_version'].place(x=520,y=y_position)
y_position += 200

var_decimal_sign = tk.StringVar()
var_separator_sign = tk.StringVar()

gui_container['label_decimal'] = tk.Label(gui_container['window'], text = "Decimal sign used in the CSV:")
gui_container['label_decimal'].place(x=5, y=y_position)

gui_container['radio_decimal_point'] = tk.Radiobutton(gui_container['window'], text=".", var = var_decimal_sign, value = ".", command=change_radio)
gui_container['radio_decimal_point'].place(x=205, y=y_position)

gui_container['radio_decimal_comma'] = tk.Radiobutton(gui_container['window'], text=",", var = var_decimal_sign, value = ",", command=change_radio)
gui_container['radio_decimal_comma'].place(x=255, y=y_position)
y_position += 30

gui_container['label_separator'] = tk.Label(gui_container['window'], text = "Separator used in the CSV:")
gui_container['label_separator'].place(x=5, y=y_position)

gui_container['radio_separator_semicolon'] = tk.Radiobutton(gui_container['window'], text=";", var = var_separator_sign, value = ";", command=change_radio)
gui_container['radio_separator_semicolon'].place(x=205, y=y_position)

gui_container['radio_separator_comma'] = tk.Radiobutton(gui_container['window'], text=",", var = var_separator_sign, value = ",", command=change_radio)
gui_container['radio_separator_comma'].place(x=255, y=y_position)

gui_container['radio_separator_tab'] = tk.Radiobutton(gui_container['window'], text="TAB", var = var_separator_sign, value = "\t", command=change_radio)
gui_container['radio_separator_tab'].place(x=305, y=y_position)
y_position += 30

gui_container['button_select_file'] = tk.Button(gui_container['window'],text="Select file",command=click_button_select_file, height = 1, width = 7)
gui_container['button_select_file'].place(x=5, y=y_position)

gui_container['textbox_filepath'] = tk.Text(gui_container['window'], height= 1, width=70,wrap=tk.NONE)
gui_container['textbox_filepath'].place(x=75,y=y_position)
#gui_container['textbox_filepath'].insert('end', "")
gui_container['textbox_filepath'].config(state='disabled')
y_position += 30

gui_container['button_open_file'] = tk.Button(gui_container['window'],text="Open file",command=click_button_open_file, height = 1, width = 7)
gui_container['button_open_file'].place(x=5, y=y_position)

var_plottype = tk.StringVar()
var_plottype.set("Histogram")
array_plot_types = ['Histogram','Countplot','Pairplot','Jointplot','Boxplot','Lmplot','Violinplot']

gui_container['optionmenu_plottype'] = tk.OptionMenu(gui_container['window'],var_plottype,*array_plot_types)
gui_container['optionmenu_plottype'].config( height= 1, width=13)
gui_container['optionmenu_plottype'].place(x=75, y=y_position-2)

gui_container['button_plot_options'] = tk.Button(gui_container['window'],text="Open plot options",command=click_button_open_plot_options, height = 1, width = 15, activebackground='yellow')
gui_container['button_plot_options'].place(x=230, y=y_position)

gui_container['button_exit'] = tk.Button(gui_container['window'], text = "Exit GUI", command = click_button_exit, height = 1, width = 10)
gui_container['button_exit'].place(x=375, y=y_position)
y_position += 30

gui_container['textbox_terminal'] = tk.Text(gui_container['window'], height= 20, width=80,wrap=tk.NONE)
gui_container['textbox_terminal'].place(x=5,y=y_position)
gui_container['textbox_terminal'].insert('end', "[Further text output is given here]")
gui_container['textbox_terminal'].config(state='disabled')

gui_container['xscrollbar_terminal'] = tk.Scrollbar(gui_container['window'], orient='horizontal')
gui_container['xscrollbar_terminal'].pack(side="bottom", fill="both")
gui_container['textbox_terminal'].config(yscrollcommand=gui_container['xscrollbar_terminal'].set, xscrollcommand=gui_container['xscrollbar_terminal'].set)
gui_container['xscrollbar_terminal'].config(command=gui_container['textbox_terminal'].xview)

gui_init()
gui_container['window'].mainloop()
