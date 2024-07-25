import os
import random
import time
import subprocess

from auto_nico.android.nico_android_element import NicoAndroidElement
from auto_nico.common.logger_config import logger
from auto_nico.common.runtime_cache import RunningCache
from auto_nico.common.send_request import send_tcp_request
from auto_nico.common.nico_basic import NicoBasic
from auto_nico.android.adb_utils import AdbUtils


class NicoAndroid(NicoBasic):
    def __init__(self, udid, port="random", **query):
        super().__init__(udid,  **query)
        self.udid = udid
        self.adb_utils = AdbUtils(udid)
        self.version = 1.2
        self.adb_utils.install_test_server_package(self.version)
        self.adb_utils.check_adb_server()
        self.__set_running_port(port)
        self.runtime_cache = RunningCache(udid)
        self.runtime_cache.set_initialized(True)
        rst = "200" in send_tcp_request(RunningCache(udid).get_current_running_port(), "print")
        if rst:
            logger.debug(f"{self.udid}'s test server is ready")
        else:
            logger.debug(f"{self.udid} test server disconnect, restart ")
            self.__init_adb_auto(RunningCache(udid).get_current_running_port())

        self.close_keyboard()

    def __set_running_port(self, port):
        exists_port = self.adb_utils.get_tcp_forward_port()
        if exists_port is None:
            logger.debug(f"{self.udid} no exists port")
            if port != "random":
                running_port = port
            else:
                random_number = random.randint(9000, 9999)
                running_port = random_number
        else:
            running_port = int(exists_port)
        RunningCache(self.udid).set_current_running_port(running_port)

    def __start_test_server(self):
        current_port = RunningCache(self.udid).get_current_running_port()
        logger.debug(
            f"""adb -s {self.udid} shell am instrument -r -w -e port {current_port} -e class nico.dump_hierarchy.HierarchyTest nico.dump_hierarchy.test/androidx.test.runner.AndroidJUnitRunner""")
        commands = f"""adb -s {self.udid} shell am instrument -r -w -e port {current_port} -e class nico.dump_hierarchy.HierarchyTest nico.dump_hierarchy.test/androidx.test.runner.AndroidJUnitRunner"""
        subprocess.Popen(commands, shell=True)
        for _ in range(10):
            response = send_tcp_request(current_port, "print")
            if "200" in response:
                logger.debug(f"{self.udid}'s test server is ready")
                break
            time.sleep(1)
        logger.debug(f"{self.udid}'s uiautomator was initialized successfully")

    def __init_adb_auto(self, port):
        self.adb_utils.set_tcp_forward_port(port)
        self.__start_test_server()

    def close_keyboard(self):
        adb_utils = AdbUtils(self.udid)
        ime_list = adb_utils.qucik_shell("ime list -s").split("\n")[0:-1]
        for ime in ime_list:
            adb_utils.qucik_shell(f"ime disable {ime}")

    def __call__(self, **query):
        current_port = RunningCache(self.udid).get_current_running_port()
        self.adb_utils.check_adb_server()
        rst = "200" in send_tcp_request(current_port, "print")
        if not rst:
            logger.debug(f"{self.udid} test server disconnect, restart ")
            self.adb_utils.install_test_server_package(self.version)
            self.__init_adb_auto(current_port)
            self.close_keyboard()
        NAE = NicoAndroidElement(**query)
        NAE.set_udid(self.udid)
        NAE.set_port(current_port)
        return NAE
