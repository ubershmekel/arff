To install this or any python package from source use:

    python setup.py install

You can also use pip:

    pip arff


Arff files are very much like CSV files except they have typing information.

Read arff files
-----

    >>> import arff
    >>> for row in arff.load('example.arff'):
    ...     x = row.hair_color
    ...     y = row[-1]
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

Write arff files:
-----

    >>> data = [[1,2,'a'], [3, 4, 'john']]
    >>> arff.dump(open('result.arff', 'w'), data, relation="whatever", names=['num', 'day', 'title'])

results in the creation of this file:

    @relation whatever
    @attribute num integer
    @attribute day integer
    @attribute title string
    @data
    1,2,'a'
    3,4,'john'


How are python types serialized to arff
-----
Using the repr() function. So strings get their quotes escaped and integers, floats, and booleans are formatted perfectly. You can customize your arff reader or writer by modifying its pytypes attribute.

How to make nominal attributes
-----
Nominal attributes are useful when you want to make decision trees algorithms. By default, booleans variables become nominals, here's an example on how to make integer types become nominal:

    output = arff.Writer('results.arff', relation='diabetics_data', names=new_headers)
    output.pytypes[int] = '{1,2,3,4}'

The top of the arff file is generated when the first row is written. Because pytypes was modified - if arff.py sees an int, it will declare that column to contain '{1,2,3,4}':

    @attribute TheNameOfThatColumn {1,2,3,4}

Changing pytypes after the first row is written will not affect the writer.

Another way to output nominal attributes
-----

    arff_writer = arff.Writer(fname, relation='diabetics_data', names)
    arff_writer.pytypes[arff.nominal] = '{not_parasite,parasite}'
    arff_writer.write([arff.nominal('parasite')])
