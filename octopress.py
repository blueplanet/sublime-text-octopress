import os
import sublime
import sublime_plugin
import subprocess
import thread


class OctopressCommand():

    def load_config(self):
        octo_set = sublime.load_settings("octopress.sublime-settings")

        self.octopress_path = octo_set.get("octopress_path")
        if self.octopress_path[-1] != '/':
            self.octopress_path += "/"

        self.rake_command = octo_set.get("rake_command")

    def exec_comman(self, command):
        self.load_config()

        os.chdir(self.octopress_path)

        self.proc = subprocess.Popen(self.rake_command + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        thread.start_new_thread(self.read_stdout, ())

    def read_stdout(self):
        while True:
            data = os.read(self.proc.stdout.fileno(), 2 ** 15)

            if data != "":
                print "octopress exec output : " + str(data)
            else:
                self.proc.stdout.close()
                print "octopress exec end."
                break

    def read_stderr(self):
        while True:
            data = os.read(self.proc.stderr.fileno(), 2 ** 15)

            if data != "":
                print "octopress exec error : " + str(data)
            else:
                self.proc.stderr.close()
                break


class NewPostCommand(sublime_plugin.WindowCommand, OctopressCommand):
    def run(self):
        self.window.show_input_panel("Enter Name Of New Post", "", self.on_done, None, None)

        print "octopress exec start."

    def on_done(self, text):
        command = " \"new_post[%s]\"" % text

        self.exec_comman(command)


class NewPageCommand(sublime_plugin.WindowCommand, OctopressCommand):
    def run(self):
        self.window.show_input_panel("Enter Name Of New Page", "", self.on_done, None, None)

        print "octopress exec start."

    def on_done(self, text):
        command = " \"new_page[%s]\"" % text

        self.exec_comman(command)
