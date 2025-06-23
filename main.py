#!/usr/bin/env python3
"""
Customer Support Ticket Analyzer
Main application entry point
"""

import json
from typing import List, Dict, Any

from agents.classifier_agent import ClassifierAgent
from agents.priority_agent import PriorityAgent
from router import Router


def load_tickets(file_path: str) -> List[Dict[str, Any]]:
    """Load ticket data from a JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)


def main():
    """Main application entry point"""
    # Initialize agents
    classifier = ClassifierAgent()
    priority_agent = PriorityAgent()
    router = Router(classifier, priority_agent)
    
    # Load test tickets
    try:
        tickets = load_tickets('test_cases/tickets.json')
        print(f"Loaded {len(tickets)} tickets for processing")
    except FileNotFoundError:
        print("Error: test_cases/tickets.json not found")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in test_cases/tickets.json")
        return
    
    # Process each ticket
    for ticket in tickets:
        print(f"\nProcessing ticket {ticket.get('id', 'UNKNOWN')}")
        print(f"Subject: {ticket.get('subject', 'No subject')}")
        
        # Get classifications from agents
        category_result = classifier.classify(ticket)
        priority_result = priority_agent.evaluate(ticket)
        
        # Route the ticket
        routing_result = router.route(ticket, category_result, priority_result)
        
        # Display results
        print(f"Category: {category_result.category} - {category_result.reasoning}")
        print(f"Priority: {priority_result.priority_level} - {priority_result.reasoning}")
        print(f"Routed to: {routing_result.team}")
        print("-" * 50)


if __name__ == "__main__":
    main()