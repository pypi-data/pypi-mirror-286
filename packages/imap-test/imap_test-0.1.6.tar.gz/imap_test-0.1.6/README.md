
# imap_test

## Introduction
This is a tool to convert Opendrive to Apollo base map, which is modified from
[apollo's imap tool](https://github.com/daohu527/imap), 
and supports generating adjacent reverse lanes of different roads.

## Quick Start
To generate Apollo base map from Opendrive file, you can run the following command:
```bash
# Method 1 [Recommended]
pip install imap_test
imap -f -i imap/data/town.xodr -o imap/data/base_map.txt
# Method 2
python3 imap/main.py -f -i imap/data/town.xodr -o imap/data/base_map.txt
# Method 3
python3 setup.py develop
imap -f -i imap/data/town.xodr -o imap/data/base_map.txt
```

## New Features
### v0.1.3
If you want to generate adjacent reverse lanes for each lane, you can run the following command:
```bash
imap -f -i imap/data/town.xodr -o imap/data/base_map.txt -r
```
The `-r` option is used to generate adjacent reverse lanes.

For visualization, you can use the following command:
```bash
imap -m imap/data/apollo_map.txt
```

### v0.1.4
For global speed limit, you can use the following command:
```bash
imap -f -i imap/data/town.xodr -o imap/data/base_map.txt -sl 7.0
```
The `-sl` option is used to set the global speed limit, which is 
followed by a float number. Here, the global speed limit is set to 7.0 m/s.


### v0.1.5
For adding additional junction polygon points, you can use the following command:
```bash
-f -i imap/data/nansha_map_normal.xodr -o imap/data/base_map.txt -r -sl 7.0 -a 96 98.0 97.99999999999997 -a 593 618.0 98.0
```
The `-a` option is used to add additional junction polygon points, which is followed by three float numbers, 
(junction_id, x, y). Here, you will see log:
```
Adding point (98.0, 97.99999999999997) to junction 96
Adding point (618.0, 98.0) to junction 593
```

### fix

when converting reverse map, left/right most boundary may not be accurate, so add `-rb` command to fix it:
```bash
imap -f -i imap/data/town.xodr -o imap/data/base_map.txt -r -rb
```

### v0.1.6
For adding additional junction lane forward neighbors, you can use the following command:
```bash
-f -i imap/data/nansha_map_normal.xodr -o imap/data/base_map.txt -e
```
The `-e` option is used to add additional junction lane forward neighbors.