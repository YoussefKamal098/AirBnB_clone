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
        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """removes the file.json temporary file"""
        try:
            os.remove("file.json")
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

    def test_class_name_all_prints_instances(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('BaseModel.all()')
            self.assertIn("BaseModel", output.getvalue())
            self.assertGreaterEqual(output.getvalue().count("BaseModel"), 2)

    def test_class_name_count_prints_instances(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Place')
            self.cmd.onecmd('create Place')
            self.cmd.onecmd('create Place')
            self.cmd.onecmd('create Place')
            self.cmd.onecmd('create Place')
            self.cmd.onecmd('Place.count()')
            self.assertIn('5', output.getvalue())

    def test_class_name_show_prints_an_instance(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            _id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'BaseModel.show("{_id}")')
            self.assertIn("BaseModel", output.getvalue())

    def test_class_name_destroy_deletes_an_object(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            _id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'BaseModel.destroy("{_id}")')
            self.cmd.onecmd(f'show BaseModel {_id}')
            self.assertIn("** no instance found **", output.getvalue())

    def test_class_name_update_updates_instance(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Review')
            _id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'Review.update("{_id}", "age", "22")')
            self.cmd.onecmd(f'show Review {_id}')
            self.assertIn('age', output.getvalue())

    def test_class_name_update_updates_instance_with_dict(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Amenity')
            _id = output.getvalue().strip('\n')
            dict_att = "{ 'name' : 'julia', 'age' : 25 }"
            self.cmd.onecmd(f'Amenity.update("{_id}", {dict_att})')
            self.cmd.onecmd(f'show Amenity {_id}')
            self.assertIn('name', output.getvalue())
            self.assertIn('julia', output.getvalue())
            self.assertIn('age', output.getvalue())

    def test_instance_update_with_dict(self):
        models = ['BaseModel', 'User', 'Place',
                  'City', 'Amenity', 'State', 'Review']

        for model in models:
            with self.subTest(model = model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    dict_attr = "{ 'name' : 'julia', 'age' : 25}"
                    self.cmd.onecmd(f'{model}.update("{_id}", {dict_attr})')
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn('name', output.getvalue())
                    self.assertIn('julia', output.getvalue())
                    self.assertIn('age', output.getvalue())


if __name__ == "__main__":
    unittest.main()
