Arff files are very much like CSV files except they have typing information.

Read arff files:
```
    >>> import arff
    >>> for row in arff.load('example.arff'):
    ...     x = row.hair_color
    ...     y = row[-1]
    ...
    >>> print(list(arff.load('example.arff')))
    [[Row(hair_color='blonde', age=17.2, patno=1),
     Row(hair_color='blue', age=27.2, patno=2),
     Row(hair_color='blue', age=18.2, patno=3)]
```


Where this is the example file:
```
@relation diabetics_data
@attribute hair_color {blonde, black, blue}
@attribute age real
@attribute patno integer
@data
blonde, 17.2, 1
blue, 27.2, 2
blue, 18.2, 3
```

Write arff files:

```
    >>> data = [[1,2,'a'], [3, 4, 'john']]
    >>> arff.dump(open('result.arff', 'w'), data, relation="whatever", names=['num', 'day', 'title'])
```

results in the creation of this file:
```
@relation whatever
@attribute num integer
@attribute day integer
@attribute title string
@data
1,2,'a'
3,4,'john'
```