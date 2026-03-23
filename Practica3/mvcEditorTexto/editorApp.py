# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:03:07 2026

@author: rgalan
"""

import sys
from PyQt5.QtWidgets import QApplication
from editorVista import Vista

app=QApplication([])
vista=Vista()
vista.show()
    
sys.exit(app.exec_())