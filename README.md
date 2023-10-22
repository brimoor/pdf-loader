# PDF Loader Plugin

A [FiftyOne plugin](https://docs.voxel51.com/plugins/index.html) for loading
PDFs as images.

https://github.com/brimoor/pdf-loader/assets/25985824/584bd14f-e076-4b88-89d5-f88190032f93

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

## What next?

Install the
[PyTesseract OCR](https://github.com/jacobmarks/pytesseract-ocr-plugin) and
[Semantic Document Search](https://github.com/jacobmarks/semantic-document-search-plugin)
plugins to make your documents searchable!

https://github.com/brimoor/pdf-loader/assets/25985824/e18fde7f-eced-41dc-849a-a0e074a20737

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
