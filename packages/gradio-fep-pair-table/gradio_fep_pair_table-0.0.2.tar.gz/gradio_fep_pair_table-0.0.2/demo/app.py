
import gradio as gr
from gradio_fep_pair_table import fep_pair_table

with gr.Blocks() as demo:
    with gr.Row():
        test = fep_pair_table(max_height=240, placeholder='{"pairs":[{"ligandA":"dp-1a","ligandB":"dp-1b","similarity":0.852,"link":true},{"ligandA":"dp-1b","ligandB":"dp-3a","similarity":0.843,"link":true},{"ligandA":"dp-1a","ligandB":"dp-3a","similarity":0.541,"link":true}]}')
    with gr.Row():
        update_button = gr.Button('Update')
    def update():
        return fep_pair_table(placeholder='{"pairs":[{"ligandA":"dp-1a","ligandB":"dp-1b","similarity":0.852,"link":false},{"ligandA":"dp-1b","ligandB":"dp-3a","similarity":0.843,"link":true},{"ligandA":"dp-1a","ligandB":"dp-3a","similarity":0.541,"link":true}]}')
    update_button.click(update, outputs=test)
    def a(b):
        print(b)
    test.change(a, inputs=test)
if __name__ == "__main__":
    demo.launch()
