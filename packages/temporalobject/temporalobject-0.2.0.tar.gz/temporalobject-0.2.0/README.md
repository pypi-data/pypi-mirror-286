# TemporalObject

`TemporalObject` is a custom Python class for storing and managing object states in a temporal sequence. It uses a deque with a fixed maximum length to maintain a rolling buffer of states, providing an efficient way to track the history of changes. Each state can be indexed by an integer, a string ID, or a slice, and the class keeps track of the current state index within the buffer.

## Installation

To use `TemporalObject`, ensure you have the required dependencies installed. You can install `LimitedDict` from the `temporal.util` module.

## Usage

### Class Definition

```python
import uuid
from collections import deque
from typing import Any
from temporal.util import LimitedDict

class TemporalObject:
    """
    An custom object for storing and managing its states in a temporal sequence.

    This class utilizes a deque with a fixed maximum length (maxlen) to maintain
    a rolling buffer of states.

    Each state can be indexed by an integer, a string ID, or a slice. The class
    also tracks the current state index within the buffer.

    Parameters
    ----------
    temporal_depth : int
        The maximum number of states to store.

    Attributes
    ----------
    buffer : deque
        A deque with a maxlen.
    id_index : LimitedDict
        A dictionary with a limit on the number of items it can store.

    Methods
    -------
    add(id: str, state: dict) -> None:
        Appends a state to the buffer.
    update(object) -> None:
        Adds the object's state to the buffer.
    get(key: str, relative_index: int = 0) -> dict:
        Returns the value of the object with the given key and relative index.
    current() -> dict:
        Returns the current state.
    """
```

### Initialization

Create an instance of `TemporalObject` by specifying the maximum number of states to store.

```python
temporal_object = TemporalObject(temporal_depth=100)
```

### Adding States

Use the `add` method to append a state to the buffer.

```python
temporal_object.add(id="state1", state={"key": "value"})
```

### Updating States

Use the `update` method to add the object's state to the buffer. If no temporal ID is provided, a new UUID will be generated.

```python
state = {"key": "new_value"}
temporal_id = temporal_object.update(object_state=state)
```

### Retrieving States

Retrieve a state using the `get` method by specifying the key and an optional relative index.

```python
state = temporal_object.get(key="state1", relative_index=0)
```

### Accessing the Current State

Get the current state using the `current` property.

```python
current_state = temporal_object.current
```

### Checking Buffer Length

Check the number of states in the buffer.

```python
buffer_length = len(temporal_object)
```

### Iterating Over States

Iterate over the states in the buffer.

```python
for state in temporal_object:
    print(state)
```

### Accessing States by Index

Access states by their index, temporal ID, or slice.

```python
state_by_index = temporal_object[0]
state_by_id = temporal_object["state1"]
```

## License

This project is licensed under the MIT License.
