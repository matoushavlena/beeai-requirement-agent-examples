# BeeAI Requirement Agent Examples

A collection of 10 ready-to-run examples demonstrating the **Requirement Agent** from the [BeeAI Framework](https://framework.beeai.dev/experimental/requirement-agent). These examples show how to guide agent behavior using constraints rather than rigid workflows or fragile prompts.

✅ Tested on `gpt-5-nano`  
🕑 Support for `ollama:gpt-oss:20b` pending ([issue](https://github.com/ollama/ollama/issues/11691))

## What is Requirement Agent?

The Requirement Agent lets you define rules and constraints that guide agent behavior across turns in multi-turn interactions:

- **Conditional tool usage**: Only run tool A after tool B
- **Usage limits**: Use a tool exactly once, no more
- **Human-in-the-loop**: Ask the user before sending an email  
- **Safety controls**: Stop the agent if sensitive content appears

This gives you predictable behavior without hardcoding logic or relying on fragile prompts.

## Use Cases

Perfect for:
- Multi-agent handoff and delegation
- Minimizing hallucinations in tool-driven workflows
- Human-in-the-loop tasks
- ReAct-style planning and reasoning

## Examples Included

1. 🌍 **[Context Before Tool Use](examples/01_context_before_tool.py)** - Ensure agent gets user location before querying weather
2. 1️⃣ **[Exact Tool Usage](examples/02_exact_tool_usage.py)** - Must use price_estimator once, anytime in the flow
3. 🔍 **[Start with Analysis](examples/03_start_with_analysis.py)** - Analyze task before taking any action, and only once
4. ♻️ **[Retry with Rephrasing](examples/04_retry_rephrasing.py)** - Rephrase the query and retry search if output is empty
5. 🤝 **[Multi-agent Handoff](examples/05_multiagent_handoff.py)** - Use DestinationExpert agent before calling WeatherExpert agent
6. 🔄 **[ReAct Loop Control](examples/06_react_loop.py)** - Alternate tools and reasoning, avoid consecutive thinking
7. ☀️ **[Tool Dependency](examples/07_tool_dependency.py)** - Must check the weather before searching events
8. 🏁 **[Final Action Required](examples/08_final_action.py)** - Must send a summary report before returning the final answer
9. ☝️ **[Permission Required](examples/09_permission_required.py)** - Ask user before sending an email to their manager
10. 🛑 **[Safety Stop](examples/10_safety_stop.py)** - Stop if agent outputs something resembling an API key

## Quickstart

```bash
# Install dependencies
uv sync

# Copy and edit environment variables
cp .env.example .env
# Set MODEL and API_KEY in .env

# Run any of the examples
uv run examples/01_context_before_tool.py
uv run examples/02_exact_tool_usage.py
uv run examples/03_start_with_analysis.py
uv run examples/04_retry_rephrasing.py
uv run examples/05_multiagent_handoff.py
uv run examples/06_react_loop.py
uv run examples/07_tool_dependency.py
uv run examples/08_final_action.py
uv run examples/09_permission_required.py
uv run examples/10_safety_stop.py
```

Required environment variables:
- `MODEL`: Defaults to `openai:gpt-5-nano` (see top note for `ollama:gpt-oss-20b` support status). Other models may also work.
- `API_KEY`: Your API key for the selected provider (optional).

**Note**: Examples have been tested on `gpt-5-nano`. Other models may behave differently with the constraints.

## Presentation

View the presentation for a visual overview of the 10 examples with code snippets:
- [Slides (Markdown)](presentation.md)
- [Slides (PDF)](presentation.pdf)

## Documentation

For full documentation, visit: https://framework.beeai.dev/experimental/requirement-agent

## Contributing

Feel free to submit additional examples or improvements via pull requests.