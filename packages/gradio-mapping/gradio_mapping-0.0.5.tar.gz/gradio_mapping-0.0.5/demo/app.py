
import gradio as gr
from gradio_mapping import Mapping

# example = MyComponent().example_value()
# demo = gr.Interface(
#     lambda value:value,
#     MyComponent(value=value),  # interactive version of your component
#     MyComponent(),  # static version of your component
#     # examples=[[example]],  # uncomment this line to view the \"example version\" of your component
# )
with gr.Blocks() as demo:
    with gr.Row():
        showbox_button = gr.Button("Remapping")
    with gr.Row():
        a = Mapping(placeholder="{\"ligandA\":\"\", \"ligandB\":\"\", \"mapping\":\"\"}", height=720, visible=True)
    def my_print_function():
        return Mapping(placeholder="{\"ligandA\":\"\", \"ligandB\":\"\", \"mapping\":\"\"}", visible=True)
    showbox_button.click(
        my_print_function,
        outputs=a
    )
if __name__ == "__main__":
    demo.launch()
