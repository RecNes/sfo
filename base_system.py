# -*- coding: utf-8 -*-
from datetime import date
from decimal import Decimal
from logging import handlers
from os.path import isfile
from urllib import urlopen
import json
import logging
import os
import sys
import threading

__author__ = 'Sencer HAMARAT'
_debug = True


class Settings():
    """
    Projenin bazı gömülü ayarları burada tutulur.
    """
    DEBUG = True if _debug else False
    if hasattr(sys, 'frozen'):
        _project_root = os.path.abspath(os.path.dirname(__file__))
        _project_dirs = _project_root.split('\\')
        del _project_dirs[-1]
        PROJECT_ROOT = '\\'.join(_project_dirs)
    else:
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def log_file_name(dosya):
    """
    Return file name without extention
    """
    return '_'.join(dosya.split('.')[:-1])


class Logger:
    def __init__(self, log_name, level='INFO', log_dir='logs', log_format=None, handler=None):
        """
        log_name: log file name
        level: log levels: CRITICAL, ERROR, WARNING, INFO, DEBUG
        log_dir: log folder. default <project_folder>/logs/
        log_format: logging format
        handler: TODO
        """
        self.log_name = log_name
        self.loger = None
        self.formatter = None
        self.handler = handler
        self.level = 'INFO'
        self.log_format = u"%(asctime)s %(levelname)s %(name)s %(process)d %(threadName)s %(module)s: " \
                          u"%(lineno)d %(funcName)s() %(message)s\r\n"

        self.__configure_level(level.upper())
        self.__configure_format(log_format)
        self.__configure_handler(log_dir)

    def __configure_level(self, level):
        if level not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
            raise Exception(u"{} geçerli bir log seviyesi değil".format(level))
        self.level = 'DEBUG' if Settings.DEBUG else level

    def __configure_format(self, log_format):
        if log_format:
            self.log_format = log_format
        self.formatter = logging.Formatter(self.log_format)

    def __configure_handler(self, log_dir):
        _dir = '{}/{}'.format(Settings.PROJECT_ROOT, log_dir)
        if not os.path.exists(_dir):
            os.mkdir(_dir)
        _filename = "{}/{}.log".format(_dir, self.log_name)
        self.handler = handlers.WatchedFileHandler(_filename, mode="a", encoding="utf-8")
        self.handler.setFormatter(self.formatter)

    def create_logger(self):
        _loger = logging.getLogger(self.log_name)
        _loger.setLevel(getattr(logging, self.level))
        _loger.addHandler(self.handler)
        self.loger = _loger
        return _loger


day = date.today().strftime('%d_%m_%Y')
log = Logger('ttfo-%s' % day).create_logger()


class Tools():
    """
    Class of Some base tools
    create_foldr: Creates folder in project base
    control_folder: Checks folder in project base
    moneyfmt: Formatting money string
    """

    def __init__(self):
        pass

    @staticmethod
    def create_foldr(captcha_folder):
        tamam = False
        try:
            if not os.path.exists(captcha_folder):
                os.makedirs(captcha_folder)
                tamam = True
            else:
                raise Exception(u"Folder exsists: {captcha_folder}".format(captcha_folder=captcha_folder))
        except Exception as e:
            log.error(e.message)
        return tamam

    @staticmethod
    def check_foldr(captcha_folder):
        var = False
        if os.path.exists(captcha_folder):
            var = True
        return var

    @staticmethod
    def moneyfmt(value, places=2, curr='', sep='.', dp=',', pos='', neg='-', trailneg=''):
        """
        Convert Decimal to a money formatted string.

        places:  required number of places after the decimal point
        curr:    optional currency symbol before the sign (may be blank)
        sep:     optional grouping separator (comma, period, space, or blank)
        dp:      decimal point indicator (comma or period)
                 only specify as blank when places is zero
        pos:     optional sign for positive numbers: '+', space or blank
        neg:     optional sign for negative numbers: '-', '(', space or blank
        trailneg:optional trailing minus indicator:  '-', ')', space or blank

        >>> d = Decimal('-1234567.8901')
        >>> moneyfmt(d, curr='$')
        '-$1,234,567.89'
        >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
        '1.234.568-'
        >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
        '($1,234,567.89)'
        >>> moneyfmt(Decimal(123456789), sep=' ')
        '123 456 789.00'
        >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
        '<.02>'
        """

        try:
            if value == '':
                return value

            value = Decimal(str(value))

            q = Decimal((0, (1,), -places))  # 2 places --> '0.01'
            sign, digits, exp = value.quantize(q).as_tuple()
            assert exp == -places
            result = []
            digits = map(str, digits)
            _build, _next = result.append, digits.pop
            if sign:
                _build(trailneg)
            if curr:
                _build(' ' + unicode(curr))
            for i in range(places):
                if digits:
                    _build(_next())
                else:
                    _build('0')
            if places > 0: 
                _build(dp)
            i = 0
            if not digits: 
                _build('0')  # ,00 yerine 0,00 gostersin diye.
            while digits:
                _build(_next())
                i += 1
                if i == 3 and digits:
                    i = 0
                    _build(sep)

            if sign:
                _build(neg)
            else:
                _build(pos)
            result.reverse()
            return ''.join(result)
        except Exception as e:
            log.error(e.message)


class ConfigLoader(threading.Thread):
    """
    Reading Configuration file.
    """

    def __init__(self, parent):
        super(ConfigLoader, self).__init__()
        self._stop = threading.Event()
        self.parent = parent
        self.file_name = "sfo.conf"
        self.file = "{root}/{file}".format(root=Settings.PROJECT_ROOT, file=self.file_name)
        self.log = log

    def stop(self):
        """
        Stops The Thread
        """
        self.parent.stat_gauge.SetValue(0)
        self._stop.set()

    def stopped(self):
        """
        Returns Thread Status
        """
        return self._stop.isSet()

    def run(self):
        content_dict = dict()
        try:
            if isfile(self.file):
                with open(self.file, mode='r') as _file:
                    content = _file.readlines()
            else:
                hata = u'\r\nERROR: Configuration file not found...'
                self.log.debug(u"File Not Found: {}".format(self.file))
                self.parent.info_flow.AppendText(hata)
                raise Exception(hata)
            try:
                for line in content:
                    if (not line.startswith('#')) and ('=' in line):
                        line = line.replace('\r', '').replace('\n', '').replace(' ', '')
                        key, value = line.split('=')
                        content_dict[key] = value
            except Exception as e:
                self.log.exception(e.message)
                self.log.error(u"Error in configuration distionary...")
                raise Exception(u"ERROR: Configuration error...")

            self.parent.service_uid = content_dict['service_uid']
            self.parent.service_url = content_dict['service_url']
            self.parent.user_name.SetValue(content_dict['remote_gui_user'])
            self.parent.user_pass.SetValue(content_dict['remote_gui_pass'])
            self.parent.user_code.SetValue(content_dict['remote_gui_code'])
        except Exception as e:
            self.log.exception(e.message)
            self.parent.info_flow.AppendText(u'\r\nERROR: Configuration file error.')
        self.stop()


class CheckConnection(threading.Thread):
    """
    Connection control class.
    """

    def __init__(self, parent, fetch_balance=False):
        super(CheckConnection, self).__init__()
        self._stop = threading.Event()
        self.parent = parent
        self.log = log
        self.fetch_balance = fetch_balance
        self.service_name = 'ServisKontrol'
        self.service_control_url = self.parent.service_uri.format(
            root=self.parent.service_url, auth=self.parent.service_auth_id, service=self.service_name
        )
        self.balance_service_name = 'OdeyiciBakiyesi'
        self.balance_service_url = self.parent.service_uri.format(
            root=self.parent.service_url, auth=self.parent.service_auth_id, service=self.balance_service_name
        )
        self.parent.stat_gauge.Pulse()

    def stop(self):
        """
        Stops The Thread
        """
        self.parent.stat_gauge.SetValue(0)
        self._stop.set()

    def stopped(self):
        """
        Returns Thread Status
        """
        return self._stop.isSet()

    def run(self):
        self.parent.service_status = False
        try:
            self.parent.info_flow.AppendText(u'\r\nChecking service...')
            if self.fetch_balance:
                self.parent.service_balance_query_url = '%s%s' % (self.balance_service_url, '/?oid=%s' % self.parent.service_uid)
                self.parent.api_balance = str(json.loads(urlopen(self.parent.service_balance_query_url).read())['bakiye'])
                self.parent.api_balance_display.SetValue(self.parent.api_balance)
            self.parent.service_control_url = '%s%s' % (self.service_control_url, '/?oid=%s' % self.parent.service_uid)
            self.parent.service_status = bool(eval(json.loads(urlopen(self.parent.service_control_url).read())['servis']))
        except Exception as e:
            self.log.debug(self.parent.service_url)
            self.log.exception(repr(e.message))
            self.log.exception(self.service_control_url)
        finally:
            if self.parent.service_status:
                self.parent.info_flow.AppendText(u'\r\nConnected to service.')
                self.parent.fetch_captcha_button.Enable()
            else:
                self.parent.info_flow.AppendText(u'\r\n\r\nERROR: Unable to connect to service...')
        self.stop()