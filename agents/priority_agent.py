#!/usr/bin/env python3
"""
Priority Agent

Responsible for evaluating the priority/urgency of customer support tickets
based on multiple factors including customer tier, revenue, sentiment, etc.
"""

from typing import Dict, Any, Literal
from pydantic import BaseModel, Field


class PriorityResult(BaseModel):
    """Result of the priority agent's evaluation"""
    priority_level: Literal["low", "medium", "high", "urgent"] = Field(
        ...,
        description="The priority level assigned to the ticket"
    )
    reasoning: str = Field(
        ...,
        description="Explanation of why this priority level was assigned"
    )


class PriorityAgent:
    """Agent that evaluates the priority/urgency of customer support tickets"""
    
    def __init__(self):
        """Initialize the priority agent"""
        pass
    
    def evaluate(self, ticket: Dict[str, Any]) -> PriorityResult:
        """Evaluate the priority of a ticket
        
        Args:
            ticket: The ticket data containing id, subject, message, customer_tier, etc.
            
        Returns:
            PriorityResult with priority_level and reasoning
        """
        # MOCK IMPLEMENTATION
        # For testing purposes, we're using a mock implementation instead of calling the OpenAI API
        # This avoids API quota issues while testing
        #
        # To use the actual Pydantic AI implementation, replace this section with:
        #
        # from pydantic_ai import Agent
        #
        # # Create an agent for priority evaluation
        # agent = Agent('openai:gpt-4o')
        #
        # # Set up the system prompt for priority evaluation
        # system_prompt = """
        # Evaluate the priority level of a customer support ticket based on multiple factors:
        #
        # 1. Customer tier (Enterprise, Business, Standard)
        # 2. Customer revenue (annual value to the company)
        # 3. Message sentiment and tone (urgent, angry, neutral, etc.)
        # 4. Account age (how long they've been a customer)
        # 5. Previous ticket history (frequency and recency)
        #
        # Assign one of the following priority levels:
        # - low: Can be addressed in normal course of business
        # - medium: Should be addressed soon but not urgent
        # - high: Requires prompt attention
        # - urgent: Requires immediate attention
        #
        # Enterprise customers and high-revenue accounts generally deserve higher priority,
        # but also consider the actual content and context of the ticket.
        #
        # Provide clear reasoning for your priority assignment.
        # """
        #
        # # Create a prompt from the ticket data
        # prompt = f"""Ticket ID: {ticket.get('id', 'Unknown')}
        # Subject: {ticket.get('subject', 'No subject')}
        # Message: {ticket.get('message', 'No message')}
        # Customer Tier: {ticket.get('customer_tier', 'Unknown')}
        # Annual Revenue: ${ticket.get('revenue', 0):,}
        # Account Age: {ticket.get('account_age', 'Unknown')} years
        # Previous Tickets: {ticket.get('previous_tickets', 'None')}
        #
        # Please evaluate the priority of this ticket."""
        #
        # # Run the agent with the output_type set to PriorityResult
        # result = agent.run_sync(
        #     prompt,
        #     system_prompt=system_prompt,
        #     output_type=PriorityResult
        # )
        #
        # # Return the structured result
        # return result.output
        
        # Get ticket data
        message = ticket.get('message', '').lower()
        customer_tier = ticket.get('customer_tier', 'Standard')
        revenue = ticket.get('revenue', 0)
        account_age = ticket.get('account_age', 0)
        previous_tickets = ticket.get('previous_tickets', 'None')
        
        # Determine priority based on rules
        
        # Start with a base score
        priority_score = 0
        
        # Add points based on customer tier
        if customer_tier == 'Enterprise':
            priority_score += 3
        elif customer_tier == 'Business':
            priority_score += 2
        else:  # Standard
            priority_score += 1
        
        # Add points based on revenue
        if revenue > 100000:
            priority_score += 3
        elif revenue > 50000:
            priority_score += 2
        elif revenue > 10000:
            priority_score += 1
        
        # Add points based on message content (simple sentiment analysis)
        urgent_words = ['urgent', 'immediately', 'emergency', 'critical', 'asap', 'right now']
        if any(word in message for word in urgent_words):
            priority_score += 2
        
        # Map score to priority level
        if priority_score >= 7:
            priority_level = "urgent"
            reasoning = "High-value customer with urgent needs requires immediate attention."
        elif priority_score >= 5:
            priority_level = "high"
            reasoning = "Important customer issue that should be addressed promptly."
        elif priority_score >= 3:
            priority_level = "medium"
            reasoning = "Standard priority issue that should be addressed in due course."
        else:
            priority_level = "low"
            reasoning = "Routine issue that can be handled during normal business operations."
        
        # Return a properly structured result
        return PriorityResult(
            priority_level=priority_level,
            reasoning=reasoning
        )