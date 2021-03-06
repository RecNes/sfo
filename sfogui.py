# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Application", pos=wx.DefaultPosition, size=wx.Size(800, 600),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Login"), wx.VERTICAL)

        gSizer4 = wx.GridSizer(5, 2, 0, 0)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"User", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        gSizer4.Add(self.m_staticText8, 0, wx.ALL, 5)

        self.user_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TE_READONLY)
        gSizer4.Add(self.user_name, 0, wx.ALL, 5)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"Pass", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        gSizer4.Add(self.m_staticText9, 0, wx.ALL, 5)

        self.user_pass = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TE_PASSWORD | wx.TE_READONLY)
        gSizer4.Add(self.user_pass, 0, wx.ALL, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"Key", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        gSizer4.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.user_code = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TE_PASSWORD | wx.TE_READONLY)
        gSizer4.Add(self.user_code, 0, wx.ALL, 5)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"Image", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)
        gSizer4.Add(self.m_staticText11, 0, wx.ALL, 5)

        self.captcha_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer4.Add(self.captcha_text, 0, wx.ALL, 5)

        self.fetch_image = wx.Button(self, wx.ID_ANY, u"Fetch Image", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer4.Add(self.fetch_image, 1, wx.ALL | wx.EXPAND, 5)

        self.sign_in = wx.Button(self, wx.ID_ANY, u"Sign In", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer4.Add(self.sign_in, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer4.Add(gSizer4, 1, wx.EXPAND, 5)

        bSizer7.Add(sbSizer4, 1, wx.EXPAND, 5)

        sbSizer5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Notices"), wx.VERTICAL)

        self.uyari_akisi = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_MULTILINE | wx.TE_READONLY)
        sbSizer5.Add(self.uyari_akisi, 1, wx.ALL | wx.EXPAND, 5)

        self.captcha_image = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(150, 50), 0)
        sbSizer5.Add(self.captcha_image, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer7.Add(sbSizer5, 1, wx.EXPAND, 5)

        sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Proc Info"), wx.VERTICAL)

        gSizer5 = wx.GridSizer(5, 2, 0, 0)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"Proc Count", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)
        gSizer5.Add(self.m_staticText12, 0, wx.ALL, 5)

        self.proc_count = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_READONLY | wx.ALIGN_RIGHT)
        gSizer5.Add(self.proc_count, 0, wx.ALL, 5)

        self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"Total", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)
        gSizer5.Add(self.m_staticText13, 0, wx.ALL, 5)

        self.proctotal = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY | wx.ALIGN_RIGHT)
        gSizer5.Add(self.proctotal, 0, wx.ALL, 5)


        self.m_staticText15 = wx.StaticText(self, wx.ID_ANY, u"Remote Balance", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText15.Wrap(-1)
        gSizer5.Add(self.m_staticText15, 0, wx.ALL, 5)

        self.api_balance_display = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                            wx.TE_READONLY | wx.ALIGN_RIGHT)
        gSizer5.Add(self.api_balance_display, 0, wx.ALL, 5)


        self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"Local Balance", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)
        gSizer5.Add(self.m_staticText14, 0, wx.ALL, 5)

        self.last_balance = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY | wx.ALIGN_RIGHT)
        gSizer5.Add(self.last_balance, 0, wx.ALL, 5)

        self.start_proc = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer5.Add(self.start_proc, 1, wx.ALL | wx.EXPAND, 5)

        self.odeme_dur = wx.Button(self, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer5.Add(self.odeme_dur, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer6.Add(gSizer5, 1, wx.EXPAND, 5)

        bSizer7.Add(sbSizer6, 1, wx.EXPAND, 5)

        bSizer6.Add(bSizer7, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.ProcList = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                         wx.LC_NO_SORT_HEADER | wx.LC_REPORT)
        bSizer8.Add(self.ProcList, 1, wx.ALL | wx.EXPAND, 5)

        self.stat_gauge = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.stat_gauge.SetValue(0)
        bSizer8.Add(self.stat_gauge, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bSizer6.Add(bSizer8, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer6)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.fetch_image.Bind(wx.EVT_BUTTON, self.fetch_captcha)
        self.sign_in.Bind(wx.EVT_BUTTON, self.do_login)
        self.start.Bind(wx.EVT_BUTTON, self.starter)
        self.stop.Bind(wx.EVT_BUTTON, self.stoper)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def fetch_captcha(self, event):
        event.Skip()

    def do_login(self, event):
        event.Skip()

    def starter(self, event):
        event.Skip()

    def stoper(self, event):
        event.Skip()
