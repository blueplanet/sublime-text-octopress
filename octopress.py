import functools
import os
import re
import sublime
import sublime_plugin
import subprocess
import thread


class OctopressCommand(sublime_plugin.WindowCommand):

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
            sublime.status_message("")
            sublime.error_message("Octopress exec failed. Please check octopress env, and try argin.\n\nYou can check exec log in sublime console.")

    def read_stdout(self):
        while True:
            sublime.set_timeout(functools.partial(self.show_status_message, "octopress runing..."), 0)

            data = os.read(self.proc.stdout.fileno(), 2 ** 15)

            if data != "":
                print data

                if self.do_open_file and self.check_str and data.startswith(self.check_str):
                    self.file = data.split(os.linesep)[0].replace(self.check_str, "")

                self.output += data
            else:
                self.proc.stdout.close()

                print "octopress exec end."

                sublime.set_timeout(functools.partial(self.finish), 0)
                break


class OctopressNewPostCommand(OctopressCommand):

    def run(self):
        self.window.show_input_panel("Enter Name Of New Post", "", self.on_done, None, None)

    def on_done(self, text):
        command = " \"new_post[%s]\"" % text

        self.check_str = "Creating new post: "
        self.do_open_file = True
        self.exec_command(command)


class OctopressNewPageCommand(OctopressCommand):
    def run(self):
        self.window.show_input_panel("Enter Name Of New Page", "", self.on_done, None, None)

    def on_done(self, text):
        command = " \"new_page[%s]\"" % text

        self.check_str = "Creating new page: "
        self.do_open_file = True
        self.exec_command(command)


class OctopressGenerateCommand(OctopressCommand):
    def run(self):
        self.file = ""
        self.check_str = "Successfully generated site:"
        self.do_open_file = False
        self.exec_command("generate")


class OctopressDeployCommand(OctopressCommand):
    def run(self):
        self.file = ""
        self.check_str = "^(## Github Pages deploy complete|OK)$"
        self.do_open_file = False
        self.exec_command("deploy")


class OctopressGenerateAndDeployCommand(OctopressCommand):
    def run(self):
        self.file = ""
        self.check_str = "^(## Github Pages deploy complete|OK)$"
        self.do_open_file = False
        self.exec_command("gen_deploy")
