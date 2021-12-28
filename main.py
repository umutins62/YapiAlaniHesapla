import sys
import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QTableWidget, \
    QHeaderView, QGroupBox, QComboBox, QTableWidgetItem, QCheckBox, QFileDialog

class yaklasikmaliyet(QWidget):


    def __init__(self):
        super().__init__()
        self.setUI()


    def setUI(self):
        self.setWindowTitle("Yapı Yaklaşık Metrajı")
        self.setGeometry(700, 150, 800, 800)
        self.setWindowIcon(QtGui.QIcon('home.png'))
        vbox=QVBoxLayout()
        hbox=QHBoxLayout()
        anabox=QVBoxLayout()

        grb1=QGroupBox("")
        grb2=QGroupBox("")

        self.yapi_alani=QLineEdit()
        self.yapi_alani.setPlaceholderText("Yapı Alanı Giriniz(m2)")
        self.yapi_alani.textChanged.connect(self.degisim)
        self.topgoster=QPushButton("Toplamları Göster")

        self.topgoster.clicked.connect(self.toplam)
        self.topgoster.setStyleSheet("QPushButton"
                                       "{"
                                       "background-color : lightblue;"
                                       "}"
                                       "QPushButton::pressed"
                                       "{"
                                       "background-color : red;"
                                       "}")

        self.exele_aktar=QPushButton("Excele Aktar")
        self.exele_aktar.clicked.connect(self.exportToExcel)
        self.exele_aktar.setStyleSheet("QPushButton"
                                       "{"
                                       "background-color : lightblue;"
                                       "}"
                                       "QPushButton::pressed"
                                       "{"
                                       "background-color : red;"
                                       "}")
        self.eklebtn=QPushButton("Kalemi Ekle")
        self.eklebtn.setStyleSheet("QPushButton"
                                   "{"
                                   "background-color : lightgreen;"
                                   "}"
                                   "QPushButton::pressed"
                                   "{"
                                   "background-color : red;"
                                   "}")
        self.eklebtn.clicked.connect(self.addRow)


        self.eklebtn.setEnabled(False)


        self.hepsiniekle = QPushButton("Satırları Sil")
        self.hepsiniekle.clicked.connect(self.removeRow)
        self.hepsiniekle.setStyleSheet("QPushButton"
                                       "{"
                                       "background-color : red;"
                                       "color : white;"
                                       "}"
                                       "QPushButton::pressed"
                                       "{"
                                       "background-color : red;"
                                       "}")
        self.eklecmb=QComboBox()
        self.eklecmb.currentTextChanged.connect(self.katlar)
        self.katlar=QComboBox()
        self.katlar.setEnabled(False)
        self.eklecmb.addItem("Betoname Betonu")
        self.eklecmb.addItem("Betoname Demiri")
        self.eklecmb.addItem("Betoname Kalıp")
        self.eklecmb.addItem("Kalıp İskelesi")
        self.eklecmb.addItem("İş İskelesi")
        self.eklecmb.addItem("Tuğla Duvar")
        self.eklecmb.addItem("İç Sıva")
        self.eklecmb.addItem("Dış Sıva")
        self.eklecmb.addItem("Tavan Sıvası")
        self.eklecmb.addItem("Badana")
        self.eklecmb.addItem("Fayans-Seramik")
        self.eklecmb.addItem("Ahşap Yapı-Karkas")
        self.eklecmb.addItem("Ahşap Pencere")
        self.eklecmb.addItem("Yağlı Boya")
        self.eklecmb.addItem("Ahşap Çatı Kiremit")
        self.katlar.addItem("Tek Kat")
        self.katlar.addItem("İki Kat")
        self.katlar.addItem("Üç Kat")
        self.katlar.addItem("Dört Kat")
        self.katlar.addItem("Beş Kat")
        self.eklecmb.addItem("Metal Örtü")



        self.eklecmb.addItem("Mozaik Döşeme Kaplama")
        self.eklecmb.addItem("Cam")



        self.tableWidget = QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(11)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Sıra No","İmalat\nCinsi","Yığma", "Birim"
                                                    ,"Betonarme\nKarkas","Birim", "Yığma\nMetrajı","Betonarme\nMetrajı","Birim\nFiyatı(TL)","Yığma\nTutarı(TL)","Betonarme\nTutarı(TL)"))

        style = ":section {""background-color: silver ; }"
        self.tableWidget.horizontalHeader().setStyleSheet(style)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.itemChanged.connect(self.hesap2)


        hbox.addWidget(self.yapi_alani)
        hbox.addWidget(self.eklecmb)
        hbox.addWidget(self.katlar)

        hbox.addWidget(self.eklebtn)
        hbox.addWidget(self.hepsiniekle)

        hbox.addStretch()
        hbox.addStretch()
        hbox.addStretch()
        hbox.addStretch()
        hbox.addStretch()
        hbox.addStretch()
        hbox.addStretch()
        hbox.addStretch()
        hbox.addWidget(self.topgoster)
        hbox.addWidget(self.exele_aktar)

        vbox.addWidget(self.tableWidget)

        grb1.setLayout(hbox)
        grb2.setLayout(vbox)

        anabox.addWidget(grb1)
        anabox.addWidget(grb2,100)
        self.setLayout(anabox)
        self.chekenabled()
        self.silicin()


        self.show()
    def katlar(self):
        if self.eklecmb.currentText()=="Ahşap Çatı Kiremit" or self.eklecmb.currentText()=="Metal Örtü":
            self.katlar.setEnabled(True)
        else:
            self.katlar.setEnabled(False)


    def chekenabled(self):
        if self.tableWidget.rowCount() == 0:
            self.topgoster.setEnabled(False)
        else:
            self.topgoster.setEnabled(True)

    def addRow(self):

        try:
            for i in range(0,1):
                self.tableWidget.insertRow(i)
                self.rowindex()
                self.tableWidget.setItem(i,1,QTableWidgetItem(str(self.eklecmb.currentText())))
                if self.tableWidget.item(i, 1).text()=="Betoname Betonu":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.25)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m3 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.38)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m3 / m2"))

                if self.tableWidget.item(i, 1).text()=="Betoname Demiri":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(22)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("kg / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(34)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("kg / m2"))

                if self.tableWidget.item(i, 1).text()=="Betoname Kalıp":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(1.75)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(2.6)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Kalıp İskelesi":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(1.9)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m3 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(2.8)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m3 / m2"))

                if self.tableWidget.item(i, 1).text()=="İş İskelesi":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(1.43)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(1.43)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Tuğla Duvar":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.2)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m3 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.15)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m3 / m2"))

                if self.tableWidget.item(i, 1).text()=="İç Sıva":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(2.4)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(2.4)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Dış Sıva":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(1.3)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(1.3)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Tavan Sıvası":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.9)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.9)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Badana":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(3)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(3)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Fayans-Seramik":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.3)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.3)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Ahşap Yapı-Karkas":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.15)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.15)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Ahşap Pencere":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.12)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.12)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Yağlı Boya":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.42)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.42)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Ahşap Çatı Kiremit" and self.katlar.currentText()=="Tek Kat":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(1.25)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(1.25)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))
                if self.tableWidget.item(i, 1).text()=="Ahşap Çatı Kiremit" and self.katlar.currentText()=="İKi Kat":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.63)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.63)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))
                if self.tableWidget.item(i, 1).text()=="Ahşap Çatı Kiremit" and self.katlar.currentText()=="Üç Kat":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.42)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.42)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))
                if self.tableWidget.item(i, 1).text()=="Ahşap Çatı Kiremit" and self.katlar.currentText()=="Dört Kat":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.33)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.33)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))
                if self.tableWidget.item(i, 1).text()=="Ahşap Çatı Kiremit" and self.katlar.currentText()=="Beş Kat":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.25)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.25)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))


                if self.tableWidget.item(i, 1).text()=="Metal Örtü" and self.katlar.currentText()=="Tek Kat":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(1.33)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(1.33)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))
                if self.tableWidget.item(i, 1).text()=="Metal Örtü" and self.katlar.currentText()=="İki Kat":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.67)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.67)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))
                if self.tableWidget.item(i, 1).text()=="Metal Örtü" and self.katlar.currentText()=="Üç Kat":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.44)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.44)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))
                if self.tableWidget.item(i, 1).text()=="Metal Örtü" and self.katlar.currentText()=="Dört Kat":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.34)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.34)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))
                if self.tableWidget.item(i, 1).text()=="Metal Örtü" and self.katlar.currentText()=="Beş Kat":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.27)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.27)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))


                if self.tableWidget.item(i, 1).text()=="Mozaik Döşeme Kaplama":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.90)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.90)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))

                if self.tableWidget.item(i, 1).text()=="Cam":
                    self.tableWidget.setItem(i,2,QTableWidgetItem(str(0.10)))
                    self.tableWidget.setItem(i,3,QTableWidgetItem("m2 / m2"))
                    self.tableWidget.setItem(i,4,QTableWidgetItem(str(0.10)))
                    self.tableWidget.setItem(i,5,QTableWidgetItem("m2 / m2"))


                self.hesapla()
                self.chekenabled()
                self.arkaplan1()
                self.arkaplan2()


        except:
            pass

    def silicin(self):
        if self.yapi_alani.text()=="":
            self.hepsiniekle.setEnabled(False)
        else:
            self.hepsiniekle.setEnabled(True)

    def rowindex(self):
        for j in range(0,self.tableWidget.rowCount()):
            a=j+1
            self.tableWidget.setItem(j,0,QTableWidgetItem(str(a)))

    def hesapla(self):
        try:
            if self.tableWidget.rowCount()>0:
                alan=float(self.yapi_alani.text().replace(".",","))
                for j in range(0,self.tableWidget.rowCount()):
                    katsayi1=float(self.tableWidget.item(j, 2).text().replace(",","."))
                    katsayi2=float(self.tableWidget.item(j, 4).text().replace(",","."))
                    miktar=round(alan*katsayi1,2)
                    miktar1=round(alan*katsayi2,2)
                    self.tableWidget.setItem(j,6,QTableWidgetItem(str(miktar)))
                    self.tableWidget.setItem(j,7,QTableWidgetItem(str(miktar1)))


                    sonuc1=float(self.tableWidget.item(j, 6).text().replace(",","."))
                    sonuc2=float(self.tableWidget.item(j, 7).text().replace(",","."))

                    fiyat=float(self.tableWidget.item(j, 8).text().replace(",","."))
                    yigmafiyat=round(fiyat*sonuc1,2)
                    betonarmefiyat=round(fiyat*sonuc2,2)

                    print(yigmafiyat)
                    print(betonarmefiyat)

                    self.tableWidget.setItem(j,9,QTableWidgetItem(str(yigmafiyat)))
                    self.tableWidget.setItem(j,10,QTableWidgetItem(str(betonarmefiyat)))


            else:
                pass
        except:
            pass

    def degisim(self):
        self.eklebtn.setEnabled(True)
        self.hesapla()
        self.silicin()

    def removeRow(self):
        for i in range(0,self.tableWidget.rowCount()):
            self.tableWidget.removeRow(i)
            self.rowindex()

    def hesap2(self,item):
        try:
            if self.tableWidget.rowCount()>0:

                for j in range(0,self.tableWidget.rowCount()):

                    sonuc1=float(self.tableWidget.item(j, 6).text().replace(",","."))
                    sonuc2=float(self.tableWidget.item(j, 7).text().replace(",","."))
                    fiyat=float(self.tableWidget.item(j, 8).text().replace(",","."))
                    yigmafiyat=round(fiyat*sonuc1, 2)
                    betonarmefiyat=round(fiyat*sonuc2,2)

                    if item.row()==j and item.column() == 8:
                        self.tableWidget.setItem(j,9,QTableWidgetItem(str(yigmafiyat)))
                        self.tableWidget.setItem(j,10,QTableWidgetItem(str(betonarmefiyat)))

                    son = self.tableWidget.rowCount()

            else:
                pass
        except:
            pass

    def toplam(self):
        try:
            for j in range(self.tableWidget.rowCount()-1,self.tableWidget.rowCount()):
                for i in range(0, 1):
                    self.tableWidget.insertRow(i)

                    self.tableWidget.sortItems(0)
                for i in range(0, 1):
                    self.tableWidget.insertRow(i)

                    self.tableWidget.sortItems(0)
                for i in range(0, 1):
                    self.tableWidget.insertRow(i)

                    self.tableWidget.sortItems(0)

                for i in range(0, 1):
                    self.tableWidget.insertRow(i)

                    self.tableWidget.sortItems(0)

                self.tableWidget.setItem(j + 1, 8, QTableWidgetItem("TUTAR"))
                self.tableWidget.setItem(j + 2, 8, QTableWidgetItem("Müteahhit Karı(%25)"))
                self.tableWidget.setItem(j + 3, 8, QTableWidgetItem("KDV(%18)"))
                self.tableWidget.setItem(j + 4, 8, QTableWidgetItem("TOPLAM"))

                son = self.tableWidget.rowCount()
                top3 = 0.00
                top4 = 0.00

                if son>1:
                    for t1 in range(0, son - 4):
                        deger1 = float(self.tableWidget.item(t1, 9).text().replace(",", "."))
                        top3 += deger1

                    for t in range(0, son - 4):
                        deger2 = float(self.tableWidget.item(t, 10).text().replace(",", "."))
                        top4 += deger2

                if son==1:
                    deger1 = float(self.tableWidget.item(0, 9).text().replace(",", "."))
                    top3 = deger1

                    deger2 = float(self.tableWidget.item(0, 10).text().replace(",", "."))
                    top4 = deger2



                mth1 = 0.25 * top3
                mth2 = 0.25 * top4

                kdv1 = (top3 + mth1) * 0.18
                kdv2 = (top4 + mth2) * 0.18

                top1 = top3 + mth1 + kdv1
                top2 = top4 + mth2 + kdv2

                self.tableWidget.setItem(j + 1, 9, QTableWidgetItem(str(top3)))
                self.tableWidget.setItem(j + 1, 10, QTableWidgetItem(str(top4)))

                self.tableWidget.setItem(j + 2, 9, QTableWidgetItem(str(mth1)))
                self.tableWidget.setItem(j + 2, 10, QTableWidgetItem(str(mth2)))

                self.tableWidget.setItem(j + 3, 9, QTableWidgetItem(str(round(kdv1, 2))))
                self.tableWidget.setItem(j + 3, 10, QTableWidgetItem(str(round(kdv2, 2))))

                self.tableWidget.setItem(j + 4, 9, QTableWidgetItem(str(round(top1, 2))))
                self.tableWidget.setItem(j + 4, 10, QTableWidgetItem(str(round(top2, 2))))
                self.topgoster.setEnabled(False)




        except:
            pass

    def exportToExcel(self):
        if self.tableWidget.rowCount()>0:
            columnHeaders = []

            # create column header list
            for j in range(self.tableWidget.columnCount()):
                columnHeaders.append(self.tableWidget.horizontalHeaderItem(j).text())

            df = pd.DataFrame(columns=columnHeaders)

            # create dataframe object recordset
            for row in range(self.tableWidget.rowCount()):
                for col in range(self.tableWidget.columnCount()):
                    thing = self.tableWidget.item(row,col)
                    if thing is not None and thing.text() != '':
                        df.at[row, columnHeaders[col]] = self.tableWidget.item(row, col).text()

            df.to_excel('Yaklaşık_Maliyet.xlsx', index=False)
            print("Excel'e aktarım başarılı")
        else:
            print("Boş Liste")

    def arkaplan1(self):
        pass
        # for j in range(self.tableWidget.rowCount()):
        #     for i in range(self.tableWidget.horizontalHeader().count()):
        #         self.tableWidget.item(j, i).setBackground(QtGui.QColor(240, 224, 74))


    def arkaplan2(self):
        pass
        # for row in range(self.tableWidget.rowCount()):
        #     for col1 in range(self.tableWidget.columnCount()-4,self.tableWidget.columnCount()):
        #         self.tableWidget.item(row, col1).setBackground(QtGui.QColor(232, 157, 216))





if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = yaklasikmaliyet()
    sys.exit(app.exec())