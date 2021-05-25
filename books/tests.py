from django.test import TestCase


class TestBookModel(TestCase):
    def setUp(self):
        self.book_data = {
            "title": "The lord of the rings",
            "description": "",
            "imageURL": "http://www.google.com/",
        }


class TestGenreModel(TestCase):
    pass


class TestAuthor(TestCase):
    pass
