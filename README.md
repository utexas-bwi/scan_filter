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
