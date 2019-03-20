# -*- coding: utf-8 -*-

#   2019/3/19 0019 上午 9:45     

__author__ = 'RollingBear'

import config

import os

from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox, QToolButton, QMenu, QAction, QGridLayout
from PyQt5.QtCore import Qt


class service_manamgement(QWidget):

    def __init__(self):
        super().__init__()

        self.conf = config.config('\\config\\config.ini')
        self.service_list = config.config('\\config\\service_name.ini')

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
        service_log.triggered.connect(lambda: on_click('log', str(service_log_address)))
        service_start_auto.triggered.connect(lambda: on_click('auto_start', service_name))
        service_start_demand.triggered.connect(lambda: on_click('auto_demand', service_name))
        service_disable.triggered.connect(lambda: on_click('disable', service_name))
        service_setup.triggered.connect(lambda: on_click('setup', service_setup_address))
        service_delete.triggered.connect(lambda: on_click('uninstall', service_name))

        def on_click(action, mes):

            if action == 'start':
                print(action, mes)
            elif action == 'stop':
                print(action, mes)
            elif action == 'restart':
                print(action, mes)
            elif action == 'log':
                print(action, mes)
                os.system('notepad ' + mes)
            elif action == 'auto_start':
                print(action, mes)
            elif action == 'auto_demand':
                print(action, mes)
            elif action == 'disable':
                print(action, mes)
            elif action == 'setup':
                print(action, mes)
            elif action == 'uninstall':
                print(action, mes)

    def paint_status(self, row, service_name):

        pass

    def center(self):
        geomotry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        geomotry.moveCenter(center_point)
        self.move(geomotry.topLeft())

    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()
