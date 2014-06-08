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
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"TTFO", pos=wx.DefaultPosition, size=wx.Size(800, 600),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"TT Giriş"), wx.VERTICAL)

        gSizer4 = wx.GridSizer(5, 2, 0, 0)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"Kullanıcı", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        gSizer4.Add(self.m_staticText8, 0, wx.ALL, 5)

        self.user_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TE_READONLY)
        gSizer4.Add(self.user_name, 0, wx.ALL, 5)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"Parola", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        gSizer4.Add(self.m_staticText9, 0, wx.ALL, 5)

        self.user_pass = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TE_PASSWORD | wx.TE_READONLY)
        gSizer4.Add(self.user_pass, 0, wx.ALL, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"Şifre", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        gSizer4.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.user_code = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TE_PASSWORD | wx.TE_READONLY)
        gSizer4.Add(self.user_code, 0, wx.ALL, 5)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"Resim", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)
        gSizer4.Add(self.m_staticText11, 0, wx.ALL, 5)

        self.captcha_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer4.Add(self.captcha_text, 0, wx.ALL, 5)

        self.resim_al = wx.Button(self, wx.ID_ANY, u"Resim Al", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer4.Add(self.resim_al, 1, wx.ALL | wx.EXPAND, 5)

        self.giris_yap = wx.Button(self, wx.ID_ANY, u"Giriş Yap", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer4.Add(self.giris_yap, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer4.Add(gSizer4, 1, wx.EXPAND, 5)

        bSizer7.Add(sbSizer4, 1, wx.EXPAND, 5)

        sbSizer5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Uyarı Akışı"), wx.VERTICAL)

        self.uyari_akisi = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_MULTILINE | wx.TE_READONLY)
        sbSizer5.Add(self.uyari_akisi, 1, wx.ALL | wx.EXPAND, 5)

        self.captcha_image = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(150, 50), 0)
        sbSizer5.Add(self.captcha_image, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer7.Add(sbSizer5, 1, wx.EXPAND, 5)

        sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"İşlem Bilgileri"), wx.VERTICAL)

        gSizer5 = wx.GridSizer(5, 2, 0, 0)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"Ödenebilen Fatura", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)
        gSizer5.Add(self.m_staticText12, 0, wx.ALL, 5)

        self.fatura_adet = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_READONLY | wx.ALIGN_RIGHT)
        gSizer5.Add(self.fatura_adet, 0, wx.ALL, 5)

        self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"Toplam Ödeme Tutarı", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)
        gSizer5.Add(self.m_staticText13, 0, wx.ALL, 5)

        self.fatura_tutar = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY | wx.ALIGN_RIGHT)
        gSizer5.Add(self.fatura_tutar, 0, wx.ALL, 5)


        self.m_staticText15 = wx.StaticText(self, wx.ID_ANY, u"Ödeyici Bakiyesi", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText15.Wrap(-1)
        gSizer5.Add(self.m_staticText15, 0, wx.ALL, 5)

        self.api_balance_display = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                            wx.TE_READONLY | wx.ALIGN_RIGHT)
        gSizer5.Add(self.api_balance_display, 0, wx.ALL, 5)


        self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"TTS Bakiyesi", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)
        gSizer5.Add(self.m_staticText14, 0, wx.ALL, 5)

        self.kalan_bakiye = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY | wx.ALIGN_RIGHT)
        gSizer5.Add(self.kalan_bakiye, 0, wx.ALL, 5)

        self.odeme_basla = wx.Button(self, wx.ID_ANY, u"Ödemeye Başla", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer5.Add(self.odeme_basla, 1, wx.ALL | wx.EXPAND, 5)

        self.odeme_dur = wx.Button(self, wx.ID_ANY, u"Ödemeyi Durdur", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer5.Add(self.odeme_dur, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer6.Add(gSizer5, 1, wx.EXPAND, 5)

        bSizer7.Add(sbSizer6, 1, wx.EXPAND, 5)

        bSizer6.Add(bSizer7, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.FaturaListesi = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                         wx.LC_NO_SORT_HEADER | wx.LC_REPORT)
        bSizer8.Add(self.FaturaListesi, 1, wx.ALL | wx.EXPAND, 5)

        self.stat_gauge = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.stat_gauge.SetValue(0)
        bSizer8.Add(self.stat_gauge, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bSizer6.Add(bSizer8, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer6)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.resim_al.Bind(wx.EVT_BUTTON, self.fetch_captcha)
        self.giris_yap.Bind(wx.EVT_BUTTON, self.do_login)
        self.odeme_basla.Bind(wx.EVT_BUTTON, self.odeme_baslat)
        self.odeme_dur.Bind(wx.EVT_BUTTON, self.odeme_durdur)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def fetch_captcha(self, event):
        event.Skip()

    def do_login(self, event):
        event.Skip()

    def odeme_baslat(self, event):
        event.Skip()

    def odeme_durdur(self, event):
        event.Skip()
