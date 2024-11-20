import argparse
from datasets import load_dataset

from problem_decomposition import build_graph
from utils import set_env

# Set environment variables
set_env("OPENAI_API_KEY")
set_env("LANGCHAIN_API_KEY")
set_env('LANGCHAIN_TRACING_V2')
set_env('LANGCHAIN_ENDPOINT')
os.environ["LANGCHAIN_PROJECT"] = "problem_decomposition"


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--model', type = str, default = 'openai')
parser.add_argument('--ExperimentName', type = str, default = 'test') # Name of the experiment, used for naming all saved files
parser.add_argument('--iteration', type = int, default = 100)

config = parser.parse_args(args=['--model', 'openai'])


def extract_dataset_info(data):
    # Extract data info
    unique_id = data['id']
    question = data['question']
    context = [
        "{}. {}: {}".format(doc_id+1, title, " ".join(sentences)) 
        for doc_id, (title, sentences)
        in enumerate(
            zip(
                data['context']['title'], 
                data['context']['sentences']
            )
        )
    ]

    return unique_id, question, context

def save_state(graph, test_set, ExperimentName: str, iteration: int):
    # instantiate states
    states = {
        'id': [],
        'question': [],
        'answer': [],
        'gt_answer': [],
        'supporting_documents': [],
        'supporting_facts': [],
        'problem': [],
        'sub_problems': [],
        'dependencies': [],
        'sub_problem_solutions': [],
        'sub_problem_reasoning': [],
        'final_reasoning': [],
        'context': []
    }

    # Get responses
    for i in range(iteration):
        # Extract data info
        unique_id = test_set[i]['id']
        question = test_set[i]['question']
        gt_answer = test_set[i]['answer']
        supp_facts = test_set[i]['supporting_facts']['title']
        supp_facts_idx = sorted(list(set(
            [
                test_set[i]['context']['title'].index(supp_fact_i) + 1
                for supp_fact_i in supp_facts
            ]
        )))
        
        # load response 
        thread = {"configurable": {"thread_id": unique_id}}
        curr_state = graph.get_state(thread).values
        curr_state['supporting_documents'] = sorted(list(set(curr_state['supporting_documents']))) # convert to set

        # Save state
        for j in states.keys():
            if j in curr_state.keys():
                states[j].append(curr_state[j])
        states['question'].append(curr_state['messages'][0].content)
        states['answer'].append(curr_state['messages'][1].content)
        states['gt_answer'].append(gt_answer)
        states['supporting_facts'].append(supp_facts_idx)
        states['id'].append(unique_id)

    # Save states
    print(f"Saved states successfully for {ExperimentName}..")
    json.dump(states, open(f'states/states_{ExperimentName}.json', 'w'), indent = 4)

if __name__ == "__main__":
    # Load Graph
    graph = build_graph(config.model, ExperimentName)

    # Prep data
    dev_set = load_dataset("hotpot_qa", 'distractor', split = 'validation', trust_remote_code = True)
    test_set = dev_set.shuffle(seed = 42) # Use as test set

    # Run
    iteration = config.iteration
    for data_i in range(iteration):
        unique_id, question, context = extract_dataset_info(test_set[data_i])

        # Invoke the graphs
        thread = {"configurable": {"thread_id": unique_id}}
        prompt = {
            'messages': question,
            'context': context
        }
        try:
            response = graph.invoke(prompt, thread) # This saves the state in the database
        except:
            print(f"Invalid input occured in the graph for {unique_id}")
            continue
    
    # Save states
    save_state(graph, test_set, ExperimentName, iteration)

    