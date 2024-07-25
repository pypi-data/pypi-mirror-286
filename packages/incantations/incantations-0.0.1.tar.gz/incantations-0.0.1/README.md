# Incantations

Incantations is a mystical collection of powerful utility functions for everyday coding wizardry. It provides a set of commonly used functions to simplify your Python spells and enchantments.

## Installation

You can install Incantations using pip:

```bash
pip install incantations
```

## Usage

Here are some examples of how to use the magical functions provided by Incantations:

### unique

Remove duplicate elements from an iterable while preserving order:

```python
from incantations import unique

original_list = [1, 2, 2, 3, 1, 4]
unique_list = unique(original_list)
print(unique_list)  # Output: [1, 2, 3, 4]
```

### chunkify

Yield successive chunks from an iterable of a specified size:

```python
from incantations import chunkify

numbers = range(10)
for chunk in chunkify(numbers, 3):
    print(chunk)

# Output:
# [0, 1, 2]
# [3, 4, 5]
# [6, 7, 8]
# [9]
```

## Contributing

Contributions to Incantations are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.

Happy coding, and may your spells be ever powerful! 🧙‍♂️✨
