from PySide2 import QtCore, QtWidgets

# https://code.qt.io/cgit/qt/qtbase.git/tree/src/widgets/kernel/qwidget.h#n873
QWIDGETSIZE_MAX = (1 << 24) - 1

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.m_deltaX = 0
        self.btn = QtWidgets.QPushButton(
            ">", checkable=True, clicked=self.closeOpenEditor
        )
        self.btn.setFixedSize(QtCore.QSize(25, 25))

        self.text1 = QtWidgets.QTextEdit()
        self.text1.setText("some sample text")

        self.text2 = QtWidgets.QTextEdit()

        layout_btn = QtWidgets.QVBoxLayout()
        layout_btn.addWidget(self.btn)

        lay = QtWidgets.QHBoxLayout(self)
        lay.addWidget(self.text1, 10)
        lay.addSpacing(15)
        lay.addLayout(layout_btn)
        lay.setSpacing(0)
        lay.addWidget(self.text2, 4)

        self.resize(800, 500)

        self.m_animation = QtCore.QPropertyAnimation(
            self.text2, b"maximumWidth", parent=self, duration=250
        )

    def closeOpenEditor(self):
        if self.btn.isChecked():
            self.text2.setMaximumWidth(self.text2.width())
            text2Start = int(self.text2.maximumWidth())
            self.m_deltaX = text2Start
            text2End = 3
            self.m_animation.setStartValue(text2Start)
            self.m_animation.setEndValue(text2End)
            self.btn.setText("<")
        else:
            text2Start = int(self.text2.maximumWidth())
            text2End = self.m_deltaX
            self.m_animation.setStartValue(text2Start)
            self.m_animation.setEndValue(text2End)
            self.btn.setText(">")

        self.m_animation.start()

    def resizeEvent(self, event: "QResizeEvent"):
        if not self.btn.isChecked():
            self.text2.setMaximumWidth(QWIDGETSIZE_MAX)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())