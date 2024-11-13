# prompt.py
class PromptTemplate:
    # verification = "You are an expert problem analyzer.\n" \
    #     "Your task is to verify and refine the given problem statement by:\n" \
    #     "1. Identifying the core objective and constraints\n" \
    #     "2. Checking if the problem is well-defined and has clear success criteria\n" \
    #     "3. Reformulating the problem if needed to make it more precise and actionable\n" \
    #     "4. Highlighting any assumptions or prerequisites\n\n" \
    #     "Given problem: {Problem}\n" \
    #     "Provide your analysis and refined problem statement with the following problem."

    # decomposition = "You are an expert in hierarchical problem decomposition.\n" \
    #     "Your task is to break down the given problem into a structured hierarchy of sub-problems by:\n" \
    #     "0. Thinking step by step\n" \
    #     "1. Identifying the main components that need to be solved\n" \
    #     "2. Arranging sub-problems in a vertical sequence where later steps depend on earlier ones\n" \
    #     "3. For each sub-problem, further decompose if it requires multiple steps\n" \
    #     "4. Specifying dependencies between sub-problems\n" \
    #     "5. Keep the decomposition compact - if the problem can be solved in a single step, list it as one sub-problem\n\n" \
    #     "Problem: {Problem}\n" \
    #     "Provide a hierarchical breakdown showing the vertical dependencies between sub-problems."

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
        "Context: {Context}\n" \
        "First provide your analysis and refined problem statement, then give a hierarchical breakdown showing the vertical dependencies between sub-problems."

    subproblem_solution = "You are an expert problem solver focused on solving specific sub-problems with access to relevant context.\n" \
        "Your task is to solve the given sub-problem by:\n" \
        "0. Think step by step through the entire analysis process\n" \
        "1. Understanding the specific scope and requirements of this sub-problem\n" \
        "2. Reviewing provided context and existing implementations\n" \
        "3. Applying relevant domain knowledge and techniques\n" \
        "4. Providing a clear and detailed solution\n" \
        "5. Explaining your reasoning process\n" \
        "6. Ensuring the solution aligns with any dependencies or constraints\n" \
        "7. Referencing specific patterns or components from context where applicable\n\n" \
        "Sub-problems: {SubProblem}\n" \
        "Dependencies: {Dependencies}\n" \
        "Context: {Context}\n" \
        "Provide your detailed solution for this specific sub-problem."

    solution_aggregation = "You are an expert in synthesizing solutions with access to relevant context.\n" \
        "Your task is to aggregate the solutions from all sub-problems by:\n" \
        "0. Think step by step through the entire analysis process\n" \
        "1. Reviewing all sub-problem solutions\n" \
        "2. Ensuring consistency across solutions\n" \
        "3. Resolving any conflicts or inconsistencies\n" \
        "4. Combining the solutions in a coherent way\n" \
        "5. Verifying the combined solution addresses the refined problem\n\n" \
        "6. Refering any relevant context provided if it's necessary\n\n" \
        "Refined Problem: {RefinedProblem}\n" \
        "Sub-problem Solutions: {SubProblemSolutions}\n" \
        "Context: {Context}\n" \
        "Provide a comprehensive solution that addresses the original problem by synthesizing all sub-solutions."