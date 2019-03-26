# -*- coding: utf-8 -*-

#   2019/3/20 0020 上午 10:59     

__author__ = 'RollingBear'

import os
import time
import logging
import traceback


class system_service():

    def __init__(self):
        pass

    def get_service_state(self, service_name):

        '''
        get service state with a cmd command
        :param service_name: service's name
        :return: service state(str)
        '''

        try:
            result = os.popen('sc query ' + service_name).read()

            if 'RUNNING' in result or "START_PENDING" in result:
                return 'active'
            elif 'STOPPED' in result or 'STOP_PENDING' in result:
                return 'inactive'
            elif '1060' in result:
                return 'uninstalled'
        except Exception:
            logging.info(traceback.format_exc())

    def service_state_operate(self, service_name, state):

        '''
        start or stop an installed service with a cmd command
        :param service_name: service's name
        :param state: start or stop, used to control function start or stop the service
        :return: service start or stop result
        '''

        try:
            result = os.popen('sc ' + state + ' ' + service_name).read()

            if '1058' in result:
                return 'error'
            elif '1060' in result:
                return 'uninstalled'
            elif '1056' in result:
                return 'active'
            elif '1062' in result:
                return 'inactive'
            elif 'START_PENDING' in result or 'STOP_PENDING' in result:
                return 'success'
        except Exception:
            logging.info(traceback.format_exc())

    def restart_service(self, service_name):

        '''
        restart an installed service with a cmd command
        :param service_name: service's name
        :return: service restart result
        '''

        try:
            result_stop = self.stop_service(service_name)
            time.sleep(1)
            try:
                result_start = self.start_service(service_name)
            except Exception:
                logging.info(traceback.format_exc())

            if (result_stop == 'success' and result_start == 'success') or (
                    result_stop == 'inactive' and result_start == 'success'):
                return 'success'
            elif result_stop == 'uninstalled' or result_start == 'uninstalled':
                return 'uninstalled'
            elif result_stop == 'error' or result_start == 'error':
                return 'error'
        except Exception:
            logging.info(traceback.format_exc())

    def auto_start_service(self, service_name, state):

        '''
        set the service start auto or demand, or disable the service
        :param service_name: service's name
        :param state: service start state, auto or demand or disable
        :return: Null
        '''

        try:
            os.popen('sc config ' + service_name + 'state= ' + state)
            return None
        except Exception:
            logging.info(traceback.format_exc())

    def delete_service(self, service_name):

        '''
        delete an installed service with a cmd command
        :param service_name: service's name
        :return: delete result
        '''

        try:
            result_stop = self.stop_service(service_name)
            time.sleep(1)
            try:
                result_delete = os.popen('sc delete ' + service_name).read()
            except Exception:
                logging.info(traceback.format_exc())

            if (result_stop == 'success' and '成功' in result_delete) or (
                    result_stop == 'inactive' and '成功' in result_delete):
                return 'success'
            elif result_stop == 'uninstalled':
                return 'success'
            elif result_stop == 'error' and '成功' not in result_delete:
                return 'error'
        except Exception:
            logging.info(traceback.format_exc())

    def open_log(self, service_log):

        '''
        open log file of the service with a cmd command
        :param service_log: service's log address
        :return: Null
        '''

        try:
            os.system('notepad ' + service_log)
            return None
        except Exception:
            logging.info(traceback.format_exc())

    # wait to rewrite
    def open_file(self, log_file_address):

        '''
        open log folder of the service with a cmd command
        :param log_file_address: address of the log file folder
        :return: Null
        '''

        try:
            os.popen('start ' + os.path.abspath(log_file_address))
            return None
        except Exception:
            logging.info(traceback.format_exc())

    def open_setup(self, service_name, service_setup):

        '''
        add service into registry and service list
        :param service_name: service's name
        :param service_setup: address of setup file
        :return: Null
        '''

        try:
            os.popen('sc create ' + service_name + ' binPath= ' + service_setup)
            return None
        except Exception:
            logging.info(traceback.format_exc())
