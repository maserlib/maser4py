#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a python viewer for the Heliophysics Feature Catalogue.
@author: Xavier Bonnin (LESIA)
"""
__version__ = "0.1"
# __license__ = "GPL"
__author__ = "Xavier BONNIN"
__credit__ = ["Xavier BONNIN"]
__maintainer__ = "Xavier BONNIN"
__email__ = "xavier.bonnin@obspm.fr"
__project__ = "HELIO"

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from tkinter import *
from tkinter import messagebox

from maser.services.helio.hfc import hfc_client
from maser.services.helio.hfc.improlib import auto_contrast, chain2image

## Constant arguments

# Background color
BG_COLOR = "#C7CBE4"

HQI_TFORMAT = "%Y-%m-%dT%H:%M:%S"
SQL_TFORMAT = "%Y-%m-%d %H:%M:%S"

DATE_PATTERN = "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"

# List for observatory radio buttons
MODES = [
    ("SDO_HMI_I", 1),
    ("SDO_HMI_M", 2),
    ("SDO_AIA", 3),
    ("SOHO_MDI_I", 4),
    ("SOHO_MDI_M", 5),
    ("SOHO_EIT", 6),
    ("NANCAY_RH", 7),
    ("MEUDON_SH_HA", 8),
    ("MEUDON_SH_K3", 9)
]


# Default input arguments
DATE = datetime.now().strftime(HQI_TFORMAT)
OBSERVATORY = "Nancay"
INSTRUMENT = "Radioheliograph"
TELESCOPE = ""
WAVENAME = ""


# Helio Interface for HFC
URL_WSDL = "http://voparis-helio.obspm.fr/hfc-hqi/HelioTavernaService?wsdl"
URL_WSDL_DEV = "http://voparis-helio.obspm.fr/hfc-hqi-dev/HelioTavernaService?wsdl"
SQL_METHOD = "SQLSelect"
OBS_HFC_TABLE = "VIEW_OBS_HQI"
PP_HFC_TABLE = "VIEW_PP_HQI"
FEATURE_TABLE = {'ar': "VIEW_AR_HQI", 'ch': "VIEW_CH_HQI", 'sp': "VIEW_SP_HQI",
               'rs': "VIEW_RS_HQI", 'pr': "VIEW_PRO_HQI", "fi": "VIEW_FIL_HQI"}

# Default colors for feature
FEATURE_COLORS = {'ar': 'r', 'ch': 'b', 'sp': 'y', 'rs' :'m' ,'pr' :'g' ,'fi' :'c'}


def input_date(date):
    return date.strftime(HQI_TFORMAT)


def sql_date(date):
    return date.strftime(SQL_TFORMAT)


class Viewer(Frame):

    def __init__(self, master=None, **kwargs):

        # Remove inputs from maser
        kwargs.pop("version", False)
        kwargs.pop("log_file", False)
        kwargs.pop("debug", False)
        kwargs.pop("quiet", False)
        kwargs.pop("maser", False)

        self.master=master
        self._date = StringVar()
        self._date.set(kwargs.pop("date"))
        self._obs = kwargs.pop("observatory",OBSERVATORY)
        self._inst = kwargs.pop("instrument",INSTRUMENT)
        self._tele = kwargs.pop("telescope",TELESCOPE)
        self._wave = kwargs.pop("wavename",WAVENAME)
        self._obsid = IntVar()
        self._obsid.set(self.__obs2id(self._obs,self._inst,telescope=self._tele,wavename=self._wave))
        self._wsdl = kwargs.pop("url_wsdl",URL_WSDL)
        self._quiet = kwargs.pop("Quiet",False)
        self._dev = kwargs.pop("Dev",False)
        if (self._dev): self._wsdl=URL_WSDL_DEV
        self._width=kwargs.pop("xsize")
        if (self._width is None):
            self._width=int(0.6*master.winfo_screenwidth())
        self._height=kwargs.pop("ysize")
        if (self._height is None):
            self._height=int(0.7*master.winfo_screenheight())

        self.master.geometry(str(self._width)+"x"+str(self._height))

        # Initialize feature set
        self._aron = IntVar() # Active regions
        self._chon = IntVar() # Coronal holes
        self._spon = IntVar() # Sunspots
        self._rson = IntVar() # NRH radio sources
        self._pron = IntVar() # Prominences
        self._fion = IntVar() # Filaments

        #if (self._feattable is None):
        #    print "Feature is unknown: %s!" % (self._feat)
        #    self.master.quit
        self._data = None
        self._image = None
        self._feat_ct = IntVar()

        Frame.__init__(self, master, **kwargs)
        self.__build_menubar()
        self.master.config(menu=self._menubar,bg= BG_COLOR)
        self.__place_widgets()

        self._feat_ct.set(0) # Initialize feature contour color table
        self._obsid.set(8) # initialize observation set
        self._obs_table = OBS_HFC_TABLE # Intialize observations table
        self.__set_date() # load and plot observation for self._date

    def __build_menubar(self):

        # menu bar
        self._menubar = Menu(self.master)
        filemenu = Menu(self._menubar, tearoff=0)
        filemenu.add_command(label="Open",command=self.__open)
        #filemenu.add_separator()
        filemenu.add_command(label="Quit",command=self.master.quit)
        self._menubar.add_cascade(label="File", menu=filemenu)

        optmenu = Menu(self._menubar, tearoff=0)
        colmenu = Menu(optmenu, tearoff=0)
        colmenu.add_radiobutton(label="Colors by tracking",variable=self._feat_ct,
                                value=1,command=self.__set_date)
        colmenu.add_radiobutton(label="Colors by feature",variable=self._feat_ct,
                                value=0,command=self.__set_date)
        optmenu.add_cascade(label="Set colors", menu=colmenu)
        self._menubar.add_cascade(label="Options", menu=optmenu)

        helpmenu = Menu(self._menubar, tearoff=0)
        helpmenu.add_command(label="Help",command=self.__show_help)
        #helpmenu.add_separator()
        helpmenu.add_command(label="About HFC Viewer", command=self.__about)
        self._menubar.add_cascade(label="Help", menu=helpmenu)

    def __place_widgets(self):

        # header frame and its widgets
        hframe = Frame(self.master,bg=BG_COLOR)

        # Date buttons
        lbtn = Button(hframe, text="Previous",
                      bg=BG_COLOR,
                      highlightbackground=BG_COLOR,
                      command=self.__prev_date)
        rbtn = Button(hframe, text="Next",
                      bg=BG_COLOR,
                      highlightbackground=BG_COLOR,
                      command=self.__next_date)
        # Date entry
        self._header = Entry(hframe,
                             highlightbackground=BG_COLOR,
                             textvariable=self._date)
        self._header.bind("<Return>", self.__date_event)

        # Image contrast slide bar
        #self._slide = Scale(hframe, from_=0, to=100,
        #                    orient=HORIZONTAL, bg=BG_COLOR)

        # Image frame
        iframe = Frame(self.master,bg=BG_COLOR)

        # the plot window frame
        self._fig = Figure(figsize=(5,4), dpi=100)
        self._plt = self._fig.add_subplot(111)

        # a tk.DrawingArea
        self._canvas = FigureCanvasTkAgg(self._fig, master=iframe)
        self._canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk( self._canvas, iframe )
        toolbar.update()

        # the option menu frame
        oframe = Frame(self.master,bg=BG_COLOR)

        # Data set buttons
        dlabel = Label(oframe,text="DATA SETS",bg=BG_COLOR)
        dframe = Frame(oframe,bg=BG_COLOR,relief=SUNKEN,bd=2)
        for text, mode in MODES:
            b = Radiobutton(dframe, text=text,
                            command=self.__set_obsid,
                            variable=self._obsid, value=mode,
                bg=BG_COLOR)
            b.pack(anchor=W)

        # Features buttons
        flabel = Label(oframe, text="FEATURES", bg=BG_COLOR)
        fframe = Frame(oframe, bg=BG_COLOR, relief=SUNKEN,bd=2)
        cb_ar = Checkbutton(fframe, text="Active regions",
                            variable=self._aron, bg=BG_COLOR,
                            command=self.__plot_qclk)
        cb_ch = Checkbutton(fframe, text="Coronal holes",
                            variable=self._chon, bg=BG_COLOR,
                            command=self.__plot_qclk)
        cb_sp = Checkbutton(fframe, text="Sunspots",
                            variable=self._spon, bg=BG_COLOR,
                            command=self.__plot_qclk)
        cb_rs = Checkbutton(fframe, text="NRH sources",
                            variable=self._rson, bg=BG_COLOR,
                            command=self.__plot_qclk)
        cb_pr = Checkbutton(fframe, text="Prominences",
                            variable=self._pron, bg=BG_COLOR,
                            command=self.__plot_qclk)
        cb_fi = Checkbutton(fframe, text="Filaments",
                            variable=self._fion, bg=BG_COLOR,
                            command=self.__plot_qclk)
        cb_ar.pack(anchor=W)
        cb_ch.pack(anchor=W)
        cb_sp.pack(anchor=W)
        cb_rs.pack(anchor=W)
        cb_pr.pack(anchor=W)
        cb_fi.pack(anchor=W)

        # pack the widgets
        hframe.pack(side='top', pady=4, anchor=CENTER)
        lbtn.grid()
        self._header.grid(column=1, row=0, padx=12)
        rbtn.grid(column=2, row=0)
        iframe.pack(expand=True, fill='both', side='left')
        oframe.pack(expand=False, fill='both', side='left')
        dlabel.pack(anchor=CENTER,ipady=2)
        dframe.pack(expand=False, fill='both', side='top')
        flabel.pack(anchor=CENTER,ipady=2)
        fframe.pack(expand=False, fill='both', side='top')
        self._canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    def __obs2id(self,observatory,instrument,
                 telescope=None,wavename=None):
        obs = observatory.lower()
        inst = instrument.lower()
        tele = telescope
        wave = wavename
        if tele is not None:
            tele = tele.lower()
        if wave is not None:
            wave = wave.lower()

        if (obs == "sdo") and (inst == "hmi"):
            if tele == "":
                return 1
            else:
                if tele == "magnetogram":
                    return 2
                else:
                    return 1
        elif (obs == "sdo") and (inst == "aia"):
            return 3
        elif (obs == "soho") and (inst == "mdi"):
            if tele == "":
                return 4
            else:
                if (tele == "magnetogram"):
                    return 5
                else:
                    return 4
        elif (obs == "soho") and (inst == "eit"):
            return 6
        elif (obs == "nancay") and (inst == "radioheliograph"):
            return 7
        elif (obs == "meudon") and (inst == "spectroheliograph"):
            if (wave == "halpha"):
                return 8
            else:
                return 9
        else:
            messagebox.showerror("ERROR","UNKNOWN OBSERVATORY/INSTRUMENT!")
            return

    def __id2obs(self,id):
        id = int(id)

        observatory = "" ; instrument = "" ; telescope = "" ; wavename = ""
        if (id == 1):
            observatory="SDO" ; instrument = "HMI" ; telescope = "Continuum"
            self._obs_table=OBS_HFC_TABLE
        elif (id == 2):
            observatory="SDO" ; instrument = "HMI" ; telescope = "Magnetogram"
            self._obs_table=OBS_HFC_TABLE
        elif (id == 3):
            observatory="SDO" ; instrument = "AIA"
            self._obs_table=OBS_HFC_TABLE
        elif (id == 4):
            observatory="SoHO" ; instrument = "MDI" ; telescope = "Continuum"
            self._obs_table=OBS_HFC_TABLE
        elif (id == 5):
            observatory="SoHO" ; instrument = "MDI" ; telescope = "Magnetogram"
            self._obs_table=OBS_HFC_TABLE
        elif (id == 6):
            observatory = "SoHO" ; instrument = "EIT"
            self._obs_table=OBS_HFC_TABLE
        elif (id == 7):
            observatory = "Nancay" ; instrument = "Radioheliograph"
            self._obs_table=OBS_HFC_TABLE
        elif (id == 8):
            observatory = "Meudon" ; instrument = "Spectroheliograph" ; wavename = "Halpha"
            self._obs_table=PP_HFC_TABLE
        elif (id == 9):
            observatory = "Meudon" ; instrument = "Spectroheliograph" ; wavename = "CAII K3"
            self._obs_table=PP_HFC_TABLE
        else:
            messagebox.showerror("ERROR","UNKNOWN OBSERVATORY ID %i!" % (id))
            return None, None, None
        return observatory, instrument, telescope, wavename

    def __set_obsid(self):
        self.__set_date()

    def __date_event(self,event):
        self.__set_date()

    def __set_date(self):
        date_obs = self._date.get()
        if (re.search(DATE_PATTERN,date_obs) is None):
            messagebox.showerror("ERROR","INPUT DATE FORMAT IS INCORRECT!")
            return False

        obs, inst, tel, wav = self.__id2obs(self._obsid.get())
        print("Loading information for the data set:")
        print("(DATE_OBS=%s, OBSERVAT=%s, INSTRUME=%s, TELESCOP=%s, WAVENAME=%s)" % (date_obs,obs,inst,tel,wav))
        date_obs = datetime.strptime(date_obs,HQI_TFORMAT)

        method=SQL_METHOD ; wsdl=self._wsdl
        WHAT="DATE_OBS, CDELT1, CDELT2, NAXIS1, NAXIS2, CENTER_X, CENTER_Y, R_SUN"
        WHAT+=", QCLK_URL, QCLK_FNAME, WAVEMIN, WAVEUNIT"
        LIMIT=1
        ORDER="ABS(UNIX_TIMESTAMP(DATE_OBS)-UNIX_TIMESTAMP(\"%s\"))" % (sql_date(date_obs))
        WHERE="(OBSERVAT=\"%s\") AND (INSTRUME=\"%s\")" % (obs,inst)
        if (tel != ""):
            WHERE+=" AND (TELESCOP=\"%s\")" % (tel)
        if (wav != ""):
            WHERE+=" AND (WAVENAME=\"%s\")" % (wav)
        FROM=self._obs_table
        self.obs_data = self.__query_hfc(method=method,wsdl=wsdl,
                                         WHAT=WHAT,WHERE=WHERE,
                                         LIMIT=1,ORDER_BY=ORDER,
                                         FROM=FROM)
        if (self.obs_data is None):
            messagebox.showerror("ERROR","Querying HFC has failed!")
            return
        if (len(self.obs_data.tabledata) == 0):
            self.obs_data = None
            messagebox.showwarning("WARNING","No data found in the HFC!")
            return

        self._date.set(self.obs_data.tabledata[0]['DATE_OBS'])
        self.ar_data=None ; self.ch_data=None ; self.sp_data=None
        self.rs_data=None ; self.pr_data=None ; self.fi_data=None
        self.__load_qclk()
        self.__plot_qclk()


    def __prev_date(self):
        print("Loading previous date...")
        date_obs = self._date.get()
        if (re.search(DATE_PATTERN,date_obs) is None):
            messagebox.showerror("ERROR","INPUT DATE FORMAT IS INCORRECT!")
            return False

        obs, inst, tel, wav = self.__id2obs(self._obsid.get())
        print("Loading information for the data set:")
        print("(DATE_OBS=%s, OBSERVAT=%s, INSTRUME=%s, TELESCOP=%s, WAVENAME=%s)" % (date_obs,obs,inst,tel, wav))
        date_obs = datetime.strptime(date_obs,HQI_TFORMAT)

        method=SQL_METHOD ; wsdl=self._wsdl
        WHAT="DATE_OBS, CDELT1, CDELT2, NAXIS1, NAXIS2, CENTER_X, CENTER_Y, R_SUN"
        WHAT+=", QCLK_URL, QCLK_FNAME, WAVEMIN, WAVEUNIT"
        LIMIT=1
        ORDER="DATE_OBS DESC"
        WHERE="(OBSERVAT=\"%s\") AND (INSTRUME=\"%s\") AND (DATE_OBS < \"%s\")" % (obs,inst,sql_date(date_obs))
        if (tel != ""):
            WHERE+=" AND (TELESCOP=\"%s\")" % (tel)
        if (wav != ""):
            WHERE+=" AND (WAVENAME=\"%s\")" % (wav)
        FROM=self._obs_table
        self.obs_data = self.__query_hfc(method=method,wsdl=wsdl,
                                         WHAT=WHAT,WHERE=WHERE,
                                         LIMIT=1,ORDER_BY=ORDER,
            FROM=FROM)
        if (self.obs_data is None):
            messagebox.showerror("ERROR","QUERYING HFC HAS FAILED!")
            return
        if (len(self.obs_data.tabledata) == 0):
            self.obs_data=None
            messagebox.showwarning("WARNING","NO DATA FOUND IN THE HFC!")
            return
        self._date.set(self.obs_data.tabledata[0]['DATE_OBS'])
        self.ar_data=None ; self.ch_data=None ; self.sp_data=None
        self.rs_data=None ; self.pr_data=None ; self.fi_data=None
        self.__load_qclk()
        self.__plot_qclk()

    def __next_date(self):
        print("Loading next date...")
        date_obs = self._date.get()
        if (re.search(DATE_PATTERN,date_obs) is None):
            messagebox.showerror("ERROR","INPUT DATE FORMAT IS INCORRECT!")
            return False

        obs, inst, tel, wav = self.__id2obs(self._obsid.get())
        print("Loading information for the data set:")
        print("(DATE_OBS=%s, OBSERVAT=%s, INSTRUME=%s, TELESCOP=%s, WAVENAME=%s)" % (date_obs,obs,inst,tel,wav))
        date_obs = datetime.strptime(date_obs,HQI_TFORMAT)

        method=SQL_METHOD ; wsdl=self._wsdl
        WHAT="DATE_OBS, CDELT1, CDELT2, NAXIS1, NAXIS2, CENTER_X, CENTER_Y, R_SUN"
        WHAT+=", QCLK_URL, QCLK_FNAME, WAVEMIN, WAVEUNIT"
        LIMIT=1
        ORDER="DATE_OBS ASC"
        WHERE="(OBSERVAT=\"%s\") AND (INSTRUME=\"%s\") AND (DATE_OBS > \"%s\")" % (obs,inst,sql_date(date_obs))
        if (tel != ""):
            WHERE+=" AND (TELESCOP=\"%s\")" % (tel)
        if (wav != ""):
            WHERE+=" AND (WAVENAME=\"%s\")" % (wav)
        FROM=self._obs_table
        self.obs_data = self.__query_hfc(method=method,wsdl=wsdl,
                                         WHAT=WHAT,WHERE=WHERE,
                                         LIMIT=1,ORDER_BY=ORDER,
                                         FROM=FROM)
        if (self.obs_data is None):
            messagebox.showerror("ERROR","QUERYING HFC HAS FAILED!")
            return
        if (len(self.obs_data.tabledata) == 0):
            self.obs_data=None
            messagebox.showwarning("WARNING","NO DATA FOUND IN THE HFC!")
            return
        self._date.set(self.obs_data.tabledata[0]['DATE_OBS'])
        self.ar_data=None ; self.ch_data=None ; self.sp_data=None
        self.rs_data=None ; self.pr_data=None ; self.fi_data=None
        self.__load_qclk()
        self.__plot_qclk()

    def __load_qclk(self):
        if (self.obs_data is None):
            messagebox.showwarning("WARNING","EMPTY DATA SET!")
            return False
        data = self.obs_data.tabledata[0]
        self.qclk_url = data["QCLK_URL"] + "/" + data["QCLK_FNAME"]

        print("Loading quicklook image from %s" % (self.qclk_url))
        self.image =  hfc_client.load_image(self.qclk_url)

    def __plot_qclk(self):
        image = self.image

        # Clear older data
        self._plt.clear()
        # Load data
        data = self.obs_data.tabledata[0]
        r_sun = np.float(data["R_SUN"])
        naxis1 = int(data['NAXIS1']) ; naxis2 = int(data['NAXIS2'])
        cdelt1 = np.float(data['CDELT1']) ; cdelt2 = np.float(data['CDELT2'])
        crpix1 = np.float(data['CENTER_X']) ; crpix2 = np.float(data['CENTER_Y'])
        wavemin = str(data['WAVEMIN']) ; waveunit = str(data['WAVEUNIT'])

        print("Plotting quicklook image")
        # X and Y axis
        X = np.arange(naxis1)
        Y = np.arange(naxis2)
        X = cdelt1*(X - crpix1)
        Y = cdelt2*(Y - crpix2)
        self._xlim=[min(X),max(X)]
        self._ylim=[min(Y),max(Y)]

        # Solar radius pixels
        theta = 2.*np.pi*np.array(range(361))/360.0
        xsun = r_sun*np.cos(theta) + crpix1 # in pix
        ysun = r_sun*np.sin(theta) + crpix2 # in pix
        xsun = cdelt1*(xsun - crpix1) # in arcsec
        ysun = cdelt2*(ysun - crpix2) # in arcsec

        if (image is None):
            #messagebox.showwarning("WARNING","NO QUICKLOOK IMAGE FOUND!")
            print("WARNING: NO QUICKLOOK IMAGE FOUND!")
            self._plt.plot(xsun,ysun) # If no image --> plot solar radius contour
        else:
            image = Image.open(image)
            image = np.flipud(image)
            enhanced_image = auto_contrast(image,low=0.,high=1.0) #TODO: Ajouter une bar pour l'intensite
            self._plt.imshow(enhanced_image,
                             cmap=plt.cm.gray,
                             extent=[min(X),max(X),min(Y),max(Y)],
                             origin='lower')
        title = "-".join(self.__id2obs(self._obsid.get())) + "["+wavemin+" "+waveunit+"]"
        self._plt.set_title(title)
        self._plt.set_xlabel("X (arcsec)")
        self._plt.set_ylabel("Y (arcsec)")

        if (self._aron.get()):
            print("Plotting active region data")
            self.__plot_feat("ar")
        if (self._chon.get()):
            print("Plotting coronal hole data")
            self.__plot_feat("ch")
        if (self._spon.get()):
            print("Plotting sunspot data")
            self.__plot_feat("sp")
        if (self._rson.get()):
            print("Plotting radio source data")
            self.__plot_feat("rs")
        if (self._pron.get()):
            print("Plotting prominence data")
            self.__plot_feat("pr")
        if (self._fion.get()):
            print("Plotting filament data")
            self.__plot_feat("fi")

        self._canvas.show()
        return True

    def __plot_feat(self,feature):

        feat = feature.lower()
        if (feat == "ar"):
            feat_data = self.ar_data
        elif (feat == "ch"):
            feat_data = self.ch_data
        elif (feat == "sp"):
            feat_data = self.sp_data
        elif (feat == "rs"):
            feat_data = self.rs_data
        elif (feat == "pr"):
            feat_data = self.pr_data
        elif (feat == "fi"):
            feat_data = self.fi_data
        else:
            messagebox.showwarning("WARNING","UNKNOWN FEATURE!")
            return False

        if (feat_data is None):
            feat_data = self.__load_feat(feat)
        if (feat_data is None):
            return False

        feat_color = FEATURE_COLORS[feat]

        # Plot feature contours
        for current_feat in feat_data:
            if ("B" in current_feat['CC_X_PIX']):
                #Prominence case -> cf Nicolas Fuller pour resoudre ce pb
                continue

            cdelt1 = float(current_feat['CDELT1'])
            cdelt2 = float(current_feat['CDELT2'])
            crpix1 = float(current_feat['CENTER_X'])
            crpix2 = float(current_feat['CENTER_Y'])
            cc = str(current_feat['CC'])
            cc_x_pix = np.int64(current_feat['CC_X_PIX'])
            cc_y_pix = np.int64(current_feat['CC_Y_PIX'])
            Xc, Yc = chain2image(cc,[cc_x_pix,cc_y_pix])
            for i, Xi in enumerate(Xc):
                Xc[i] = cdelt1*(Xc[i] - crpix1)
                Yc[i] = cdelt2*(Yc[i] - crpix2)
            track_id = int(current_feat['TRACK_ID'])

            if (track_id > 0) and (self._feat_ct.get() == 1):
                track_id = (5000 * track_id) % 16777216 # (256*256*256)
                r = track_id % 256 ; g = track_id/256 % 256
                b = (track_id - r - g*256) % 256
                feat_color=[float(r)/256.0,float(g)/256.0,float(b)/256.0]
            self._plt.plot(Xc,Yc,color=feat_color)

        self._plt.set_xlim(self._xlim[0], self._xlim[1])
        self._plt.set_ylim(self._ylim[0], self._ylim[1])
        self._canvas.show()
        return True

    def __load_feat(self,feature):
        feat = feature.lower()
        if not (FEATURE_TABLE.has_key(feat)):
            messagebox.showwarning("WARNING","UNKNOWN FEATURE!")
            return None
        feat_table=FEATURE_TABLE[feat]

        date_obs = self._date.get()
        if (re.search(DATE_PATTERN,date_obs) is None):
            messagebox.showerror("ERROR","INPUT DATE FORMAT IS INCORRECT!")
            return False
        date_obs = datetime.strptime(date_obs,HQI_TFORMAT)
        starttime = date_obs - timedelta(hours=1)
        endtime = date_obs + timedelta(hours=1)
        obs, inst, tel, wav = self.__id2obs(self._obsid.get())

        method = SQL_METHOD
        wsdl = self._wsdl
        WHAT="DATE_OBS, CDELT1, CDELT2, NAXIS1, NAXIS2, CENTER_X, CENTER_Y, CC,CC_X_PIX,CC_Y_PIX, TRACK_ID"
        WHERE="(DATE_OBS BETWEEN \"%s\" AND \"%s\")" % (sql_date(starttime),sql_date(endtime))
        FROM=feat_table
        feat_data = self.__query_hfc(method=method,wsdl=wsdl,
                                     WHAT=WHAT,WHERE=WHERE,FROM=FROM)
        if (feat_data is None):
            messagebox.showerror("ERROR","QUERYING HFC HAS FAILED!")
            return None
        if (len(feat_data.tabledata) == 0):
            msg = "NO %s DATA FOUND \n" % (feat.upper())
            msg+= "AROUND THIS DATE \n"
            msg+= "IN THE HFC!"
            #messagebox.showwarning("WARNING", msg)
            print(msg)
            return None

        # Keep only data for the current date of observation
        dt = []
        for td in feat_data.tabledata:
            current_date_obs = datetime.strptime(td['DATE_OBS'],HQI_TFORMAT)
            dt.append(abs(current_date_obs - date_obs))
        dt_min=min(dt)

        tabledata = []
        for td in feat_data.tabledata:
            current_date_obs = datetime.strptime(td['DATE_OBS'],HQI_TFORMAT)
            dt=abs(current_date_obs - date_obs)
            if (dt == dt_min): tabledata.append(td)
        print("HFC %s data found for the date %s" % (feat.upper(),tabledata[0]['DATE_OBS']))

        return tabledata

    def __query_hfc(self, **kwargs):

        votable = hfc_client.query(**kwargs)
        return votable

    def __open(self):
        print("Open")

    def __show_help(self):
        print("Show help")

    def __about(self):
        msg = "HFC Viewer %s \n" % (__version__)
        msg += "\n"
        msg += "HFC Viewer for Python is developped and \n"
        msg += "maintened by LESIA-Observatoire de Paris.\n"
        msg += "\n"
        msg += "More information about available data \n"
        msg += "can be found on the HFC web page: \n"
        msg += "http://voparis-helio.obspm.fr/hfc-gui/\n"
        msg += "\n"
        msg += "The Heliophysics Feature Catalogue (HFC)\n"
        msg += "is a service of the HELIO virtual observatory:\n"
        msg += "http://www.helio-vo.eu/ \n"
        msg += "\n"
        msg += "\n"
        msg += "Any feedback is welcome, please send your "
        msg += "comments to xavier dot bonnin at obspm dot fr."
        messagebox.showinfo("HFC Viewer",msg)
        return


def main(**kwargs):

    root = Tk()
    root.title('HFC Viewer')
    tkview = Viewer(master=root, **kwargs)
    tkview.pack(expand=1, fill='both')

    root.mainloop()

if __name__ == '__main__':
    print(__file__)
