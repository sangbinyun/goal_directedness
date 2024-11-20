from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel

from prompt import PromptTemplate
from utils import load_llm, connect_to_sql_memory

# State
class State(MessagesState):
    context: list[str]
    problem: str
    sub_problems: list
    dependencies: list
    sub_problem_solutions: list
    sub_problem_reasoning: list
    supporting_documents: list
    final_reasoning: str
    def __init__(self, given_context):
        # super().__init__(given_context)
        self.context = given_context

class Refined(BaseModel):
    problem: str
    sub_problems: list[str]
    dependencies: list[str]

class Solved(BaseModel):
    sub_problem_solutions: list[str]
    sub_problem_reasoning: list[str]
    supporting_documents: list[int]

class Aggregated(BaseModel):
    answer: str
    final_reasoning: str

# Graph call
def build_graph(model_name: str, ExperimentName: str):
    # LLM
    llm = load_llm(model_name)

    # graph functions
    def problem_analyzer(state: State):
        # Refinement prompt
        _orig_problem = state['messages'][-1].content
        _prompt = [
            SystemMessage(
                PromptTemplate.problem_analysis.format(
                    Problem = _orig_problem,
                    Context = state['context']
                )
            )
        ]

        # Invoke the LLM
        structured_llm = llm.with_structured_output(Refined)
        _response = structured_llm.invoke(_prompt)

        return {
            'problem': _response.problem, 
            'sub_problems': _response.sub_problems,
            'dependencies': _response.dependencies
        }

    def subproblem_solver(state: State):
        # sub-problem solver
        _prompt = [
            SystemMessage(
                PromptTemplate.subproblem_solution.format(
                    SubProblem = state['sub_problems'],
                    Dependencies = state['dependencies'],
                    Context = state['context']
                )
            )
        ]

        # Invoke the LLM
        structured_llm = llm.with_structured_output(Solved)
        _response = structured_llm.invoke(_prompt)
        
        return {
            'sub_problem_solutions': _response.sub_problem_solutions,
            'sub_problem_reasoning': _response.sub_problem_reasoning,
            'supporting_documents': _response.supporting_documents
        }

    def solution_aggregator(state: State):
        # solution aggregator
        _prompt = [
            SystemMessage(
                PromptTemplate.solution_aggregation.format(
                    RefinedProblem = state['problem'],  
                    SubProblemSolutions = state['sub_problem_solutions'],
                    SubProblemSolutionsReasoning = state['sub_problem_reasoning'],
                    Dependencies = state['dependencies'],
                    SupportingDocuments = state['supporting_documents'],
                    Context = state['context']
                )
            )
        ]

        # Invoke the LLM
        structured_llm = llm.with_structured_output(Aggregated)
        _response = structured_llm.invoke(_prompt)
        
        return {
            'messages': AIMessage(_response.answer), 
            'final_reasoning': _response.final_reasoning
        }

    # Graph
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("analyzer", problem_analyzer)
    graph.add_node("solver", subproblem_solver)
    graph.add_node("aggregator", solution_aggregator)

    # Add edges
    graph.add_edge(START, "analyzer")
    graph.add_edge("analyzer", "solver")
    graph.add_edge("solver", "aggregator")
    graph.add_edge("aggregator", END)

    # Compile the graph
    memory = connect_to_sql_memory(ExperimentName)
    graph = graph.compile(checkpointer = memory)

    return graph

# from IPython.display import Image, display
# display(Image(graph.get_graph().draw_mermaid_png()))