#!/usr/bin/python3
"""
This module defines the HBNBCommand class, which implements
a command-line interface for an AirBnB-like application.
"""

import cmd
import shlex
import ast
import re
import subprocess
from console_commands import AirBnBCommand
from console_commands import CreateCommand
from console_commands import ShowCommand
from console_commands import AllCommand
from console_commands import DestroyCommand
from console_commands import UpdateCommand
from console_commands import CountCommand
from models import storage
import readline


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class represents the command-line interface for
    the AirBnB-like application.
   """

    prompt: str = "(hbnb) "
    __history_file: str = ".airbnb_cmd_history.txt"
    __history: list[str] = []
    __MAX_HIS: int = 100
    __current_cmd: str = ""

    __airbnb_commands: dict[str, AirBnBCommand] = {
        "create": CreateCommand(storage),
        "show": ShowCommand(storage),
        "destroy": DestroyCommand(storage),
        "all": AllCommand(storage),
        "update": UpdateCommand(storage),
        "count": CountCommand(storage)
    }

    def preloop(self) -> None:
        self.load_history()

    def do_create(self, line: str) -> None:
        """
        Create a new class instance and print its id.
        Usage: create <class>
        """
        self.__airbnb_commands["create"].execute()

    def do_show(self, line: str) -> None:
        """
        Display the string representation of a class instance of a given id.
        Usage: show <class> <id>
        """
        self.__airbnb_commands["show"].execute()

    def do_destroy(self, line: str) -> None:
        """
        Delete a class instance of a given id.
        Usage: destroy <class> <id>
        """
        self.__airbnb_commands["destroy"].execute()

    def do_all(self, line: str) -> None:
        """
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.

        Usage: all or all <class>
        """
        self.__airbnb_commands["all"].execute()

    def do_update(self, line: str) -> None:
        """
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.

        Usage: update <class> <id> <attribute_name> <attribute_value>
        """
        self.__airbnb_commands["update"].execute()

    def do_quit(self, line: str) -> bool:
        """
        Quits the command-line interface.

        Parameters:
            line (str): The command line input.

        Returns:
            bool: True to exit the interface.

        """
        self.save_history()
        return True

    def do_EOF(self, line: str) -> bool:
        """
        Handles the end-of-file signal.

        Parameters:
            line (str): The command line input.

        Returns:
            bool: True to exit the interface.

        """
        self.save_history()
        return True

    def do_clear(self, line: str) -> None:
        """
        Clears the Screen
        """
        try:
            result = subprocess.run(["clear"], capture_output=True)
        except OSError as err:
            print(err)
            return

        print(result.stderr.decode(), end="")
        print(result.stdout.decode(), end="")

    def default(self, line: str) -> None:
        """
        Handles unmatched commands by delegating execution to
        the parent class's default method. If parsing fails,
        an error message is printed.

        Parameters:
            line (str): The command line input.

        Returns:
            None
        """
        extracted_data = self.extract_method_call(line)

        if not extracted_data:
            super().default(line)
            return

        class_name, function_name, function_args = extracted_data

        tokens = [class_name]

        if isinstance(function_args, tuple):
            tokens.extend(function_args)
        else:
            tokens.append(function_args)

        self.__airbnb_commands[function_name].set_tokens(tokens)
        self.__airbnb_commands[function_name].execute()

    def extract_method_call(self, line: str) -> tuple[any, any, any] | None:
        """
        Extracts method call information (class name, function name, arguments)
        from a line using regular expressions. Handles potential errors during
        argument parsing.

        Parameters:
            line (str): The command line input.

        Returns:
            tuple or None: A tuple containing (class_name, function_name, args)
            if successful, None otherwise.
        """
        pattern = re.match(r'^([A-Z]\w*)?\s*\.\s*([A-Za-z]\w*)\((.*)\)$', line)
        if not pattern:
            return None

        class_name, function_name, function_args_literal = pattern.groups()
        if function_name not in self.__airbnb_commands:
            return None

        function_args = None
        try:
            if function_args_literal:
                function_args = ast.literal_eval(function_args_literal)
        except (SyntaxError, ValueError) as err:
            print(err)
            return None

        return class_name, function_name, function_args

    def emptyline(self: str) -> None:
        """
        Handles empty input.
        """
        pass

    def precmd(self, line: str) -> str:
        """
        Processes the command before execution.
        Parameters:
            line (str): The command line input.
        Returns:
            str: The processed command line input.

        """
        self.add_history(line)

        tokens = self.parse_line(line)
        if not tokens:
            return ""

        command = tokens[0]

        self.__current_cmd = command
        if command in self.__airbnb_commands:
            self.__airbnb_commands[command].set_tokens(tokens[1:])

        return line.strip()

    @staticmethod
    def parse_line(line: str) -> list[str] | str:
        """
        Splits a command line input string into a list of tokens using shlex.
        Parameters:
            line (str): The command line input string.
        Returns:
            list: A list of tokens parsed from the input string,
            or an empty list if parsing fails.
        """
        try:
            tokens = shlex.split(line)
            return tokens
        except ValueError as err:
            print(err)
            return ""

    def postcmd(self, stop, line: str) -> bool:
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

    def add_history(self, line: str) -> None:
        """
        Adds a command line input to the command history,
        maintaining a maximum size.
        Parameters:
            line (str): The command line input to be added.
        """
        self.__history.append(line)
        history_length = len(self.__history)

        if history_length > self.__MAX_HIS:
            self.__history.pop(0)

    def load_history(self) -> None:
        """Loads the command history from the file (if it exists)."""
        try:
            with open(self.__history_file, "r") as file:
                for line in file:
                    line = line.strip("\n")
                    self.__history.append(line)
                    readline.add_history(line)

                history_length = len(self.__history)
                if history_length > self.__MAX_HIS:
                    self.__history =\
                        self.__history[history_length - self.__MAX_HIS:]

        except FileNotFoundError:
            pass

    def save_history(self) -> None:
        """Saves the current command history to the file."""
        with open(self.__history_file, "w") as file:
            for line in self.__history:
                file.write(f"{line}\n")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
