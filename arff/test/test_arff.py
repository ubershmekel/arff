

import unittest

import arff

def u(text):
	if str == bytes:
		return text.decode('utf-8')
	else:
		# python 3
		return text

class TestArff(unittest.TestCase):
	def test_read(self):
		text = u('''@relation diabetics_data
@attribute hair_color {blonde, black, blue}
@attribute age real
@attribute patno integer
@data
blonde, 17.2, 1
blue, 27.2, 2
blue, 18.2, 3
''')
		expected = [
			['blonde', 17.2, 1],
			['blue', 27.2, 2],
			['blue', 18.2, 3],
			]
			
		result = list(arff.loads(text))
		result = [list(row) for row in result]
		
		self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

