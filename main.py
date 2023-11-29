from collections import defaultdict
from openai import OpenAI
import json
import os
import subprocess
import difflib
import argparse


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# Extract JSON from a directory
def extract_json_from_directory(abs_directory_path):
  
  # Create a list to store the JSON objects
  json_objects= {}
  # Iterate through each file in the directory
  for filename in os.listdir(abs_directory_path):
    # Get the absolute path of the file
    file_path = os.path.join(abs_directory_path, filename)
    # Check if it's a file
    if os.path.isfile(file_path):
      # Open the file and extract the JSON object
      with open(file_path, 'r') as file:
        # Read the file
        data = file.read()
        # Convert the JSON object to a Python dictionary
        json_object = json.loads(data)
        json_objects[json_object["id"]] = json_object
        # Close the file
        file.close()
        
  return json_objects



#2: Then, prompt ChatGPT to act as python executor and generate the possible errors or the correct output
def prompt_chat_gpt(problem_descriptions):
  # Create a list to store the JSON objects
  gpt_responses = {}
  # Create a directory to store the JSON objects
  abs_directory_path = os.path.join(os.getcwd(), 'gpt_responses')
  # If the path already exists, then there is no need to reprompt ChatGPT
  if not os.path.exists(abs_directory_path):
    os.makedirs(abs_directory_path)
  # Iterate through each problem description
  for problem_id, problem_description in problem_descriptions.items():
    # Generate the prompt for ChatGPT
    chatgpt_prompt = f"The code is:\n{problem_description['code']}"
    
    # Make an API request to ChatGPT
    
        # Make an API request to ChatGPT
    response = client.chat.completions.create(   model="gpt-4",  # or whatever the latest model is
       messages=[
        {"role": "system", "content": "Act as the Command-Line Interface. You do not need to excute code. Infer how the Command-Line Interface would behave. Display nothing else except the Command-Line Interface output (do not include ChatGPT thinking or planning text). Here are the specifications for acting as the Command-Line Interface: read python3 code in a text format, display raw output of the python code execution, capture both stdout and stderr in output, run incomplete or erroneous code as given, do not change or fix the given code, for the Open AI API request just return the raw output as the response, do not show any additional text from ChatGPT."},
        {"role": "user", "content": chatgpt_prompt}
    ],

      max_tokens=60,
      n=1,
      stop=None,
      temperature=0.5
    )  
    # Save the response to a file
    filename = f"{problem_id}.json"
    # Create a directory to store the JSON objects
    full_path = os.path.join(abs_directory_path, filename)
    # Create a JSON object to store the prompt solution
    prompt_solution =  {"id": problem_id, 
        "description": problem_description['description'], 
        "output": response.choices[0].message.content,
        "tags": problem_description['tags'],
                              }
    # Append the prompt solution to the list
    gpt_responses[problem_id] = prompt_solution
    # Write the prompt solution to a file
    with open(full_path, 'w') as file:
      # Convert the JSON object to a string
      json_object = json.dumps(
     prompt_solution, indent=4)
      # Write the string to the file
      file.write(json_object)
      # Close the file
      file.close()  
  return gpt_responses

def get_chat_gpt_score(actual_command_line_output, chatgpt_output):
    prompt = f"Calculate the similarity score between these two strings, returning a decimal value between 0 and 1, where 1 means the strings are identical:\n\nString 1: \"{actual_command_line_output}\"\n\nString 2: \"{chatgpt_output}\""

    # Make an API request to ChatGPT
    response = client.chat.completions.create(
        model="gpt-4",  # Use the latest available model
        messages=[
            {"role": "system", "content": "Analyze the semantic content and overall meaning of these two strings and provide an estimated similarity score. Return just the score value which should be a decimal value between 0 and 1, where 1 indicates that the strings have very similar or identical meanings, and 0 indicates no similarity in meaning. Please base your analysis solely on the semantic content and general themes of the strings, without focusing on their syntactical structure. If you're unable to assess the similarity due to language or format limitations, return a 0."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5
    )
  
    # Parse the response
    # Assuming the response is a dictionary and the answer is in the format we expect
    try:
        score_str = response.choices[0].message.content
        score = float(score_str)
        return score
    except (KeyError, ValueError, TypeError):
        # Handle any parsing errors or unexpected response formats
        print("Error in parsing the response or invalid response format.")
        return None
  
#4: Then, execute each of the python files and save the output to a file
def execute_python_code_from_directory(problem_descriptions, gpt_responses):
  comparison_scores = {"difflib_scores": defaultdict(int), "chatgpt_scores": defaultdict(int)}

  for problem_id, problem_description in problem_descriptions.items():

    # TODO: remove problems with while loops / recursion and inputs
    result = subprocess.run(['python3',"-c", problem_description["code"]], 
                            # input="Hello World",
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                       
                  text=True)
    actual_command_line_output = result.stdout if result.stdout else result.stderr
    chatgpt_output = gpt_responses[problem_id]["output"]
    # Prepend the setrecursionlimit call to the existing code
  
    # Use SequenceMatcher to compare the two lists of lines
    # TODO: run the ChatGPT prompt comparison functoin here to get a comparison score.
    comparison = difflib.SequenceMatcher(None, actual_command_line_output, chatgpt_output)
    ratio = comparison.ratio()  
    chat_gpt_score = get_chat_gpt_score(actual_command_line_output, chatgpt_output)
    comparison_scores["difflib_scores"][problem_description["id"]] = ratio * 100
    if chat_gpt_score != None:
      comparison_scores["chatgpt_scores"][problem_description["id"]] = chat_gpt_score * 100
    else:
      comparison_scores["chatgpt_scores"][problem_description["id"]] = 0
    
    # Prompt Chat GPT to generate the Python Interpreter output
    abs_directory_path = os.path.join(os.getcwd(), 'terminal_outputs')
    filename = f"{problem_description['id']}.txt"
    if not os.path.exists(abs_directory_path):
      os.makedirs(abs_directory_path) 
    full_path = os.path.join(abs_directory_path, filename)
    
    with open(full_path, 'w') as file:
        file.write(actual_command_line_output)
        file.close()
  return comparison_scores
 
# Check if the correct number of arguments are passed (excluding the script name itself)

# Set up argument parsing
parser = argparse.ArgumentParser(description='Get ChatGPT responses and write to files.')
parser.add_argument('--regenerate', action='store_true',
                    help='Force regeneration of ChatGPT responses')
# TODO: if regenerate is on then regenerate everything 
# Check if gpt responses exist
# TODO: if no regenerate then check if the directory exists and if it does then don't regenerate
# Check if json_problem_scores exists
args = parser.parse_args()

#
# Extract the python files from the directory
problem_path = os.path.join(os.getcwd(), 'coding_problems')
problem_descriptions = extract_json_from_directory(problem_path)


### Prompt Generation Occurs Here ###
response_folder = 'gpt_responses'

# Check if the folder exists
folder_exists = os.path.exists(response_folder)
# Prompt Chat GPT to generate the Python Interpreter output
abs_directory_path = os.path.join(os.getcwd(), response_folder)
# If the path already exists, then there is no need to reprompt ChatGPT
gpt_responses = {}
if not os.path.exists(abs_directory_path) or args.regenerate:
    if not os.path.exists(abs_directory_path):
      os.makedirs(abs_directory_path)
    gpt_responses = prompt_chat_gpt(problem_descriptions)
else:
    # Extract the prompt solutions from the directory
    gpt_responses = extract_json_from_directory(abs_directory_path)



# Write the comparison_scores to JSON
directory = 'json_problem_scores'  # Replace with your desired path
 # Get the absolute path of the directory relative to the current working directory
json_probs_directory_path = os.path.join(os.getcwd(), directory)
comparison_scores = execute_python_code_from_directory(problem_descriptions, gpt_responses)


if not os.path.exists(json_probs_directory_path):
  os.makedirs(json_probs_directory_path)
output_json = {"name": "Python Execution Output Comparison: Total Score", "tags": [], "output": 0, "difflib_overall_score": 0, "chatgpt_overall_score": 0,"difflib_scores": defaultdict(int), "chatgpt_scores": defaultdict(int), }

tag_num_problems = defaultdict(int)
for id, score in comparison_scores["difflib_scores"].items():
    filename = f"{id}.json"
    # Write the code to the file
  
    cur_problem_output_json = {
      
      "problem_id": id, "difflib_score": score, "chatgpt_score": comparison_scores["chatgpt_scores"][id]}
    for tag in gpt_responses[id]["tags"]:
        output_json["difflib_scores"][tag] += score
        output_json["chatgpt_scores"][tag] += comparison_scores["chatgpt_scores"][id]
        tag_num_problems[tag] += 1
    
    
    output_json["difflib_overall_score"] += score / len(problem_descriptions)
    output_json["chatgpt_overall_score"] += comparison_scores["chatgpt_scores"][id] / len(problem_descriptions)
    full_path = os.path.join(json_probs_directory_path, filename)
    with open(full_path, 'w') as file:
        
        file.write(json.dumps(cur_problem_output_json, indent=4))
        file.write("\n")
        file.close()  # Close the file
        
        
        
print("TAG SCORES:")
print("-----------")
for tag, score in output_json["difflib_scores"].items():
    average_score = (score / tag_num_problems[tag]) 
    output_json["difflib_scores"][tag] = average_score
    if tag in ["Easy", "Medium", "Hard"]:
      print(f"{tag}: {average_score: .2f}%")
for tag, score in output_json["chatgpt_scores"].items():
    average_score = (score / tag_num_problems[tag]) 
    output_json["chatgpt_scores"][tag] = average_score
    if tag in ["Easy", "Medium", "Hard"]:
      print(f"{tag}: {average_score: .2f}%")

output_json["output"] = (output_json["difflib_overall_score"] + output_json["chatgpt_overall_score"]) / 2
average_total_score = output_json["output"]
print("-----------")
print(f"TOTAL SCORE, {average_total_score: .2f}%")


total_score_path = os.path.join(os.getcwd(), "")
filename = "output.json"
full_path = os.path.join(total_score_path, filename)
with open(full_path, 'w') as file:
    file.write(json.dumps(output_json, indent=4))
    file.write("\n")
    file.close()  # Close the file

