#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorageInstantiation
    TestFileStorageMethods
"""
import json
import os
import models
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        storage = FileStorage()
        self.assertEqual(type(storage), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorageMethods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        base_model = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()

        models.storage.new(base_model)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)

        objects_keys = models.storage.all().keys()
        objects_values = models.storage.all().values()

        self.assertIn("BaseModel." + base_model.id, objects_keys)
        self.assertIn(base_model, objects_values)

        self.assertIn("User." + user.id, objects_keys)
        self.assertIn(user, objects_values)

        self.assertIn("State." + state.id, objects_keys)
        self.assertIn(state, objects_values)

        self.assertIn("Place." + place.id, objects_keys)
        self.assertIn(place, models.storage.all().values())

        self.assertIn("City." + city.id, objects_keys)
        self.assertIn(city, objects_values)

        self.assertIn("Amenity." + amenity.id, objects_keys)
        self.assertIn(amenity, objects_values)

        self.assertIn("Review." + review.id, objects_keys)
        self.assertIn(review, objects_values)

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), None)

    def test_save(self):
        base_model = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()

        models.storage.new(base_model)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)

        models.storage.save()

        with open("file.json", "r") as file:
            deserialized_objects = json.load(file)

            self.assertIn("BaseModel." + base_model.id, deserialized_objects)
            self.assertIn("User." + user.id, deserialized_objects)
            self.assertIn("State." + state.id, deserialized_objects)
            self.assertIn("Place." + place.id, deserialized_objects)
            self.assertIn("City." + city.id, deserialized_objects)
            self.assertIn("Amenity." + amenity.id, deserialized_objects)
            self.assertIn("Review." + review.id, deserialized_objects)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        base_model = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()

        models.storage.new(base_model)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)

        models.storage.save()
        models.storage.reload()

        objects = models.storage.all()

        self.assertIn("BaseModel." + base_model.id, objects)
        self.assertIn("User." + user.id, objects)
        self.assertIn("State." + state.id, objects)
        self.assertIn("Place." + place.id, objects)
        self.assertIn("City." + city.id, objects)
        self.assertIn("Amenity." + amenity.id, objects)
        self.assertIn("Review." + review.id, objects)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
