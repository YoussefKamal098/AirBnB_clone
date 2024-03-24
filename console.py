#!/usr/bin/python3
"""
This module defines the HBNBCommand class, which implements
a command-line interface for an AirBnB-like application.
"""

import cmd
import shlex
import subprocess
from console_commands import AirBnBCommand
from console_commands import CreateCommand
from console_commands import ShowCommand
from console_commands import AllCommand
from console_commands import DestroyCommand
from console_commands import UpdateCommand
from models import storage


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

    __commands = {
        "create": CreateCommand(storage),
        "show": ShowCommand(storage),
        "destroy": DestroyCommand(storage),
        "all": AllCommand(storage),
        "update": UpdateCommand(storage)
    }

    def do_create(self, line):
        """
        Create a new class instance and print its id.
        Usage: create <class>
        """
        self.__commands["create"].execute(line)

    def do_show(self, line):
        """
        Display the string representation of a class instance of a given id.
        Usage: show <class> <id>
        """
        self.__commands["show"].execute(line)

    def do_destroy(self, line):
        """
        Delete a class instance of a given id.
        Usage: destroy <class> <id>
        """
        self.__commands["destroy"].execute(line)

    def do_all(self, line):
        """
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.

        Usage: all or all <class>
        """
        self.__commands["all"].execute(line)

    def do_update(self, line):
        """
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.

        Usage: update <class> <id> <attribute_name> <attribute_value>
        """
        self.__commands["update"].execute(line)

    def do_quit(self, line):
        """
        Quits the command-line interface.

        Parameters:
            line (str): The command line input.

        Returns:
            bool: True to exit the interface.

        """
        return True

    def do_EOF(self, line):
        """
        Handles the end-of-file signal.

        Parameters:
            line (str): The command line input.

        Returns:
            bool: True to exit the interface.

        """
        return True

    def do_clear(self, line):
        result = None

        try:
            result = subprocess.run(["clear"], capture_output=True)
        except OSError as err:
            print(err)
            return

        print(result.stderr.decode(), end="")
        print(result.stdout.decode(), end="")

    def emptyline(self):
        """
        Handles empty input.

        """
        pass

    def precmd(self, line):
        """
        Processes the command before execution.

        Parameters:
            line (str): The command line input.

        Returns:
            str: The processed command line input.

        """
        tokens = self.parse_line(line)
        if not tokens:
            return ""

        command = tokens[0]
        if command in tokens:
            AirBnBCommand.set_tokens(tokens[1:])

        return line.strip()

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
        AirBnBCommand.reset_tokens()
        return stop


if __name__ == '__main__':
    HBNBCommand().cmdloop()
