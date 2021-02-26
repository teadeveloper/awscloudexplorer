import npyscreen
from forms import aws_form

class App(npyscreen.NPSAppManaged):

    keypress_timeout_default = 1

    def onStart(self):
        self.CloudForm = self.addForm(
            'MAIN', aws_form.AwsMeanForm, name="AWS Cloud Explorer")

if (__name__ == "__main__"):
    try:
        CloudExplorer = App().run()
    except:
        print ("Exiting")
