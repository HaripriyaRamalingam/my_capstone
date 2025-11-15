"""
agent.py
A minimal agent that uses tools and memory.
Run: python agent.py
"""

import json
import os
import re
from typing import Any, Dict

from tools import turn_on_light, set_temperature, get_schedule, help_text
from memory import MemoryStore

class Agent:
    def __init__(self, memory: MemoryStore):
        self.memory = memory

    def handle(self, user_input: str) -> Dict[str, Any]:
        text = user_input.strip().lower()

        # remember command: "remember my favorite drink is coffee"
        m = re.search(r"remember (?:my )?(.+?) is (.+)", text)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            self.memory.add(key, val)
            return {"text": f"Saved '{key}' = '{val}'."}

        # recall command: "what did i ask you to remember?"
        if "what did i ask you to remember" in text or text.startswith("what did i ask"):
            return {"text": json.dumps(self.memory.all(), indent=2)}

        # light control
        if "light" in text:
            # basic room extraction
            rooms = ["kitchen", "bedroom", "living", "bathroom"]
            room = next((r for r in rooms if r in text), "unknown")
            result = turn_on_light(room)
            return {"text": result["message"], "meta": result}

        # temperature control
        mtemp = re.search(r"set (?:the )?temperature to (\d{1,2})", text)
        if mtemp:
            temp = int(mtemp.group(1))
            result = set_temperature(temp)
            return {"text": result["message"], "meta": result}

        # schedule query
        mdate = re.search(r"schedule.*(\d{4}-\d{2}-\d{2})", text)
        if mdate:
            date = mdate.group(1)
            result = get_schedule(date)
            events = result.get("events", [])
            if events:
                return {"text": f"Events on {date}: " + "; ".join(events), "meta": result}
            else:
                return {"text": f"No events found on {date}.", "meta": result}

        if "help" in text or "commands" in text:
            return {"text": help_text()}

        # fallback
        return {"text": "Sorry, I didn't understand. Type 'help' for examples."}

def run_interactive(agent: Agent):
    print("Agent interactive mode. Type 'exit' to quit or 'run_eval' to run simulation tests.")
    while True:
        user = input("You: ").strip()
        if not user:
            continue
        if user.lower() in ("exit", "quit"):
            print("Goodbye.")
            break
        if user.lower() == "run_eval":
            run_evaluations(agent)
            continue
        resp = agent.handle(user)
        print("Agent:", resp.get("text"))

def run_evaluations(agent: Agent):
    eval_path = os.path.join("evaluation", "user_simulation_tests.json")
    if not os.path.exists(eval_path):
        print("No evaluation file found at:", eval_path)
        return
    with open(eval_path, "r", encoding="utf-8") as f:
        tests = json.load(f)

    results = []
    for t in tests:
        print(f"\n--- Running scenario: {t.get('name')} ---")
        convo = t.get("scenario", [])
        scenario_out = []
        for turn in convo:
            user = turn.get("user", "")
            print("User:", user)
            resp = agent.handle(user)
            print("Agent:", resp.get("text"))
            scenario_out.append({"user": user, "agent": resp})
        results.append({"name": t.get("name"), "conversation": scenario_out})

    # save results
    with open("evaluation/eval_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\nEvaluation complete. Results saved to evaluation/eval_results.json")

if __name__ == "__main__":
    mem = MemoryStore()
    agent = Agent(mem)
    run_interactive(agent)

