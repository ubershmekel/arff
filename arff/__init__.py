'''
Weka arff file type reader for python.

Usage:

    >>> import arff
    >>> for row in arff.load('example.arff'):
    ...     print(row.hair_color)
    ...     print(row[-1])
    ...
    >>> print(list(arff.load('example.arff')))
    [[Row(hair_color='blonde', age=17.2, patno=1),
     Row(hair_color='blue', age=27.2, patno=2),
     Row(hair_color='blue', age=18.2, patno=3)]
    
     

Where this is the example file:

@relation diabetics_data
@attribute hair_color {blonde, black, blue}
@attribute age real
@attribute patno integer
@data
blonde, 17.2, 1
blue, 27.2, 2
blue, 18.2, 3

-----
    >>> data = [[1,2,'a'], [3, 4, 'john']]
    >>> arff.dump('result.arff', data, relation="whatever", names=['num', 'day', 'title'])

results in the creation of this file:

@relation whatever
@attribute num integer
@attribute day integer
@attribute title string
@data
1,2,'a'
3,4,'john'


-----

supports: numeric, integer, real, string

in the future: dates

Tested on python 2.7 and 3.2

License: BSD, do what you wish with this. Could be awesome to hear if you found
it useful and/or you have suggestions. ubershmekel at gmail

Based on http://weka.wikispaces.com/ARFF+%28stable+version%29


'''

import os
import io
import csv
from collections import namedtuple

COMMENT = '%'
SPECIAL = '@'
RELATION = '@relation'
ATTRIBUTE = '@attribute'
DATA = '@data'

def str_remove_quotes(obj):
    return str(obj[1:-1])

    
ARFF_TYPES = {
    'numeric': float,
    'integer': int,
    'real': float,
    'string': str_remove_quotes,
}

PYTHON_TYPES = {
    float: 'real',
    int: 'integer',
    str: 'string',
}

# python2/3 compatible unicode
def u(text):
    if str == bytes:
        return text.decode('utf-8')
    else:
        # python 3
        return text
    
    
class _Nominal:
    '''an enum in arff'''
    def __init__(self, name, type_text):
        self.name = name
        self.type_text = type_text
        values_str = type_text.strip('{} ')
        self.options = values_str.split()
        self.options = [opt.strip(', ') for opt in self.options]
    
    def parse(self, text):
        if text in self.options:
            return text
        else:
            raise ValueError("'%s' is not in {%s}" % (text, self.options))

class _SimpleType:
    def __init__(self, name, type_text):
        self.name = name
        self.type = ARFF_TYPES[type_text]
    def parse(self, text):
        return self.type(text)

def _field_type(name, type_text):
    if type_text in ARFF_TYPES:
        return _SimpleType(name, type_text)
    
    if type_text.startswith('{'):
        return _Nominal(name, type_text)
    
    raise ValueError("Unrecognized attribute type: %s" % type_text)

    #'date': date_format,


def _parse_types(row, fields):
    typed_row = []
    for i, ftype in enumerate(fields):
        typed_row.append(ftype.parse(row[i]))
    
    return typed_row

class _RowParser:
    def __init__(self, fields):
        self.fields = fields
        self.tuple = namedtuple('Row', [f.name for f in fields])
    
    def parse(self, row):
        values = []
        for f, item in zip(self.fields, row):
            values.append(f.parse(item))
        
        return self.tuple(*values)

def loads(text):
    if bytes == str:
        if type(text) != unicode:
            raise ValueError('arff.loads works with unicode strings only')
    else:
        if type(text) != str:
            raise ValueError('arff.loads works with strings only')
    lines_iterator = io.StringIO(text)
    for item in reader(lines_iterator):
        yield item


def load(fname):
    with open(fname, 'r') as fhand:
        for item in reader(fhand):
            yield item

def reader(lines_iterator):
    fields = []
    
    for line in lines_iterator:
        if line.startswith(COMMENT):
            continue
        
        if line.lower().startswith(DATA):
            break
        
        if line.lower().startswith(RELATION):
            _, name = line.split()
        
        if line.lower().startswith(ATTRIBUTE):
            space_separated = line.split(' ', 2)
            name = space_separated[1]
            field_type_text = space_separated[2].strip()
            
            fields.append(_field_type(name, field_type_text))
    
    # data
    reader = csv.reader(lines_iterator)
    row_parser = _RowParser(fields)
    for row in reader:
        typed_row = row_parser.parse(row)
        yield typed_row


def _convert_row(row):
    items = [repr(item) for item in row]
    return ','.join(items)
        
def dumps(*args, **kwargs):
    items = []
    rows_gen = (row for row in dump_lines(*args, **kwargs))
    return u(os.linesep).join(rows_gen)

    
    

def dump_lines(row_iterator, relation='untitled', names=None):
    if not hasattr(row_iterator, '__next__'):
        row_iterator = (item for item in row_iterator)
    first_row = next(row_iterator)
    ftypes = [PYTHON_TYPES[type(item)] for item in first_row]
    if names is None:
        names = ['attr%d' % i for i in range(len(first_row))]
    
    yield "%s %s" % (RELATION, relation)
    
    for name, f in zip(names, ftypes):
        yield "%s %s %s" % (ATTRIBUTE, name, f)
    
    yield DATA
    
    
    yield _convert_row(first_row)
    for row in row_iterator:
        yield _convert_row(row)

def dump(fname, *args, **kwargs):
    with open(fname, 'wb') as fhand:
        for row in dump_lines(*args, **kwargs):
            fhand.write(row + os.linesep)


