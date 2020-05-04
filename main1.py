from PyQt5.QtWidgets import QMainWindow
import sys
from Qt import *
from StormClimb import stormClimb
from EBCclimb import EBCclimb
from ETtodayClimb import ETtodayClimb
from udnClimb import udnClimb
from BBCnewsClimb import BBCclimb
from chinatimeClimb import chinatimeClimb
from TVBSclimb import TVBSclimb
from todayClimb import todayClimb
from pchome import pchome
from CW import CW
from crossing_news import crossing_news
from hket_news import hket_news
from liberty_times import liberty_times
from line import line
from dcard import dcard
from tech_news import tech_news
from set_news import  set_news
from pttGossip import pttGossip
from pttMoney import pttMoney
from QCandyUi import CandyWindow
from QCandyUi.CandyWindow import colorful
# @colorful('blue')
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self , parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.label_news.setText('keyword')  # 我要怎麼讓一開始是空白
        # comboBOx
        choice = ['ALL','EBC(1頁30筆)','Storm(1頁16筆)','ETtoday(1頁20筆)','udn(1頁20筆)','BBC(1頁10筆)','中時(1頁20筆)',
        'ptt八卦版(1頁20筆)','ptt省錢版(1頁20筆)','TVBS(1頁25筆)','今周刊(1頁10筆)','pchome','天下雜誌','換日線','hket_news','自由時報(請輸入筆數)','line新聞',
        'tech_news','Dcard(僅輸入關鍵字)','三立新聞']
        self.comboBox.addItems(choice)
        self.comboBox.currentIndexChanged.connect(self.display)
        self.display()

    def display(self):
        self.label_news.setText(self.comboBox.currentText())

    def but_start(self):
        keyword = self.lineEdit_keyword.text()
        pagenum = self.lineEdit_page.text()
        if self.comboBox.currentText() == 'ALL':
            stormClimb(int(pagenum)+1, keyword)
            EBCclimb(int(pagenum)+1,keyword)
            ETtodayClimb(int(pagenum)+1,keyword)
            udnClimb(int(pagenum)+1,keyword)
            BBCclimb(int(pagenum),keyword)
            chinatimeClimb(int(pagenum)+1,keyword)
            pttGossip(int(pagenum)+1, keyword)
            pttMoney(int(pagenum)+1, keyword)
            TVBSclimb(int(pagenum)+1,keyword)
            todayClimb(int(pagenum)+1,keyword)
            pchome(int(pagenum)+1,keyword)
            crossing_news(int(pagenum)+1,keyword)
            CW(int(pagenum)+1,keyword)
            hket_news(int(pagenum)+1,keyword)
            liberty_times(int(pagenum)+1,keyword)
            line(int(pagenum)+1,keyword)
            tech_news(int(pagenum)+1,keyword)
            dcard(keyword)
            set_news(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'Storm(1頁16筆)':
            stormClimb(int(pagenum)+1, keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'EBC(1頁30筆)':
            EBCclimb(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'ETtoday(1頁20筆)':
            ETtodayClimb(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'udn(1頁20筆)':
            udnClimb(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'BBC(1頁10筆)':
            BBCclimb(int(pagenum),keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == '中時(1頁20筆)':
            chinatimeClimb(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'ptt八卦版(1頁20筆)':  
            pttGossip(int(pagenum)+1, keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'ptt省錢版(1頁20筆)':  
            pttMoney(int(pagenum)+1, keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'TVBS(1頁25筆)':  
            TVBSclimb(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == '今周刊(1頁10筆)':
            todayClimb(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'pchome':
            pchome(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == '天下雜誌':
            CW(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == '換日線':
            crossing_news(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'hket_news':
            hket_news(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == '自由時報(請輸入筆數)':
            liberty_times(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'line新聞':
            line(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'tech_news':
            tech_news(int(pagenum)+1,keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == 'Dcard(僅輸入關鍵字)':
            dcard(keyword)
            self.label_news.setText('done!')
        if self.comboBox.currentText() == '三立新聞':
            set_news(int(pagenum)+1,keyword)
            self.label_news.setText('done!')

    def initUI(self):
        self.pushButton_start.clicked.connect(self.but_start)

if __name__ == "__main__":
    """
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    win = QtWidgets.QMainWindow()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec_())
    """
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    # win = MainWindow()
    win = CandyWindow.createWindow(mainWindow, 'blueGreen')
    win.setWindowTitle('C r a w l e r')
    win.show()
    sys.exit(app.exec_())