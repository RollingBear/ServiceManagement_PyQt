# -*- coding: utf-8 -*-

#   2019/3/19 0019 上午 9:45     

__author__ = 'RollingBear'

import config
import system_service

import os
import time

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox, QPushButton, QToolButton, QMenu, QAction, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class service_manamgement(QWidget):

    def __init__(self):

        '''
        Initialization the service management
        '''

        super().__init__()

        self.conf = config.config('\\config\\config.ini')
        self.service_list = config.config('\\config\\service_name.ini')

        self.len_count = self.service_list.outer_element_count()

        self.red_img = QPixmap(self.conf.get('image_address').red)
        self.green_img = QPixmap(self.conf.get('image_address').green)
        self.yellow_img = QPixmap(self.conf.get('image_address').yellow)
        self.logo_img = QPixmap(self.conf.get('image_address').logo)
        self.message_img = QPixmap(self.conf.get('image_address').message)

        self.system_svc = system_service.system_service()

        self.init_ui()

    def init_ui(self):

        '''
        Initialization the service management UI
        :return: None
        '''

        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(10)

        for i in range(self.len_count):
            service_display_name = self.service_list.get('service_' + str(i + 1)).service_display_name
            service_name = self.service_list.get('service_' + str(i + 1)).service_name
            service_log = self.service_list.get('service_' + str(i + 1)).service_log
            service_setup = self.service_list.get('service_' + str(i + 1)).service_setup

            if service_log == 'Null':
                service_log = None
            else:
                service_log = os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + (
                        '.' * service_log.count('..\\'))) + '\\' + service_log.replace('..\\', '')

            service_setup = os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + (
                    '.' * service_setup.count('..\\'))) + '\\' + service_setup.replace('..\\', '')

            self.paint_tool_button(i, service_display_name, service_name, service_log, service_setup)

            self.get_state(i, service_name)

        self.mes_label = QLabel(self)
        self.mes_label.setPixmap(self.message_img)
        self.grid.addWidget(self.mes_label, self.len_count + 1, 0, 1, 3)

        log_address = self.conf.get('file_address').log_file_address
        self.paint_button('open file', self.len_count + 2, 0, self.system_svc.open_file, log_address)
        self.paint_button('start all', self.len_count + 2, 1, self.state_operate, 'start')
        self.paint_button('stop all', self.len_count + 2, 2, self.state_operate, 'stop')

        self.center()
        self.setWindowTitle('Service Management')

        self.show()

    def paint_tool_button(self, row, service_display_name, service_name, service_log_address, service_setup_address):

        '''
        Packaging the tool button paint to reduce code quantity
        :param row: the number of rows in which the button is located
        :param service_display_name: the service's name which to display
        :param service_name: service's name
        :param service_log_address: the address of the log file for the service
        :param service_setup_address: the address of the installation document for the service
        :return: None
        '''

        self.tool_button = QToolButton(self)
        self.tool_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tool_button.setToolTip('Select a action to perform')
        self.tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        self.tool_button.setText(service_display_name)
        self.tool_button.setAutoRaise(True)
        self.grid.addWidget(self.tool_button, row, 0)

        tb_menu = QMenu()

        start_service = QAction('Start Service', self)
        stop_service = QAction('Stop Service', self)
        restart_service = QAction('ReStart Service', self)
        service_log = QAction('Open Service Log', self)
        service_start_auto = QAction('Set Service Start Auto', self)
        service_start_demand = QAction('Set Service Start Demand', self)
        service_disable = QAction('Set Service Disable', self)
        service_setup = QAction('Setup the Service', self)
        service_delete = QAction('Uninstall the Service', self)

        tb_menu.addAction(start_service)
        tb_menu.addAction(stop_service)
        tb_menu.addAction(restart_service)
        tb_menu.addSeparator()
        tb_menu.addAction(service_log)
        tb_menu.addSeparator()
        tb_menu.addAction(service_start_auto)
        tb_menu.addAction(service_start_demand)
        tb_menu.addAction(service_disable)
        tb_menu.addSeparator()
        tb_menu.addAction(service_setup)
        tb_menu.addAction(service_delete)

        self.tool_button.setMenu(tb_menu)

        start_service.triggered.connect(lambda: on_click(row, 'start', service_name))
        stop_service.triggered.connect(lambda: on_click(row, 'stop', service_name))
        restart_service.triggered.connect(lambda: on_click(row, 'restart', service_name))
        service_log.triggered.connect(lambda: on_click(row, 'log', service_log_address))
        service_start_auto.triggered.connect(lambda: on_click(row, 'auto_start', service_name))
        service_start_demand.triggered.connect(lambda: on_click(row, 'auto_demand', service_name))
        service_disable.triggered.connect(lambda: on_click(row, 'disable', service_name))
        service_setup.triggered.connect(lambda: on_click(row, 'setup', service_setup_address, service_name))
        service_delete.triggered.connect(lambda: on_click(row, 'uninstall', service_name))

        def on_click(row, action, mes, param=None):

            '''
            Button click event control
            :param row: the number of rows in which the button is located
            :param action: set tool button event name
            :param mes: param of event
            :param param: param of event
            :return:
            '''

            result = None

            if action == 'start' or action == 'stop':
                step = self.system_svc.service_state_operate(mes, action)
                if step != 'uninstalled' and step != 'active' and step != 'inactive':
                    time.sleep(0.5)
                    result = self.system_svc.get_service_state(mes)
                else:
                    result = step
            elif action == 'restart':
                step = self.system_svc.restart_service(mes)
                if step != 'uninstalled':
                    time.sleep(0.5)
                    result = self.system_svc.get_service_state(mes)
                else:
                    result = step
            elif action == 'log':
                result = self.system_svc.open_log(mes)
            elif action == 'auto_start' or action == 'auto_demand' or action == 'disable':
                result = self.system_svc.auto_start_service(mes, action)
            elif action == 'setup':
                result = self.system_svc.open_setup(param, mes)
            elif action == 'uninstall':
                result = self.system_svc.delete_service(mes)

            self.state_pic.deleteLater()
            self.state_label.deleteLater()
            self.get_state(row, mes)

            if result == 'uninstalled':
                QMessageBox.about(self, 'Error', 'Service uninstalled')
            else:
                if action == 'log' or action == 'auto_start' or action == 'setup':
                    QMessageBox.about(self, 'result', 'Executed operation')
                elif action == 'start' or action == 'stop' or action == 'restart':
                    if result == 'active' and action == 'start':
                        QMessageBox.about(self, 'result', '{name} has already started'.format(name=mes))
                    elif result == 'active' and action == 'stop':
                        QMessageBox.about(self, 'Error', '{name} stop error'.format(name=mes))
                    elif result == 'inactive' and action == 'stop':
                        QMessageBox.about(self, 'result', '{name} has already stopped'.format(name=mes))
                    elif result == 'inactive' and action == 'start':
                        QMessageBox.about(self, 'Error', '{name} start error'.format(name=mes))
                    elif result == 'success' or result == 'error':
                        QMessageBox.about(self, 'result',
                                          '{name} {state} {result}'.format(name=mes, state=action, result=result))
                elif action == 'delete':
                    QMessageBox.about(self, 'result',
                                      '{name} {state} {result}'.format(name=mes, state=action, result=result))

    def get_state(self, row, service_name):

        '''
        Get service's state
        :param row: the number of rows in which the message is located
        :param service_name: service's name
        :return: None
        '''

        state = self.system_svc.get_service_state(service_name)
        mes = 'Initialization'
        pic = self.red_img

        if state == 'active':
            mes = '已启动'
            pic = self.green_img
        elif state == 'inactive':
            mes = '未启动'
            pic = self.red_img
        elif state == 'uninstalled':
            mes = '未安装'
            pic = self.yellow_img

        self.state_pic = QLabel(self)
        self.state_pic.setPixmap(pic)
        self.grid.addWidget(self.state_pic, row, 1)

        self.state_label = QLabel(mes, self)
        self.grid.addWidget(self.state_label, row, 2)

    def paint_button(self, btn_name, row, column, function, *args, **kwargs):

        '''
        Packaging the button paint to reduce code quantity
        :param btn_name: button's name
        :param row: the number of rows in which the button is located
        :param column: the number of columns in which the button is location
        :param function: the function which linked to the button
        :param args: button-linked-function's params
        :param kwargs: button-linked-function's params
        :return: None
        '''

        button = QPushButton(btn_name, self)
        button.setCheckable(False)
        self.grid.addWidget(button, row, column)

        button.clicked.connect(lambda: function(*args, **kwargs))

    def center(self):

        '''
        Set the window center of screen
        :return: None
        '''

        geomotry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        geomotry.moveCenter(center_point)
        self.move(geomotry.topLeft())

    def closeEvent(self, QCloseEvent):

        '''
        Show a message box when close the window
        :param QCloseEvent:
        :return: None
        '''

        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def state_operate(self, state):

        '''
        The function which used to link to the button
        :param state: use to distinction different operate
        :return: None
        '''

        success_count = 0
        uninstall_count = 0
        error_count = 0
        already_count = 0

        for i in range(self.len_count):
            result = self.system_svc.service_state_operate(self.service_list.get('service_' + str(i + 1)).service_name,
                                                           state)
            if result == 'success':
                success_count += 1
            elif result == 'uninstalled':
                uninstall_count += 1
            elif result == 'error':
                error_count += 1
            elif result == 'active' or result == 'inactive':
                already_count += 1

            self.get_state(i, self.service_list.get('service_' + str(i + 1)).service_name)

        QMessageBox.about(self, 'result',
                          '{success_count}/{totality_count} have successful {state}\n'
                          '{uninstall_count}/{totality_count} uninstalled\n'
                          '{error_count}/{totality_count} {state} error\n'
                          '{already_count}/{totality_count} already {state}'.format(
                              success_count=success_count, uninstall_count=uninstall_count,
                              error_count=error_count, already_count=already_count,
                              totality_count=self.len_count, state=state))
