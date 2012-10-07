import sublime
import sublime_plugin


class NewPostCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel('Enter Name Of New Post', "", self.on_done, None, None)
        self.panel = self.window.get_output_panel("exec")

    def load_config(self):
        octo_set = sublime.load_settings("octopress.sublime-settings")

        self.octopress_path = octo_set.get("octopress_path")
        if self.octopress_path[-1] != '/':
            self.octopress_path += "/"

        self.rake_command = octo_set.get("rake_command")

    def on_done(self, text):
        self.load_config()

        self.window.run_command("exec", {
            "cmd": [self.rake_command + " \"new_post[" + text + "]\""],
            "shell": True,
            "working_dir": self.octopress_path
        })

        self.window.run_command("hide_panel")
        sublime.set_timeout(self.show_new_file, 1000)

    def show_new_file(self):
        region_all = sublime.Region(0, self.panel.size())
        line2 = self.panel.substr(region_all).split("\n")[1]
        if line2.startswith("Creating new post: "):
            new_file = line2.replace("Creating new post: ", "")
            self.window.open_file(self.octopress_path + new_file)
        else:
            self.window.run_command("show_panel", {"panel": "output.exec"})
