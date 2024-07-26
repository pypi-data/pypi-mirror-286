from typing import Callable

import gradio as gr

from samgis_core.utilities.type_hints import ListStr, DictStrInt


def get_example_complete(example_text, example_body):
    import json
    example_dict = dict(**example_body)
    example_dict["string_prompt"] = example_text
    return json.dumps(example_dict)


def get_gradio_interface_geojson(
        fn_inference: Callable, markdown_text: str, examples_text_list_text: ListStr, example_body: DictStrInt):
    with gr.Blocks() as gradio_app:
        gr.Markdown(markdown_text)

        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(lines=1, placeholder=None, label="Payload input")
                btn = gr.Button(value="Submit")
            with gr.Column():
                text_output = gr.Textbox(lines=1, placeholder=None, label="Geojson Output")

        gr.Examples(
            examples=[
                get_example_complete(example, example_body) for example in examples_text_list_text
            ],
            inputs=[text_input],
        )
        btn.click(
            fn_inference,
            inputs=[text_input],
            outputs=[text_output]
        )
    return gradio_app
