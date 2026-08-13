# scan_filter

Ensures all lidar ranges fall within the specified bracket and republishes.

## Parameters

Pass different parameters if needed.

### min_range

```ros2 parameters
[default]:=0.1
```

### max_range

```ros2 parameters
[default]:=5.0
```

### ignored_indices

Can be used to discard faulty data or limit scan width using a formatted string of indices or ranges.

```ros2 parameters
[default]:=""
    Keeps all data
:="1:5,8:10,12"
    Discards indices 1, 2, 3, 4, 5, 8, 9, 10, 12
```

## Topics

Pass remappings if needed.

### Input Topic

```ros2 topics
/scan
```

### Output Topic

```ros2 topics
/filtered_scan
```
