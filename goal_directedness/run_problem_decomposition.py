import os
import argparse
from dotenv import load_dotenv
from datasets import load_dataset

from problem_decomposition import build_graph
from utils import set_env, extract_data_info

# Set environment variables
load_dotenv()
set_env("OPENAI_API_KEY")
set_env("LANGCHAIN_API_KEY")
set_env('LANGCHAIN_TRACING_V2')
set_env('LANGCHAIN_ENDPOINT')
os.environ["LANGCHAIN_PROJECT"] = "problem_decomposition" # LangSmith project name

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--ExperimentName', type = str, default = 'demo') # Name of the experiment, used for naming all saved files
parser.add_argument('--iteration', type = int, default = 1)
config = parser.parse_args()

# Load the dataset
dev_set = load_dataset("hotpot_qa", 'distractor', split = 'validation', trust_remote_code = True)
test_set = dev_set.shuffle(seed = 42) # Use as test set

if __name__ == "__main__":
    # Load Graph
    graph = build_graph('openai', config.ExperimentName)

    # Run
    iteration = config.iteration
    for data_i in range(iteration):
        print('-----------------------------------')
        print(f"Running iteration {data_i+1}/{iteration}")
        data = test_set[i]

        # Extract data info
        unique_id, question, context = extract_data_info(test_set[data_i])

        # Invoke the graphs
        thread = {"configurable": {"thread_id": unique_id}} # This is used to save the state in the database
        prompt = {
            'messages': question,
            'context': context
        }
        try:
            response = graph.invoke(prompt, thread) # This saves the state in the database
            print(f'Question: {question}')
            print(f'Answer: {response["answer"]}')
        except:
            print(f"Invalid input occured in the graph for {unique_id}")
            continue