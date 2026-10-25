# Multi-Step Reasoning Agent (Planner-Executor-Verifier)

A production-ready Multi-Step Reasoning Agent built using Python, Pydantic, and the Google Gemini API (`gemini-3.6-flash`). The agent implements a 3-phase cognitive loop—**Planner → Executor → Verifier**—to ensure mathematical accuracy, structured outputs, and self-correction for complex problem-solving.

---

## 🛠️ Architecture & Tech Stack

* **Language:** Python 3.10+
* **SDK:** `google-genai` (Official Google GenAI SDK)
* **Validation:** `pydantic` (Schema validation & structured JSON outputs)
* **Configuration:** `python-dotenv` (Environment variable management)

### 3-Phase Cognitive Loop
1. **Planner Phase:** Accepts a user query and breaks it down into an ordered, step-by-step plan without performing final calculations.
2. **Executor Phase:** Receives the original question and generated plan, executing each step sequentially to derive the solution.
3. **Verifier Phase:** Audits the execution logic, verifying mathematical operations and returning an explicit verification check (`passed: true/false`). If verification fails, the system triggers a self-correction retry loop.

---

## 🚀 Setup & Execution Guide

### 1. Clone & Navigate
```bash
git clone [https://github.com/YOUR_USERNAME/multi-step-reasoning-agent.git](https://github.com/YOUR_USERNAME/multi-step-reasoning-agent.git)
cd multi-step-reasoning-agent
**2. Install Dependencies**
Bash
pip install -r requirements.txt
**3. Environment Configuration**
Create a .env file in the root directory and insert your Gemini API Key:

Code snippet
GEMINI_API_KEY=my_api_key_here
**4. Run Test Suite**
To execute the multi-step agent against the test cases:

Bash
python test_runner.py
📁 Repository Structure & Code Locations
agent.py: Contains the core logic for the 3-phase loop (solve()) and includes exponential backoff retry handling (call_with_retry()) to handle API rate limits (429) and high demand (503).

prompts.py: Where prompts live. Holds system instructions (PLANNER_SYSTEM_PROMPT, EXECUTOR_SYSTEM_PROMPT, VERIFIER_SYSTEM_PROMPT) and Pydantic schemas (PlannerResponse, ExecutorResponse, VerifierResponse).

test_runner.py: Test suite script that runs sample questions through the agent, formats JSON outputs, and enforces pacing between requests to respect API rate limits.

requirements.txt: List of required dependencies.

run_logs.json: Output logs showcasing multi-step reasoning results across test cases.

💡 Key Assumptions
Native Structured JSON Outputs: The implementation assumes strict adherence to JSON schemas via pydantic types and Gemini's native response_schema configuration, avoiding standard regex text-parsing errors.

Model Selection & Quota Optimizations: Uses gemini-3.6-flash to optimize free-tier API quota usage while retaining strong reasoning capabilities.

Rate Limit Handling: Assumes potential API throttling on free-tier keys, implementing programmatic sleeping and retries within call_with_retry().

📝 Prompt Design & Rationale
Why Prompts Were Designed This Way
Role Separation: Splitting the workflow into three distinct roles prevents cognitive overload in a single prompt call. The Planner focuses purely on strategy, the Executor focuses on calculation, and the Verifier provides an unbiased check.

Type-Safe Outputs: Constraining outputs via Pydantic schemas guarantees that every API response maps directly into structured fields (plan, checks, status, reasoning_visible_to_user).

What We Tried That Didn't Work Well
Single-Prompt Chain of Thought: Combining planning, solving, and auditing into a single prompt led to calculation drift and false positive self-verifications.

Unstructured Text Parsing: Relying on markdown extraction (```json ... ```) resulted in occasional JSON parsing failures when models appended preamble text. Switching to explicit API response_schema parameters eliminated output parsing errors.

Improvements With More Time
Iterative Feedback Injection: Instead of running full pipeline retries on verification failure, pass the Verifier's specific error feedback back into the Executor for targeted correction.

Code Sandbox (Python REPL Tool): Equipping the Executor with a code execution engine for complex mathematical or symbolic calculations rather than relying solely on LLM mental math.

Async Processing: Refactoring API calls with asyncio to speed up multi-question batch runs.
