# BeeAI Requirement Agent Examples

A collection of practical examples demonstrating the **Requirement Agent** from the [BeeAI Framework](https://framework.beeai.dev/experimental/requirement-agent). These examples show how to guide agent behavior using constraints rather than rigid workflows or fragile prompts.

## What is Requirement Agent?

The Requirement Agent allows you to define rules and constraints that guide agent behavior across turns in multi-turn interactions:

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

1. **[Context Before Tool Use](examples/01_context_before_tool.py)** - Ensure agent gets user location before querying weather
2. **[Exact Tool Usage](examples/02_exact_tool_usage.py)** - Must use price_estimator once, anytime in the flow
3. **[Start with Analysis](examples/03_start_with_analysis.py)** - Analyze task before taking any action, and only once
4. **[Retry with Rephrasing](examples/04_retry_rephrasing.py)** - Rephrase the query and retry search if output is empty (max 3 attempts)
5. **[Multi-agent Handoff](examples/05_multiagent_handoff.py)** - Use DestinationExpert agent before calling WeatherExpert agent
6. **[ReAct Loop Control](examples/06_react_loop.py)** - Alternate tools and reasoning, avoid consecutive thinking
7. **[Tool Dependency](examples/07_tool_dependency.py)** - Must check the weather before searching events
8. **[Final Action Required](examples/08_final_action.py)** - Must send a summary report before returning the final answer
9. **[Permission Required](examples/09_permission_required.py)** - Ask user before sending an email to their manager
10. **[Safety Stop](examples/10_safety_stop.py)** - Stop if agent outputs something resembling an API key

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Configure your environment:
```bash
cp .env.example .env
# Edit .env and set your API_KEY
```

Required environment variables:
- `API_KEY`: Your OpenAI API key
- `MODEL`: Model to use (default: `openai:gpt-5-nano`)

**Note**: Examples have been tested on `gpt-5-nano`. Other models may behave differently with the constraints.

## Running Examples

Each example can be run independently:

```bash
uv run examples/01_context_before_tool.py
uv run examples/02_exact_tool_usage.py
# ... etc
```

## Documentation

For full documentation, visit: https://framework.beeai.dev/experimental/requirement-agent

## Contributing

Feel free to submit additional examples or improvements via pull requests.

## License

MIT License - see LICENSE file for details.