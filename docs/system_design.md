# Customer Support Ticket Analyzer - System Design

## Implementation Note

The current implementation uses mock agents instead of actual AI models to avoid API quota limitations. The mock implementations use rule-based approaches:

1. **Classifier Agent**: Uses keyword matching to categorize tickets based on common terms associated with each category.

2. **Priority Agent**: Uses a scoring system based on customer tier, revenue, and message content to determine priority levels.

To use actual AI models with Pydantic AI:

1. Uncomment the dependencies in `requirements.txt`
2. Install the dependencies with `pip install -r requirements.txt`
3. Replace the mock implementations in the agent files with the AI-powered implementations that use the Pydantic AI Agent class.

The original design using Pydantic AI is documented below.

## Architecture Overview

The Customer Support Ticket Analyzer is a multi-agent system designed to process and route customer support tickets efficiently. The system consists of two specialized AI agents working together:

1. **Classifier Agent**: Categorizes tickets into specific types (bug, feature request, billing issue, general complaint)
2. **Priority Agent**: Evaluates the urgency of tickets based on multiple factors

These agents feed their outputs to a **Router** component that makes the final decision on which team should handle each ticket.

## Why Two Agents Instead of One?

The system deliberately uses two separate agents rather than a single agent for several important reasons:

### 1. Separation of Concerns

By separating classification and prioritization into distinct agents, each agent can focus on a specific aspect of ticket analysis. This leads to:

- **Improved Accuracy**: Each agent can specialize in its specific task without being distracted by other considerations
- **Better Maintainability**: Changes to classification logic don't affect prioritization logic and vice versa
- **Easier Debugging**: When issues arise, it's clearer which agent is responsible

### 2. Independent Evaluation

The two-agent approach allows for independent evaluation of different aspects of ticket analysis:

- A ticket's category (what it's about) is conceptually distinct from its priority (how urgent it is)
- A feature request from an enterprise customer might be high priority despite not being a bug
- A bug report from a new standard-tier customer might be lower priority despite being a legitimate bug

### 3. Flexibility in Routing Rules

Having separate outputs for category and priority gives the router more flexibility in determining the appropriate team:

- The router can apply complex business rules that consider both category and priority
- The system can be easily adjusted to accommodate changing business priorities
- Different organizations can customize routing rules without changing the underlying agents

## Prompt Iterations

### Classifier Agent Prompt Evolution

#### Version 1 (Initial)

```python
@ai_model
def classify_ticket(ticket: Dict[str, Any]) -> ClassifierResult:
    """
    Analyze the customer support ticket and classify it into one of the following categories:
    - bug
    - feature request
    - billing issue
    - general complaint
    
    Provide reasoning for your classification.
    """
    pass
```

**Issues with V1:**
- Too vague about what constitutes each category
- No guidance on which parts of the ticket to focus on
- Minimal instruction on reasoning requirements

#### Version 2 (Improved)

```python
@ai_model
def classify_ticket(ticket: Dict[str, Any]) -> ClassifierResult:
    """
    Analyze the customer support ticket and classify it into one of the following categories:
    - bug: Issues with the product not working as expected, errors, crashes
    - feature request: Requests for new functionality or improvements
    - billing issue: Problems with payments, subscriptions, or pricing
    - general complaint: Other complaints or feedback that don't fit the above
    
    Carefully analyze the subject and message content to determine the most appropriate category.
    Provide clear reasoning for your classification.
    """
    pass
```

**Improvements in V2:**
- Clear definitions for each category
- Explicit instruction to focus on subject and message content
- Direction to provide clear reasoning

### Priority Agent Prompt Evolution

#### Version 1 (Initial)

```python
@ai_model
def evaluate_priority(ticket: Dict[str, Any]) -> PriorityResult:
    """
    Evaluate the priority level of a customer support ticket.
    Assign one of the following priority levels: low, medium, high, urgent
    Consider the customer tier and message content.
    Provide reasoning for your priority assignment.
    """
    pass
```

**Issues with V1:**
- Limited factors to consider
- No guidance on how different factors should influence priority
- Minimal instruction on reasoning requirements

#### Version 2 (Improved)

```python
@ai_model
def evaluate_priority(ticket: Dict[str, Any]) -> PriorityResult:
    """
    Evaluate the priority level of a customer support ticket based on multiple factors:
    
    1. Customer tier (Enterprise, Business, Standard)
    2. Customer revenue (annual value to the company)
    3. Message sentiment and tone (urgent, angry, neutral, etc.)
    4. Account age (how long they've been a customer)
    5. Previous ticket history (frequency and recency)
    
    Assign one of the following priority levels:
    - low: Can be addressed in normal course of business
    - medium: Should be addressed soon but not urgent
    - high: Requires prompt attention
    - urgent: Requires immediate attention
    
    Enterprise customers and high-revenue accounts generally deserve higher priority,
    but also consider the actual content and context of the ticket.
    
    Provide clear reasoning for your priority assignment.
    """
    pass
```

**Improvements in V2:**
- Comprehensive list of factors to consider
- Clear definitions for each priority level
- Guidance on balancing customer tier/revenue with actual ticket content
- Direction to provide clear reasoning

## Tricky Behavior in Tickets

The system is designed to handle several challenging scenarios that require nuanced analysis:

### 1. Rude Tone vs. Low Revenue

Some tickets may contain angry or rude language but come from low-revenue customers. The Priority Agent needs to balance:

- Responding appropriately to customer frustration
- Allocating resources based on business impact

The current design allows the Priority Agent to consider both the message sentiment and customer value, potentially assigning a medium priority to acknowledge the frustration while not diverting resources from higher-value customers.

### 2. Feature Requests from Enterprise Customers

Feature requests are typically lower priority than bugs, but when they come from enterprise customers, they may warrant higher attention. The system handles this by:

- Having the Classifier Agent categorize the ticket as a feature request
- Having the Priority Agent assign a higher priority based on customer tier
- Allowing the Router to send it to the Product Team (due to category) while still flagging its importance

### 3. Vague or Ambiguous Tickets

Some tickets may be difficult to categorize because they contain minimal information or mix multiple issues. The system addresses this by:

- Encouraging agents to provide detailed reasoning for their decisions
- Allowing the Classifier Agent to use the "general complaint" category when appropriate
- Enabling the Router to default to General Support when uncertainty is high

### 4. Urgent but Minor Issues

Customers may mark minor issues as "urgent" in their subject line. The system handles this by:

- Having the Priority Agent evaluate the actual content rather than just keywords
- Considering multiple factors beyond just the customer's stated urgency
- Providing clear reasoning when downgrading a self-labeled "urgent" ticket

## Future Improvements

1. **Feedback Loop**: Implement a mechanism to capture agent performance and incorporate feedback
2. **Additional Agents**: Add specialized agents for sentiment analysis or technical complexity assessment
3. **Historical Analysis**: Incorporate analysis of similar past tickets and their resolutions
4. **Confidence Scores**: Have agents provide confidence levels for their classifications
5. **Human-in-the-Loop**: Add capability for human review of uncertain cases