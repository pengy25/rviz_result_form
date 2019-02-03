import sys

from python_qt_binding.QtGui import QWidget, QVBoxLayout, QApplication
from single_input_form import SingleInputForm

class InputFormManager(QWidget):
    def __init__(self, label_names):
        QWidget.__init__(self)
        self.label_names = label_names
        self.forms = {name:SingleInputForm(name, -1) for name in self.label_names}
        layout = QVBoxLayout()
        for name in self.label_names:
            layout.addWidget(self.forms[name])
        self.setLayout(layout)

    def set_pair(label, value):
        if label not in self.forms:
            print("Error: attempt to set input form through invalid label!")
            return

        self.forms[label].set_value(value)

    def get_pairs_str():
        if len(self.label_names) < 1:
            return

        res = self.forms[self.label_names[0]].get_value()
        for i in range(1, len(self.label_names)):
            name = self.label_names[i]
            res += ',' + self.forms[name].get_value()

        return res

if __name__ == '__main__':
    app = QApplication(sys.argv)
    names = ['name1', 'name2']
    mgr = InputFormManager(names)
    mgr.show()
    app.exec_()
