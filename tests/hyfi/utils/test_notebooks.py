from hyfi.main import HyFI
import ipywidgets as widgets


def test_notebooks():
    options = ["English", "Spanish", "French"]
    from_lang = HyFI.create_dropdown(options, "English", "From Language")
    to_lang = HyFI.create_dropdown(options, "Spanish", "To Language")
    input_prompt = HyFI.create_textarea(
        "I am a student",
        "Input",
        "Enter the sentence to translate",
        style={"description_width": "50px"},
        layout={"width": "95%", "height": "100px"},
    )
    generated_txt = HyFI.create_textarea(
        "",
        "Output",
        "Translated sentence",
        style={"description_width": "50px"},
        layout={"width": "95%", "height": "100px"},
    )
    translate_button = HyFI.create_button("Translate", layout={"width": "95%"})

    grid = widgets.GridspecLayout(4, 2, height="300px")
    grid[0, 0] = from_lang
    grid[0, 1] = to_lang
    grid[1, :] = input_prompt
    grid[2, :] = generated_txt
    grid[3, :] = translate_button

    instruction = (
        "Instruction: Given an input question, respond with syntactically correct PostgreSQL. Only use table called 'employees'.\n"
        + "Input: Select names of all the employees who are working under 'Peter'.\nPostgreSQL query: "
    )
    input_prompt = HyFI.create_textarea(
        instruction,
        "Input",
        "Enter the instruction to generate",
        style={"description_width": "50px"},
        layout={"width": "95%", "height": "100px"},
    )

    generated_txt = HyFI.create_textarea(
        "",
        "Output",
        "Generated SQL",
        style={"description_width": "50px"},
        layout={"width": "95%", "height": "150px"},
    )
    generate_button = HyFI.create_button("Generate SQL", layout={"width": "95%"})
    assert isinstance(generate_button, widgets.Button)


if __name__ == "__main__":
    test_notebooks()
