#!/usr/bin/env python3
"""
Classifier Agent

Responsible for categorizing customer support tickets into different types:
- Bug reports
- Feature requests
- Billing issues
- General complaints
"""

from typing import Dict, Any, Literal
from pydantic import BaseModel, Field


class ClassifierResult(BaseModel):
    """Result of the classifier agent's analysis"""
    category: Literal["bug", "feature request", "billing issue", "general complaint"] = Field(
        ...,
        description="The category of the ticket"
    )
    reasoning: str = Field(
        ...,
        description="Explanation of why this category was chosen"
    )


class ClassifierAgent:
    """Agent that classifies customer support tickets into categories"""
    
    def __init__(self):
        """Initialize the classifier agent"""
        pass
    
    def classify(self, ticket: Dict[str, Any]) -> ClassifierResult:
        """Classify a ticket into a category
        
        Args:
            ticket: The ticket data containing id, subject, message, etc.
            
        Returns:
            ClassifierResult with category and reasoning
        """
        # MOCK IMPLEMENTATION
        # For testing purposes, we're using a mock implementation instead of calling the OpenAI API
        # This avoids API quota issues while testing
        #
        # To use the actual Pydantic AI implementation, replace this section with:
        #
        # from pydantic_ai import Agent
        #
        # # Create an agent for classification
        # agent = Agent('openai:gpt-4o')
        #
        # # Set up the system prompt for classification
        # system_prompt = """
        # Analyze the customer support ticket and classify it into one of the following categories:
        # - bug: Issues with the product not working as expected, errors, crashes
        # - feature request: Requests for new functionality or improvements
        # - billing issue: Problems with payments, subscriptions, or pricing
        # - general complaint: Other complaints or feedback that don't fit the above
        #
        # Carefully analyze the subject and message content to determine the most appropriate category.
        # Provide clear reasoning for your classification.
        # """
        #
        # # Create a prompt from the ticket data
        # prompt = f"Ticket ID: {ticket.get('id', 'Unknown')}\nSubject: {ticket.get('subject', 'No subject')}\nMessage: {ticket.get('message', 'No message')}\n\nPlease classify this ticket."
        #
        # # Run the agent with the output_type set to ClassifierResult
        # result = agent.run_sync(
        #     prompt,
        #     system_prompt=system_prompt,
        #     output_type=ClassifierResult
        # )
        #
        # # Return the structured result
        # return result.output
        
        # Simple keyword-based classification logic
        subject = ticket.get('subject', '').lower()
        message = ticket.get('message', '').lower()
        combined_text = subject + ' ' + message
        
        # Determine category based on keywords
        if any(word in combined_text for word in ['crash', 'error', 'bug', 'fix', 'broken', 'not working']):
            category = "bug"
            reasoning = "The ticket mentions software issues, errors or crashes."
        elif any(word in combined_text for word in ['feature', 'add', 'new', 'improve', 'enhancement', 'suggestion']):
            category = "feature request"
            reasoning = "The ticket requests new functionality or improvements."
        elif any(word in combined_text for word in ['bill', 'payment', 'charge', 'subscription', 'price', 'refund', 'credit']):
            category = "billing issue"
            reasoning = "The ticket relates to billing, payments, or pricing concerns."
        else:
            category = "general complaint"
            reasoning = "The ticket contains general feedback that doesn't fit other categories."
        
        # Return a properly structured result
        return ClassifierResult(
            category=category,
            reasoning=reasoning
        )