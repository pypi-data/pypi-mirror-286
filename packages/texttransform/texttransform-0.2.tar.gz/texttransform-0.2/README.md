# texttransform

`texttransform` is a simple Python tool designed to:
- Convert sentences to uppercase or lowercase.
- Properly format sentences by capitalizing the first letter of each sentence and handling ellipses correctly.

## Features
- **Convert**: Change text to uppercase or lowercase.
- **Format**: Properly capitalize sentences and handle ellipses.

## Installation
You can install `texttransform` using pip from the local source. Navigate to the directory containing `setup.py` and run:

```bash
pip install .
```

## Usage
After installation, you can use the texttransform command-line tool to perform various text transformations.

### Convert to Uppercase
```bash
texttransform -upper "your text here"
```

### Convert to Lowercase
```bash
texttransform -lower "YOUR TEXT HERE"
```

### Format Sentences
```bash
texttransform -sentence "your text here. another sentence here."
```

### Example
```bash
texttransform -sentence "hello. world. this is an example..."
```

#### Output:
```bash
Hello. World. This is an example...
```

## Running Tests
To run the tests for texttransform, use:

```bash
python -m unittest text_transform_test.py
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Genevieve - [GitHub Profile](https://github.com/Genevieveok/)

