import sublime
import sublime_plugin
import os, errno
import re

class RunTests(sublime_plugin.TextCommand):
  def run(self, edit, scope):
    last_run = sublime.load_settings("Rspec.last-run")

    if scope == "last":
      self.run_spec(last_run.get("root_path"), last_run.get("path"))
    else:
      path = self.find_path(scope)
      root_path = re.sub("\/spec\/.*", "", path)
      self.run_spec(root_path, path)

      last_run.set("path", path)
      last_run.set("root_path", root_path)
      sublime.save_settings("Rspec.last-run")

  def find_path(self, scope):
    path = self.view.file_name()

    if path.find("/spec/") < 0:
      return sublime.error_message("Run this command from a file in a subdirectory of spec/")

    if scope == "line":
      line_number, column = self.view.rowcol(self.view.sel()[0].begin())
      line_number += 1
      path += ":" + str(line_number)

    return path

  def run_spec(self, root_path, path):
    self.run_in_terminal('cd ' + root_path)
    self.run_in_terminal('bundle exec rspec ' + path)

  def run_in_terminal(self, command):
    osascript_command = 'osascript '
    osascript_command += '"' + sublime.packages_path() + '/RSpecTerminal/run_command.applescript"'
    osascript_command += ' "' + command + '"'
    osascript_command += ' "Ruby Tests"'
    os.system(osascript_command)
