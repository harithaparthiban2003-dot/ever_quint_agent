import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import (
    PLANNER_SYSTEM_PROMPT,
    EXECUTOR_SYSTEM_PROMPT,
    VERIFIER_SYSTEM_PROMPT,
    PlannerResponse,
    ExecutorResponse,
    VerifierResponse
)

load_dotenv()
client = genai.Client()

# Using gemini-3.6-flash to use a separate per-model free quota bucket
MODEL_NAME = 'gemini-3.6-flash'

def call_with_retry(model, contents, config, max_attempts=3):
    """Automatically retry if rate-limited (429) or busy (503)."""
    delay = 5
    for attempt in range(max_attempts):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
        except Exception as e:
            err_msg = str(e)
            if any(code in err_msg for code in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]):
                if attempt < max_attempts - 1:
                    print(f"   [Rate limit / high demand. Retrying in {delay}s... (Attempt {attempt+1}/{max_attempts})]")
                    time.sleep(delay)
                    delay *= 2
                    continue
            raise e

def solve(question: str) -> dict:
    max_retries = 2
    retries = 0
    plan_str = ""
    checks = []
    status = "failed"
    final_answer = ""
    reasoning_user = ""

    while retries <= max_retries:
        try:
            # Phase 1: Planner
            p_res = call_with_retry(
                model=MODEL_NAME,
                contents=f"{PLANNER_SYSTEM_PROMPT}\n\nQuestion: {question}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=PlannerResponse,
                ),
            )
            plan_obj = PlannerResponse.model_validate_json(p_res.text)
            plan_str = "\n".join([f"{i+1}. {step}" for i, step in enumerate(plan_obj.steps)])

            # Phase 2: Executor
            e_res = call_with_retry(
                model=MODEL_NAME,
                contents=f"{EXECUTOR_SYSTEM_PROMPT}\n\nQuestion: {question}\n\nPlan:\n{plan_str}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ExecutorResponse,
                ),
            )
            exec_obj = ExecutorResponse.model_validate_json(e_res.text)

            # Phase 3: Verifier
            v_res = call_with_retry(
                model=MODEL_NAME,
                contents=f"{VERIFIER_SYSTEM_PROMPT}\n\nQuestion: {question}\n\nExecution Answer: {exec_obj.answer}\nExplanation: {exec_obj.explanation}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=VerifierResponse,
                ),
            )
            ver_obj = VerifierResponse.model_validate_json(v_res.text)

            checks.append({
                "check_name": ver_obj.check_name,
                "passed": ver_obj.passed,
                "details": ver_obj.details
            })

            if ver_obj.passed:
                status = "success"
                final_answer = exec_obj.answer
                reasoning_user = exec_obj.explanation
                break
            else:
                retries += 1
                if retries > max_retries:
                    status = "failed"
                    final_answer = "Could not verify solution after multiple attempts."
                    reasoning_user = ver_obj.details

        except Exception as e:
            retries += 1
            if retries > max_retries:
                status = "error"
                final_answer = f"Error during execution: {str(e)}"
                reasoning_user = "An exception occurred during agent processing."

    return {
        "answer": final_answer,
        "status": status,
        "reasoning_visible_to_user": reasoning_user,
        "metadata": {
            "plan": plan_str,
            "checks": checks,
            "retries": min(retries, max_retries)
        }
    }