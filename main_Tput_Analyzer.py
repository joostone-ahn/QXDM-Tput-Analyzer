import msg_load
import msg_filter
import msg_convert
import sys
import csv
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtGui

BoldFont = QtGui.QFont()
BoldFont.setBold(True)

CourierNewFont = QtGui.QFont()
CourierNewFont.setFamily("Courier New")

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('ENDC Tput Decoder v.2.0')
        self.setGeometry(110, 50, 1700, 800)
        self.show()

        self.open_btn = QPushButton("Open")
        self.open_btn.setFixedWidth(100)
        self.open_btn.setCheckable(False)
        self.LBL_OPENED =QLabel()
        self.open_btn.clicked.connect(self.open_msg)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.open_btn)
        hbox1.addWidget(self.LBL_OPENED)
        hbox1.addStretch()

        self.LBL_LINK = QLabel(" Tput : ")
        self.LBL_LINK.setFixedWidth(50)
        self.Link_1 = QCheckBox("Downlink")
        self.Link_2 = QCheckBox("Uplink")
        self.Link_1.toggle()

        self.Link_1.stateChanged.connect(self.changed)
        self.Link_2.stateChanged.connect(self.changed)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.LBL_LINK)
        hbox3.addWidget(self.Link_1)
        hbox3.addWidget(self.Link_2)
        hbox3.addStretch()

        self.LBL_NR = QLabel(" NR : ")
        self.LBL_NR.setFixedWidth(50)
        self.NR_2 = QCheckBox("BLER")
        self.NR_3 = QCheckBox("MCS")
        self.NR_4 = QCheckBox("RB")
        self.NR_5 = QCheckBox("TB")
        self.NR_2.stateChanged.connect(self.changed)
        self.NR_3.stateChanged.connect(self.changed)
        self.NR_4.stateChanged.connect(self.changed)
        self.NR_5.stateChanged.connect(self.changed)


        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.LBL_NR)
        hbox4.addWidget(self.NR_2)
        hbox4.addWidget(self.NR_3)
        hbox4.addWidget(self.NR_4)
        hbox4.addWidget(self.NR_5)
        hbox4.addStretch()

        self.LBL_LTE = QLabel(" LTE : ")
        self.LBL_LTE.setFixedWidth(50)
        self.LTE_2 = QCheckBox("BLER")
        self.LTE_3 = QCheckBox("MCS")
        self.LTE_4 = QCheckBox("RB")
        self.LTE_5 = QCheckBox("TB")
        self.LTE_2.stateChanged.connect(self.changed)
        self.LTE_3.stateChanged.connect(self.changed)
        self.LTE_4.stateChanged.connect(self.changed)
        self.LTE_5.stateChanged.connect(self.changed)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.LBL_LTE)
        hbox5.addWidget(self.LTE_2)
        hbox5.addWidget(self.LTE_3)
        hbox5.addWidget(self.LTE_4)
        hbox5.addWidget(self.LTE_5)
        hbox5.addStretch()

        self.Save_btn = QPushButton("Save as .csv")
        self.Save_btn.setFixedWidth(120)
        self.Save_btn.setCheckable(False)
        self.Save_btn.setDisabled(True)
        self.LBL_SAVE = QLabel("")
        self.Save_btn.clicked.connect(self.save)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(self.Save_btn)
        hbox6.addWidget(self.LBL_SAVE)
        hbox6.addStretch()

        msg_all_1 = ''
        self.te1 = QTextEdit()
        self.te1.setAcceptRichText(False)
        self.te1.setFixedHeight(150)
        self.te1.setFont(CourierNewFont)
        self.te1.textChanged.connect(self.pasted)

        msg_all_2 = ''
        self.te2 = QTextEdit()
        self.te2.setAcceptRichText(False)
        self.te2.setFixedHeight(400)
        self.te2.setFont(CourierNewFont)

        self.note1 = QLabel("Please open a log file(.txt) or paste real-time logs to analyze")
        self.note2 = QLabel("Please select items that you want to analyze")
        self.note3 = QLabel("")
        self.note1.setFont(BoldFont)
        self.note2.setFont(BoldFont)
        self.note3.setFont(BoldFont)
        self.note3.setFont(CourierNewFont)

        self.Exe_btn = QPushButton("Execute")
        self.Exe_btn.setFixedWidth(120)
        self.Exe_btn.setCheckable(False)
        self.Exe_btn.setDisabled(True)
        self.Exe_btn.clicked.connect(self.execute)

        vbox = QVBoxLayout()
        vbox.addWidget(self.note1)
        vbox.addLayout(hbox1)
        vbox.addWidget(QLabel("NR logs (QXDM5 > View > QSH > Filtered Views-Analysis > QSH Analysis-All)"))
        vbox.addWidget(self.te1)
        vbox.addWidget(QLabel())
        vbox.addWidget(self.note2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addWidget(self.Exe_btn)
        vbox.addWidget(QLabel())
        vbox.addWidget(self.note3)
        vbox.addWidget(self.te2)
        vbox.addLayout(hbox6)
        vbox.addWidget(QLabel())

        vbox.addStretch()
        self.setLayout(vbox)

    @pyqtSlot()
    def open_msg(self):
        self.te1.clear()
        self.te2.clear()
        self.note3.clear()

        self.msg_all = []
        fname = QFileDialog.getOpenFileName(self,'Load file','',"Text files(*.txt)")
        if fname[0]:
            f = open(fname[0],'rt',encoding='UTF8') #https://m.blog.naver.com/yejoon3117/221058408177
            with f:
                try:
                    self.msg_all = f.readlines()
                except:
                    print("read fail")
                for n in range(len(self.msg_all)):
                    self.msg_all[n] = self.msg_all[n].replace('\n', '')

        self.msg_filtered = msg_load.process(self.msg_all)

        for n in self.msg_filtered:
            self.te1.append(n)

        self.Exe_btn.setEnabled(True)
        self.Save_btn.setDisabled(True)
        self.LBL_OPENED.setText(fname[0])
        self.LBL_SAVE.setText("")

        if self.Link_1.isChecked() == False:
            self.Link_1.toggle()

    @pyqtSlot()
    def pasted(self):
        self.te2.clear()
        self.note3.clear()

        self.Exe_btn.setEnabled(True)
        self.Save_btn.setDisabled(True)
        self.LBL_OPENED.setText("")
        self.LBL_SAVE.setText("")

        if self.Link_1.isChecked() == False:
            self.Link_1.toggle()

        if self.te1.toPlainText() == '':
            self.Exe_btn.setDisabled(True)

    @pyqtSlot()
    def changed(self):
        if self.te1.toPlainText():
            self.Exe_btn.setEnabled(True)
            self.LBL_SAVE.setText("")

    @pyqtSlot()
    def execute(self):

        self.te2.clear()
        msg_all_str = self.te1.toPlainText()
        msg_all = msg_all_str.split('\n')

        msg_filtered = msg_filter.process(msg_all)
        # self.msg_rst = msg_convert.process(msg_filtered)
        self.msg_rst, self.CA_max, self.ENDC = msg_convert.process(msg_filtered)

        # print(self.CA_max)
        # print(self.ENDC)

        msg_title = []
        msg_title.append("TIME")
        if self.Link_1.isChecked():
            if self.ENDC == True:
                msg_title.append("DL_ENDC_Tput")
            for n in range(self.CA_max['DL_NR']+1):
                msg_title.append("DL_NR_" + str(n) + "_Tput")
            if self.ENDC == True:
                for n in range(self.CA_max['DL_LTE']+1):
                    msg_title.append("DL_LTE_" + str(n) + "_Tput")
        if self.Link_2.isChecked():
            if self.ENDC == True:
                msg_title.append("UL_ENDC_Tput")
            for n in range(self.CA_max['UL_NR']+1):
                msg_title.append("UL_NR_" + str(n) + "_Tput")
            if self.ENDC == True:
                for n in range(self.CA_max['UL_LTE']+1):
                    msg_title.append("UL_LTE_" + str(n) + "_Tput")

        if self.Link_1.isChecked():
            for n in range(self.CA_max['DL_NR']+1):
                if self.NR_2.isChecked():
                    msg_title.append("DL_NR_" + str(n) +"_BLER")
                if self.NR_3.isChecked():
                    msg_title.append("DL_NR_" + str(n) + "_MCS")
                if self.NR_4.isChecked():
                    msg_title.append("DL_NR_" + str(n) + "_RB")
                if self.NR_5.isChecked():
                    msg_title.append("DL_NR_" + str(n) + "_TB")
            if self.ENDC == True:
                for n in range(self.CA_max['DL_LTE']+1):
                    if self.LTE_2.isChecked():
                        msg_title.append("DL_LTE_" + str(n) +"_BLER")
                    if self.LTE_3.isChecked():
                        msg_title.append("DL_LTE_" + str(n) + "_MCS")
                    if self.LTE_4.isChecked():
                        msg_title.append("DL_LTE_" + str(n) + "_RB")
                    if self.LTE_5.isChecked():
                        msg_title.append("DL_LTE_" + str(n) + "_TB")

        if self.Link_2.isChecked():
            for n in range(self.CA_max['UL_NR']+1):
                if self.NR_2.isChecked():
                    msg_title.append("UL_NR_" + str(n) +"_BLER")
                if self.NR_3.isChecked():
                    msg_title.append("UL_NR_" + str(n) + "_MCS")
                if self.NR_4.isChecked():
                    msg_title.append("UL_NR_" + str(n) + "_RB")
                if self.NR_5.isChecked():
                    msg_title.append("UL_NR_" + str(n) + "_TB")
            if self.ENDC == True:
                for n in range(self.CA_max['UL_LTE']+1):
                    if self.LTE_2.isChecked():
                        msg_title.append("UL_LTE_" + str(n) +"_BLER")
                    if self.LTE_3.isChecked():
                        msg_title.append("UL_LTE_" + str(n) + "_MCS")
                    if self.LTE_4.isChecked():
                        msg_title.append("UL_LTE_" + str(n) + "_RB")
                    if self.LTE_5.isChecked():
                        msg_title.append("UL_LTE_" + str(n) + "_TB")

        # print(msg_title)

        self.msg_save = []
        for i in self.msg_rst:
            msg_save_item =[]
            for n in range(len(msg_title)):
                if 'ENDC' in msg_title[n]:
                    endc_sum = 0
                    if 'DL' in msg_title[n]:
                        for m in range(1, self.CA_max['DL_NR'] + self.CA_max['DL_LTE'] + 3):
                            if msg_title[n+m] in i:
                                endc_sum += i[msg_title[n + m]]
                            else:
                                endc_sum += 0
                    elif 'UL' in msg_title[n]:
                        for m in range(1, self.CA_max['UL_NR'] + self.CA_max['UL_LTE'] + 3):
                            if msg_title[n+m] in i:
                                endc_sum += i[msg_title[n + m]]
                            else:
                                endc_sum += 0
                    msg_save_item.append(endc_sum)
                else:
                    if msg_title[n] in i:
                        msg_save_item.append(i[msg_title[n]])
                    else:
                        msg_save_item.append("")
            self.msg_save.append(msg_save_item)


        result = []
        for n in self.msg_save:
            result_item = ''
            for i in n:
                if type(i) == datetime.datetime:
                    result_item += f"{i.strftime('%H:%M:%S.%f')[:-3]:<13}" + ' |'
                else:
                    result_item += f'{str(i):>15}' +' |'
            result.append(result_item)

        result_title = ''
        for n in msg_title:
            if n == 'TIME':
                result_title += f"{' '+n:<14}" +' |'
            else:
                result_title += f'{n:>15}' +' |'

        self.note3.setText(result_title)
        for n in result:
            self.te2.append(n)

        self.msg_save.insert(0, msg_title)
        # for n in self.msg_save:
        #     print(n)

        self.Exe_btn.setDisabled(True)
        self.Save_btn.setEnabled(True)
        self.LBL_SAVE.setText("")

    @pyqtSlot()
    def save(self):

        save_path = QFileDialog.getSaveFileName(self, 'Save file', '', "CSV files(*.csv)")
        fp = open(save_path[0], "w",newline='')
        wr = csv.writer(fp)
        for i in self.msg_save:
            wr.writerow(i)
        fp.close()
        self.LBL_SAVE.setText(" " + save_path[0])
        self.Exe_btn.setEnabled(True)
        self.Save_btn.setDisabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())