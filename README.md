# cs8395-test-chat-gpt-in-finding-first-error

## Welcome to "Enhancing Predictive Analysis of Python Code Errors"!

### Elevating Python Code Quality with AI and Expert Tools

Embark on an insightful journey into the world of code quality with our ChatGPT Code Readability and Maintainability Tester. This innovative tool is your gateway to uncovering the depths of readability and maintainability in Python code, especially the kind generated by the advanced AI of OpenAI's GPT models.

A Fusion of AI and Linting Excellence

At the heart of our tool lies a powerful combination of AI-generated Python code and a suite of renowned linting tools. We employ the best in class – Flake8, Black, Radon, Pydocstyle, and Pylint – to delve into the intricacies of code quality. It's a symphony of technological prowess designed to offer you comprehensive insights into how ChatGPT's code stacks up in terms of readability, maintainability, and adherence to revered coding standards.

A Kaleidoscope of Coding Challenges

The adventure doesn't end there. Our tool features 6 unique prompts, each a call to ChatGPT to craft a Python program based on specific guidelines. These guidelines are not just any rules; they are inspired by one or more keywords from a curated list of 100, ensuring a diverse range of coding scenarios.

Adhering to the Gold Standards

Each piece of ChatGPT-generated Python code is an exploration in itself, conforming to one of the five different linting standards: Flake8, Black, Radon, Pydocstyle, and Pylint. We also introduce a default prompt, free from the specifics of any linting tool, adding another layer to this fascinating analysis.

120 Programs, Unbounded Insights

With 20 Python programs generated for each prompt type, we present you with a total of 120 ChatGPT-crafted Python programs. This extensive collection is more than just code; it's a treasure trove of insights waiting to be discovered.


### Exploring the Frontiers of AI and Python Development

This repository, part of the innovative research project "Enhancing Predictive Analysis of Python Code Errors: Integrating Semantic Similarity Assessment with ChatGPT," aims to push the boundaries of automated error detection in Python programming. Our objective is clear: to test the effectiveness of ChatGPT, a cutting-edge AI model, in identifying the first error in Python code.

### Harnessing the Power of AI-Generated Python Programs

Diving into the core of this project, we utilize an array of Python programs, each uniquely generated by ChatGPT and containing a deliberate error. These programs, sourced from this [repository](https://github.com/RajayPreddie/cs8395-problem-generation), represent a diverse set of challenges and are neatly stored in the coding_problems folder, each within its own JSON file.

### The Journey of Code Analysis with ChatGPT

The `main.py` script in this repository is where the magic happens. It executes these Python programs, capturing their outputs and errors. But it doesn't stop there – ChatGPT steps in as a command-line interface, presenting its own take on the output. This setup allows for a fascinating comparison: how does ChatGPT's output stack up against the actual terminal output?

### A Unique Blend of Technologies

Leveraging both ChatGPT's insights and the analytical power of difflib, we then embark on a mission to score the similarity between these outputs. It's a blend of human ingenuity and AI precision, aiming to provide a deeper understanding of ChatGPT's abilities.

**Prerequisites:**
- Python 3.9.6 (if this does not work, try a higher version)
- pip package manager

**Steps:**
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Set up the environment:
```
python3 -m venv venv
```
```
source venv/bin/activate  # Unix/MacOS
```
```
venv\Scripts\activate  # Windows
```
4. Install the required dependencies:
   ```
   pip3 install -r requirements.txt
   ```

## Usage
Run `main.py` to execute the ChatGPT-generated Python programs. The script will capture errors, compare outputs using ChatGPT and `difflib`, and store the results in JSON format.
Execute the tool with the following command:
```
python3 main.py --generate_responses
```

Use the following command if you do not want to regenerate ChatGPT responses:
```
python3 main.py
```
### Command-Line Arguments
The `main.py` script supports the following command-line arguments:

- `--generate_responses`: Use this flag to force the generation of ChatGPT responses. This is useful when you want to regenerate responses for the Python programs.
  
  Example:
  ```
  python main.py --generate_responses
  ```
- `-- model`: This is here for integrating with the [cs8395/test-suite](https://github.com/nkalupahana/cs8395-test-suite). The input model is not used. The repository utilizes gpt-4. I recommend to not use the model argument.


## Features
- **Error Detection**: Identifies first-error in Python programs using ChatGPT.
- **Output Comparison**: Compares the output of Python programs with ChatGPT-generated responses.
- **Semantic Similarity Assessment**: Utilizes `difflib` and ChatGPT to assess the similarity between program outputs.

## Output Explanation
Outputs are stored in:
- `gpt_responses`: JSON files each containing a ChatGPT response acting as a command-line interface.
- `json_problem_scores`: JSON files containing scores for each problem.
- `terminal_outputs`: Text files with terminal outputs when running the code.

## Acknowledgement
The inspiration for the methodology diffculty levels comes from one of the research 
presentations I viewed in CS8395.

The following repository of mine helped with the development of this code: 
1. [ChatGPT Python Code Execution Comparison](https://github.com/RajayPreddie/cs8395-chatgpt-python-code-execution-comparison)

## ChatGPT Chat Links:
1. [ChatLink](https://chat.openai.com/share/9c43608f-52d8-4415-8203-57a693547093)
2. [ChatLink](https://chat.openai.com/share/cbfa536a-aa16-4024-b7df-bf2bf43df448)
3. [ChatLink](https://chat.openai.com/share/8216251e-6534-4e45-b0e6-1b085bdc25e3)
4. [ChatLink](https://chat.openai.com/share/5a456d75-a3ac-403c-b974-f255f947e5dc)
5. I utilized many other ChatGPT chats for developing the code.

## License
[MIT License]
