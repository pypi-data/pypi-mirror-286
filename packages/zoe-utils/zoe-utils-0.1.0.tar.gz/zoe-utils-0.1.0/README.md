## Overview

This library provides a utility class `ShellTask` to execute shell commands in a subprocess. It captures the output and errors, logs the output line by line, and raises an exception if the command fails.

## Installation

To use this utility, you need to have Python installed on your system. And install it via Pip.

## Usage

### ShellTask Class

The [`ShellTask`](utilities/shell_utils.py) class is designed to run shell commands and handle their output and errors.

#### Initialization

To create an instance of [`ShellTask`](utilities/shell_utils.py), you need to pass the shell command as a string to the constructor and execute method 'run()'

```python
from shell_utils import ShellTask

command = "ls -la"
task = ShellTask(command).run()
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## Contact

For any questions or suggestions, please open an issue on the GitHub repository.
