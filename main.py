import logging
import sys

import psutil
import time
from bif.ocr.core_ocr import core_ocr
from bif.logger import log_level, logger

# CRITICAL
# FATAL
# ERROR
# WARNING
# WARN
# INFO
# DEBUG

log_level("INFO")


def check_if_process_running(process_name):
    """
    Check if there is any running process that contains the given name processName.
    :param process_name:
    :return:
    """
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def find_process_id_by_name(process_name):
    """
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    :param process_name:
    :return:
    """
    list_of_process_objects = []
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if process_name.lower() in pinfo['name'].lower():
                list_of_process_objects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return list_of_process_objects


def main():
    print("Running")

    proc = check_if_process_running("python")
    no_proc = 0
    if proc:
        no_proc = find_process_id_by_name("python")

    if len(no_proc) > 2:
        logger.info("Another python process is running. Will quit.")
        sys.exit()

    logger.info("Running core ocr")
    # FIXME
    #   Change Path to Correct Drive
    base_path = "E:\\"
    base_path = os.path.abspath(os.getcwd())
    core_ocr('config.json', 'TestBIFDB', base_path)
    logger.info("Ending program")


if __name__ == "__main__":
    main()
