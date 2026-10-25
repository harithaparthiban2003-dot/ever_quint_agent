from pydantic import BaseModel, Field

# --- 1. Pydantic Schemas for Structured Outputs ---

class PlannerResponse(BaseModel):
    steps: list[str] = Field(description="Step-by-step plan to solve the question.")

class ExecutorResponse(BaseModel):
    explanation: str = Field(description="Step-by-step execution and calculations.")
    answer: str = Field(description="The final short answer.")

class VerifierResponse(BaseModel):
    check_name: str = Field(description="Name of the constraint being verified.")
    passed: bool = Field(description="True if all constraints pass, false otherwise.")
    details: str = Field(description="Explanation of why it passed or failed.")


# --- 2. System Prompts & Few-Shot Examples ---

PLANNER_SYSTEM_PROMPT = """
You are an expert logical planner. Given a question, break it down into clear, sequential, numbered steps.
Do not solve the problem yet; only create the plan.
"""

EXECUTOR_SYSTEM_PROMPT = """
You are a precise calculation and execution agent. Follow the provided step-by-step plan to solve the question. 
Show your intermediate work in the explanation, and provide a clear final answer.
"""

VERIFIER_SYSTEM_PROMPT = """
You are a strict quality control verifier. Review the original question and the executor's solution.
Check for mathematical errors, constraint violations, or missed details. 
Return whether the solution passes or fails, with a clear explanation.
"""