# -*- coding: utf-8 -*-
import json
import os
import re
import threading
from os.path import isfile
from time import sleep
from urllib import urlopen
from datetime import date, datetime
from decimal import Decimal
import wx
from base_system import Tools, Settings, log

__author__ = 'Sencer HAMARAT'


def path_finder(filen, foldern=None, root_path=None):
    """
    filen:      Fale name
    foldern:    Subfolder name
    root_path:  Default Settings.PROJECT_ROOT
    full_path:  full file path
    """
    full_path = None
    try:
        if root_path is None:
            root_path = Settings.PROJECT_ROOT

        if foldern is None:
            full_path = '{root_path}/{filen}'.format(root_path=root_path, filen=filen)
        else:
            if not Tools().check_foldr(foldern):
                Tools().create_foldr(foldern)
            full_path = '{root_path}/{foldern}/{filen}'.format(root_path=root_path, foldern=foldern, filen=filen)
    except Exception as e:
        log.exception(e.message)
        log.error(u"%s error." % filen)
    return full_path


class FetchCaptcha(threading.Thread):
    def __init__(self, parent):
        """
        Read captcha from url and write into file
        """
        super(FetchCaptcha, self).__init__()
        self._stop = threading.Event()
        self.parent = parent
        self.log = log

        self.captcha_folder_name = 'media'
        self.captcha_file_name = 'captcha.jpeg'
        self.captcha_file = path_finder(self.captcha_file_name, foldern=self.captcha_folder_name)

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

    def _check_file(self, operation):
        """
        Does file operations

        If operation not 'd' or 'r', file mode will be "wb"
        'd' : Delete file from file system
        'r' : Read file
        """
        if operation == 'd':
            try:
                os.remove(self.captcha_file)
            except OSError as e:
                self.log.error(repr(e.message))
                self.log.error(u"No file: %s" % self.captcha_file)

        elif operation == 'r':
            if isfile(self.captcha_file):
                jpg_image = wx.Image(self.captcha_file, wx.BITMAP_TYPE_JPEG)
                self.parent.captcha_image.SetBitmap(wx.BitmapFromImage(jpg_image))
            else:
                raise Exception("- No File: %s" % self.captcha_file)

        else:
            try:
                with open(self.captcha_file, mode='wb') as _file:
                    _file.write(operation)
            except Exception as e:
                self.log.error(e.message)
                raise Exception(u"> ERROR: File can't created...")

    def _fetch_captcha(self):
        """
        Read captcha from url.
        """
        try:
            self._check_file(self.captcha_fetcher_method_from_outer_class())
        except Exception as e:
            self.log.error(e.message)
            raise Exception(u'> ERROR: File cant read...')

    def run(self):
        """
        Event method.
        """
        self.parent.stat_gauge.Pulse()
        try:
            self.parent.display_captcha.Disable()
            self.parent.info_flow.AppendText(
                u"\r\nPlease wait..."
            )
            self._fetch_captcha()
            self._check_file('r')
            self.parent.info_flow.AppendText(
                u"\r\n> Info: Enter captcha text."
            )
            self.parent.sign_in_button.Enable()
            self.parent.stat_gauge.SetValue(0)
        except Exception as e:
            self.log.error(e.message)
            self.parent.info_flow.AppendText(u"\r\n{}".format(e.message))
            self.parent.display_captcha.Enable()
            self.parent.sign_in_button.Disable()
            self.stop()


class SessionProtector(threading.Thread):
    def __init__(self, parent):
        """
        Protects API session
        """
        super(SessionProtector, self).__init__()
        self._stop = threading.Event()
        self.parent = parent.parent
        self.log = log

    def stop(self):
        """
        Stops The Thread
        """
        self._stop.set()

    def stopped(self):
        """
        Returns Thread Status
        """
        return self._stop.isSet()

    def run(self):
        """
        Event Method
        """
        while not self.stopped():
            timer_counter = 0
            while not self.stopped():
                if (not self.parent.is_session_alive) or self.stopped() or timer_counter >= 60:
                    break
                sleep(1)
                timer_counter += 1

            if self.parent.is_session_alive and not self.parent.process_started:
                self.log.debug(u"Session protector started.")
                self.log.debug(repr(self.balance_fetcher_method_from_outer_class()))
            if not self.parent.is_session_alive:
                self.stop()
                self.log.debug(u"No Session. Session protector ended.")

            if self.stopped() or not self.parent.is_session_alive:
                break


class APISignIn(threading.Thread):
    def __init__(self, parent):
        """
        API Sign in
        """
        super(APISignIn, self).__init__()
        self._stop = threading.Event()
        self.parent = parent
        self.log = log
        self.captcha_text = None
        self.session_protector = SessionProtector(self)

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

    def __get_captcha_text(self):
        """
        Fetch data from self.captcha_text
        """
        if self.parent.captcha_text.GetValue():
            self.captcha_text = self.parent.captcha_text.GetValue()
        else:
            raise Exception(u"\r\n> WARNING: Catpcha code required")

    def __sing_in(self):
        """
        Sing in method
        """
        try:
            self.parent.sign_in_button.Disable()
            self.parent.info_flow.AppendText(u"\r\n- Starting to Sign In...")
            self.__get_captcha_text()
            bilgiler = (self.parent.user_name.GetValue(), self.parent.user_pass.GetValue(),
                        self.parent.user_code.GetValue(), self.parent.captcha_text.GetValue())
            self.parent.is_session_alive = self.sign_in_method_from_outer_class(bilgiler=bilgiler)

            if not self.parent.is_session_alive:
                raise Exception(u"\r\n- Error while Signing In. Please press 'Fetch Captcha' "
                                u"button to restart.")

            balance = str(self.service_balance_fetcher_method_from_outer_class())
            if balance is not None:
                self.parent.api_balance_display.SetValue(balance)
            else:
                self.parent.api_balance_display.SetValue('0.00')

            self.session_protector.start()
            self.parent.stat_gauge.SetValue(0)
            self.parent.sign_in_button.SetLabel(u"Sign Out")
            self.parent.sign_in_button.Enable()
            self.parent.start_button.Enable()
            self.log.info(u'Signed In...')
        except Exception as e:
            self.parent.sign_in_button.Disable()
            self.parent.fetch_captcha_button.Enable()
            raise Exception(e.message)

    def __sign_out(self):
        """
        Sign out method
        """
        try:
            self.parent.start_button.Disable()
            self.parent.info_flow.AppendText(u"\r\n> INFO: Session going to be ended...")
            if self.parent.sign_out_method_from_outer_class():
                self.parent.is_session_alive = False

            if self.parent.is_session_alive:
                raise Exception(u"\r\n> WARNING: Session Unable to Ended!")
            self.parent.sign_in_button.SetLabel(u"Sign In")
            self.parent.info_flow.AppendText(u"\r\n> WARNING: Session Ended.")
            self.session_protector.stop()
            self.log.info(u'Session Ended...')
        except Exception as e:
            raise Exception(e.message)
        finally:
            self.parent.stat_gauge.SetValue(0)
            self.parent.sign_in_button.Disable()
            self.parent.fetch_captcha_button.Enable()

    def run(self):
        """
        Event method
        """
        self.parent.stat_gauge.Pulse()

        try:
            if not self.parent.is_session_alive:
                self.__sing_in()
                if self.parent.is_session_alive:
                    self.parent.info_flow.AppendText(u"\r\n- Session OK.")
                else:
                    self.parent.captcha_text.SetValue("")
                    raise Exception(u"\r\n> ERROR: Unable to Sign In.")
            else:
                self.__sign_out()
                if not self.parent.is_session_alive:
                    self.parent.info_flow.AppendText(u"\r\n- Session Ended.")
                    self.parent.captcha_text.SetValue("")
                else:
                    raise Exception(u"\r\n> Error: Session unable to ended.")
            self.stop()
        except Exception as e:
            self.parent.info_flow.AppendText(u"\r\n{}".format(e.message))
            self.log.error(e.message)
            self.stop()


class FaturaOde(threading.Thread):
    def __init__(self, parent):
        """
        Do something
        """
        super(FaturaOde, self).__init__()
        self._stop = threading.Event()
        self.parent = parent
        self.log = log

        self.fail_counter = 0

        self.status_dict = {
            u'OK': 10,
            u'FAIL': 20,
        }

        self.service_query = dict()

        self.query_response = list()

        self.xls_file = self.__csv_file()
        self.__write_csv(header=True)

        self.fetch_service_url = self.parent.service_uri.format(root=self.parent.service_url, 
                                                                auth=self.parent.service_auth_id, service='OA')
        self.fetch_query_uri = '{url}/{query}'.format(url=self.fetch_service_url,
                                                      query='/?data={data}'.format(data=self.parent.service_uid))
        self._update_service_url = self.parent.service_uri.format(root=self.parent.service_url, 
                                                                  auth=self.parent.service_auth_id,service='FDG')
        self.update_query_uri = u'{url}/{fid}/{durum}/{comment}'

    def stop(self):
        """
        Stop Event
        """
        self.parent.process_started = False
        self._stop.set()
        if self.parent.ongoing_task:
            self.parent.info_flow.AppendText(u"\r\n- Ongoing process exists, Automatically stops when process done.")
            self.parent.info_flow.AppendText(u"\r\n> Warning: Do not close application before process done.")
        self.parent.ongoing_task = False
        self.parent.stop_process_button.Disable()
        self.parent.start_button.Enable()
        self.parent.sign_in_button.Enable()
        self.parent.stat_gauge.SetValue(0)

    def stopped(self):
        """
        Event Status.
        """
        return self._stop.isSet()

    @staticmethod
    def __force_decode(string, codecs=None):
        """
        String Decode
        """
        if not codecs:
            codecs = ['utf8', 'cp1252']
        for i in codecs:
            try:
                return string.decode(i)
            except Exception as e:
                log.exception(e.message)
                log.error(u"String decode error on: '%s'" % repr(string))
        log.warn(u"Cannot decode string: '%s'" % ([string]))

    @staticmethod
    def __csv_file():
        """
        Returns full CSV file path
        """
        day = date.today().strftime('%d_%m_%Y')
        xls_folder_name = 'CSV_Out'
        xls_file_name = '{day}.csv'.format(day=day)
        full_path = path_finder(xls_file_name, foldern=xls_folder_name)
        return full_path

    def __write_csv(self, header=False):
        """
        Write into CSV file
        """
        _content = None
        try:
            if (not header) and self.service_query.get('id'):
                _content = u'\n\r%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' % (
                    self.service_query['Field 1'],
                    self.service_query['Field 2'],
                    self.service_query['Field 3'],
                    self.service_query['Field 4'],
                    self.service_query['Field 5'],
                    self.service_query['Field 6'],
                    self.service_query['Field 7'],
                    u'%s (%s)' % (self.service_query['status'], self.status_dict[self.service_query['status']]),
                    self.service_query['Field 9'] or '',
                    self.service_query['Field 10'] or '')
            else:
                if not isfile(self.xls_file):
                    _content = u'%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' % (
                        u'Field 1', u'Field 2', u'Field 3', u'Field 4', u'Field 5',
                        u'Field 6', u'Field 7', u'Field 8', u'Field 9', u'Field 10')

            if _content is not None:
                with open(self.xls_file, mode='a') as _file:
                    _file.write(_content.encode("UTF-8"))
        except Exception as e:
            self.log.error(e.message)
            self.log.error(u'> ERROR: CSV file create/write error.')
            raise Exception(u"\r\n")

    def __status_update(self, status, comment=None, query=True):
        """
        Updates some fields in self.service_query dict.
        """
        self.service_query['status'] = status
        self.service_query['query'] = query
        self.service_query['comment'] = str(comment) if comment else ''
        self.service_query['operation_time'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self.parent.QueryList.SetStringItem(0, 5, self.service_query['status'])

    def __display(self):
        """
        Displays data.
        """
        if isinstance(self.service_query['Field 1'], str):
            self.service_query.update({'Field 1': self.__force_decode(self.service_query['Field 1'])})
        self.parent.QueryList.InsertStringItem(0, self.service_query['Field 2'])
        self.parent.QueryList.SetStringItem(0, 1, self.service_query['Field 1'])
        self.parent.QueryList.SetStringItem(0, 2, self.service_query['Field 3'])
        self.parent.QueryList.SetStringItem(0, 3, self.service_query['Field 4'])
        self.parent.QueryList.SetStringItem(0, 4, str(self.service_query['Field 5']))
        self.__status_update(u'Must Processed')

    def __convert_query_to_dict(self, datas):
        """
        Service data to dict
        """
        keys = ['Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7']
        data_list = datas.split(',')
        if data_list <= 1:
            raise Exception(u'> ERROR: No service data.')
        elif not len(data_list) == 7:
            self.log.error(repr(data_list))
            raise Exception(u'> ERROR: Wrong service data.')
        self.service_query = dict(zip(keys, data_list))
        self.parent.ongoing_task = True
        self.service_query.update({'amount': Decimal(self.service_query['amount'])})

    def __calculate_counter(self, detract=False):
        """
        Increase or Decrease counter
        """
        cntr = long(self.parent.query_count.GetValue())
        if not detract:
            self.parent.query_count.SetValue(str(cntr + 1))
        else:
            self.parent.query_count.SetValue(str(cntr - 1))

    def __calculate_amount(self, detract=False):
        """
        Increase or Decrease amount
        """
        total_amount = Decimal(self.parent.amount.GetValue())
        if not detract:
            self.parent.amount.SetValue(str(total_amount + Decimal(self.service_query['tutar'])))
        else:
            self.parent.amount.SetValue(str(total_amount - Decimal(self.service_query['tutar'])))

    @staticmethod
    def __clear_text(param):
        """
        For URL compitability.
        """
        chars = [' ', ',', '.', '-']
        return re.sub('[%s]' % ''.join(chars), '_', param.lstrip('- ').lstrip(' '))

    def __update_service_query(self):
        """
        Update Service Query
        """
        if self.service_query['status'] == u'OK':
            self.__status_update(u"Updating")
        try:
            status_no = self.status_dict[self.service_query['status']]
            if not status_no == 15:
                update_query_url = self.update_query_uri.format(url=self._update_service_url, fid=self.service_query['id'], 
                                                                durum=status_no, 
                                                                comment=self.__clear_text(self.service_query['comment']))
                _response = urlopen(update_query_url).read()
                if _response == '0':
                    self.log.info(u'Servis URL: %s' % repr(update_query_url))
                    error_text = u'Update Service Response: %s' % _response
                    self.log.info(error_text)
                    self.__status_update(u'!Unable To Update!', comment=error_text)
                elif self.service_query['status'] == u"Updating":
                    self.__status_update(u"Updated")
            else:
                self.__status_update(self.service_query['status'], comment=u'Not Updated.')
        except Exception as e:
            self.log.exception(e.message)
            self.stop()
            error_text = u'Status not reported to Update Service.'
            self.__status_update(u'!Not Updated!', comment=error_text)
            raise Exception(error_text)
        finally:
            self.__write_csv()
            if not self.parent.process_started:
                self.parent.info_flow.AppendText(u"\r\n> Warning: Process STOPPED.")
                self.parent.stat_gauge.SetValue(0)

    def _pull_service_amount(self):
        """
        Fetch amount.
        """
        amount = self.balance_fetcher_method_from_outer_class()
        if amount is not None:
            self.parent.api_balance_display.SetValue(str(amount))
        else:
            error_text = u'> ERROR: Unable to fetch service balance.'
            self.parent.info_flow.AppendText(error_text)
            self.parent.api_balance_display.SetValue('0.00')
            raise Exception(error_text)

    def _service_status(self, fetch_balance=False):
        try:
            service_control_url = self.parent.service_uri.format(
                root=self.parent.service_url, auth=self.parent.service_auth_id, service='SC'
            )
            self.parent.service_control_url = '%s%s' % (service_control_url, '/?data=%s' % self.parent.service_uid)
            self.parent.service_status = bool(eval(json.loads(urlopen(self.parent.service_control_url).read())['service']))

            if fetch_balance:
                balance_service_url = self.parent.service_uri.format(
                    root=self.parent.service_url, auth=self.parent.service_auth_id, service='OB'
                )
                self.parent.service_balance_query_url = '%s%s' % (balance_service_url, '/?data=%s' % self.parent.service_uid)
                self.parent.service_balance_read = str(json.loads(urlopen(self.parent.service_balance_query_url).read())['balance'])
                self.parent.service_balance.SetValue(self.parent.service_balance_read)
        except Exception as e:
            raise Exception(e)

    def _pull_service_query(self):
        """
        Does service query
        """
        self.__calculate_counter()
        try:
            self._service_status()
            if self.parent.service_status:
                _response = urlopen(self.fetch_query_uri).read()
                self.__convert_query_to_dict(_response)
                self.__display()
                self.__calculate_amount()
            else:
                self.parent.ongoing_task = False
                error_text = u"WARNING: Service stoppet from remote."
                self.parent.info_flow.AppendText(u"\r\n> %s" % error_text)
                raise Exception(error_text)
        except Exception as e:
            self.log.error(e.message)
            self.__write_csv()
            self.__calculate_counter(detract=True)
            raise Exception(u"\r\n> ERROR: Unable to fetch query response...")

    def _make_query(self):
        """
        Making query
        """
        self.__status_update(u'Querying')
        try:
            query_response = self.parent.fatura_sorgula(self.service_query)['sonuc']

            self.log.info(repr(query_response))
            if len(query_response) > 3:
                if query_response[0] and query_response[1]:
                    self.parent.QueryList.SetStringItem(0, 1, query_response[0])
                    self.parent.QueryList.SetStringItem(0, 2, query_response[3][3])
                    self.service_query.update({'aad': query_response[0]})
                    self.__status_update(u'Found')
                else:
                    if not query_response[0]:
                        self.__status_update(u'!Fail!', comment=u'Data Mismatch', query=query_response[1])
                    elif not query_response[1]:
                        self.__status_update(u'!Fail!', comment=query_response[2].encode('ascii', errors='ignore'),
                                             query=query_response[1])
                    self.__update_service_query()
            elif len(query_response) == 3:
                self.__status_update(u'!Not Found!', comment=query_response[2].encode('ascii', errors='ignore'),
                                     query=query_response[1])
                self.__update_service_query()
            else:
                self.log.info(query_response)
                self.__status_update(u'!Not Found!', query=False,
                                     comment='Odenecek fatura bulunamadi.'.encode('ascii', errors='ignore'))
                self.__update_service_query()
        except Exception as e:
            # Hata durumunda sonraki faturayı işleme almalı, o yüzden self.stop() ÇAĞIRILMAYACAK
            self.log.exception(e.message)
            self.__status_update(u'!Not Found!', comment=e)
            self.__calculate_amount(detract=True)
            self.__update_service_query()
            raise Exception(e.message)

    def _do_a_job(self):
        """
        Does something with data fetched from service.
        """
        self.__status_update(u'RUNNING')
        try:
            a_job = self.a_job_method_from_outer_class()['response']
            if a_job:
                self.fail_counter = 0
                self.__status_update(u'OK')
                self.parent.ongoing_task = False
            else:
                self.fail_counter += 1
                self.log.info(u"FAILED: %s" % self.service_query)
                if self.fail_counter == 5:
                    raise Exception("- Error occured.")
        except Exception as e:
            self.parent.ongoing_task = True
            self.log.exception(e.message)
            self.__calculate_amount(detract=True)
            error_text = u"- Status Failed."
            self.__status_update(u'!FAILED!', comment=error_text)
            raise Exception(error_text)
        finally:
            self.__update_service_query()
            self._service_status(fetch_balance=True)

    def run(self):
        """
        Event method
        """
        self.parent.info_flow.AppendText(u"\r\n- Starting a job...")
        self.parent.stat_gauge.Pulse()
        self.parent.start_button.Disable()
        self.parent.sign_in_button.Disable()
        self.parent.stop_process_button.Enable()
        self.parent.process_started = True
        self.parent.info_flow.AppendText(u"\r\n- Job started.")
        try:
            while self.parent.process_started:
                self._pull_service_query()
                self._pull_service_amount()
                if Decimal(self.parent.api_balance_display.GetValue()) >= Decimal(self.service_query['tutar']):
                    self._make_query()
                else:
                    raise Exception(u"\r\n> WARNING: BALANCE UNSETISFIED. Job Stopped.")
                if self.service_query['Field 6']:
                    self._do_a_job()
        except Exception as e:
            self.parent.info_flow.AppendText(u'\r\n{}'.format(e.message))
            self.log.exception(e.message)
            self.parent.do_task = False
            self.parent.process_started = False
            self.stop()
