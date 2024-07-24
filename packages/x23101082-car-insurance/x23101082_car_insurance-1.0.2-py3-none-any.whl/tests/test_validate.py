
import unittest
from  library.validate import is_between

class ValidateGreater(unittest.TestCase):

	def test_validate(self):
		self.assertEqual(is_between(12, 10,20), False)
		self.assertEqual(is_between(10, 20, 30), True)

unittest.main()
