from typing import override

from docling.datamodel import vlm_model_specs
from docling.datamodel.accelerator_options import AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import VlmPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline
from langfuse import observe

from tabletopmagnat.node.abstract_node import AbstractNode


class DoclingNode(AbstractNode):
    def __init__(self, name: str, max_retries=1, wait: int | float = 10):
        super().__init__(name, max_retries, wait)
        pipeline_options = VlmPipelineOptions(
            vlm_options=vlm_model_specs.GRANITE_VISION_VLLM,
            accelerator_options=AcceleratorOptions(
                device="AUTO",
                num_threads=10,

            )
        )
        self._converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_cls=VlmPipeline,
                    pipeline_options=pipeline_options,
                ),
            }
        )

    @override
    @observe
    async def prep_async(self, shared):
        name = f"{self._name}:prep"
        self._lf_client.update_current_span(name=name)

        dialog = shared["dialog"]
        last_msg = dialog.get_last_message()
        url = last_msg.content
        return url

    @override
    @observe
    async def exec_async(self, prep_res):
        name = f"{self._name}:exec"
        self._lf_client.update_current_span(name=name)

        converted = self._converter.convert(prep_res)
        doc = converted.document
        data = {
            "document": doc,
            "title": doc.name.title(),
            "md": doc.export_to_markdown(),
        }
        return data

    @override
    @observe
    async def post_async(self, shared, prep_res, exec_res):
        name = f"{self._name}:post"
        self._lf_client.update_current_span(name=name)

        shared["document"] = exec_res
        return "default"
