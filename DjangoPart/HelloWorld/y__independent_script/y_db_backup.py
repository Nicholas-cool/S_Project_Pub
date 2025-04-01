"""
    数据库备份
"""

import os
import shutil
import datetime
import time


def do_db_backup():
    source_location = '../../../data.db'
    target_location = '../../../data_store'
    date_info = str(datetime.date.today()) + str(time.strftime("-%H-%M-%S"))

    # adding exception handling
    try:
        shutil.copy(source_location, target_location)
    except IOError as e:
        print("Unable to copy file. %s" % e)

    # rename the file
    old_name = target_location + '\\' + os.path.basename(source_location)
    new_name = target_location + '\\' + os.path.splitext(os.path.basename(source_location))[0] + date_info + \
        os.path.splitext(os.path.basename(source_location))[1]
    os.rename(old_name, new_name)


if __name__ == '__main__':
    do_db_backup()
