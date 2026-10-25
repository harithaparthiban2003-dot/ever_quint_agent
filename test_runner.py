import json
import time
from agent import solve

# Define the complete test suite
test_cases = [
    "If a bakery bakes 120 muffins and sells 3/4 of them in the morning, how many muffins are left?",
    "John is 3 times as old as his son. In 10 years, John will be twice as old as his son. How old is John now?",
    "A clothing store has a 20% off sale. If a jacket originally costs $150, what is the final price after the discount and a 5% sales tax applied to the discounted price?"
]

def run_test_suite():
    print("🚀 Starting Full Agent Test Runner...\n")
    
    for i, question in enumerate(test_cases, 1):
        print(f"==================== Test Case {i} ====================")
        print(f"Q: {question}\n")
        
        # Run the agent
        response = solve(question)
        
        # Print the structured JSON output
        print("Agent Output:")
        print(json.dumps(response, indent=2))
        print("\n" + "="*50 + "\n")
        
        # Pause briefly between test cases
        if i < len(test_cases):
            print("⏳ Pausing 5 seconds between test cases...\n")
            time.sleep(5)

if __name__ == "__main__":
    run_test_suite()