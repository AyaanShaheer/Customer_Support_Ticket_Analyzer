#!/usr/bin/env python3
"""
Ticket Router

Combines the outputs of the classifier and priority agents to determine
the appropriate team for handling each customer support ticket.
"""

from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

from agents.classifier_agent import ClassifierAgent, ClassifierResult
from agents.priority_agent import PriorityAgent, PriorityResult


class RoutingResult(BaseModel):
    """Result of the routing decision"""
    team: Literal["Escalation Team", "Product Team", "Finance Support", "General Support"] = Field(
        ...,
        description="The team that should handle this ticket"
    )
    reasoning: str = Field(
        ...,
        description="Explanation of why this team was chosen"
    )


class Router:
    """Routes customer support tickets to the appropriate team"""
    
    def __init__(self, classifier: ClassifierAgent, priority_agent: PriorityAgent):
        """Initialize the router with the classifier and priority agents
        
        Args:
            classifier: The classifier agent
            priority_agent: The priority agent
        """
        self.classifier = classifier
        self.priority_agent = priority_agent
    
    def route(self, ticket: Dict[str, Any], 
              category_result: ClassifierResult, 
              priority_result: PriorityResult) -> RoutingResult:
        """Route a ticket to the appropriate team
        
        Args:
            ticket: The ticket data
            category_result: The result from the classifier agent
            priority_result: The result from the priority agent
            
        Returns:
            RoutingResult with the team and reasoning
        """
        # Extract relevant information
        category = category_result.category
        priority = priority_result.priority_level
        customer_tier = ticket.get("customer_tier", "").lower()
        
        # Apply routing rules
        if (priority == "urgent" or 
                (category == "bug" and customer_tier == "enterprise")):
            team = "Escalation Team"
            reasoning = f"Routed to Escalation Team because "
            if priority == "urgent":
                reasoning += f"the ticket is marked as {priority}"
                if category == "bug" and customer_tier == "enterprise":
                    reasoning += " and "
            if category == "bug" and customer_tier == "enterprise":
                reasoning += f"it's a {category} from an {customer_tier} customer"
        
        elif category == "feature request":
            team = "Product Team"
            reasoning = f"Routed to Product Team because the ticket is categorized as a {category}"
        
        elif category == "billing issue":
            team = "Finance Support"
            reasoning = f"Routed to Finance Support because the ticket is categorized as a {category}"
        
        else:
            team = "General Support"
            reasoning = f"Routed to General Support as it doesn't meet criteria for specialized teams"
        
        return RoutingResult(team=team, reasoning=reasoning)