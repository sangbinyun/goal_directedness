from pydantic import BaseModel
from langchain_core.messages import SystemMessage
from prompt import PromptTemplate
from utils import load_llm

class SingleRes(BaseModel):
    answer: str
    reasoning: str
    supporting_documents: list[int]

def naive_decomposition(model_name):
    # Load LLM
    llm = load_llm(model_name)
    structured_llm = llm.with_structured_output(SingleRes)

    return structured_llm

def load_naive_prompt(question, context):
    # Prompt
    single_prompt = [
        SystemMessage(
            PromptTemplate.direct_solution.format(
                Problem = question,
                Context = context
            )
        )
    ]
    
    return single_prompt