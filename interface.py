# -*- coding: utf-8 -*-

#   2019/3/19 0019 上午 9:45     

__author__ = 'RollingBear'

import config
import system_service

import os

from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox, QPushButton, QToolButton, QMenu, QAction, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class service_manamgement(QWidget):

    def __init__(self):
        super().__init__()

        self.conf = config.config('\\config\\config.ini')
        self.service_list = config.config('\\config\\service_name.ini')

        self.red_img = QPixmap(self.conf.get('image_address').red)
        self.green_img = QPixmap(self.conf.get('image_address').green)
        self.yellow_img = QPixmap(self.conf.get('image_address').yellow)
        self.logo_img = QPixmap(self.conf.get('image_address').logo)
        self.message_img = QPixmap(self.conf.get('image_address').message)

        self.system_svc = system_service.system_service()

        self.init_ui()

    def init_ui(self):

        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(10)

        for i in range(self.service_list.outer_element_count()):
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

        log_address = self.conf.get('file_address').log_file_address
        self.paint_button('open file',
                          self.service_list.outer_element_count() + 1,
                          0,
                          self.system_svc.open_file,
                          log_address)
        self.paint_button('start all',
                          self.service_list.outer_element_count() + 1,
                          1,
                          self.state_operate,
                          'start')
        self.paint_button('stop all',
                          self.service_list.outer_element_count() + 1,
                          2,
                          self.state_operate,
                          'stop')

        self.center()
        self.setWindowTitle('Service Management')

        self.show()

    def paint_tool_button(self, row, service_display_name, service_name, service_log_address, service_setup_address):

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

        start_service.triggered.connect(lambda: on_click('start', service_name))
        stop_service.triggered.connect(lambda: on_click('stop', service_name))
        restart_service.triggered.connect(lambda: on_click('restart', service_name))
        service_log.triggered.connect(lambda: on_click('log', service_log_address))
        service_start_auto.triggered.connect(lambda: on_click('auto_start', service_name))
        service_start_demand.triggered.connect(lambda: on_click('auto_demand', service_name))
        service_disable.triggered.connect(lambda: on_click('disable', service_name))
        service_setup.triggered.connect(lambda: on_click('setup', service_setup_address, service_name))
        service_delete.triggered.connect(lambda: on_click('uninstall', service_name))

        def on_click(action, mes, param):

            if action == 'start' or action == 'stop':
                result = self.system_svc.service_state_operate(mes, action)
            elif action == 'restart':
                result = self.system_svc.restart_service(mes)
            elif action == 'log':
                result = self.system_svc.open_log(mes)
            elif action == 'auto_start' or action == 'auto_demand' or action == 'disable':
                result = self.system_svc.auto_start_service(mes, action)
            elif action == 'setup':
                result = self.system_svc.open_setup(param, mes)
            elif action == 'uninstall':
                result = self.system_svc.delete_service(mes)

            if result == None:
                QMessageBox.information(self, 'result', 'result', QMessageBox.Yes)
            elif action == 'start' or action == 'stop':
                QMessageBox.information(self, 'result',
                                        '{name} {state} {result}'.format(name=mes, state=action, result=result),
                                        QMessageBox.Yes)

    def get_state(self, row, service_name):

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

        button = QPushButton(btn_name, self)
        button.setCheckable(False)
        self.grid.addWidget(button, row, column)

        button.clicked.connect(lambda: function(*args, **kwargs))

    def center(self):
        geomotry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        geomotry.moveCenter(center_point)
        self.move(geomotry.topLeft())

    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def state_operate(self, state):

        success_count = 0
        uninstall_count = 0
        error_count = 0
        already_count = 0

        totality_count = self.service_list.outer_element_count()

        for i in range(totality_count):
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

        QMessageBox.information(self, 'result',
                                '{success_count}/{totality_count} have successful {state}\n'
                                '{uninstall_count}/{totality_count} uninstalled\n'
                                '{error_count}/{totality_count} {state} error\n'
                                '{already_count}/{totality_count} already {state}'.format(
                                    success_count=success_count, uninstall_count=uninstall_count,
                                    error_count=error_count, already_count=already_count,
                                    totality_count=totality_count, state=state),
                                QMessageBox.Yes)
