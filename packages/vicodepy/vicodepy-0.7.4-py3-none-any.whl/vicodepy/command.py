# ViCodePy - A video coder for psychological experiments
#
# Copyright (C) 2024 Esteban Milleret
# Copyright (C) 2024 Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

"""
ViCodePy
~~~~~~~~

Video coder in Python for Experimental Psychology

Usage:
  vicodepy [<path>]
  vicodepy -h | --help
"""

import os
import sys

from PySide6.QtWidgets import QApplication
from docopt import docopt

from .video import Video

usage = __doc__.split("\n\n")[2]


def main():
    """Entry point for the application"""
    args = docopt(usage, argv=sys.argv[1:])
    app = QApplication([])
    video = Video()
    video.show()
    video.resize(640, 480)
    if args["<path>"]:
        video.load_file(os.path.abspath(args["<path>"]))
    else:
        video.no_video_loaded()
    sys.exit(app.exec())
