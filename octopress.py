# -*- coding: utf-8 -*-
import functools
import os
import re
import sublime
import sublime_plugin
import subprocess
try:
    import thread
except ImportError:
    import _thread as thread

import glob
import sys

class StopPreview(sublime_plugin.TextCommand):
    def run(self, edit):
        print("\nStopping preview server...")
        proc = subprocess.Popen(["ps aux | grep [r]ackup | awk '{print $2}' | xargs kill -9"], stdout=subprocess.PIPE, shell=True)
        proc = subprocess.Popen(["ps aux | grep [j]ekyl | awk '{print $2}' | xargs kill -9"], stdout=subprocess.PIPE, shell=True)
        proc = subprocess.Popen(["ps aux | grep [c]ompas | awk '{print $2}' | xargs kill -9"], stdout=subprocess.PIPE, shell=True)
        print("Preview Stopped!")


class OctopressCommand(sublime_plugin.WindowCommand):

    def exec_command(self, command):
        print("octopress exec start.")

        self.output = ""
        self.load_config()

        os.chdir(self.octopress_path)

        exec_command = "%s %s" % (self.rake_command, command)

        self.proc = subprocess.Popen(exec_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, executable=self.shell_executable)

        thread.start_new_thread(self.read_stdout, ())

    def set_filename(self, view, filename):
        return os.path.basename(view.file_name())
        

    def check_current(self, view):
        new = self.octopress_path + "/source/_posts"
        print(new)
        return re.search(self.octopress_path + "/source/_posts/.*", view.file_name())

    def if_default(self,key):
        octo_set = sublime.load_settings("octopress.sublime-settings")
        beno_set = self.window.active_view().settings()
        if beno_set.get(key):
            return beno_set.get(key)
        else:
            return octo_set.get(key)

    def load_config(self):
            
        self.octopress_path = self.if_default("octopress_path")
        pre_rake = self.if_default("octopress_cmd_before_rake")
        use_bundle = self.if_default("use_bundle")
        shell_exec = self.if_default("octopress_shell_executable")

        if self.octopress_path[-1] != os.sep:
            self.octopress_path += os.sep

        if (pre_rake != ''):
            pre_rake += '; '

        self.rake_command = pre_rake + "rake"

        if use_bundle:
            self.rake_command = pre_rake + "bundle exec rake"
            
        if shell_exec == '':
            shell_exec = '/bin/sh'

        self.shell_executable = shell_exec

        print(self.rake_command)

    def show_status_message(self, msg):
        sublime.status_message(msg)

    def finish(self):
        finded = re.search(self.check_str, self.output)

        if self.DoubleSearch == 1:
            finded2 = re.search(self.check_str2, self.output)  
            if finded and finded2:
                sublime.status_message("octopress exec successfully finished.\n\nGenerated and deployed without errors.")
            else:
                sublime.status_message("")
                sublime.error_message("Octopress exec failed. Please check octopress env, and try again.\n\nYou can check exec log in sublime console.") 
        elif self.DoubleSearch == 2:
            finded2 = re.search(self.check_str2, self.output) 
            if finded:
                sublime.status_message("octopress exec successfully finished.\n\nDeployed without any errors.")
            elif finded2:
                sublime.status_message("octopress exec successfully finished.\n\nEverything is up-to-date.")
            else:
                sublime.status_message("")
                sublime.error_message("Octopress exec failed. Please check octopress env, and try again.\n\nYou can check exec log in sublime console.")
        else:
            if finded:
                sublime.status_message("octopress exec successfully finished.")

                if self.file:
                    print("Open File : " + self.file)
                    self.window.open_file(self.octopress_path + self.file)
            else:
                sublime.status_message("")
                sublime.error_message("Octopress exec failed. Please check octopress env, and try again.\n\nYou can check exec log in sublime console.")

    def read_stdout(self):
        while True:
            sublime.set_timeout(functools.partial(self.show_status_message, "octopress running..."), 0)

            data = os.read(self.proc.stdout.fileno(), 2 ** 15)
            if sys.version[0]=='3':
                data = data.decode(sys.getdefaultencoding())
                
            if data != "":
                print(data)

                if self.do_open_file and self.check_str and data.startswith(self.check_str):
                    self.file = data.split(os.linesep)[0].replace(self.check_str, "")

                self.output += data 
            else:
                self.proc.stdout.close()

                print("octopress exec end.")

                sublime.set_timeout(functools.partial(self.finish), 0)
                break


class OctopressNewPostCommand(OctopressCommand):

    def run(self):
        self.window.show_input_panel("Enter Name Of New Post", "", self.on_done, None, None)

    def on_done(self, text):
        print("\nCreating new post...")
        command = " \"new_post[%s]\"" % text

        self.check_str = u'Creating new post: '
        self.DoubleSearch = 0
        self.do_open_file = True
        self.exec_command(command)


class OctopressNewPageCommand(OctopressCommand):
    def run(self):
        self.window.show_input_panel("Enter Name Of New Page", "", self.on_done, None, None)

    def on_done(self, text):
        print("\nCreating new page...")
        command = " \"new_page[%s]\"" % text

        self.check_str = u'Creating new page: '
        self.DoubleSearch = 0
        self.do_open_file = True
        self.exec_command(command)


class OctopressGenerateCommand(OctopressCommand):
    def run(self):
        print("\nStarting to generate...")
        self.file = ""
        self.check_str = u'Successfully generated site:'
        self.DoubleSearch = 0
        self.do_open_file = False
        self.exec_command("generate")


class OctopressDeployCommand(OctopressCommand):
    def run(self):
        print("\nStarting to deploy...")
        self.file = ""
        self.check_str = u"To"
        self.check_str2 = u"Everything up-to-date"
        self.DoubleSearch = 2
        self.do_open_file = False
        self.exec_command("deploy")


class OctopressGenerateAndDeployCommand(OctopressCommand):
    def run(self):
        print("\nStrating to generate and deploy...")
        self.file = ""
        self.DoubleSearch = 1
        self.check_str = u"To"
        self.check_str2 = u"Successfully generated site:"
        self.do_open_file = False
        self.exec_command("gen_deploy")

class OctopressStartPreviewCommand(OctopressCommand):
    def run(self):
        print("\nStarting Preview server...")
        self.file = ""
        self.DoubleSearch = 0
        self.check_str = u"Compass is watching for changes."
        self.do_open_file = False
        self.exec_command("preview")


class OctopressIsolate(OctopressCommand):
    
    def run(self):
        print("\n")
        view = self.window.active_view()
        global_settings = sublime.load_settings(__name__ + '.sublime-settings')
        octo_set = sublime.load_settings("octopress.sublime-settings")
        self.octopress_onsave_action = octo_set.get("octopress_onsave_action")
        self.octopress_path = octo_set.get("octopress_path")
        if self.check_current(view):       
            filename = None
            filename = self.set_filename(view, filename)
            command = " isolate[\"%s\"]" % filename
            print("\nIsolating...")
            self.file = ""
            self.DoubleSearch = 0
            self.check_str = u""
            self.do_open_file = False
            self.exec_command(command)
        else:
            sublime.error_message("Not a post file")


class OctopressIntegrate(OctopressCommand):
    def run(self):
        print("\nIntegrating...")
        self.file = ""
        self.DoubleSearch = 0
        self.check_str = u""
        self.do_open_file = False
        self.exec_command("integrate")

class OctopressAutoGenerate(sublime_plugin.EventListener):
    def on_post_save(self, view):
        global_settings = sublime.load_settings(__name__ + '.sublime-settings')
        octo_set = sublime.load_settings("octopress.sublime-settings")

        self.octopress_onsave_action = octo_set.get("octopress_onsave_action")
        self.octopress_path = octo_set.get("octopress_path")

        valid_actions = ["", "generate", "deploy", "generate_and_deploy"]
        if (self.octopress_onsave_action not in valid_actions):
            # No valid on_save action present, abort
            sublime.error_message("Given action: '" + self.octopress_onsave_action + "' is not valid")
            return

        if (self.octopress_onsave_action == ""):
            # They don't want an onsave, so abort
            return

        if not re.search(self.octopress_path + ".*", view.file_name()):
            # current file being saved is not in the octopress path
            return

        view.window().run_command('octopress_' + self.octopress_onsave_action)

class OctopressOpenExistingPostCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        octo_set = sublime.load_settings("octopress.sublime-settings")
        self.octopress_path = octo_set.get("octopress_path")
        self.posts_dir = octo_set.get("octopress_posts_dir")

        files = [f for f in os.listdir(self.octopress_path + "/source/" + self.posts_dir)]
        files.reverse()
        self.quick_panel_items = files
        self.view.window().show_quick_panel(self.quick_panel_items, self.on_done, sublime.MONOSPACE_FONT)

    def on_done(self, index):
        if (index == -1):
            return
        sublime.active_window().run_command("open_file", {"file":self.octopress_path + "/source/" + self.posts_dir + "/" + self.quick_panel_items[index]})
        return

class OctopressOpenExistingPageCommand(OctopressOpenExistingPostCommand):
    def run(self, edit):
        octo_set = sublime.load_settings("octopress.sublime-settings")
        self.octopress_path = octo_set.get("octopress_path")
        self.page_extension = octo_set.get("octopress_page_extension")
        
        files = glob.glob(self.octopress_path + "/source/*/index." + self.page_extension);
        files.reverse()
        self.quick_panel_items = []
        for file in files:
            self.quick_panel_items.append(file.replace(self.octopress_path + "/source/", ""))
        self.view.window().show_quick_panel(self.quick_panel_items, self.on_done, sublime.MONOSPACE_FONT)

    def on_done(self, index):
        if (index == -1):
            return
        sublime.active_window().run_command("open_file", {"file":self.octopress_path + "/source/" + self.quick_panel_items[index]})
        return
