"""Gradio web interface for the RSU Unofficial Dining Guide."""

import gradio as gr

from query import ask


def handle_query(question: str) -> tuple[str, str]:
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="RSU Unofficial Dining Guide") as demo:
    gr.Markdown(
        "# RSU Unofficial Dining Guide\n"
        "Ask questions about campus dining halls, wait times, meal plans, "
        "vegetarian options, late-night food, and more. Answers are grounded "
        "in student reviews and guides."
    )
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g., What are lunch wait times at North Dining Hall?",
        lines=2,
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
