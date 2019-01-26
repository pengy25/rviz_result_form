import sys

from python_qt_binding.QtGui import QWidget, QLineEdit, QLabel, QHBoxLayout, QApplication

class SingleInputForm(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QHBoxLayout()
        self.label = QLabel()
        self.value = QLineEdit()
        layout.addWidget(self.label)
        layout.addWidget(self.value)
        self.setLayout(layout)

    def set_label(self, text):
        self.label.setText(text)

    def set_value(self, text):
        self.value.setText(text)

    def get_value(self):
        return self.value.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    testForm = SingleInputForm()
    testForm.set_label('test label')
    testForm.set_value('test value')
    print('The value obtained from the form is %s' % (testForm.get_value(),))
    testForm.show()
    app.exec_()
