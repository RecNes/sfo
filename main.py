# -*- coding: utf-8 -*-
from time import sleep

from sfo import MainFrame, wx
from base_system import ConfigLoader, CheckConnection, log
from tts import FetchCaptcha, APISignIn


class MainProcessFrame(MainFrame):                                      # Constructor
    def __init__(self, parent):                                         # Initialize parent class
        """
        Some Docstrings was here. Removed because of some cases.
        """
        MainFrame.__init__(self, parent)
        self.log = log
        self.debug = False
        self.process_started = False
        self.do_task = False
        self.ongoing_task = False

        self.ftrc_trd = None

        self.service_uid = None
        self.service_url = None
        self.service_status = False
        self.service_control_url = None
        self.service_balance_query_url = None
        self.service_balance_read = '0.00'
        self.service_auth_id = 'api_service_auth_id'
        self.service_uri = "{root}/{auth}/{service}"

        self.api_balance = '0.00'
        self.is_session_alive = False

        self._init_display()
        self._read_config()
        sleep(1)                                                        # Waiting for reading config file
        if self.service_url is not None:
            self._check_connection()

    def _init_display(self):
        self.QueryList.InsertColumn(0, u'Field 1', width=80)
        self.QueryList.InsertColumn(1, u'Field 2', width=280)
        self.QueryList.InsertColumn(2, u'Field 3', width=110)
        self.QueryList.InsertColumn(3, u'Field 4', width=120)
        self.QueryList.InsertColumn(4, u'Field 5', width=80)
        self.QueryList.InsertColumn(5, u'Field 6', width=100)
        self.query_count.SetValue('0')
        self.amount.SetValue('0.00')
        self.api_balance_display.SetValue('0.00')
        self.api_balance_display.SetValue(self.api_balance)

    def _read_config(self):
        cfg_trd = ConfigLoader(self)
        cfg_trd.start()

    def _check_connection(self):
        conn_trd = CheckConnection(self, fetch_balance=True)
        conn_trd.start()

    def fetch_captcha(self, event):
        cptc_trd = FetchCaptcha(self)
        cptc_trd.start()

    def do_login(self, event):
        grs_trd = APISignIn(self)
        grs_trd.start()


class App(wx.App):
    def OnInit(self):
        """
        Some Docstrings was here. Removed because of some cases.
        """
        frame = MainProcessFrame(None)   # create an object of MainProcessFrame
        frame.start_button.Disable()
        frame.stop_process_button.Disable()
        frame.sign_in_button.Disable()
        frame.fetch_captcha_button.Disable()
        frame.Show(True)            # Show the frame
        self.SetTopWindow(frame)
        return True


# Mandatory in wx, create an app, False stands for not deteriction stdin/stdout refer manual for details
if __name__ == '__main__':
    app = App()
    app.MainLoop()                  # start the applications
