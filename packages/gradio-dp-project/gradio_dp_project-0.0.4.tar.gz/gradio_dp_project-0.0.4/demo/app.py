
import gradio as gr
from gradio_dp_project import dp_project


example = dp_project().example_value()

demo = gr.Interface(
    lambda x:x,
    dp_project(),  # interactive version of your component
    dp_project(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
