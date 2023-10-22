"""
PDF Loader.

| Copyright 2017-2023, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import os

import numpy as np

import fiftyone as fo
import fiftyone.core.utils as fou
import fiftyone.operators as foo
import fiftyone.operators.types as types


class PDFLoader(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="pdf_loader",
            label="PDF loader",
            light_icon="/assets/icon-light.svg",
            dark_icon="/assets/icon-dark.svg",
            dynamic=True,
            execute_as_generator=True,
        )

    def resolve_input(self, ctx):
        inputs = types.Object()

        ready = _pdf_loader_inputs(ctx, inputs)
        if ready:
            _execution_mode(ctx, inputs)

        view = types.View(label="PDF loader")
        return types.Property(inputs, view=view)

    def resolve_delegation(self, ctx):
        return ctx.params.get("delegate", False)

    def execute(self, ctx):
        for update in _pdf_loader(ctx):
            yield update

        yield ctx.trigger("reload_dataset")


def _pdf_loader_inputs(ctx, inputs):
    file_explorer = types.FileExplorerView(button_label="Choose a file...")
    prop = inputs.file(
        "input_path",
        label="Input path",
        description=f"Choose a PDF to add to this dataset",
        required=True,
        view=file_explorer,
    )

    input_path = _parse_path(ctx, "input_path")
    if input_path is None:
        return False

    file_explorer = types.FileExplorerView(
        choose_dir=True,
        button_label="Choose a directory...",
    )
    inputs.file(
        "output_dir",
        label="Output directory",
        description="Choose a directory to write the per-page images",
        required=True,
        view=file_explorer,
    )

    output_dir = _parse_path(ctx, "output_dir")
    if output_dir is None:
        return False

    inputs.int(
        "dpi",
        default=200,
        required=True,
        label="Image quality",
        description="Image quality in dots per inch (DPI)",
    )

    fmt_choices = types.Dropdown()
    fmt_choices.add_choice("jpg", label="JPEG")
    fmt_choices.add_choice("png", label="PNG")

    inputs.enum(
        "fmt",
        fmt_choices.values(),
        default="jpg",
        required=True,
        label="Image format",
        description="The format to write the page images",
        view=fmt_choices,
    )

    inputs.list(
        "tags",
        types.String(),
        default=None,
        label="Tags",
        description="An optional list of tags to give each new sample",
    )

    return True


def _pdf_loader(ctx):
    input_path = _parse_path(ctx, "input_path")
    output_dir = _parse_path(ctx, "output_dir")
    dpi = ctx.params["dpi"]
    fmt = ctx.params["fmt"]
    tags = ctx.params.get("tags", None)

    from pdf2image import convert_from_path

    root = os.path.splitext(os.path.basename(input_path))[0]
    images = convert_from_path(input_path, dpi=dpi, fmt=fmt)

    num_images = len(images)
    ifmt = f"0{int(np.ceil(np.log10(num_images)))}d"

    os.makedirs(output_dir, exist_ok=True)

    batcher = fou.DynamicBatcher(images, target_latency=0.3, max_batch_beta=2)

    i = 0
    with batcher:
        for batch in batcher:
            samples = []
            for image in batch:
                i += 1
                filepath = os.path.join(
                    output_dir, f"{root}-page{i:{ifmt}}.{fmt}"
                )
                image.save(filepath)
                samples.append(fo.Sample(filepath=filepath, tags=tags))

            ctx.dataset._add_samples_batch(samples, True, False, True)

            p = i / num_images
            l = f"Loaded {i} of {num_images}"
            yield ctx.trigger("set_progress", dict(progress=p, label=l))


def _execution_mode(ctx, inputs):
    delegate = ctx.params.get("delegate", False)

    if delegate:
        description = "Uncheck this box to execute the operation immediately"
    else:
        description = "Check this box to delegate execution of this task"

    inputs.bool(
        "delegate",
        default=False,
        required=True,
        label="Delegate execution?",
        description=description,
        view=types.CheckboxView(),
    )

    if delegate:
        inputs.view(
            "notice",
            types.Notice(
                label=(
                    "You've chosen delegated execution. Note that you must "
                    "have a delegated operation service running in order for "
                    "this task to be processed. See "
                    "https://docs.voxel51.com/plugins/index.html#operators "
                    "for more information"
                )
            ),
        )


def _parse_path(ctx, key):
    value = ctx.params.get(key, None)
    return value.get("absolute_path", None) if value else None


def register(p):
    p.register(PDFLoader)
