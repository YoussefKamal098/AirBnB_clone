#!/usr/bin/python3
"""
This module defines the HBNBCommand class, which implements
a command-line interface for an AirBnB-like application.
"""

import cmd
import shlex
# import ast
# import re
# import subprocess
from console_commands import CreateCommand
from console_commands import ShowCommand
from console_commands import AllCommand
from console_commands import DestroyCommand
from console_commands import UpdateCommand
from models import storage
import readline


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class represents the command-line interface for
    the AirBnB-like application.

    Attributes:
        prompt (str): The command prompt.

    Methods:
        do_create(self, line): Executes the 'create' command.
        do_show(self, line): Executes the 'show' command.
        do_destroy(self, line): Executes the 'destroy' command.
        do_all(self, line): Executes the 'all' command.
        do_update(self, line): Executes the 'update' command.
        do_quit(self, line): Quits the command-line interface.
        do_EOF(self, line): Handles the end-of-file signal.
        emptyline(self): Handles empty input.
        precmd(self, line): Processes the command before execution.
        postcmd(self, stop, line): Processes the command after execution.
    """

    prompt = "(hbnb) "
    __history_file = ".airbnb_cmd_history.txt"
    __history = []
    __MAX_HIS = 100
    __current_cmd = ""

    __airbnb_commands = {
        "create": CreateCommand(storage),
        "show": ShowCommand(storage),
        "destroy": DestroyCommand(storage),
        "all": AllCommand(storage),
        "update": UpdateCommand(storage)
    }

    def preloop(self) -> None:
        self.load_history()

    def do_create(self, line):
        """
        Create a new class instance and print its id.
        Usage: create <class>
        """
        self.__airbnb_commands["create"].execute(line)

    def do_show(self, line):
        """
        Display the string representation of a class instance of a given id.
        Usage: show <class> <id>
        """
        self.__airbnb_commands["show"].execute(line)

    def do_destroy(self, line):
        """
        Delete a class instance of a given id.
        Usage: destroy <class> <id>
        """
        self.__airbnb_commands["destroy"].execute(line)

    def do_all(self, line):
        """
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.

        Usage: all or all <class>
        """
        self.__airbnb_commands["all"].execute(line)

    def do_update(self, line):
        """
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.

        Usage: update <class> <id> <attribute_name> <attribute_value>
        """
        self.__airbnb_commands["update"].execute(line)

    def do_quit(self, line):
        """
        Quits the command-line interface.

        Parameters:
            line (str): The command line input.

        Returns:
            bool: True to exit the interface.

        """
        self.save_history()
        return True

    def do_EOF(self, line):
        """
        Handles the end-of-file signal.

        Parameters:
            line (str): The command line input.

        Returns:
            bool: True to exit the interface.

        """
        self.save_history()
        return True

    # def do_clear(self, line):
    #     """
    #     Clears the Screen
    #     """
    #     result = None
    #
    #     try:
    #         result = subprocess.run(["clear"], capture_output=True)
    #     except OSError as err:
    #         print(err)
    #         return
    #
    #     print(result.stderr.decode(), end="")
    #     print(result.stdout.decode(), end="")

    def emptyline(self):
        """
        Handles empty input.

        """
        pass

    # def default(self, line):
    #     pattern = re.match(r'^([A-Z]\w*)?\s*\.\s*([A-Za-z]\w*)\((.*)\)$', line)
    #     if not pattern:
    #         super().default(line)
    #         return
    #
    #     class_name, function_name, args_literal = pattern.groups()
    #     if function_name not in self.__airbnb_commands:
    #         super().default(line)
    #         return
    #
    #     args = None
    #     try:
    #         if args_literal:
    #             args = ast.literal_eval(args_literal)
    #     except SyntaxError as err:
    #         print(err)
    #         super().default(line)
    #         return
    #
    #     tokens = [class_name, args]
    #     self.__airbnb_commands[function_name].set_tokens(tokens)
    #     self.__airbnb_commands[function_name].execute(line)

    def precmd(self, line):
        """
        Processes the command before execution.

        Parameters:
            line (str): The command line input.

        Returns:
            str: The processed command line input.

        """
        # self.add_history(line)

        tokens = self.parse_line(line)
        if not tokens:
            return ""

        command = tokens[0]

        self.__current_cmd = command
        if command in self.__airbnb_commands:
            self.__airbnb_commands[command].set_tokens(tokens[1:])

        return line.strip()

    def add_history(self, line):
        self.__history.append(line)
        history_length = len(self.__history)

        if history_length > self.__MAX_HIS:
            self.__history.pop(0)

    @staticmethod
    def parse_line(line):
        tokens = []

        try:
            tokens = shlex.split(line)
        except ValueError as err:
            print(err)
            return ""

        return tokens

    def postcmd(self, stop, line):
        """
        Processes the command after execution.

        Parameters:
            stop (bool): Flag indicating whether to stop further processing.
            line (str): The command line input.

        Returns:
            bool: Flag indicating whether to stop further processing.

        """
        if self.__current_cmd in self.__airbnb_commands:
            self.__airbnb_commands[self.__current_cmd].reset_tokens()

        self.__current_cmd = ""
        return stop

    def load_history(self):
        """Loads the command history from the file (if it exists)."""
        try:
            with open(self.__history_file, "r") as file:
                for line in file:
                    line = line.strip("\n")
                    self.__history.append(line)
                    readline.add_history(line)

                history_length = len(self.__history)
                if history_length > self.__MAX_HIS:
                    self.__history = self.__history[history_length - self.__MAX_HIS:]

        except FileNotFoundError:
            pass

    def save_history(self):
        """Saves the current command history to the file."""
        with open(self.__history_file, "w") as file:
            for line in self.__history:
                file.write(f"{line}\n")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
