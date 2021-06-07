from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from time import sleep
import time
from threading import Thread
import BlynkLib
import serial
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from gpiozero import LED

# Initialize Blynk
blynk = BlynkLib.Blynk('6NrT6x2zQwq_pzZmvZmt4K1UwqR5QTKe')

s=serial.Serial('/dev/ttyACM0',9600)
s.flush()
time.sleep(1)
data = s.readline().decode()

WIDTH = 128
HEIGHT = 32
BORDER = 5
oled_reset = None
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

motor = LED(23)
motor.off()

seleccion = 1
 
listaHumedad  = [0,0,0,0,0,0,0,0,0,0]
listaTemperatura = [0,0,0,0,0,0,0,0,0,0]
listaLuz = [0,0,0,0,0,0,0,0,0,0]
#def regar(luz, temp, hum):
    

def medirVariables(thread_name, thread_ID, thread_planta):
        while True:
            global listaHumedad, listaTemperatura, listaLuz, seleccion
            for j in range(10):
                if seleccion == 1 :
                    item = QtWidgets.QTableWidgetItem(listaHumedad[j])
                elif seleccion == 2:
                    item = QtWidgets.QTableWidgetItem(listaTemperatura[j])
                elif seleccion == 3:
                    item = QtWidgets.QTableWidgetItem(listaLuz[j])
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                thread_planta.tableWidget.setItem(j,1,item)
            #print (type(listaHumedad[0]))
            oled.fill(0)
            image = Image.new("1", (oled.width, oled.height))
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()
            if seleccion == 1 :
                    text = "Humedad="+str(listaHumedad[0]).rstrip()+"%"
            elif seleccion == 2:
                    text = "Temperatura="+str(listaTemperatura[0]).rstrip()+"°C"
            elif seleccion == 3:
                    text = "Lux="+str(listaLuz[0]).rstrip()+"%"
            text = text.rstrip()
            # Draw Some Text
            (font_width, font_height) = font.getsize(text)
            draw.text(
            (oled.width // 2 -font_width // 2, oled.height // 2 -font_height // 2),
            text,
            font=font,
            fill=255,
            )
            oled.image(image)
            oled.show()
            
            if int(float(listaLuz[0])) <= 20 and (int(float (listaTemperatura[0])) <= 25 or int(float(listaHumedad[0]))<= 30):
                if int(float(listaHumedad[0])) <= 70:
                    motor.on()
                else:
                    motor.off()
            else:
                motor.off()
        
            for i in range(9):
                listaHumedad[9-i]=listaHumedad[9-i-1]
                listaTemperatura[9-i]=listaTemperatura[9-i-1]
                listaLuz[9-i]=listaLuz[9-i-1]
            print(str(thread_name) +" "+ str(thread_ID));
            s.write(b"1")#Temperatura
            temp_value = s.readline().decode()
            listaTemperatura[0] = temp_value
            print("La temperatura es: "+temp_value)
            time.sleep(0.1)
            s.write(b"2")#Humedad
            humidity_value = s.readline().decode()
            listaHumedad[0] = humidity_value
            print("La humedad es: "+humidity_value)
            time.sleep(0.1)
            s.write(b"3")#Luminosidad
            lux_value = s.readline().decode()
            listaLuz[0] = lux_value
            print("La luminosidad es: "+lux_value)
            time.sleep(0.8)

def actualizarBlynk(thread_name, thread_ID):
        while True:
            blynk.run()
            
# Register Virtual Pin
@blynk.VIRTUAL_READ(2)
def my_read_handler():
     blynk.virtual_write(2, listaLuz[0])
     blynk.virtual_write(1, listaTemperatura[0])
     blynk.virtual_write(3, listaHumedad[0])

class Ui_Planta(object):
    def setupUi(self, Planta):
        Planta.setObjectName("Planta")
        Planta.resize(992, 649)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 191))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 106, 159))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 56, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(134, 197, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(196, 220, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 191))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 106, 159))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 56, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(134, 197, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(196, 220, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 191))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 106, 159))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 56, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 42, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(196, 220, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        Planta.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(Planta)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 971, 111))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setStyleSheet("background-color: rgb(207, 229, 255);")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/home/pi/Documents/Arq de computadoras/Final/humedadSinFondo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(100, 100))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setStyleSheet("background-color: rgb(207, 229, 255);")
        self.pushButton_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("/home/pi/Documents/Arq de computadoras/Final/temperatura.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(100, 100))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setStyleSheet("background-color: rgb(207, 229, 255);")
        self.pushButton_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("/home/pi/Documents/Arq de computadoras/Final/luminosidad.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QtCore.QSize(100, 100))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 140, 941, 418))
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(7, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(8, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(9, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(9, 1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(450)
        self.tableWidget.verticalHeader().setDefaultSectionSize(37)
        Planta.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Planta)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 992, 26))
        self.menubar.setObjectName("menubar")
        Planta.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Planta)
        self.statusbar.setObjectName("statusbar")
        Planta.setStatusBar(self.statusbar)

        self.retranslateUi(Planta)
        QtCore.QMetaObject.connectSlotsByName(Planta)

        self.tableWidget.setHorizontalHeaderLabels("Tiempo (s);Valor Humedad (%)".split(";"))
        for i in range(10):
            item = QtWidgets.QTableWidgetItem("Hace "+str((i+1))+" segundo")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,1,item)

    def retranslateUi(self, Planta):
        _translate = QtCore.QCoreApplication.translate
        Planta.setWindowTitle(_translate("Planta", "Sistema de riego App"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Planta", "Hace 1 segundo"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("Planta", "Hace 2 segundos"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("Planta", "Hace 3 segundos"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("Planta", "Hace 4 segundos"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("Planta", "Hace 5 segundos"))
        item = self.tableWidget.item(5, 0)
        item.setText(_translate("Planta", "Hace 6 segundos"))
        item = self.tableWidget.item(6, 0)
        item.setText(_translate("Planta", "Hace 7 segundos"))
        item = self.tableWidget.item(7, 0)
        item.setText(_translate("Planta", "Hace 8 segundos"))
        item = self.tableWidget.item(8, 0)
        item.setText(_translate("Planta", "Hace 9 segundos"))
        item = self.tableWidget.item(9, 0)
        item.setText(_translate("Planta", "Hace 10 segundos"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.pushButton.clicked.connect(self.onClicked1)
        self.pushButton_2.clicked.connect(self.onClicked2)
        self.pushButton_3.clicked.connect(self.onClicked3) 

    def onClicked1(self):
        global seleccion
        seleccion = 1
        self.tableWidget.setHorizontalHeaderLabels("Tiempo (s);Valor Humedad (%)".split(";"))

    def onClicked2(self):
        global seleccion
        seleccion = 2
        self.tableWidget.setHorizontalHeaderLabels("Tiempo (s);Valor Temperatura (°C)".split(";"))

    def onClicked3(self):
        global seleccion
        seleccion = 3
        self.tableWidget.setHorizontalHeaderLabels("Tiempo (s);Valor Luminosidad (%)".split(";"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Planta = QtWidgets.QMainWindow()
    ui = Ui_Planta()
    ui.setupUi(Planta)
    Planta.show()
    threadV = Thread(target = medirVariables, args=("Midiendo",1001, ui))
    threadB = Thread(target = actualizarBlynk, args= ("Blynkeando", 1002))
    threadV.start()
    threadB.start()
    sys.exit(app.exec_())
