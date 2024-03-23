#!/usr/bin/python3

"""
Module: AirBnBCommand

This module defines a set of commands used in an AirBnB application.

Classes:
    - AirBnBCommand: Abstract base class for AirBnB commands.
    - CreateCommand: Command to create a new object.
    - ShowCommand: Command to display details of an object.
    - DestroyCommand: Command to delete an object.
    - AllCommand: Command to display all objects of a specific type.
    - UpdateCommand: Command to update attributes of an object.

"""

from abc import ABC, abstractmethod


class AirBnBCommand(ABC):
    """
    AirBnBCommand is an abstract base class for defining
    command objects in an AirBnB application.

    Attributes:
        __tokens (dict): A dictionary containing tokens used by the command.
        _storage (object): A storage object used to interact with the database.

    Methods:
        reset_tokens(cls): Resets the tokens dictionary to default values.
        set_tokens(cls, tokens): Sets the tokens based on the provided values.
        get_model_name(self): Retrieves the model name token.
        get_instance_id(self): Retrieves the instance ID token.
        get_attribute_name_value_pair(self): Retrieves attribute
        name-value pair tokens.
        get_model_class(self): Retrieves the model class based on
        the model name.
        get_model_instance(self): Retrieves the model instance based on
        the model class and instance ID.
        execute(self, line): Abstract method to execute the command.

    """

    __tokens = {
            "model_name": None,
            "instance_id": None,
            "attribute_name": None,
            "attribute_value": None
    }

    def __init__(self, storage):
        """
        Initializes a new instance of the AirBnBCommand class.

        Parameters:
            storage (Storage): A storage object used to interact with
            the database.

        """
        self._storage = storage

    @abstractmethod
    def execute(self, line):
        """
        Abstract method to execute the command.

        Parameters:
            line (str): The command line input.

        """
        pass

    @classmethod
    def reset_tokens(cls):
        """
        Resets the tokens dictionary to default values.

        """
        for key in cls.__tokens.keys():
            cls.__tokens[key] = None

    @classmethod
    def set_tokens(cls, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list): A list of token values.

        """
        for key, value in zip(cls.__tokens, tokens):
            cls.__tokens[key] = value

    def get_model_name(self):
        """
        Retrieves the model name token.

        Returns:
            str: The model name token.

        """
        model_name = self.__tokens.get("model_name", None)

        if not model_name:
            print("** class name missing **")
            return None

        return model_name

    def get_instance_id(self):
        """
        Retrieves the instance ID token.

        Returns:
            str: The instance ID token.

        """
        _id = self.__tokens.get("instance_id", None)

        if not _id:
            print("** instance id missing **")
            return None

        return _id

    def get_attribute_name_value_pair(self):
        """
        Retrieves attribute name-value pair tokens.

        Returns:
            dict: A dictionary containing attribute name-value pair.

        """
        attribute_name = self.__tokens.get("attribute_name")
        attribute_value = self.__tokens.get("attribute_value")

        if not attribute_name:
            print("** attribute name missing **")
            return None
        if not attribute_value:
            print("** value missing **")
            return None

        return {"attribute_name": attribute_name,
                "attribute_value": attribute_value}

    def get_model_class(self):
        """
        Retrieves the model class based on the model name.

        Returns:
            class: The model class.

        """
        model_name = self.get_model_name()
        if not model_name:
            return None

        model_class = self._storage.get_model_class(model_name)
        if not model_class:
            return None

        return model_class

    def get_model_instance(self):
        """
        Retrieves the model instance based on the model class and instance ID.

        Returns:
            tuple: A tuple containing the model class and model instance.

        """
        model_class = self.get_model_class()
        if not model_class:
            return None

        _id = self.get_instance_id()
        if not _id:
            return None

        instance = self._storage.find_obj(model_class.__name__, _id)
        if not instance:
            return None

        return model_class, instance


class CreateCommand(AirBnBCommand):
    """
    CreateCommand is a concrete subclass of AirBnBCommand for
    creating new objects.

    Methods:
        execute(self, line): Executes the create command.

    """

    def execute(self, line):
        """
        Executes the create command.

        Parameters:
            line (str): The command line input.

        """
        model_class = self.get_model_class()
        if not model_class:
            return

        model_class().save()


class ShowCommand(AirBnBCommand):
    """
    ShowCommand is a concrete subclass of AirBnBCommand for
    displaying object details.

    Methods:
        execute(self, line): Executes the show command.

    """

    def execute(self, line):
        """
        Executes the show command.

        Parameters:
            line (str): The command line input.

        """
        model_instance = self.get_model_instance()
        if not model_instance:
            return

        _, instance = model_instance
        print(instance)


class DestroyCommand(AirBnBCommand):
    """
    DestroyCommand is a concrete subclass of AirBnBCommand for
    deleting objects.

    Methods:
        execute(self, line): Executes the destroy command.

    """

    def execute(self, line):
        """
        Executes the destroy command.

        Parameters
        line (str): The command line input.

        """
        model_instance = self.get_model_instance()
        if not model_instance:
            return

        model_class, instance = model_instance
        self._storage.remove_obj(model_class.__name__, instance.id)


class AllCommand(AirBnBCommand):
    """
    AllCommand is a concrete subclass of AirBnBCommand for
    displaying all objects or objects of a specific type.

    Methods:
        execute(self, line): Executes the all command.

    """

    def execute(self, line):
        """
        Executes the all command.

        Parameters:
            line (str): The command line input.

        """
        if not line:
            print(self._storage.find_all())
            return

        model_class = self.get_model_class()
        if not model_class:
            return

        print(self._storage.find_all(model_name=model_class.__name__))


class UpdateCommand(AirBnBCommand):
    """
    UpdateCommand is a concrete subclass of AirBnBCommand for
    updating attributes of an object.

    Methods:
        execute(self, line): Executes the update command.

    """

    def execute(self, line):
        """
        Executes the update command.

        Parameters:
            line (str): The command line input.

        """
        model_instance = self.get_model_instance()
        if not model_instance:
            return

        model_class, instance = model_instance
        attribute_name_value_pair = self.get_attribute_name_value_pair()
        if not attribute_name_value_pair:
            return

        self._storage.update_obj_attribute(
            model_class.__name__, instance.id,
            **attribute_name_value_pair
        )
