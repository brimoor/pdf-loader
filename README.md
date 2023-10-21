# PDF Loader Plugin

A [FiftyOne plugin](https://github.com/voxel51/fiftyone-plugins) for loading
PDFs as images.

## Installation

```shell
fiftyone plugins download https://github.com/brimoor/pdf-loader

brew install poppler
pip install pdf2image
```

## Usage

1. Launch the App:

```py
import fiftyone as fo

dataset = fo.Dataset()
session = fo.launch_app(dataset)
```

2.  Press `` ` `` or click the `Browse operations` action to open the Operators
    list

3.  Run the `pdf_loader` operator

## Implementation

This plugin is a wrapper around the following code:

```py
import os
from pdf2image import convert_from_path

import fiftyone as fo

INPUT_PATH = "/path/to/your.pdf"
OUTPUT_DIR = "/path/for/images"

os.makedirs(OUTPUT_DIR, exist_ok=True)
convert_from_path(INPUT_PATH, output_folder=OUTPUT_DIR, fmt="jpeg")

dataset = fo.Dataset.from_images_dir(OUTPUT_DIR)
```
