import sys

from python_qt_binding.QtGui import QWidget, QVBoxLayout, QApplication
from .single_input_form import SingleInputForm

class InputFormManager(QWidget):
    def __init__(self, label_value_pr):
        QWidget.__init__(self)
        self.label_names = []
        self.forms = {}
        self.form_state = {}

        for label, value in label_value_pr:
            self.label_names.append(label)
            self.forms[label] = SingleInputForm(label, value)
            self.form_state[label] = str(value)

        layout = QVBoxLayout()
        for name in self.label_names:
            layout.addWidget(self.forms[name])
        self.setLayout(layout)

    def set_pair(self, label, value):
        if label not in self.form_state:
            print("Error: attempt to store input through invalid label!")
            return

        self.form_state[label] = str(value)

    def set_pair_all(self):
        for label, value in self.form_state.items():
            self.form_state[label] = str(value)

    def refresh(self):
        for label, value in self.form_state.items():
            self.forms[label].set_label(label)
            self.forms[label].set_value(value)

    def get_pairs_str(self):
        if len(self.label_names) < 1:
            return

        res = self.form_state[self.label_names[0]]
        for i in range(1, len(self.label_names)):
            name = self.label_names[i]
            res += ',' + self.form_state[name]

        return res

if __name__ == '__main__':
    app = QApplication(sys.argv)
    names = [('name1', 1), ('name2', None)]
    mgr = InputFormManager(names)
    mgr.show()
    app.exec_()
