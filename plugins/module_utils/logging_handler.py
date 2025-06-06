# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Custom rotating file handler for OpenManage"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from datetime import datetime
from logging.handlers import RotatingFileHandler


class CustomRotatingFileHandler(RotatingFileHandler):
    def rotation_filename(self, default_name):
        """
        Modify the filename of a log file when rotating.
        :param default_name: The default name of the log file.
        """
        src_file_name = default_name.split('.')
        dest_file_name = "{0}_{1}.{2}.{3}".format(
            src_file_name[0], '{0:%Y%m%d}'.format(datetime.now()),
            src_file_name[1], src_file_name[2]
        )
        return dest_file_name
