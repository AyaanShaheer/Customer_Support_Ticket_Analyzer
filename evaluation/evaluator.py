#!/usr/bin/env python3
"""
Evaluator

Runs all test cases and computes evaluation metrics for the
customer support ticket analysis and routing system.
"""

import json
import sys
import os
from typing import Dict, Any, List, Tuple

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.classifier_agent import ClassifierAgent, ClassifierResult
from agents.priority_agent import PriorityAgent, PriorityResult
from router import Router, RoutingResult


# Expected results for evaluation
EXPECTED_RESULTS = {
    "SUP-001": {
        "category": "bug",
        "priority": "high",  # Could be high or urgent depending on interpretation
        "team": "Escalation Team"
    },
    "SUP-002": {
        "category": "feature request",
        "priority": "low",
        "team": "Product Team"
    },
    "SUP-003": {
        "category": "billing issue",
        "priority": "medium",
        "team": "Finance Support"
    },
    "SUP-004": {
        "category": "general complaint",  # Could also be classified as bug
        "priority": "urgent",
        "team": "Escalation Team"
    },
    "SUP-005": {
        "category": "general complaint",
        "priority": "low",
        "team": "General Support"
    }
}


def load_tickets(file_path: str) -> List[Dict[str, Any]]:
    """Load ticket data from a JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)


def calculate_agent_agreement(category_results: Dict[str, ClassifierResult],
                             priority_results: Dict[str, PriorityResult]) -> float:
    """Calculate agreement between agent outputs
    
    Measures how well the priority aligns with the category
    (e.g., bugs should generally be higher priority than feature requests)
    
    Returns:
        Score between 0.0 and 1.0
    """
    agreement_count = 0
    total_count = len(category_results)
    
    # Define expected priority levels for each category
    expected_priorities = {
        "bug": {"high", "urgent"},  # Bugs should be high or urgent priority
        "feature request": {"low", "medium"},  # Feature requests should be low or medium
        "billing issue": {"medium", "high"},  # Billing issues should be medium or high
        "general complaint": {"low", "medium", "high", "urgent"}  # General complaints can be any priority
    }
    
    # Check if priority aligns with category expectations
    for ticket_id in category_results:
        category = category_results[ticket_id].category
        priority = priority_results[ticket_id].priority_level
        
        if priority in expected_priorities.get(category, set()):
            agreement_count += 1
    
    return agreement_count / total_count if total_count > 0 else 0.0


def calculate_routing_accuracy(routing_results: Dict[str, RoutingResult]) -> float:
    """Calculate accuracy of routing decisions compared to expected results
    
    Returns:
        Score between 0.0 and 1.0
    """
    correct_count = 0
    total_count = len(routing_results)
    
    for ticket_id, result in routing_results.items():
        if ticket_id in EXPECTED_RESULTS:
            expected_team = EXPECTED_RESULTS[ticket_id]["team"]
            if result.team == expected_team:
                correct_count += 1
    
    return correct_count / total_count if total_count > 0 else 0.0


def calculate_consistency(category_results: Dict[str, ClassifierResult],
                         priority_results: Dict[str, PriorityResult]) -> float:
    """Calculate consistency of agent outputs
    
    Measures if similar tickets receive similar classifications and priorities
    
    Returns:
        Score between 0.0 and 1.0
    """
    # For this simplified implementation, we'll check if tickets with similar subjects
    # receive similar classifications
    
    # Group tickets by keywords in subject
    keyword_groups = {
        "crash": [],  # For crash-related tickets
        "feature": [],  # For feature request tickets
        "billing": [],  # For billing-related tickets
        "urgent": [],  # For urgent tickets
        "help": []  # For general help tickets
    }
    
    # Assign tickets to groups based on keywords in subject
    for ticket_id in category_results:
        subject = ticket_id.lower()
        
        if "crash" in subject:
            keyword_groups["crash"].append(ticket_id)
        elif "feature" in subject:
            keyword_groups["feature"].append(ticket_id)
        elif "billing" in subject:
            keyword_groups["billing"].append(ticket_id)
        elif "urgent" in subject:
            keyword_groups["urgent"].append(ticket_id)
        elif "help" in subject:
            keyword_groups["help"].append(ticket_id)
    
    # Count consistent classifications within each group
    consistent_count = 0
    total_comparisons = 0
    
    for group in keyword_groups.values():
        if len(group) <= 1:
            continue
        
        # Check all pairs in the group
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                total_comparisons += 1
                
                # Check if category is consistent
                if category_results[group[i]].category == category_results[group[j]].category:
                    consistent_count += 0.5  # Half point for category match
                
                # Check if priority is consistent
                if priority_results[group[i]].priority_level == priority_results[group[j]].priority_level:
                    consistent_count += 0.5  # Half point for priority match
    
    return consistent_count / total_comparisons if total_comparisons > 0 else 1.0


def run_evaluation() -> Tuple[float, float, float]:
    """Run evaluation on all test cases and compute metrics
    
    Returns:
        Tuple of (agent_agreement, routing_accuracy, consistency) scores
    """
    # Initialize agents
    classifier = ClassifierAgent()
    priority_agent = PriorityAgent()
    router = Router(classifier, priority_agent)
    
    # Load test tickets
    try:
        tickets = load_tickets(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                          'test_cases', 'tickets.json'))
        print(f"Loaded {len(tickets)} tickets for evaluation")
    except FileNotFoundError:
        print("Error: test_cases/tickets.json not found")
        return 0.0, 0.0, 0.0
    except json.JSONDecodeError:
        print("Error: Invalid JSON in test_cases/tickets.json")
        return 0.0, 0.0, 0.0
    
    # Store results for each ticket
    category_results = {}
    priority_results = {}
    routing_results = {}
    
    # Process each ticket
    for ticket in tickets:
        ticket_id = ticket.get('id', 'UNKNOWN')
        print(f"\nProcessing ticket {ticket_id}")
        print(f"Subject: {ticket.get('subject', 'No subject')}")
        
        # Get classifications from agents
        category_result = classifier.classify(ticket)
        priority_result = priority_agent.evaluate(ticket)
        
        # Route the ticket
        routing_result = router.route(ticket, category_result, priority_result)
        
        # Store results
        category_results[ticket_id] = category_result
        priority_results[ticket_id] = priority_result
        routing_results[ticket_id] = routing_result
        
        # Display results
        print(f"Category: {category_result.category} - {category_result.reasoning}")
        print(f"Priority: {priority_result.priority_level} - {priority_result.reasoning}")
        print(f"Routed to: {routing_result.team} - {routing_result.reasoning}")
        print("-" * 50)
    
    # Calculate metrics
    agent_agreement = calculate_agent_agreement(category_results, priority_results)
    routing_accuracy = calculate_routing_accuracy(routing_results)
    consistency = calculate_consistency(category_results, priority_results)
    
    return agent_agreement, routing_accuracy, consistency


def main():
    """Main function to run the evaluation"""
    print("=== Customer Support Ticket Analysis System Evaluation ===\n")
    
    # Run evaluation
    agent_agreement, routing_accuracy, consistency = run_evaluation()
    
    # Display results
    print("\n=== Evaluation Results ===")
    print(f"Agent Agreement: {agent_agreement:.2f} (How well priority aligns with category)")
    print(f"Routing Accuracy: {routing_accuracy:.2f} (Correct routing decisions)")
    print(f"Consistency: {consistency:.2f} (Similar tickets get similar results)")
    print("\nNote: Scores range from 0.0 (worst) to 1.0 (best)")


if __name__ == "__main__":
    main()