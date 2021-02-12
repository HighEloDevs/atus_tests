# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 17:10:06 2021

@author: Leonardo Eiji Tamayose & Guilherme Ferrari Fortino 

Main File

"""
import sys
from pathlib import Path

from PySide2 import QtGui, QtQml, QtCore

# from matplotlib_backend_qtquick.qt_compat import QtGui, QtQml, QtCore
from matplotlib_backend_qtquick.backend_qtquickagg import FigureCanvasQtQuickAgg
from src.MatPlotLib import DisplayBridge
from src.Model import Model

# Instantiating the display bridge || Global variable, fuck the world
displayBridge = DisplayBridge()

class Bridge(QtCore.QObject):
    # Instantiating the fit class
    model = Model() 

    # Signal fillDataTable
    fillDataTable = QtCore.Signal(str, str, str, str, str)

    # Signal fillParamsTable
    fillParamsTable = QtCore.Signal(str, str, str)

    # Signal to Properties page
    signalPropPage = QtCore.Signal()

    # Signal to write infos
    writeInfos = QtCore.Signal(str)

    @QtCore.Slot(str)
    def loadData(self, file_path):
        """Gets the path to data's file and fills the data's table"""
        self.model.load_data(QtCore.QUrl(file_path).toLocalFile())
        x, y, sy, sx = self.model.get_data()        

        # Getting file's name
        fileName = QtCore.QUrl(file_path).toLocalFile().split('/')[-1]
        if self.model.has_sx and self.model.has_sy:
            for i in range(len(x)):
                self.fillDataTable.emit("{:.2g}".format(x[i]), "{:.2g}".format(y[i]), "{:.2g}".format(sy[i]), "{:.2g}".format(sx[i]), fileName)
        elif self.model.has_sx:
            for i in range(len(x)):
                self.fillDataTable.emit("{:.2g}".format(x[i]), "{:.2g}".format(y[i]), "", "{:.2g}".format(sx[i]), fileName)
        elif self.model.has_sy:
            for i in range(len(x)):
                self.fillDataTable.emit("{:.2g}".format(x[i]), "{:.2g}".format(y[i]), "{:.2g}".format(sy[i]), "", fileName)
        else:
            for i in range(len(x)):
                self.fillDataTable.emit("{:.2g}".format(x[i]), "{:.2g}".format(y[i]), "", "", fileName)
        # print("Model: Data Loaded")

    @QtCore.Slot(str, str, str, int, int, int, int, int, int, str, int, str, str, int, str)
    def loadOptions(self, title, xaxis, yaxis, residuals, grid, sigma_x, sigma_y, log_x, log_y, symbol_color, symbol_size, symbol, curve_color, curve_thickness, curve_style):
        """Gets the input options and set them to the model"""
        # print("Título:", title)
        # print('Eixo X:', xaxis)
        # print('Eixo Y:', yaxis)
        # print('Resíduos:', residuals)
        # print('Grade:', grid)
        
        curveStyles = {
            'Sólido':'-',
            'Tracejado':'--',
            'Ponto-Tracejado':'-.'
            }

        symbols = {
            'Círculo':'o',
            'Triângulo':'^',
            'Quadrado':'s',
            'Pentagono':'p',
            'Octagono':'8',
            'Cruz':'P',
            'Estrela':'*',
            'Diamante':'d',
            'Produto':'x'
            }

        # Setting style of the plot
        self.model.set_title(title)
        self.model.set_x_axis(xaxis)
        self.model.set_y_axis(yaxis)
        displayBridge.setStyle(sigma_x, sigma_y, log_x, log_y, symbol_color, symbol_size, symbols[symbol], curve_color, curve_thickness, curveStyles[curve_style])

        # Making plot
        displayBridge.Plot(self.model, residuals, grid)

        # Filling paramsTable
        params = self.model.get_params()
        keys = list(params.keys())
            
        for i in range(len(keys)):
            self.fillParamsTable.emit(keys[i], "{:.8g}".format(params[keys[i]][0]), "{:.8g}".format(params[keys[i]][1]))

        # Writing infos
        self.writeInfos.emit(self.model.report_fit)
    
    @QtCore.Slot(str, str)
    def loadExpression(self, expression, p0):
        """Gets the expression and set it up"""
        # print("Expressão:", expression)
        # print("Parâmetros Iniciais:", p0)

        p0_tmp = list()
        if p0 != '':
            for i in p0.split(','):
                p0_tmp.append(float(i))
            self.model.set_p0(p0_tmp)
        
        self.model.set_expression(expression)
        self.signalPropPage.emit()

    @QtCore.Slot(str)
    def savePlot(self, save_path):
        """Gets the path from input and save the actual plot"""
        displayBridge.figure.savefig(QtCore.QUrl(save_path).toLocalFile(), dpi = 400)

if __name__ == "__main__":
    # Matplotlib stuff
    QtQml.qmlRegisterType(FigureCanvasQtQuickAgg, "Backend", 1, 0, "FigureCanvas")
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    # Setting up app
    app = QtGui.QGuiApplication(sys.argv)
    app.setOrganizationName("High Elo Devs")
    app.setOrganizationDomain("https://www.instagram.com/guiiiferrari/")
    app.setApplicationName("Analysis Tool for Undergrad Students")
    engine = QtQml.QQmlApplicationEngine()

    # Creating bridge
    bridge = Bridge()

    # Expose the Python object to QML
    context = engine.rootContext()
    context.setContextProperty("displayBridge", displayBridge)

    # Creating 'link' between front-end and back-end
    engine.rootContext().setContextProperty("funcsPlotPage", bridge)
    engine.rootContext().setContextProperty("funcsPropPage", bridge)
    engine.rootContext().setContextProperty("funcsAjustePage", bridge)
    
    # Loading QML files
    qmlFile = Path(Path.cwd(), Path(__file__).parent, "qml/main.qml")
    engine.load(QtCore.QUrl.fromLocalFile(str(qmlFile)))

    # Updating canvasPlot with the plot
    win = engine.rootObjects()[0]
    displayBridge.updateWithCanvas(win.findChild(QtCore.QObject, "canvasPlot"))
    
    # Stopping program if PySide fails loading the file
    if not engine.rootObjects():
        sys.exit(-1)    

    # Starting program
    sys.exit(app.exec_())