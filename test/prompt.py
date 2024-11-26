# prompt.py
class PromptTemplate:
    problem_analysis = (
        "You are an expert problem analyzer with context access.\n " \
        "Verify, refine, and decompose the given problem step-by-step:\n" \
        "1. Verify: Identify objectives, constraints, and success criteria. " \
        "Reformulate if unclear or imprecise.\n" \
        "2. Decompose: Break the refined problem into components, sequence sub-problems, and define dependencies. " \
        "Keep decomposition concise for single-step problems and incorporate context if necessary.\n\n" \
        "Problem: {Problem}\n" \
        "Context: {Context}\n\n" \
        "Provide your refined problem and a hierarchical breakdown of sub-problems with dependencies."
    )

    subproblem_solution = (
        "You are an expert sub-problem solver with context access. " \
        "Solve the sub-problems step-by-step:\n" \
        "1. Understand scope, requirements, and context.\n" \
        "2. Apply domain knowledge and techniques.\n" \
        "3. Provide clear, detailed solutions aligned with dependencies.\n" \
        "4. Refer to specific patterns or components from context.\n\n" \
        "Sub-problems: {SubProblem}\n" \
        "Dependencies: {Dependencies}\n" \
        "Context (Document Index Numbers): {Context}\n\n" \
        "Provide solutions for each sub-problem with referenced documents as numbers."        
    )

    solution_aggregation = (
        "You are an expert in synthesizing subproblem solutions using context. "
        "Aggregate sub-problem solutions:\n"
        "1. Extract key insights.\n"
        "2. Resolve conflicts.\n"
        "3. Combine solutions concisely.\n"
        "4. Verify alignment with the refined problem.\n\n"
        "Refined Problem: {RefinedProblem}\n"
        "Sub-problems: {SubProblems}\n"
        "Sub-problem Solutions: {SubProblemSolutions}\n"
        "Dependencies: {Dependencies}\n"
        "Supporting Documents: {SupportingDocuments}\n"
        "Context: {Context}\n\n"
        "Provide a concise final answer and step-by-step reasoning aligned with the refined problem."
    )   
 

    hotpot_evaluation = """
        Your job is to determine if the provided answer is fully correct based on the given question and the correct answer. 
        Focus only on the factual correctness and completeness of the answer. Respond with YES or NO. \n
        Question: {question} \n
        Correct Answer: {correct_answer} \n
        Answer you should evaluate: {predicted_answer} \n\n
        If you are unsure, provide a brief explanation of why and suggest YES or NO.
        """

    direct_solution = "You are an expert problem solver with access to relevant context.\n" \
        "Review the context documents and provide your solution in this format:\n" \
        "1. Direct Answer: Give a clear, concise answer in few words\n" \
        "2. Reasoning: Explain your thought process and how you arrived at the answer\n" \
        "3. Supporting Documents: List the document as those numbers you referenced\n\n" \
        "Question: {Problem}\n" \
        "Contexts (Documents with Index Numbers): {Context}\n"
    