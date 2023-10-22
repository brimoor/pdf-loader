# PDF Loader Plugin

A [FiftyOne plugin](https://docs.voxel51.com/plugins/index.html) for loading
PDFs as images.

## Installation

```shell
fiftyone plugins download https://github.com/brimoor/pdf-loader

brew install poppler
pip install pdf2image
```

## Usage

1. Launch the App

```py
import fiftyone as fo

dataset = fo.Dataset()
session = fo.launch_app(dataset)
```

2.  Press `` ` `` or click the `Browse operations` icon above the grid

3.  Run the `pdf_loader` operator

## Implementation

This plugin is a basically a wrapper around the following code:

```py
import os
from pdf2image import convert_from_path

INPUT_PATH = "/path/to/your.pdf"
OUTPUT_DIR = "/path/for/page/images"

os.makedirs(OUTPUT_DIR, exist_ok=True)
convert_from_path(INPUT_PATH, output_folder=OUTPUT_DIR, fmt="jpg")

dataset.add_images_dir(OUTPUT_DIR)
```
