
import gradio as gr
from gradio_dp_machine import dp_machine


example = dp_machine().example_value()

demo = gr.Interface(
    lambda x:x,
    dp_machine(),  # interactive version of your component
    dp_machine(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
