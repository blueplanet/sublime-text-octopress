import functools
import os
import sublime
import sublime_plugin
import subprocess
import thread


class OctopressCommand():

    def exec_command(self, command):
        self.load_config()

        os.chdir(self.octopress_path)

        self.proc = subprocess.Popen(self.rake_command + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        thread.start_new_thread(self.read_stdout, ())

    def load_config(self):
        octo_set = sublime.load_settings("octopress.sublime-settings")

        self.octopress_path = octo_set.get("octopress_path")
        if self.octopress_path[-1] != os.sep:
            self.octopress_path += os.sep

        self.rake_command = octo_set.get("rake_command")

    def finish(self):
        if self.file:
            print "Open File : " + self.file
            self.window.open_file(self.octopress_path + self.file)

    def read_stdout(self):
        while True:
            data = os.read(self.proc.stdout.fileno(), 2 ** 15)

            if data != "":
                if data.startswith(self.exec_result):
                    self.file = data.split(os.linesep)[0].replace(self.exec_result, "")

                print "octopress exec output : " + data
            else:
                self.proc.stdout.close()

                sublime.set_timeout(functools.partial(self.finish), 0)
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

        self.exec_result = "Creating new post: "
        self.exec_command(command)


class NewPageCommand(sublime_plugin.WindowCommand, OctopressCommand):
    def run(self):
        self.window.show_input_panel("Enter Name Of New Page", "", self.on_done, None, None)

        print "octopress exec start."

    def on_done(self, text):
        command = " \"new_page[%s]\"" % text

        self.exec_result = "Creating new page: "
        self.exec_command(command)
