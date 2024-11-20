# prompt.py
class PromptTemplate:
    problem_analysis = "You are an expert problem analyzer and decomposer with access to relevant context.\n" \
        "Your task is to verify, refine, and break down the given problem by following these steps:\n" \
        "0. Think step by step through the entire analysis process\n" \
        "1. Verify the problem:\n" \
        "   - Identify the core objective and constraints\n" \
        "   - Check if the problem is well-defined with clear success criteria\n" \
        "   - Highlight key assumptions and prerequisites\n" \
        "   - Reformulate if needed to make more precise and actionable\n" \
        "2. Decompose the refined problem:\n" \
        "   - Identify the main components that need to be solved\n" \
        "   - Arrange sub-problems in a vertical sequence with dependencies\n" \
        "   - Further decompose sub-problems that require multiple steps\n" \
        "   - Specifying dependencies between sub-problems\n" \
        "   - Keep decomposition compact for single-step problems\n" \
        "3. Consider the provided context:\n" \
        "   - Review any relevant documentation provided\n" \
        "   - Reference specific components or patterns that could be reused\n\n" \
        "Given problem: {Problem}\n" \
        "Context: {Context}\n\n" \
        "First provide your analysis and refined problem statement, then give a hierarchical breakdown showing the vertical dependencies between sub-problems."

    subproblem_solution = "You are an expert problem solver focused on solving specific sub-problems with access to relevant context.\n" \
        "Your task is to solve the given sub-problems by:\n" \
        "0. Think step by step through the entire analysis process\n" \
        "1. Understanding the specific scope and requirements of these sub-problems\n" \
        "2. Reviewing provided context\n" \
        "3. Applying relevant domain knowledge and techniques\n" \
        "4. Providing a clear and detailed solutions\n" \
        "5. Explaining your reasoning processes\n" \
        "6. Ensuring the solutions align with any dependencies or constraints\n" \
        "7. Referencing specific patterns or components from context where applicable\n\n" \
        "Sub-problems: {SubProblem}\n" \
        "Dependencies: {Dependencies}\n" \
        "Contexts (Documents with Index Numbers): {Context}\n\n" \
        "Provide your detailed solutions for each sub-problems and lists all referred documents as those number."

    solution_aggregation = "You are an expert in synthesizing solutions with access to relevant context.\n" \
        "Your task is to aggregate the solutions from all sub-problems by:\n" \
        "1. Reviewing all sub-problem solutions to extract key insights\n" \
        "2. Ensuring consistency and resolving any conflicts across solutions\n" \
        "3. Combining the solutions in a coherent way and concise way\n" \
        "4. Verifying the combined solution effectively addresses the refined problem\n" \
        "5. Refering to relevant context only if necessary for clarity\n\n" \
        "Refined Problem: {RefinedProblem}\n" \
        "Sub-problem Solutions: {SubProblemSolutions}\n" \
        "Sub-problem Solutions Reasoning: {SubProblemSolutionsReasoning}\n" \
        "Dependencies: {Dependencies}\n" \
        "Expected Supporting Documents Numbers: {SupportingDocuments}\n" \
        "Context: {Context}\n\n" \
        "Provide your solution for the refined problem in the following format:\n" \
        "1. Final Solution (Compact): Provide a direct and concise answer to the refined problem within few or several words.\n" \
        "2. Comprehensive Reasoning: Explain step-by-step how the sub-problem solutions were synthesized, highlighting key insights, resolving conflicts, and how the final solution aligns with the refined problem.\n"     

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
    