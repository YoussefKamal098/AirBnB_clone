#!/usr/bin/python3
"""Module test_amenity

This Module contains a tests for Amenity Class
"""

import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand


class TestConsole(unittest.TestCase):
    """Tests the console application"""
    @classmethod
    def setUpClass(cls):
        """sets up the test console"""
        cls.models = ['BaseModel', 'User', 'Place',
                      'City', 'Amenity', 'State', 'Review']
        try:
            os.rename("file.json", "tmp")
        except OSError:
            pass

        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """removes the file.json temporary file"""
        try:
            os.remove("file.json")
        except OSError:
            pass

        try:
            os.rename("tmp", "file.json")
        except OSError:
            pass

    def test_create_prints_class_name_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_create_prints_class_does_not_exist_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BModel')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_create_creates_an_instance(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            _id = output.getvalue()
            self.assertNotIn(_id, [None, ""])

        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'show BaseModel {_id}')
            self.assertIn(_id.strip('\n'), output.getvalue())

    def test_show_prints_class_name_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_show_prints_class_does_not_exist_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show BModel')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_show_prints_an_instance(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            _id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'show BaseModel {_id}')
            self.assertIn("BaseModel", output.getvalue())

    def test_destroy_prints_class_name_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_destroy_prints_class_does_not_exist(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy BModel')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_destroy_prints_instance_not_found(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy BaseModel "id that doesn\'t exists"')
            self.assertIn("** no instance found **", output.getvalue())

    def test_destroy_deletes_an_instance(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            _id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'destroy BaseModel {_id}')
            self.cmd.onecmd(f'show BaseModel {_id}')
            self.assertIn("** no instance found **", output.getvalue())

    def test_all_displays_instance_instance(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd(f'all')
            self.assertIn("BaseModel", output.getvalue())
            self.assertGreaterEqual(output.getvalue().count("BaseModel"), 2)

    def test_all_prints_class_instances(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('create User')
            self.cmd.onecmd('all User')
            self.assertIn("User", output.getvalue())
            self.assertNotIn("BaseModel", output.getvalue())

    def test_update_attribute_name_missing_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            _id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'update BaseModel {_id}')
            self.assertIn("** attribute name missing **", output.getvalue())

    def test_update_attribute_value_missing_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            _id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'update BaseModel {_id} first_name')
            self.assertIn("** value missing **", output.getvalue())

    def test_update_updates_instance(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create State')
            _id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'update State {_id} name example_state')
            self.cmd.onecmd(f'show State {_id}')
            self.assertIn('name', output.getvalue())
            self.assertIn('example_state', output.getvalue())

    def test_class_name_all_displays_instances(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    self.cmd.onecmd(f'create {model}')
                    self.cmd.onecmd(f'{model}.all()')
                    self.assertIn(model, output.getvalue())
                    self.assertGreaterEqual(output.getvalue().count(model), 2)

    def test_class_name_instances_count(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()):
                    for _ in range(10):
                        self.cmd.onecmd(f'create {model}')

                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'{model}.count()')
                    self.assertLessEqual(10, int(output.getvalue()))

    def test_class_name_instance_show(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    self.cmd.onecmd(f'{model}.show("{_id}")')
                    self.assertIn(model, output.getvalue())

    def test_class_name_instance_destroy(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    self.cmd.onecmd(f'{model}.destroy("{_id}")')
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn('** no instance found **', output.getvalue())

    def test_class_name_instance_update_with_key_value_pair(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    key, value = "name", "Julia"
                    self.cmd.onecmd(
                        f'{model}.update("{_id}", "{key}", "{value}")')
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn('name', output.getvalue())
                    self.assertIn('Julia', output.getvalue())

    def test_class_name_instance_update_with_dict(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    dict_attr = "{ 'name' : 'Julia', 'age' : 25}"
                    self.cmd.onecmd(f'{model}.update("{_id}", {dict_attr})')
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn('name', output.getvalue())
                    self.assertIn('25', output.getvalue())
                    self.assertIn('Julia', output.getvalue())
                    self.assertIn('age', output.getvalue())


if __name__ == "__main__":
    unittest.main()
