import os.path
import re

import sublime
import sublime_plugin


SETTINGS_FILE_NAME = "CodeWrapper.sublime-settings"
PROJECT_SETTINGS_KEY = "CodeWrapper"
ALPHA_RE = re.compile(r"[a-zA-Z]")
INDENT_RE = re.compile(r"(^\s*)")


def _has_alpha(string):
    return ALPHA_RE.search(string) is not None


class CodeWrapperCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        super(CodeWrapperCommand, self).__init__(view)
        file_name = view.file_name()
        self.ext = None
        if file_name:
            self.ext = os.path.splitext(file_name)[1][1:]

    def is_enabled(self):
        # TODO
        return True

    def is_visible(self):
        # TODO
        return True

    def run(self, edit):
        regions = self.view.sel()
        for region in regions:
            selection = self._get_selection(region)
            if not selection:
                continue

            project_settings = self.view.settings().get(
                PROJECT_SETTINGS_KEY, {})
            commands = self._get_commands(project_settings, selection)
            if not commands:
                global_settings = sublime.load_settings(SETTINGS_FILE_NAME)
                commands = self._get_commands(global_settings, selection)
                if not commands:
                    continue

            for command in commands[::-1]:
                self._write_line(command, edit, region)

    def _get_selection(self, region):
        if region.empty():
            region = self.view.word(region.begin())
        if region.empty():
            return None

        selection = self.view.substr(region)
        if not _has_alpha(selection):
            return None

        return selection

    def _get_commands(self, settings, selection):
        for command in settings.get("commands", []):
            extensions = command.get("extensions", [])
            syntaxes = command.get("syntaxes", [])
            this_syntax = os.path.splitext(
                os.path.split(self.view.settings().get("syntax"))[-1])[0]
            if self.ext not in extensions and this_syntax not in syntaxes:
                continue

            regexes = command.get("regexes", None)
            if regexes:
                is_match = False
                for regex in regexes:
                    if self.view.find(regex, 0):
                        is_match = True
                if not is_match:
                    continue

            output_options = command.get("output_options", None)
            if not output_options:
                continue

            commands = []
            for output_option in output_options:
                commands.append(output_option.format(selection))

            return commands

    def _get_indent(self, region):
        line = self.view.substr(self.view.line(region.begin()))
        indent_match = INDENT_RE.search(line)
        indent = ""
        if indent_match:
            indent = indent_match.group(1)

        return indent

    def _write_line(self, command, edit, region):
        new_line = "\n" + self._get_indent(region) + command
        self.view.insert(edit, self.view.line(region.begin()).end(), new_line)
