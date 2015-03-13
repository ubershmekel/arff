# How are python types serialized to arff #
Using the repr() function. So strings get their quotes escaped and integers, floats, and booleans are formatted perfectly. You can customize your arff reader or writer by modifying its pytypes attribute.

# How to make nominal attributes #
[Nominal attributes](http://weka.wikispaces.com/ARFF+%28stable+version%29#Examples-The%20@attribute%20Declarations-Nominal%20attributes) are useful when you want to make decision trees algorithms. By default, booleans variables become nominals, here's an example on how to make integer types become nominal:

```
output = arff.Writer('results.arff', relation='diabetics_data', names=new_headers)
output.pytypes[int] = '{1,2,3,4}'
```

The top of the arff file is generated when the first row is written. Because pytypes was modified - if arff.py sees an int, it will declare that column to contain '{1,2,3,4}':

```
@attribute TheNameOfThatColumn {1,2,3,4}
```

Changing pytypes after the first row is written will not affect the writer.

# Another way to output nominal attributes #
```
arff_writer = arff.Writer(fname, relation='diabetics_data', names)
arff_writer.pytypes[arff.nominal] = '{not_parasite,parasite}'
arff_writer.write([arff.nominal('parasite')])
```