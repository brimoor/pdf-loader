# PDF Loader Plugin

A [FiftyOne plugin](https://docs.voxel51.com/plugins/index.html) for loading
PDFs as images.

https://github.com/brimoor/pdf-loader/assets/25985824/584bd14f-e076-4b88-89d5-f88190032f93

## Installation

If you haven't already,
[install FiftyOne](https://docs.voxel51.com/getting_started/install.html):

```shell
pip install fiftyone
```

Then install the plugin and its dependencies:

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

2.  Press `` ` `` or click the `Browse operations` icon above the grid

3.  Run the `pdf_loader` operator

## What next?

Install the
[PyTesseract OCR](https://github.com/jacobmarks/pytesseract-ocr-plugin) and
[Semantic Document Search](https://github.com/jacobmarks/semantic-document-search-plugin)
plugins to make your documents searchable!

https://github.com/brimoor/pdf-loader/assets/25985824/e18fde7f-eced-41dc-849a-a0e074a20737

1. Install the plugins and their dependencies:

```shell
fiftyone plugins download https://github.com/jacobmarks/pytesseract-ocr-plugin
pip install pytesseract

https://github.com/jacobmarks/semantic-document-search-plugin
pip install qdrant_client
pip install sentence_transformers
```

2.  Launch a Qdrant server:

```
docker run -p "6333:6333" -p "6334:6334" -d qdrant/qdrant
```

3.  Run the `run_ocr_engine` operator to detect text blocks

4.  Run the `create_semantic_document_index` operator to generate a semantic
    index for the text blocks

5.  Run the `semantically_search_documents` operator to perform arbitrary
    searches against the index!

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
