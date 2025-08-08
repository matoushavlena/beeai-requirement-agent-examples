"""Example 10: Stop the agent if API keys are detected

Demonstrates safety controls that stop the agent before it can output
sensitive information like API keys to prevent credential leakage.
"""

import asyncio
import re

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.requirement import Requirement
from beeai_framework.tools import Tool, tool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware

from examples.utils import llm


# Global counter to simulate state (in real use, this would be handled differently)
review_count = 0


@tool
def log_reviewer(log_file: str) -> str:
    """Tool that reviews logs and might accidentally expose API keys."""
    global review_count
    review_count += 1

    # Simulate different log review results
    safe_logs = [
        "Log review complete: No issues found in application logs.",
        "Authentication logs show normal user activity patterns.",
        "Error logs contain standard HTTP 404 and 500 responses.",
    ]

    # Simulate accidental API key exposure on 2nd review
    if review_count == 2:
        return "Log analysis found: API_KEY=sk-1234567890abcdef1234567890abcdef configuration error"

    import random

    return random.choice(safe_logs)


# Temporary fix for the bug in the framework
log_reviewer.input_schema.model_config["extra"] = "forbid"


class PrematureStopRequirement(Requirement):
    """Custom requirement to stop agent if sensitive patterns are detected."""

    def __init__(self, pattern: str, reason: str):
        super().__init__()
        self.pattern = re.compile(pattern)
        self.reason = reason
        self.enabled = True

    async def run(self, state, **kwargs):
        """Check if output contains sensitive patterns and force stop if found."""
        try:
            # Check the most recent tool output for sensitive patterns
            if state.steps:
                last_step = state.steps[-1].output.get_text_content()
                if last_step and self.pattern.search(str(last_step)):
                    # Stop the agent immediately if sensitive pattern found
                    raise Exception(f"SAFETY STOP: {self.reason}. Detected pattern in tool output.")
        except (AttributeError, IndexError):
            # If we can't access the step content, continue safely
            pass
        return []


async def main():
    # Create agent with safety stop requirement
    agent = RequirementAgent(
        llm=llm,
        tools=[log_reviewer],
        requirements=[
            PrematureStopRequirement(
                pattern=r"sk-[A-Za-z0-9]{32,}",  # OpenAI API key pattern
                reason="output may contain leaked credentials",
            )
        ],
    )

    # First review will be safe, second review will expose API key and trigger safety stop
    print("First review:")
    response1 = await agent.run("Review the application logs for any issues").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response1.answer.text)

    print("\nSecond review (should trigger safety stop):")
    response2 = await agent.run("Review the system logs for configuration errors").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response2.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
