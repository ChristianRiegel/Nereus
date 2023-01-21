# Nereus
Often enough data files with data tables reach us and all we want is to get a quick glance at the data, at potential correlations, and/or if the data even contains the data we expect it to be. Getting such an overview requires scripting or (for people preferring working with GUIs) multiple steps in spreadsheet software. In the latter case, even a simple histogram takes time. Nereus is aimed at being a fast lane.

## Nereus - What does it do?
Nereus is a simple (pandas and seaborn based) python tool to open and plot csv files via a tkinter GUI. Before opening a data file, the separator and decimal sign can be chosen to easily open data files created with different localisations. Currently, datetime string formats can not yet be specified and are interpreted by default via the pandas package.

Since Nereus aimes to provide a fast ans easy glance into data, the produced plots are not refined or polished:
* The header of the data is used to create axis labels.
* Data selection aside from data sets is not supported.
* No diagram title can be given.

# Usage

## Required packages

Nereus is to be used with python3
* tkinter
* sys
* pandas
* seaborn
* matplotlib
* tabulate

## Execution

( 1 ) Specify decimal sign and separator

( 2 ) Open data file

( 3 ) The first ten rows as imported are displayed. Correct decimal sign or separator if necessary and open data again.

( 4 ) Select plot type in the drop-down menu (default: Histogram)

( 5 ) Open plot options for the selected plot type

( 6 ) Select plot options and plot :)

(>6 ) Repeat steps 4-6 for the same file, if desired

# Improvements planned for the future

* "Install packages" script / dialog
* Implementation of further useful plot types
* Better histogram style for more than one data set
* More elaborate output in the GUI terminal
* Clean up GUI, then clean up code
* Checkboxes for pairplot plot option

# License
MIT License

Copyright (c) 2023 Christian Riegel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Contact

Christian Riegel - Nereus.Software[at]mailbox.org
