"""Example 10: Stop the agent if credit card numbers are detected

Demonstrates safety controls that stop the agent before it can output
sensitive information like credit card numbers to prevent data leakage.
"""

import asyncio
import re

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.requirement import Requirement, Rule
from beeai_framework.backend import SystemMessage
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool, tool

from examples.utils import llm


@tool
def log_reviewer(log_file: str) -> str:
    """Tool that reviews payment logs and might accidentally expose credit card numbers."""
    # Simulate a log review that accidentally exposes sensitive data
    return "Payment error found: Failed transaction for card 4532-1234-5678-9012 - insufficient funds"


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
                    # Force immediate stop with direct instruction to agent
                    await state.memory.add(
                        SystemMessage(
                            f"Your ONLY allowed response is exactly this: 'I cannot complete this task because {self.reason}.' Say nothing else. This is a mandatory safety requirement.",
                            {"tempMessage": True},  # the message gets removed in the next iteration
                        )
                    )
                    return [Rule(target="final_answer", forced=True)]
                    # raise Exception(f"SAFETY STOP: {self.reason}. Detected pattern in tool output.") # alternatively you can raise
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
                pattern=r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # Credit card pattern
                reason="tool output contains credit card numbers",
            )
        ],
    )

    response = await agent.run("Review the transaction error logs").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
