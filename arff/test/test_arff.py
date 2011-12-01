'''
unittests for arff.py
'''

import unittest
import os

import arff
from arff import u

SRC_DIR = os.path.dirname(os.path.abspath(__file__))


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
        list_result = [list(row) for row in result]
        
        self.assertEqual(list_result, expected)
        
        self.assertEqual(result[0].hair_color, 'blonde')
        
    def test_write(self):
        table = [
            ['blonde', 17.2, 1],
            ['blue', 27.2, 2],
            ['blue', 18.2, 3],
            ]
        
        expected = [
            '@relation untitled',
            '@attribute attr0 string',
            '@attribute attr1 real',
            '@attribute attr2 integer',
            '@data',
            "'blonde',17.2,1",
            "'blue',27.2,2",
            "'blue',18.2,3"
            ]
        
        
        
        res = arff.dump_lines(table)
        res = list(res)
        
        self.assertEqual(res, expected)
        
    def test_files(self):
        fname = os.path.join(SRC_DIR, 'example.arff')
        data = [
            ['blonde', 17.2, 1],
            ['blue', 27.2, 2],
            ['blue', 18.2, 3],
            ]        
        arff.dump(fname, data, relation='diabetics_data', names=('hair_color', 'age', 'patno'))
        data = list(arff.load(os.path.join(SRC_DIR, fname)))
        arff_rows = arff.dumps(data)
        reparsed_data = list(arff.loads(arff_rows))
        
        data = [list(row) for row in data]
        reparsed_data = [list(row) for row in reparsed_data]
        
        self.assertEqual(data, reparsed_data)
        
        

if __name__ == '__main__':
    unittest.main()

