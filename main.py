# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 11:59:27 2021

@author: Leonardo Eiji Tamayose & Guilherme Ferrari Fortino 
"""

# =============================================================================
# import numpy as np
# import matplotlib.pyplot as plt
# from lmfit.models import ExpressionModel
# from lmfit import Parameters
# =============================================================================

import sys
from src.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtGui, QtCore
import qdarkstyle


def main():
    # Initializing App
    app = QApplication(sys.argv)
    
    # Setting Style
    app.setStyle('Fusion')
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    
    # Opening Main Window
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()      