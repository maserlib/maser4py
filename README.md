# Usage

```python
filepath = "path/to/my/data/file.ext"
data = Data(filepath=filepath)
```

# Tests

Use `pytest -m "not test_data_required"` to skip tests that require test data (and to skip auto download).