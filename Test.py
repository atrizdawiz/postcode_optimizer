import unittest
from PostCodeOptimizer import PostCodeOptimizer

class RangeFinderTestCase(unittest.TestCase):

   def test_one(self):
       text_input_filename = "test-input1.txt" # 10012, 10044, 10153, 10154, 10155, 10156

       postCodeOptimizer = PostCodeOptimizer(text_input_filename)
       post_dictionary = PostCodeOptimizer.postal_dictionary_creator(postCodeOptimizer)
       result = postCodeOptimizer.postal_range_finder(post_dictionary)
       self.assertEqual(result, "10012,10044,10153-10156")

   def test_unsorted_input(self):
       text_input_filename = "test-input-unsorted.txt"  # 10012, 10154, 10153, 10155, 10156, 10044
       postCodeOptimizer = PostCodeOptimizer(text_input_filename)
       post_dictionary = PostCodeOptimizer.postal_dictionary_creator(postCodeOptimizer)
       result = postCodeOptimizer.postal_range_finder(post_dictionary)
       self.assertEqual(result, "10012,10044,10153-10156")

   def test_bad_character_input(self):
       text_input_filename = "test-input-bad-characters.txt"  # 10012, 10154, 10a53, 10155, 10156, 10044
       postCodeOptimizer = PostCodeOptimizer(text_input_filename)
       post_dictionary = PostCodeOptimizer.postal_dictionary_creator(postCodeOptimizer)
       result = postCodeOptimizer.validate_input(text_input_filename)
       self.assertEqual(result, False)