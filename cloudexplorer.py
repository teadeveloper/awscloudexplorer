#!/usr/bin/python
import npyscreen
from forms import aws_form

import curses


class App(npyscreen.NPSAppManaged):

    keypress_timeout_default = 1

    def onStart(self):
        self.CloudForm = self.addForm(
            'MAIN', aws_form.AwsMeanForm, name="AWS Cloud Explorer")


if (__name__ == "__main__"):

    CloudExplorer = App().run()



