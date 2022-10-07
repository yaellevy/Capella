import os
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(0)
import scipy.stats
os.system('color')
import matplotlib
import datetime as dt

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *

import cnav
from cnav import Sight, Sight_session, Sight_Reduction
import pyperclip as pc
import re
from tabulate import tabulate

from ttkwidgets.autocomplete import AutocompleteCombobox
from skyfield.api import Angle, utc
import numpy as np
import geomag as gm

from collections import Counter



LARGE_FONT = ("Gotham", 35)
SMALL_FONT = ('Gotham', 11)
style.use("ggplot")


class Capella(tk.Tk):
    # _init_ function for class Capella
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # create a container
        container = ttk.Frame()
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # configure appearance
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_width = screen_width / 2
        app_height = screen_width / 1.68
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2.2) - (app_height / 2)
        self.geometry(f'{int(app_width)}x{int(app_height)}+{int(x)}+{int(y)}')
        #transparency
        self.attributes('-alpha', 0.97)
        ttk.Style("darkly")

        tk.Tk.wm_title(self, "Capella")

        # Add menu bar to top
        menubar = ttk.Menu(container)
        filemenu = ttk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load Sights from Clipboard", command=lambda: load_sights_from_clipboard(), accelerator='Ctrl+l')
        filemenu.add_separator()
        filemenu.add_command(label="Save Sights to Clipboard", command=lambda: save(), accelerator='Ctrl+s')
        filemenu.add_separator()

        # liability pop-up message box
        message = "This program is intended for educational purposes only.\n\nYou accept the following: \nTHE " \
                  "SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT " \
                  "LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND " \
                  "NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, " \
                  "DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, " \
                  "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. " \
                  "\nCopyright A.Spradling 2022 "
        Messagebox.ok(title='About', message=message)

        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple of the different page layouts
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    """Main Menu with buttons to reach other pages"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Capella", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        wrapper1 = ttk.LabelFrame(self, text='Menu')
        wrapper1.pack(padx=10, pady=10)

        # sight entry page
        button4 = ttk.Button(wrapper1, text="Sight Entry",
                             command=lambda: controller.show_frame(PageFour), bootstyle='warning-outline')
        button4.pack(pady=50, padx=50)
        button4.configure(width=20)

        # lop plot page
        button3 = ttk.Button(wrapper1, text="LOP Plot",
                             command=lambda: controller.show_frame(PageThree), bootstyle='warning-outline')
        button3.pack(pady=50, padx=50)
        button3.configure(width=20)

        # fit slope page
        button2 = ttk.Button(wrapper1, text="Fit Slope Analysis",
                             command=lambda: controller.show_frame(PageTwo), bootstyle='warning-outline')
        button2.pack(pady=50, padx=50)
        button2.configure(width=20)

        # planning/session page
        button = ttk.Button(wrapper1, text="Planning/Session Data",
                            command=lambda: controller.show_frame(PageOne), bootstyle='warning-outline')
        button.pack(pady=50, padx=50)
        button.configure(width=20)

        # Azimuth page
        button5 = ttk.Button(wrapper1, text="Azimuth",
                             command=lambda: controller.show_frame(PageFive), bootstyle='warning-outline')
        button5.pack(pady=50, padx=50)
        button5.configure(width=20)

class PageOne(tk.Frame, Sight):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # date
        plan1 = ttk.StringVar()
        # time
        plan2 = ttk.StringVar()
        # lat
        plan3 = ttk.StringVar()
        # long
        plan4 = ttk.StringVar()

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10)

        wrapper1 = ttk.LabelFrame(self, text='Sight Data')
        wrapper2 = ttk.LabelFrame(self, text='Analytics')
        wrapper3 = ttk.Labelframe(self, text='Sight Planning')
        wrapper3.pack(fill='both', expand='yes', padx=20, pady=10)

        wrapper1.pack(fill='both', expand='yes', padx=20, pady=10)
        wrapper2.pack(fill='y', expand='no', padx=20, pady=10)

        # Sight Analysis
        notebook = ttk.Notebook(wrapper2, bootstyle='dark')
        notebook.pack()
        # Sight Planning treeviews
        notebook2 = ttk.Notebook(wrapper3, bootstyle='dark')
        notebook2.pack()

        # Frame for Sight Planning Entry Fields

        frame = ttk.Frame(self)
        planlbl1 = ttk.Label(frame, text="Date UTC")
        planlbl1.grid(row=0, column=0, padx=5, pady=3)
        helplbl1 = ttk.Label(frame, text='1. Set DR Position, DR Time, and Course/Speed on the first page (Sight '
                                         'Entry).                                ')
        helplbl1.grid(row=0, column=6, padx=5, pady=3)
        global planent1
        planent1 = ttk.Entry(frame, textvariable=plan1, width=12)
        planent1.grid(row=0, column=2, padx=5, pady=3)
        planent1.insert(0, dt.datetime.utcnow().strftime('%Y-%m-%d'))

        planlbl2 = ttk.Label(frame, text="Time UTC")
        planlbl2.grid(row=1, column=0, padx=5, pady=3)
        helplbl2 = ttk.Label(frame, text="2. Input the approximate time you would like to plan a sight session for. "
                                         "Press Set Time.\n The DR Lat and Long on this page will update "
                                         "automatically with a new computed DR position.")
        helplbl2.grid(row=1, column=6, padx=5, pady=3)

        global planent2
        planent2 = ttk.Entry(frame, textvariable=plan2, width=12)
        planent2.grid(row=1, column=2, padx=5, pady=3)
        planent2.insert(0, dt.datetime.utcnow().strftime('%H:%M:%S'))



        planbutton1 = ttk.Radiobutton(frame, text='Set Time', command=lambda: plan(),
                                      bootstyle="info-outline-toolbutton")
        planbutton1.grid(row=3, column=2, padx=5, pady=3)

        planlbl3 = ttk.Label(frame, text="DR Lat")
        planlbl3.grid(row=5, column=0, padx=5, pady=3)
        planent3 = ttk.Entry(frame, textvariable=plan3, width=12)
        planent3.grid(row=5, column=2, padx=5, pady=3)
        helplbl3 = ttk.Label(frame,text="3. Browse the body lists to see all visible bodies as well as the optimal "
                                        "triads to create                    \n a shooting schedule                  "
                                        "                             ")
        helplbl3.grid(row=5, column=6, padx=5, pady=3)
        planlbl4 = ttk.Label(frame, text="DR Long")
        planlbl4.grid(row=6, column=0, padx=5, pady=3)
        planent4 = ttk.Entry(frame, textvariable=plan4, width=12)
        planent4.grid(row=6, column=2, padx=5, pady=3)

        def sight_data():
            for i in Sight.data_table:
                sight = i
                trv1.insert('', 'end', text='', iid=sight, values=sight)

        global trv1
        global trvanl
        global trverror

        # sight data treeview
        trv1 = ttk.Treeview(wrapper1, show='headings', height='12')
        trv1['columns'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        trv1.column(1, anchor='center', width=60)
        trv1.column(2, anchor='center', width=75)
        trv1.column(3, anchor='center', width=60)
        trv1.column(4, anchor='center', width=60)
        trv1.column(5, anchor='center', width=60)
        trv1.column(6, anchor='center', width=60)
        trv1.column(7, anchor='center', width=60)
        trv1.column(8, anchor='center', width=60)
        trv1.column(9, anchor='center', width=60)
        trv1.column(10, anchor='center', width=60)
        trv1.column(11, anchor='center', width=60)

        trv1.pack(expand='yes', fill='both')
        trv1.heading(1, text='Idx')
        trv1.heading(2, text='Body')
        trv1.heading(3, text="DR L")
        trv1.heading(4, text="DR λ")
        trv1.heading(5, text='Time')
        trv1.heading(6, text='GHA')
        trv1.heading(7, text="DEC")
        trv1.heading(8, text="AZ")
        trv1.heading(9, text="Ho")
        trv1.heading(10, text="Hc")
        trv1.heading(11, text="Int")
        ToolTip(trv1,
                "This table has sight data displayed from the Sight Reduction computed on the Sight Entry Page. The "
                "sights highlighted in green have the lowest scatter value per your observations of that body.",
                bootstyle=WARNING)

        sight_data()

        # sight analysis treeview
        trvanl = ttk.Treeview(wrapper2, show='headings', height='12')
        trvanl['columns'] = (1, 2, 3)
        trvanl.column(1, anchor='center', width=80)
        trvanl.column(2, anchor='center', width=85)
        trvanl.column(3, anchor='center', width=140)

        trvanl.pack(side=tk.BOTTOM, padx=10, pady=10, anchor='w')
        trvanl.heading(1, text='Body')
        trvanl.heading(2, text='Index')
        trvanl.heading(3, text="Time")
        notebook.add(trvanl, text='Best Sights')
        ToolTip(trvanl,
                "This table has the sights per body with the lowest scatter value. These are also highlighted in "
                "green in the table above.",
                bootstyle=WARNING)

        def sight_data():
            for i in Sight_Reduction.sight_anl_table:
                sight = i
                trvanl.insert('', 'end', text='', iid=sight, values=sight)

        # confidence interval treeview
        trverror = ttk.Treeview(wrapper2, show='headings', height='1')
        trverror.pack(side=tk.TOP, anchor='w', padx=10, pady=10)
        trverror['columns'] = (1, 2, 3, 4, 5)
        trverror.column(1, anchor='center', width=140)
        trverror.column(2, anchor='center', width=140)
        trverror.column(3, anchor='center', width=140)
        trverror.column(4, anchor='center', width=140)
        trverror.column(5, anchor='center', width=140)
        trverror.heading(1, text="N/S Err (nm) 68%")
        trverror.heading(2, text='E/W Err (nm) 68%')
        trverror.heading(3, text='N/S Err (nm) 95%')
        trverror.heading(4, text='E/W Err (nm) 95%')
        trverror.heading(5, text="Sys-Err (') ")
        notebook.add(trverror, text='Position Errors')
        ToolTip(trverror,
                "A table with the one and two Sigma errors for the fitting algorithm converted into nautical mile "
                "estimates.",
                bootstyle=WARNING)

        # times of phenomena treeview
        global trvphenom
        trvphenom = ttk.Treeview(wrapper3, show='headings', height='12')
        trvphenom['columns'] = (1, 2, 3)
        trvphenom.column(1, anchor='center')
        trvphenom.column(2, anchor='center')
        trvphenom.column(3, anchor='center')
        trvphenom.pack(side=tk.BOTTOM, padx=10, pady=10, anchor='w', expand='yes', fill='both')
        trvphenom.heading(1, text='Date GMT')
        trvphenom.heading(2, text=f'Date LMT')
        trvphenom.heading(3, text='Event')
        notebook2.add(frame, text='Planning Controls')
        notebook2.add(trvphenom, text='Time of Phenomena')

        # sight planning treeview
        global trvsightplan
        trvsightplan = ttk.Treeview(wrapper3, show='headings', height='12')
        trvsightplan['columns'] = (1, 2, 3, 4)
        trvsightplan.column(1, anchor='center', width=140)
        trvsightplan.column(2, anchor='center', width=140)
        trvsightplan.column(3, anchor='center', width=140)
        trvsightplan.column(4, anchor='center', width=140)
        trvsightplan.pack(side=tk.BOTTOM, padx=10, pady=10, anchor='w', expand='yes', fill='both')
        trvsightplan.heading(1, text='Body')
        trvsightplan.heading(2, text='Alt')
        trvsightplan.heading(3, text='Az')
        trvsightplan.heading(4, text='Mag')
        ToolTip(trvsightplan,
                'Listed bodies are between 25° and 65° of altitude at the time and DR position specified under the '
                'Planning Controls tab',
                bootstyle=WARNING)
        notebook2.add(trvsightplan, text='Body List')

        # optimized triad treeview
        global trvtriad
        trvtriad = ttk.Treeview(wrapper3, show='headings', height='12')
        trvtriad['columns'] = (1, 2, 3, 4)
        trvtriad.column(1, anchor='center', width=170)
        trvtriad.column(2, anchor='center', width=170)
        trvtriad.column(3, anchor='center', width=170)
        trvtriad.column(4, anchor='center', width=170)
        trvtriad.pack(side=tk.BOTTOM, padx=10, pady=10, anchor='w', expand='yes', fill='both')
        trvtriad.heading(1, text='Body')
        trvtriad.heading(2, text='Alt')
        trvtriad.heading(3, text='Az')
        trvtriad.heading(4, text='Mag')
        notebook2.add(trvtriad, text=f'Optimal Triads')
        ToolTip(trvtriad,
                'This is a sorted list of 3 body sets, weighted by azimuthal distribution, magnitude and altitude.',
                bootstyle=WARNING)

        sighthelptext = 'To Use: \n\n 1. Set DR Position, DR Time, and Course/Speed in Sight Entry. \n \n 2. Input ' \
                        'time you would like to plan for in Planning Controls, the DR Lat and Long on this page will ' \
                        'update automatically with a new computed DR position, or you can manually enter a position ' \
                        'if you would like. \n\n 3. Read the computed values in Body List and Optimal Triads. '
        ToolTip(notebook2, text=sighthelptext, bootstyle=WARNING)

        global phenomena
        def phenomena():
            """Refreshes the time of phenomena, sight planning and optimal triad treeviews"""
            for i in trvphenom.get_children():
                trvphenom.delete(i)
            for i in trvsightplan.get_children():
                trvsightplan.delete(i)
            for i in trvtriad.get_children():
                trvtriad.delete(i)
            try:
                latitude = cnav.Utilities.hmtstrtodecimald(t7.get(), t8.get())[0]
                longitude = cnav.Utilities.hmtstrtodecimald(t8.get(), t8.get())[1]
                # twilight and LAN times
                phenomenatimes = cnav.Utilities.time_of_phenomena(t5.get(), t6.get(), latitude, longitude, t9.get(),
                                                                  t10.get())
                for i in phenomenatimes:
                    trvphenom.insert('', 'end', text='', iid=i, values=i)
            except:
                # if DR info wasn't added...
                returntopagefour = Messagebox.show_warning('Input Error',
                                                             'DR Latitude, DR Longitude, Course and Speed need to be '
                                                             'entered on 1. Sight Entry Page')
                if returntopagefour: controller.show_frame(PageFour)

        global sight_planning
        def sight_planning(datetime, latitude, longitude):
            """Function to find all visible celestial bodies at the time requested, and sort them into weighted
            triads based on azimuth and magnitude """

            possibleobvs = []
            named_bodies = ['SunLL', 'SunUL', 'MoonLL', 'MoonUL', 'Mars', 'Venus', 'Jupiter', 'Saturn']
            named_stars = [*cnav.Sight.named_star_dict]
            options = named_bodies + named_stars

            for body in options:
                ephem = cnav.Utilities.get_GHADEC(body, datetime, latitude, longitude)
                obsv = (body, ephem[3].degrees, ephem[4].degrees, ephem[5])
                # constrain to visible bodies that are easily shot
                if 10 < obsv[1] < 65:
                    obsv = (body, cnav.Utilities.hmtstr(ephem[3].degrees), round(ephem[4].degrees), ephem[5])
                    possibleobvs.append(obsv)

            triads = []
            # iterative process to create triad groupings
            for i in range(len(possibleobvs)):
                one = possibleobvs[i]
                try:
                    for x in range(len(possibleobvs)):
                        difference = (possibleobvs[i][2] - possibleobvs[x][2]) % 360
                        if difference > 115 and difference < 130:
                            two = possibleobvs[x]
                            for y in range(len(possibleobvs)):
                                difference2 = (possibleobvs[x][2] - possibleobvs[y][2]) % 360
                                if difference2 > 115 and difference2 < 130:
                                    three = possibleobvs[y]
                                    triad = [one, two, three]
                                    triads.append(triad)
                except:
                    pass

            sorted_triads = sorted(triads, key=lambda x: (x[0][3] + x[1][3] + x[2][3]) / 3)
            triad_bodies = []
            for i in range(len(sorted_triads)):
                body_list = (sorted_triads[i][0][0], sorted_triads[i][1][0], sorted_triads[i][2][0])
                triad_bodies.append(body_list)

            seen = set()

            triad_results = []
            for lst in triads:
                current = frozenset(Counter(lst).items())
                if current not in seen:
                    triad_results.append(lst)
                    seen.add(current)

            for i in possibleobvs:
                trvsightplan.insert('', 'end', text='', iid=i, values=i)
            counter = 0

            i = 1
            while i < len(triad_results):
                triad_results.insert(i, ('-'))
                i += (1 + 1)

            for i in triad_results:
                for y in i:
                    trvtriad.insert('', 'end', text='', iid=counter, values=y)
                    counter += 1
            return

        global plan
        def plan():
            """Grabs DR info from Sight Session page and feeds to other planning functions"""
            phenomena()
            planent3.delete(0, 'end')
            planent4.delete(0, 'end')
            datetimedrstart = cnav.Utilities.datetime(t5.get(), t6.get())
            datetimedrstop = cnav.Utilities.datetime(plan1.get(), plan2.get())
            timed = dt.timedelta.total_seconds(datetimedrstop - datetimedrstart)

            course = t9.get()
            speed = t10.get()

            drlatstart = cnav.Utilities.hmtstrtodecimald(t7.get(), t8.get())[0]
            drlongstart = cnav.Utilities.hmtstrtodecimald(t8.get(), t8.get())[1]

            drlat = cnav.dr_calc(drlatstart, drlongstart, timed, float(course), float(speed)).drlatfwds
            drlong = cnav.dr_calc(drlatstart, drlongstart, timed, float(course), float(speed)).drlongfwds

            planent3.insert(0, cnav.Utilities.print_position2(drlat, latitude=True))
            planent4.insert(0, cnav.Utilities.print_position2(drlong, latitude=False))

            sight_planning(cnav.Utilities.datetime(plan1.get(), plan2.get()),
                           latitude=cnav.Utilities.hmtstrtodecimald(plan3.get(), plan4.get())[0],
                           longitude=cnav.Utilities.hmtstrtodecimald(plan3.get(), plan4.get())[1])


# Fit Slope Page
class PageTwo(ttk.Frame):
    def __init__(self, parent, controller):
        global f
        f = cnav.plt.figure(1)
        ttk.Frame.__init__(self, parent)

        cnav.plt.figure(1).set_facecolor('#222222')

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10)

        global canvas2
        canvas2 = FigureCanvasTkAgg(f, self)

        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas2, self)
        toolbar.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



class PageThree(ttk.Frame, Sight_Reduction):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # label = tk.Label(self, text=(f'{session.fixtime.strftime("%Y-%m-%d %H:%M:%S UTC")} RUNNING FIX'), font=LARGE_FONT)
        # label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))

        button1.pack(pady=10)

        cnav.plt.figure(2).set_facecolor('#222222')
        self.plot_lops()

    def plot_lops(self):
        f = cnav.plt.figure(2)
        global canvas
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        return

        controller.bind('<Control-p', reduce_sight)
        controller.bind('<Control-l', load_sights_from_clipboard)


# Sight Entry Page
class PageFour(ttk.Frame, Sight, Sight_session):
    counter = 0

    def __init__(self, parent, controller):

        f = cnav.plt.figure(2)
        ttk.Frame.__init__(self, parent)
        # home button
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage), bootstyle=OUTLINE)
        button1.pack(side=tk.TOP, anchor='n', padx=5, pady=10)

        # Body input variable
        t1 = tk.StringVar(self)
        # Hs input variable
        t2 = tk.StringVar(self)
        # Sight Date input variable
        t3 = tk.StringVar(self)
        # Sight Time input variable
        t4 = tk.StringVar(self)
        # DR Date input variable
        global t5
        t5 = tk.StringVar(self)
        # DR Time input variable
        global t6
        t6 = tk.StringVar(self)
        # DR Lat input variable
        global t7
        t7 = tk.StringVar(self)
        # DR Long input variable
        global t8
        t8 = tk.StringVar(self)
        # DR course input variable
        global t9
        t9 = tk.StringVar(self)
        # DR speed input variable
        global t10
        t10 = tk.StringVar(self)
        # index correction input variable
        t11 = tk.StringVar(self)
        # H.O.E input variable
        t12 = tk.StringVar(self)
        # temp input variable
        t13 = tk.StringVar(self)
        # barometric pressure input variable
        t14 = tk.StringVar(self)
        # fix date input variable
        t15 = tk.StringVar(self)
        # fix time input variable
        t16 = tk.StringVar(self)
        # t17 = tk.StringVar(self)
        # t20 = tk.StringVar(self)

        def update_sight():
            """Updates entry fields in 'Sight Entry' section"""
            selected = trv.focus()
            selection = trv.item(selected, 'values')
            trv.tag_configure('main', font=('Arial Bold', 10))
            trv.item(selected, text='', values=(t1.get(), t2.get(), t3.get(), t4.get()), tags=('main', 0))

            return

        global save
        def save(event=''):
            """ Saves Sight Session and Sight info from Sight List trv and Session Data section, formats it as a
            Markdown table and saves to clipboard. """
            session_array = []
            sight_array = []
            session = (
            t5.get(), t6.get(), t7.get(), t8.get(), t9.get(), t10.get(), t11.get(), t12.get(), t13.get(), t14.get(),
            t15.get(), t16.get())
            session_array.append(session)
            for record in trv.get_children():
                sight = trv.item(record, 'values')
                sight_array.append(sight)
            # create Markdown table
            session_headers = ["DR Date", "DR Time", "DR L", "DR λ", "Course", "Speed", "I.C.", "H.O.E", "Temp.",
                               "Press.", "Fix Date", "Fix Time"]
            session_copy = tabulate(session_array, headers=session_headers, tablefmt="github")
            sight_headers = ["Body", "Hs", "Date", "Time"]

            sight_copy = tabulate(sight_array, headers=sight_headers, tablefmt="github")

            copied_data = session_copy + "\n \n" + sight_copy
            pc.copy(copied_data)

            return session_copy, sight_copy

        global load_sights_from_clipboard
        def load_sights_from_clipboard(event=''):
            """loads Sight Session DR info and Sights into the Session info Sights Treeview from the clipboard"""
            try:
                # raw copied data
                copied1 = pc.paste()
                copied1 = re.sub(r" ", '', copied1)
                # split into session data chunk
                split = str(copied1.split()[2]).strip("|")

                length = len(split)
                # further slice session chunk and populate Session info text fields
                ent5.delete(0, 'end')
                ent5.insert(0, (split.split('|')[0]))
                ent6.delete(0, 'end')
                ent6.insert(0, split.split('|')[1])
                ent7.delete(0, 'end')
                ent7.insert(0, split.split('|')[2])
                ent8.delete(0, 'end')
                ent8.insert(0, split.split('|')[3])
                ent9.delete(0, 'end')
                ent9.insert(0, split.split('|')[4])
                ent10.delete(0, 'end')
                ent10.insert(0, split.split('|')[5])
                ent11.delete(0, 'end')
                ent11.insert(0, split.split('|')[6])
                ent12.delete(0, 'end')
                ent12.insert(0, split.split('|')[7])
                ent13.delete(0, 'end')
                ent13.insert(0, split.split('|')[8])
                ent14.delete(0, 'end')
                ent14.insert(0, split.split('|')[9])
                ent15.delete(0, 'end')
                ent15.insert(0, split.split('|')[10])
                ent16.delete(0, 'end')
                ent16.insert(0, split.split('|')[11])

                # clear Sight Entry treeview
                for i in trv.get_children():
                    trv.delete(i)
                # populate Sight Entry treeview
                for i in range(length):
                    try:
                        trv.tag_configure('main', font=('Arial Bold', 10))
                        trv.insert('', 'end', text='', iid=i, values=(copied1.split()[i + 5]).strip("|").split('|'),
                                   tags=('main',))
                        PageFour.counter += 1
                    except:
                        pass
            # if info is formatted incorrectly send error message
            except:
                Messagebox.show_warning('Input Error', 'Data Formatted Incorrectly')

            return
        s = ttk.Style()
        s.map('Treeview', background=[('selected', 'grey')])

        global setzd

        def setzd():
            global zd
            zd = 10
            return

        def add_new():
            avg_lbl.grid_forget()
            avg_lbl_2.grid_forget()

            try:
                if len(hsList) >= 2:
                    trv.insert('', 'end', text='', iid=PageFour.counter,
                               values=(f'{t1.get()}', f'{t2.get()}', f'{t3.get()}', f'{t4.get()}'), tags=('averaged',))
                    trv.tag_configure('averaged', background='aquamarine', foreground='black', font=('Arial Bold', 10))
                else:
                    trv.tag_configure('main', font=('Arial Bold', 10))
                    trv.insert('', 'end', text='', iid=PageFour.counter,
                               values=(f'{t1.get()}', f'{t2.get()}', f'{t3.get()}', f'{t4.get()}'), tags=('main',))
                bodies.delete(0, 'end')
                ent2.delete(0, 'end')

                PageFour.counter += 1

            except:
                trv.tag_configure('main', font=('Arial Bold', 10))
                trv.insert('', 'end', text='', iid=PageFour.counter,
                           values=(f'{t1.get()}', f'{t2.get()}', f'{t3.get()}', f'{t4.get()}'), tags=('main',))
                bodies.delete(0, 'end')
                ent2.delete(0, 'end')

                PageFour.counter += 1

            bodies.focus()

            return

        def delete_sight():

            selection = trv.selection()

            for record in selection:
                trv.delete(record)

        global reduce_sight

        def reduce_sight(event=''):
            """Strips data from Sight Entry page fields to instantiate Sight_session, Sight and Sight_Reduction
            objects """
            avg_lbl.grid_forget()
            avg_lbl_2.grid_forget()
            # get necessary session data in list
            session_data_list = (
            t5.get(), t6.get(), t7.get(), t8.get(), t9.get(), t10.get(), t11.get(), t12.get(), t13.get(), t14.get(),
            t15.get(), t16.get())
            session_str = ','.join(session_data_list)
            # instantiate Sight_session object
            global session
            session = Sight_session(session_str)

            # adds sights for reduction
            for record in trv.get_children():
                value = trv.item(record, 'values')
                value_str = ','.join(value)
                # instantiate Sight objects for each entered Sight
                sight = Sight(value_str)

            # instantiates Sight_Reduction object-calculates fix, calculates error statistics, plots LOPS
            global reduce
            reduce = Sight_Reduction(True)

            # Lop Plot/Clear for refresh - breaks zoom/pan

            canvas.draw()
            canvas2.draw()


            s = ttk.Style()

            # clear treeviews on Session Info/Planning page for refreshing
            for i in trv1.get_children():
                trv1.delete(i)
            for i in trvfix.get_children():
                trvfix.delete(i)
            for i in trverror.get_children():
                trverror.delete(i)
            for i in trvanl.get_children():
                trvanl.delete(i)
            for i in trvphenom.get_children():
                trvphenom.delete(i)
            for i in trvsightplan.get_children():
                trvsightplan.delete(i)
            for i in trvtriad.get_children():
                trvtriad.delete(i)

            s.map('Treeview', background=[('selected', 'grey')])
            best_index = []
            for i in Sight_Reduction.sight_anl_table[0]:
                sight = i
                trvanl.insert('', 'end', text='', iid=sight, values=sight)
                best_index.append(trvanl.item(i, 'values')[1])

            # enter sight data into treeview Page1
            for i in Sight.data_table:

                if i[0] in best_index:

                    trv1.tag_configure('best', background='DarkSeaGreen1', foreground='black')
                    trv1.insert('', 'end', text='', iid=i, values=i, tags=('best',))
                else:
                    trv1.insert('', 'end', text='', iid=i, values=i)

            # enter statistical error table into treeview Page4
            for i in Sight_Reduction.stats_table_2:
                item = i[0]
                trverror.insert('', 'end', text='', iid=item, values=item)

            # enter fix data into treeview Page 4
            for i in Sight_Reduction.gui_position_table:
                trvfix.tag_configure('best', background='DarkSeaGreen1', foreground='black', font=('Arial Bold', 10))
                item = i
                trvfix.insert('', 'end', text='', iid=item, values=item, tag=('best',))

            systematicerr = np.mean(Sight_Reduction.d_array)

            # get z_scores in list
            z_scores = scipy.stats.zscore(Sight_Reduction.d_array)
            # if d value(scatter) has a z-score greater than 2, it is likely erroneous
            for d in Sight_Reduction.d_array:
                if abs(z_scores[Sight_Reduction.d_array.index(d)]) > 2.0:
                    erroneous_body = Sight.body_array[Sight_Reduction.d_array.index(d)]
                    erroneous_sighttime = Sight.sight_times[Sight_Reduction.d_array.index(d)]
                    Messagebox.show_question(
                        f'{erroneous_body} observation at {erroneous_sighttime} is likely erroneous.\nCorrect the '
                        f'observation or remove from Sight List, otherwise consider fix and analysis unreliable.')

            message = f"Capella found a Constant Error (Uncorrected Index Error + Personal Error) of {np.round(systematicerr, 2)}'.\n\nWould you like to remove this error and recompute? "

            for d in Sight_Reduction.d_array:
                d_corr = d * (1 / np.var(Sight_Reduction.d_array))

            # if the systematic error is greater than .25 arc minutes, something is off
            if abs(systematicerr) >= .25:
                answer = Messagebox.show_question(message, 'Systematic Error')
                if systematicerr < 0:
                    systematicerr = abs(systematicerr / 60)
                else:
                    systematicerr = systematicerr / 60 * -1

                if answer == 'Yes':
                    # remove systematic error from each Sight
                    for i in trv.get_children():
                        body = trv.item(i, 'values')[0]
                        hs = trv.item(i, 'values')[1]
                        date = trv.item(i, 'values')[2]
                        time = trv.item(i, 'values')[3]
                        hs_deg, hs_min = hs.split('-')
                        hs = (float(hs_deg) + (float(hs_min) / 60))
                        hs = Angle(degrees=(hs))
                        hs = cnav.Utilities.hmtstr2(hs.degrees + (systematicerr))
                        trv.delete(i)
                        trv.insert('', 'end', text='', iid=i, values=(body, hs, date, time), tags=('main',))
                else:
                    pass


            phenomena()

            # Sight_session
            Sight_session.num_of_sights = 0
            Sight_session.dr_details = []
            # Sight
            Sight.data_table = []
            Sight.sight_times = []
            Sight.num_of_sights = 0
            Sight.body_array = []
            Sight.sight_az_array = []
            Sight.sight_times = []
            Sight.computedlong = []
            Sight.computedlat = []
            Sight.intercept_array = []
            Sight.ho_array = []
            Sight.dec_array_lop = []
            Sight.gha_array_lop = []
            Sight.hc_array = []
            Sight.gha_dec_array = []
            Sight.test_array_ho = []
            Sight.ho_vec_array = []
            Sight.test_array_gha = []

            # Sight_Reduction

            Sight_Reduction.gui_position_table = []
            Sight_Reduction.test_array
            Sight_Reduction.final_position_array = []
            Sight_Reduction.stats_table_2 = []
            Sight_Reduction.latx_lists = []
            Sight_Reduction.longx_lists = []

            Sight_Reduction.ho_array_rfix = []
            Sight_Reduction.time_delta_array = []
            Sight_Reduction.sight_anl_table = []
            Sight_Reduction.final_ho_array = []
            Sight_Reduction.pos_array_lop_lon = []
            Sight_Reduction.pos_array_lop_lat = []
            Sight_Reduction.d_array = []
            Sight_Reduction.ho_corrections_array = []
            Sight_Reduction.longitude_array = []
            Sight_Reduction.latitude_array = []
            Sight_Reduction.hc_timeofsight = []
            Sight_Reduction.sight_analysis_lat_time_of_sight = []
            Sight_Reduction.sight_analysis_long_time_of_sight = []
            Sight_Reduction.sight_analysis_lat_minus_one = []
            Sight_Reduction.sight_analysis_long_minus_one = []
            Sight_Reduction.sight_analysis_lat_plus_one = []
            Sight_Reduction.sight_analysis_long_plus_one = []
            Sight_Reduction.hc_minusone = []
            Sight_Reduction.hc_plusone = []
            Sight_Reduction.position_array_l = []

            # Special cases

            return

        s = ttk.Style()
        # Sight Entry page label frame wrappers
        wrapper1 = ttk.LabelFrame(self, text='Sight List')
        wrapper1.pack(fill='both', expand='yes', padx=10, pady=10)
        wrapper2 = ttk.LabelFrame(self, text='Step 1 - Session Data')
        wrapper2.pack(fill='y', anchor='c', expand='yes', padx=10, pady=10)
        wrapper3 = ttk.LabelFrame(self, text='Step 2 - Sight Entry')
        wrapper3.pack(fill='y', anchor='c', expand='yes', padx=10, pady=10)
        wrapper4 = ttk.Labelframe(self, text='Fix')
        wrapper4.pack(fill='both', expand='yes', padx=10, pady=10)

        # create Sight List treeview
        trv = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4),
                           show='headings', height='12')
        trv.pack(fill='x')
        trv.column(1, anchor='center', width=140)
        trv.column(2, anchor='center', width=140)
        trv.column(3, anchor='center', width=140)
        trv.column(4, anchor='center', width=140)
        trv.heading(1, text='Body')
        trv.heading(2, text='Hs')
        trv.heading(3, text="Date")
        trv.heading(4, text="Time ")
        s.configure('Treeview.Heading', font=('Arial Bold', 9))

        # create computer fix treeview
        trvfix = ttk.Treeview(wrapper4, show='headings', height='2')
        trvfix.pack(fill='x')
        trvfix['columns'] = (1, 2, 3, 4, 5)
        trvfix.column(1, anchor='center', width=200)
        trvfix.column(2, anchor='center', width=140)
        trvfix.column(3, anchor='center', width=140)
        trvfix.column(4, anchor='center', width=140)
        trvfix.column(5, anchor='center', width=140)
        trvfix.heading(1, text="Date")
        trvfix.heading(2, text='Computed L')
        trvfix.heading(3, text='Computed λ')
        trvfix.heading(4, text="DR L")
        trvfix.heading(5, text="DR λ")

        def check_time_format(x) -> bool:
            """Checks for hh:mm:ss format"""
            import re
            pattern = r'^([0-1]?\d|2[0-3])(?::([0-5]?\d))?(?::([0-5]?\d))?$'
            match = re.search(pattern, x)
            if match:

                return True
            else:
                return False

        def check_date_format(x) -> bool:
            """Checks for yyyy-mm-dd format"""
            import re

            pattern = r'^[0-9]{4}-(((0[13578]|(10|12))-(0[1-9]|[1-2][0-9]|3[0-1]))|(02-(0[1-9]|[1-2][0-9]))|((0[469]|11)-(0[1-9]|[1-2][0-9]|30)))$'
            match = re.search(pattern, x)
            if match:
                return True
            else:
                return False

        def check_hs_format(x) -> bool:
            """Checks for dd-mm.t format"""
            pattern = r"^([0-8][0-9]|89)+-(0?[0-9]|[1-5][0-9])\.\d"
            match = re.search(pattern, x)
            if match:

                return True
            else:
                return False

        def check_lat_format(x) -> bool:
            """Checks for dd-mm.t-N/S format"""
            pattern = r"^([0-8][0-9]|89)+-(0?[0-9]|[1-5][0-9])\.\d-[N|S]+"
            match = re.search(pattern, x)
            if match:
                return True
            else:
                return False

        def check_long_format(x) -> bool:
            """Checks for ddd-mm.t-E/W format"""
            pattern = r"^([0-1][0-9][0-9]|179)+-(0?[0-9]|[1-5][0-9])\.\d-[W|E]+"
            match = re.search(pattern, x)
            if match:
                return True
            else:
                return False

        def validate_number(x) -> bool:
            """Validates that the input is a number"""
            if x.strip('-').replace('.', '').isdigit():
                return True
            elif x == "":
                return True
            else:
                return False

        validate_number = self.register(validate_number)
        check_time_format = self.register(check_time_format)
        check_date_format = self.register(check_date_format)
        check_hs_format = self.register(check_hs_format)
        check_lat_format = self.register(check_lat_format)
        check_long_format = self.register(check_long_format)

        named_bodies = ['SunLL', 'SunUL', 'MoonLL', 'MoonUL', 'Mars', 'Venus', 'Jupiter', 'Saturn']
        named_stars = [*cnav.Sight.named_star_dict]
        options = named_bodies + named_stars

        # Sight data section
        # Input fields for celestial object
        lbl1 = ttk.Label(wrapper3, text="Body", width=10, bootstyle=LIGHT)
        lbl1.config(font=SMALL_FONT)
        lbl1.grid(row=0, column=0, padx=5, pady=3)
        bodies = AutocompleteCombobox(wrapper3, textvariable=t1, completevalues=options, width=14)
        bodies.config(font=SMALL_FONT)
        bodies['values'] = options
        bodies.grid(row=0, column=1, padx=5, pady=3)

        # Input fields for hs values, changes format if an average of multiple sights is chosen
        lbl2 = ttk.Label(wrapper3, text="Hs", width=10, bootstyle=LIGHT)
        lbl2.config(font=SMALL_FONT)
        lbl2.grid(row=1, column=0, padx=2, pady=3)
        ent2 = ttk.Entry(wrapper3, textvariable=t2, width=10, validate='focus', validatecommand=(check_hs_format, '%P'))
        ent2.config(font=SMALL_FONT)
        ent2.insert(0, 'dd-mm.t')
        ent2.grid(row=1, column=1, padx=2, pady=3)
        avg_lbl = ttk.Label(wrapper3, text="Avg. Hs")
        avg_lbl.config(font=SMALL_FONT)
        avg_lbl.configure(foreground='red')
        avg_lbl.grid(row=1, column=2, padx=2, pady=3)
        avg_lbl.grid_forget()
        ToolTip(ent2, text="dd-mm.t", bootstyle=WARNING)

        # Input fields for Sight Date values, changes format if an average of multiple sights is chosen
        lbl3 = ttk.Label(wrapper3, text="Date UTC", width=10, bootstyle=LIGHT)
        lbl3.config(font=SMALL_FONT)
        lbl3.grid(row=2, column=0, padx=2, pady=3)
        ent3 = ttk.Entry(wrapper3, textvariable=t3, width=10, validate='focus',
                         validatecommand=(check_date_format, '%P'))
        ent3.config(font=SMALL_FONT)
        ent3.grid(row=2, column=1, padx=2, pady=3)
        ToolTip(ent3, text="yyyy-mm-dd", bootstyle=WARNING)

        # Input fields for Sight Time values, changes format if an average of multiple sights is chosen
        lbl4 = ttk.Label(wrapper3, text="Time UTC", width=10, bootstyle=LIGHT)
        lbl4.config(font=SMALL_FONT)
        lbl4.grid(row=3, column=0, padx=2, pady=3)
        ent4 = ttk.Entry(wrapper3, textvariable=t4, width=10, validate='focus',
                         validatecommand=(check_time_format, '%P'))
        ToolTip(ent4, text="hh:mm:ss UTC", bootstyle=WARNING)
        ent4.config(font=SMALL_FONT)
        ent4.grid(row=3, column=1, padx=2, pady=3)
        avg_lbl_2 = ttk.Label(wrapper3, text="Avg. Time")
        avg_lbl_2.config(font=SMALL_FONT)
        avg_lbl_2.grid(row=3, column=2, padx=2, pady=3)
        avg_lbl_2.configure(foreground='red')
        avg_lbl_2.grid_forget()
        ent4.insert(0, 'hh:mm:ss')

        # Sight Session section

        # DR Date entry fields
        lbl5 = ttk.Label(wrapper2, text="DR Date UTC", width=12, bootstyle=LIGHT)
        lbl5.config(font=SMALL_FONT)
        lbl5.grid(row=2, column=0, padx=5, pady=3)
        ent5 = ttk.Entry(wrapper2, textvariable=t5, width=10, validate='focus',
                         validatecommand=(check_date_format, '%P'))
        ent5.insert(0, dt.datetime.utcnow().strftime('%Y-%m-%d'))
        ent5.config(font=SMALL_FONT)
        ent5.grid(row=2, column=1, padx=5, pady=3)
        ToolTip(ent5, text="yyyy-mm-dd", bootstyle=WARNING)

        # DR Time entry fields
        lbl6 = ttk.Label(wrapper2, text="DR Time UTC", width=12, bootstyle=LIGHT)
        lbl6.config(font=SMALL_FONT)
        lbl6.grid(row=3, column=0, padx=5, pady=3)
        ent6 = ttk.Entry(wrapper2, textvariable=t6, width=11, validate='focus',
                         validatecommand=(check_time_format, '%P'))
        ent6.config(font=SMALL_FONT)
        ent6.grid(row=3, column=1, padx=5, pady=3)
        ent6.insert(0, dt.datetime.utcnow().strftime('%H:%M:%S'))
        ToolTip(ent6, text="hh:mm:ss UTC", bootstyle=WARNING)

        # DR Lat entry fields
        lbl7 = ttk.Label(wrapper2, text="DR Lat", width=12, bootstyle=LIGHT)
        lbl7.config(font=SMALL_FONT)
        lbl7.grid(row=4, column=0, padx=5, pady=3)
        ent7 = ttk.Entry(wrapper2, textvariable=t7, width=12, validate='focus',
                         validatecommand=(check_lat_format, '%P'))
        ent7.config(font=SMALL_FONT)
        ent7.grid(row=4, column=1, padx=5, pady=3)
        ent7.insert(0, '37-45.8-N')
        ToolTip(ent7, text="dd-mm.t-N/S", bootstyle=WARNING)

        # DR Long entry fields
        lbl8 = ttk.Label(wrapper2, text="DR Long", width=12, bootstyle=LIGHT)
        lbl8.config(font=SMALL_FONT)
        lbl8.grid(row=5, column=0, padx=5, pady=3)
        ent8 = ttk.Entry(wrapper2, textvariable=t8, width=12, validate='focus',
                         validatecommand=(check_long_format, '%P'))
        ent8.config(font=SMALL_FONT)
        ent8.grid(row=5, column=1, padx=5, pady=3)
        ent8.insert(0, '122-38.4-W')
        ToolTip(ent8, text="ddd-mm.t-E/W", bootstyle=WARNING)

        # DR Course entry field
        lbl9 = ttk.Label(wrapper2, text="Course", width=12, bootstyle=LIGHT)
        lbl9.config(font=SMALL_FONT)
        lbl9.grid(row=2, column=2, padx=5, pady=3)
        ent9 = ttk.Entry(wrapper2, textvariable=t9, width=11, validate='focus', validatecommand=(validate_number, '%P'))
        ent9.config(font=SMALL_FONT)
        ent9.grid(row=2, column=3, padx=5, pady=3)
        ent9.insert(0, '000')
        ToolTip(ent9, text="ddd", bootstyle=WARNING)

        # DR Speed entry field
        lbl10 = ttk.Label(wrapper2, text="Speed kts", width=12, bootstyle=LIGHT)
        lbl10.config(font=SMALL_FONT)
        lbl10.grid(row=3, column=2, padx=5, pady=3)
        ent10 = ttk.Entry(wrapper2, textvariable=t10, width=11, validate='focus',
                          validatecommand=(validate_number, '%P'))
        ent10.config(font=SMALL_FONT)
        ent10.grid(row=3, column=3, padx=5, pady=3)
        ent10.insert(0, '0.0')

        # Index correction entry field
        lbl11 = ttk.Label(wrapper2, text="Index Corr.", width=12, bootstyle=LIGHT)
        lbl11.config(font=SMALL_FONT)
        lbl11.grid(row=4, column=2, padx=5, pady=3)
        ent11 = ttk.Entry(wrapper2, textvariable=t11, width=11, validate='focus',
                          validatecommand=(validate_number, '%P'))
        ent11.config(font=SMALL_FONT)
        ent11.grid(row=4, column=3, padx=5, pady=3)
        ent11.insert(0, '+/-m.t')
        ToolTip(ent11, text="Enter correction\n On arc = -\n Off arc = +", bootstyle=WARNING)

        # Height of eye entry field
        lbl12 = ttk.Label(wrapper2, text="H.O.E. ft", width=12, bootstyle=LIGHT)
        lbl12.config(font=SMALL_FONT)
        lbl12.grid(row=5, column=2, padx=5, pady=3)
        ent12 = ttk.Entry(wrapper2, textvariable=t12, width=11, validate='focus',
                          validatecommand=(validate_number, '%P'))
        ent12.config(font=SMALL_FONT)
        ent12.grid(row=5, column=3, padx=5, pady=3)
        ToolTip(ent12, text="ft", bootstyle=WARNING)

        # Temperature entry field - only in Celcius
        lbl13 = ttk.Label(wrapper2, text="Temp C", width=12, bootstyle=LIGHT)
        lbl13.config(font=SMALL_FONT)
        lbl13.grid(row=2, column=4, padx=5, pady=3)
        ent13 = ttk.Entry(wrapper2, textvariable=t13, width=11, validate='focus',
                          validatecommand=(validate_number, '%P'))
        ent13.config(font=SMALL_FONT)
        ent13.grid(row=2, column=5, padx=5, pady=3)
        ent13.insert(0, '10')

        # Barometric pressure entry field - only in milibars
        lbl14 = ttk.Label(wrapper2, text="Press. MB", width=12, bootstyle=LIGHT)
        lbl14.config(font=SMALL_FONT)
        lbl14.grid(row=3, column=4, padx=5, pady=3)
        ent14 = ttk.Entry(wrapper2, textvariable=t14, width=11, validate='focus',
                          validatecommand=(validate_number, '%P'))
        ent14.config(font=SMALL_FONT)
        ent14.grid(row=3, column=5, padx=5, pady=3)
        ent14.insert(0, '1010')

        # Date of fix entry field
        lbl15 = ttk.Label(wrapper2, text="Fix Date UTC", width=12, bootstyle=LIGHT)
        lbl15.config(font=SMALL_FONT)
        lbl15.grid(row=4, column=4, padx=5, pady=3)
        ent15 = ttk.Entry(wrapper2, textvariable=t15, width=11, validate='focus',
                          validatecommand=(check_date_format, '%P'))
        ent15.config(font=SMALL_FONT)
        ent15.grid(row=4, column=5, padx=5, pady=3)

        # Time of fix entry field
        lbl16 = ttk.Label(wrapper2, text="Fix Time UTC", width=12, bootstyle=LIGHT)
        lbl16.config(font=SMALL_FONT)
        lbl16.grid(row=5, column=4, padx=5, pady=3)
        ent16 = ttk.Entry(wrapper2, textvariable=t16, width=11, validate='focus',
                          validatecommand=(check_time_format, '%P'))
        ent16.config(font=SMALL_FONT)
        ent16.grid(row=5, column=5, padx=5, pady=3)
        ent16.insert(0, 'hh:mm:ss')

        seperator = ttk.Separator(wrapper3, orient=HORIZONTAL)

        # Add Sight to Sight Field treeview
        add_btn = ttk.Button(wrapper3, text="Add", command=add_new, bootstyle=OUTLINE)
        add_btn.config(width=12)
        ToolTip(add_btn, text="Adds Sight to Sight Entry Field", bootstyle=WARNING)
        up_btn = ttk.Button(wrapper3, text="Update", command=update_sight, bootstyle=OUTLINE)
        up_btn.config(width=12)
        ToolTip(up_btn,
                text="To Update a Sight Entry: \n 1. Click on sight in Sight Entry table. The Sight details will "
                     "populate in the step 2 area.\n 2. Make any changes and click Update.",
                bootstyle=WARNING)

        # Delete Sight from Sight Field treeview
        delete_btn = ttk.Button(wrapper3, text="Delete", command=delete_sight, bootstyle=OUTLINE)
        delete_btn.config(width=12)
        ToolTip(delete_btn,
                text="To Delete a Sight Entry: \n 1. Click on sight in Sight Entry table. You can shift select as "
                     "many sights as you'd like to delete. \n 2. Press Delete.",
                bootstyle=WARNING)

        # button to call reduce_sight function
        compute_btn = ttk.Button(wrapper4, text="COMPUTE FIX", command=reduce_sight, bootstyle='warning-outline')
        ToolTip(compute_btn, text="Ctrl+p", bootstyle=WARNING)
        # arrange buttons in grid
        seperator.grid(row=4, column=0, pady=10, columnspan=10)
        add_btn.grid(row=5, column=0, padx=10, pady=10)
        up_btn.grid(row=5, column=1, padx=10, pady=10)
        delete_btn.grid(row=5, column=2, padx=5, pady=3)
        compute_btn.pack(side=tk.BOTTOM, anchor='center', padx=10, pady=10)
        compute_btn.configure(width=20)

        def print_element(event):
            """Click on a Sight in the Sight Field treeview and the Sight Entry input box values will change
            respectively """
            trv = event.widget
            selected = trv.focus()
            selection = trv.item(selected, 'values')

            bodies.delete(0, 'end')
            ent2.delete(0, 'end')
            ent3.delete(0, 'end')
            ent4.delete(0, 'end')
            bodies.insert(0, selection[0])
            ent2.insert(0, selection[1])
            ent3.insert(0, selection[2])
            ent4.insert(0, selection[3])

            # Sight Averaging

            selection = trv.selection()
            datetimeList = []
            global hsList
            hsList = []
            for record in selection:
                # time averaging
                values = trv.item(record, 'values')
                year, month, day = values[2].split('-')
                hour, minute, second = values[3].split(':')
                sight_dt_obj = dt.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
                datetimeList.append(sight_dt_obj)
                avgTime = dt.datetime.strftime(dt.datetime.fromtimestamp(
                    sum(map(dt.datetime.timestamp, datetimeList)) / len(datetimeList)), "%H:%M:%S")
                avgDate = dt.datetime.strftime(dt.datetime.fromtimestamp(
                    sum(map(dt.datetime.timestamp, datetimeList)) / len(datetimeList)), "%Y-%m-%d")

                # hs averaging
                hs_deg, hs_min = values[1].split('-')
                hs = (float(hs_deg) + (float(hs_min) / 60))
                hs = Angle(degrees=(hs))
                hsList.append(hs.degrees)

                hs_avg = cnav.Utilities.hmtstr2(np.mean(hsList))

                ent2.delete(0, 'end')
                ent3.delete(0, 'end')
                ent4.delete(0, 'end')
                ent2.insert(0, hs_avg)
                ent3.insert(0, avgDate)
                ent4.insert(0, avgTime)

                if len(hsList) >= 2:
                    avg_lbl.grid(row=1, column=2, padx=2, pady=3)
                    avg_lbl_2.grid(row=3, column=2, padx=2, pady=3)
                else:
                    avg_lbl.grid_forget()
                    avg_lbl_2.grid_forget()

        def insert_characters(event):
            """Inserts - or : or . spacers characters inbetween typed values for faster and more accurate data input.
            Parameters
            ----------
            sight time : hh:mm:ss, inserts(:)
            dr time : hh:mm:ss, inserts(:)
            fix time : hh:mm:ss, inserts(:)
            hs : dd-mm.t, inserts(-) and (.)

            """
            time_variables = t4.get() or t6.get() or t16.get()
            # hs
            if len(t2.get()) == 2:
                ent2.insert(3, f'-')
            if len(t2.get()) == 5:
                ent2.insert(5, f'.')
            # Sight Time
            if len(t4.get()) == 2:
                ent4.insert(3, f':')
            if len(t4.get()) == 5:
                ent4.insert(5, f':')
            # dr time
            if len(t6.get()) == 2:
                ent6.insert(3, f':')
            if len(t6.get()) == 5:
                ent6.insert(5, f':')
            # fix time
            if len(t16.get()) == 2:
                ent16.insert(3, f':')
            if len(t16.get()) == 5:
                ent16.insert(5, f':')

            planent2.delete(0, 'end')
            planent2.insert(0, t6.get())

        def insert_position_characters(event):
            """Inserts - or . spacer characters into lat/long values. Additionally, formats N/S/E/W suffix """

            # Latitude
            if len(t7.get()) == 2:
                ent7.insert(3, f'-')
            if len(t7.get()) == 5:
                ent7.insert(5, f'.')
            if len(t7.get()) == 7:
                ent7.insert(7, f'-')

            # autocorrects lower cases
            try:
                if len(t7.get()) == 9 and t7.get()[-1] == 'n' or t7.get()[-1] == 's':

                    if t7.get()[-1] == 'n':
                        ent7.delete(8)
                        ent7.insert(9, 'N')
                    else:
                        ent7.delete(8)
                        ent7.insert(9, 'S')
            except:
                pass

            # Longitude
            if len(t8.get()) == 3:
                ent8.insert(4, f'-')
            if len(t8.get()) == 6:
                ent8.insert(6, f'.')
            if len(t8.get()) == 8:
                ent8.insert(8, f'-')

            # autocorrects lower cases
            try:
                if len(t8.get()) == 10 and t8.get()[-1] == 'e' or t8.get()[-1] == 'w':

                    if t8.get()[-1] == 'e':
                        ent8.delete(9)
                        ent8.insert(10, 'E')
                    else:
                        ent8.delete(9)
                        ent8.insert(10, 'W')
            except:
                pass

        def update_dates(event):
            if len(t5.get()) == 4:
                ent5.insert(5, f'-')

            if len(t5.get()) == 7:
                ent5.insert(8, f'-')

            ent3.delete(0, 'end')
            ent3.insert(0, t5.get())

            ent15.delete(0, 'end')
            ent15.insert(0, t5.get())

            planent1.delete(0, 'end')
            planent1.insert(0, t5.get())

        trv.bind("<<TreeviewSelect>>", print_element)
        ent2.bind('<KeyRelease>', insert_characters, add='+')
        ent4.bind('<KeyRelease>', insert_characters, add='+')
        ent5.bind('<KeyRelease>', update_dates)
        ent6.bind('<KeyRelease>', insert_characters)
        ent7.bind('<KeyRelease>', insert_position_characters)
        ent8.bind('<KeyRelease>', insert_position_characters)
        ent16.bind('<KeyRelease>', insert_characters)
        controller.bind('<Control-l>', load_sights_from_clipboard)
        controller.bind('<Control-s>', save)
        controller.bind('<Control-p>', reduce_sight)


class PageFive(ttk.Frame, Sight):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack(padx=5, pady=10)

        azwrap = ttk.LabelFrame(self, text='Compass Observations Records')
        azwrap2 = ttk.LabelFrame(self, text='Observation Input')

        azwrap.pack(fill='x', expand='yes', padx=10, pady=10)
        azwrap2.pack(fill='y', expand='no', padx=10, pady=100, anchor='n')

        az1 = tk.StringVar(self)
        az2 = tk.StringVar(self)
        az3 = tk.StringVar(self)
        az4 = tk.StringVar(self)
        az5 = tk.StringVar(self)
        az6 = tk.StringVar(self)
        az7 = tk.StringVar(self)
        az8 = tk.StringVar(self)
        az9 = tk.StringVar(self)

        def compass_correction():

            year, month, day = az3.get().split('-')
            hour, minute, second = az4.get().split(':')
            datetimeaz = dt.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), tzinfo=utc)

            deg, minutes, direction = az5.get().split('-')
            latitude = (float(deg) + (float(minutes) / 60)) * (-1 if direction in 'S' else 1)
            deg, minutes, direction = az6.get().split('-')
            longitude = (float(deg) + (float(minutes) / 60)) * (-1 if direction in 'W' else 1)

            body = az1.get()

            if body == 'Pier Hdg':
                Messagebox.show_warning('Input Error', 'Enter Pier Heading')

            ephem = cnav.Utilities.get_GHADEC(body, datetimeaz, latitude, longitude)

            az = ephem[4]

            gyro_hd = float(az2.get())
            std_hd = float(az7.get())
            gyro_az = float(az8.get())
            variation = float(gm.declination(latitude, longitude, 0))

            gyro_error = np.round(float(gyro_az - az.degrees), 2)

            if gyro_error < 0:
                gyro_error_str = f'{abs(gyro_error)} E'
            else:
                gyro_error_str = f'{abs(gyro_error)} W'
            deviation = gyro_hd - gyro_error - variation - std_hd

            com_error = variation + deviation
            com_az = 0

            az_date = datetimeaz.strftime("%Y-%m-%d")
            az_time = datetimeaz.strftime("%H-%M-%S")
            az_lat = cnav.Utilities.print_position(latitude, latitude=True)
            az_lon = cnav.Utilities.print_position(longitude, latitude=False)

            if variation < 0:
                var_str = f'{np.round(abs(variation), 1)} W'
            else:
                var_str = f'{np.round(abs(variation), 1)} E'

            if deviation < 0:
                dev_str = f'{np.round(abs(deviation), 1)} W'
            else:
                dev_str = f'{np.round(abs(deviation), 1)} E'

            if com_error < 0:
                com_error_str = f'{np.round(abs(com_error), 1)} W'
            else:
                com_error_str = f'{np.round(abs(com_error), 1)} E'

            for i in trvaz.get_children():
                trvaz.delete(i)
            trvazstr = [az_date, az_time, az_lat, az_lon, gyro_hd, std_hd, np.round(az.degrees, 1), gyro_az, body,
                        gyro_error_str, com_error_str, var_str, dev_str]

            trvaz.insert('', 'end', text='', iid=0, values=trvazstr)

            return

        named_bodies = ['Pier Hdg', 'SunLL', 'SunUL', 'MoonLL', 'MoonUL', 'Mars', 'Venus', 'Jupiter', 'Saturn']
        named_stars = [*cnav.Sight.named_star_dict]
        options = named_bodies + named_stars

        # Sight data section
        azlbl1 = ttk.Label(azwrap2, text="Body", width=10)
        azlbl1.grid(row=0, column=0, padx=5, pady=3)
        azbodies = AutocompleteCombobox(azwrap2, textvariable=az1, completevalues=options, width=14)
        azbodies['values'] = options
        azbodies.grid(row=0, column=1, padx=5, pady=3)

        azlbl2 = ttk.Label(azwrap2, text="Gryo Hd", width=10)
        azlbl2.grid(row=1, column=0, padx=2, pady=3)
        azent2 = ttk.Entry(azwrap2, textvariable=az2, width=10)
        azent2.insert(0, '300')
        azent2.grid(row=1, column=1, padx=2, pady=3)

        azlbl2 = ttk.Label(azwrap2, text="Mag Hd", width=10)
        azlbl2.grid(row=2, column=0, padx=2, pady=3)
        azent2 = ttk.Entry(azwrap2, textvariable=az7, width=10)
        azent2.insert(0, '300')
        azent2.grid(row=2, column=1, padx=2, pady=3)

        azlbl2 = ttk.Label(azwrap2, text="Gyro Obsv.", width=10)
        azlbl2.grid(row=3, column=0, padx=2, pady=3)
        azent2 = ttk.Entry(azwrap2, textvariable=az8, width=10)
        azent2.insert(0, '300')
        azent2.grid(row=3, column=1, padx=2, pady=3)

        # azlbl2 = ttk.Label(azwrap2, text="Comp. Obsv.", width=10)
        # azlbl2.grid(row=4, column=0, padx=2, pady=3)
        # azent2 = ttk.Entry(azwrap2, textvariable=az9, width=10)
        # azent2.insert(0, '300')
        # azent2.grid(row=4, column=1, padx=2, pady=3)

        azlbl3 = ttk.Label(azwrap2, text="Date UTC", width=10)
        azlbl3.grid(row=0, column=3, padx=2, pady=3)
        azent3 = ttk.Entry(azwrap2, textvariable=az3, width=10)
        azent3.grid(row=0, column=4, padx=2, pady=3)
        azent3.insert(0, dt.datetime.utcnow().strftime('%Y-%m-%d'))

        azlbl4 = ttk.Label(azwrap2, text="Time UTC", width=10)
        azlbl4.grid(row=1, column=3, padx=2, pady=3)
        azent4 = ttk.Entry(azwrap2, textvariable=az4, width=10)
        azent4.grid(row=1, column=4, padx=2, pady=3)
        azent4.insert(0, dt.datetime.utcnow().strftime('%H:%M:%S'))

        azlbl6 = ttk.Label(azwrap2, text="DR Lat", width=12)
        azlbl6.grid(row=2, column=3, padx=5, pady=3)
        azent5 = ttk.Entry(azwrap2, textvariable=az5, width=11)
        azent5.grid(row=2, column=4, padx=5, pady=3)

        azlbl5 = ttk.Label(azwrap2, text="DR Long", width=12)
        azlbl5.grid(row=3, column=3, padx=5, pady=3)
        azent6 = ttk.Entry(azwrap2, textvariable=az6, width=11)
        azent6.grid(row=3, column=4, padx=5, pady=3)

        compute_btn = ttk.Button(azwrap2, text="COMPUTE", command=compass_correction)
        compute_btn.grid(row=6, column=0, padx=5, pady=10)
        compute_btn.configure(width='12')

        trvaz = ttk.Treeview(azwrap, show='headings', height='12')
        trvaz.pack(padx=10)
        trvaz['columns'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
        trvaz.column(1, anchor='center', width=67)
        trvaz.column(2, anchor='center', width=60)
        trvaz.column(3, anchor='center', width=60)
        trvaz.column(4, anchor='center', width=64)
        trvaz.column(5, anchor='center', width=47)
        trvaz.column(6, anchor='center', width=48)
        trvaz.column(7, anchor='center', width=48)
        trvaz.column(8, anchor='center', width=48)
        trvaz.column(9, anchor='center', width=48)
        trvaz.column(10, anchor='center', width=54)
        trvaz.column(11, anchor='center', width=54)
        trvaz.column(12, anchor='center', width=54)
        trvaz.column(13, anchor='center', width=50)

        trvaz.heading(1, text="Date")
        trvaz.heading(2, text='G.M.T.')
        trvaz.heading(3, text='L')
        trvaz.heading(4, text="λ")
        trvaz.heading(5, text="G Hd")
        trvaz.heading(6, text="C Hd")
        trvaz.heading(7, text="T Brg")
        trvaz.heading(8, text="G Brg")
        # trvaz.heading(9, text="C Brg")
        trvaz.heading(9, text="Obj")
        trvaz.heading(10, text="G Err")
        trvaz.heading(11, text="C Err")
        trvaz.heading(12, text="Var")
        trvaz.heading(13, text="Dev")

        # formats times as hh:mm:ss

        def insert_characters(event):
            # Sight Time
            if len(az4.get()) == 2:
                azent4.insert(3, f':')
            if len(az4.get()) == 5:
                azent4.insert(5, f':')

        def update_dates(event):
            if len(azent3.get()) == 4:
                azent3.insert(5, f'-')
            if len(azent3.get()) == 7:
                azent3.insert(8, f'-')

        def insert_position_characters(event):

            # Latitude
            if len(az5.get()) == 2:
                azent5.insert(3, f'-')
            if len(az5.get()) == 5:
                azent5.insert(5, f'.')
            if len(az5.get()) == 7:
                azent5.insert(7, f'-')

            # auto corrects lower cases
            try:
                if len(az5.get()) == 9 and az5.get()[-1] == 'n' or az5.get()[-1] == 's':

                    if az5.get()[-1] == 'n':
                        azent5.delete(8)
                        azent5.insert(9, 'N')
                    else:
                        azent5.delete(8)
                        azent5.insert(9, 'S')
            except:
                pass

            # Longitude
            if len(az6.get()) == 3:
                azent6.insert(4, f'-')
            if len(az6.get()) == 6:
                azent6.insert(6, f'.')
            if len(az6.get()) == 8:
                azent6.insert(8, f'-')

            # auto corrects lower cases
            try:
                if len(az6.get()) == 10 and az6.get()[-1] == 'e' or az6.get()[-1] == 'w':

                    if az6.get()[-1] == 'e':
                        azent6.delete(9)
                        azent6.insert(10, 'E')
                    else:
                        azent6.delete(9)
                        azent6.insert(10, 'W')
            except:
                pass

        azent3.bind('<KeyRelease>', update_dates)
        azent4.bind('<KeyRelease>', insert_characters)
        azent5.bind('<KeyRelease>', insert_position_characters)
        azent6.bind('<KeyRelease>', insert_position_characters)


class about(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Capella", font=LARGE_FONT, bootstyle=LIGHT)
        label.pack(pady=10, padx=10)

        wrapper1 = ttk.LabelFrame(self, text='Menu', bootstyle=LIGHT)
        wrapper1.pack(padx=10, pady=10)


if __name__ == '__main__':
    app = Capella("Capella")
    app.mainloop()




