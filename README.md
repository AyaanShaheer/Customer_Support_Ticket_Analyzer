# Customer Support Ticket Analyzer

A multi-agent system using Pydantic AI for customer support ticket analysis and routing.

## Overview

This system uses two specialized AI agents to analyze customer support tickets:

1. **Classifier Agent**: Categorizes tickets into bug reports, feature requests, billing issues, or general complaints
2. **Priority Agent**: Evaluates the urgency of tickets based on multiple factors

The system then routes tickets to the appropriate teams based on the combined analysis.

## Installation and Usage

### Note on Implementation

The current implementation uses **mock agents** instead of actual AI models to avoid API quota limitations. This allows you to run and test the system without needing API keys or worrying about usage limits.

### To use the mock implementation (default):

```bash
# Clone the repository
git clone https://github.com/AyaanShaheer/Customer_Support_Ticket_Analyzer.git
cd ayaanshaheer-customer-support-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the main application
python main.py
```

### To use actual AI models:

1. Edit `requirements.txt` to uncomment the AI dependencies:

```bash
# Uncomment these lines in requirements.txt
pydantic-ai>=0.2.0
openai>=1.0.0
```

2. Install the updated dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:

```bash
# On Windows
set OPENAI_API_KEY=your_api_key_here

# On Linux/Mac
export OPENAI_API_KEY=your_api_key_here
```

4. Edit the agent files to use the AI implementation instead of the mock implementation:
   - Update `agents/classifier_agent.py` and `agents/priority_agent.py` to use the Pydantic AI Agent class as described in the comments.

5. Run the application:

```bash
python main.py
```

# Run the evaluator
python evaluation/evaluator.py
```

## Agent Descriptions

### Classifier Agent
The Classifier Agent analyzes the content of support tickets and categorizes them into one of the following types:
- Bug reports
- Feature requests
- Billing issues
- General complaints

It examines the ticket subject, message content, and other metadata to make its determination.

### Priority Agent
The Priority Agent evaluates the urgency of each ticket based on multiple factors:
- Customer tier (Enterprise, Business, Standard)
- Customer revenue
- Message sentiment
- Account age
- Previous ticket history

It assigns a priority level of Low, Medium, High, or Urgent to each ticket.

## Evaluation Results

The system was evaluated on a set of 5 test cases with the following results:

- **Agent Agreement**: 0.60 (How well priority aligns with category)
- **Routing Accuracy**: 0.80 (Correct routing decisions)
- **Consistency**: 1.00 (Similar tickets get similar results)

Note: Scores range from 0.0 (worst) to 1.0 (best)

Detailed evaluation results can be found in the evaluation directory.

## Project Structure

```

ayaanshaheer-customer-support-analyzer/
├── main.py                      # Main application entry point
├── agents/
│   ├── classifier_agent.py      # Ticket category classifier
│   └── priority_agent.py        # Ticket priority evaluator
├── router.py                    # Routes tickets based on agent outputs
├── evaluation/
│   └── evaluator.py             # Runs test cases and computes metrics
├── docs/
│   └── system_design.md         # Architecture and design decisions
├── test_cases/
│   └── tickets.json             # Test ticket data
└── ai_chat_history.txt          # Development conversation history
```

## License

MIT
