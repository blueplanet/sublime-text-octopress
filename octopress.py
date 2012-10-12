import functools
import os
import re
import sublime
import sublime_plugin
import subprocess
import thread


class OctopressCommand():

    def exec_command(self, command):
        print "octopress exec start."

        self.output = ""
        self.load_config()

        os.chdir(self.octopress_path)

        exec_command = "%s %s" % (self.rake_command, command)

        self.proc = subprocess.Popen(exec_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        thread.start_new_thread(self.read_stdout, ())

    def load_config(self):
        octo_set = sublime.load_settings("octopress.sublime-settings")

        self.octopress_path = octo_set.get("octopress_path")
        if self.octopress_path[-1] != os.sep:
            self.octopress_path += os.sep

        self.rake_command = octo_set.get("rake_command")

    def show_status_message(self, msg):
        sublime.status_message(msg)

    def finish(self):
        finded = re.search(self.check_str, self.output)

        if finded:
            sublime.status_message("octopress exec successfully finished.")

            if self.file:
                print "Open File : " + self.file
                self.window.open_file(self.octopress_path + self.file)
        else:
            sublime.error_message("Octopress exec failed. Please check octopress env, and try argin.\n\nYou can check exec log in sublime console.")

    def read_stdout(self):
        while True:
            sublime.set_timeout(functools.partial(self.show_status_message, "octopress runing..."), 0)

            data = os.read(self.proc.stdout.fileno(), 2 ** 15)

            if data != "":
                print data

                if self.exec_result and data.startswith(self.exec_result):
                    self.file = data.split(os.linesep)[0].replace(self.exec_result, "")

                self.output += data
            else:
                self.proc.stdout.close()

                print "octopress exec end."

                sublime.set_timeout(functools.partial(self.finish), 0)
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

    def on_done(self, text):
        command = " \"new_post[%s]\"" % text

        self.exec_result = "Creating new post: "
        self.exec_command(command)


class NewPageCommand(sublime_plugin.WindowCommand, OctopressCommand):
    def run(self):
        self.window.show_input_panel("Enter Name Of New Page", "", self.on_done, None, None)

    def on_done(self, text):
        command = " \"new_page[%s]\"" % text

        self.exec_result = "Creating new page: "
        self.exec_command(command)


class GenerateCommand(sublime_plugin.WindowCommand, OctopressCommand):
    def run(self):
        self.exec_result = ""
        self.file = ""
        self.check_str = "Successfully generated site:"
        self.exec_command("generate")
