from crewai import Agent
import json
from typing import Dict, List, Any

class PartnerFitScoreCalculator:
    """
    A utility class to calculate partner fit scores based on multiple criteria
    
    This class demonstrates how the Partner Fit Score Agent might evaluate
    potential partners using a scoring system.
    """
    
    def __init__(self):
        # Define scoring criteria and weights
        self.criteria = {
            "brand_alignment": {
                "weight": 0.25,
                "description": "How well the partner's brand aligns with MLSE's values and image"
            },
            "financial_health": {
                "weight": 0.20,
                "description": "The partner's financial stability and growth potential"
            },
            "audience_overlap": {
                "weight": 0.20,
                "description": "How much the partner's audience overlaps with MLSE's fan base"
            },
            "partnership_history": {
                "weight": 0.15,
                "description": "The partner's history with sports sponsorships and partnerships"
            },
            "activation_potential": {
                "weight": 0.10,
                "description": "Potential for creative and engaging partnership activations"
            },
            "exclusivity_value": {
                "weight": 0.10,
                "description": "Value of category exclusivity and competitive advantage"
            }
        }
    
    def calculate_score(self, partner_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate a comprehensive fit score for a potential partner
        
        Args:
            partner_data: Dictionary containing partner information and individual criteria scores
            
        Returns:
            Dictionary with overall score and breakdown by criteria
        """
        if "criteria_scores" not in partner_data:
            raise ValueError("Partner data must include criteria_scores")
        
        criteria_scores = partner_data["criteria_scores"]
        
        # Calculate weighted score for each criterion
        weighted_scores = {}
        total_score = 0.0
        
        for criterion, details in self.criteria.items():
            if criterion not in criteria_scores:
                raise ValueError(f"Missing score for criterion: {criterion}")
            
            score = criteria_scores[criterion]
            weight = details["weight"]
            weighted_score = score * weight
            
            weighted_scores[criterion] = {
                "raw_score": score,
                "weight": weight,
                "weighted_score": weighted_score
            }
            
            total_score += weighted_score
        
        # Create result dictionary
        result = {
            "partner_name": partner_data["name"],
            "overall_score": round(total_score, 2),
            "score_breakdown": weighted_scores,
            "recommendation": self._generate_recommendation(total_score)
        }
        
        return result
    
    def _generate_recommendation(self, score: float) -> str:
        """Generate a recommendation based on the overall score"""
        if score >= 8.5:
            return "Excellent fit - Pursue partnership immediately"
        elif score >= 7.0:
            return "Strong fit - Highly recommended for partnership"
        elif score >= 5.5:
            return "Good fit - Consider for partnership"
        elif score >= 4.0:
            return "Moderate fit - Explore specific opportunities"
        else:
            return "Poor fit - Not recommended at this time"

def create_partner_fit_score_agent():
    """Create the Partner Fit Score Agent"""
    
    partner_fit_score_agent = Agent(
        role="Partner Fit Score Agent",
        goal="Evaluate potential partners using a scoring system based on relevance, financials, and strategic alignment",
        backstory="You are a sophisticated evaluation agent with expertise in partner assessment frameworks. You've developed a comprehensive scoring system that analyzes potential partners based on multiple criteria including financial health, brand alignment, strategic fit, and market position.",
        verbose=True
    )
    
    return partner_fit_score_agent

def example_partner_evaluation():
    """Example of how the Partner Fit Score Agent might evaluate partners"""
    
    # Sample partner data (in a real system, this would come from the Research Agent)
    sample_partners = [
        {
            "name": "TechCorp Inc.",
            "industry": "Technology",
            "description": "Leading technology company specializing in consumer electronics",
            "annual_revenue": "$5.2B",
            "previous_sports_partnerships": ["NBA Team", "European Soccer League"],
            "criteria_scores": {
                "brand_alignment": 8.5,
                "financial_health": 9.0,
                "audience_overlap": 7.5,
                "partnership_history": 8.0,
                "activation_potential": 9.0,
                "exclusivity_value": 8.5
            }
        },
        {
            "name": "HealthFit Co.",
            "industry": "Health & Fitness",
            "description": "Health and fitness company with premium workout equipment and supplements",
            "annual_revenue": "$850M",
            "previous_sports_partnerships": ["Olympic Committee", "Fitness Competitions"],
            "criteria_scores": {
                "brand_alignment": 9.0,
                "financial_health": 7.5,
                "audience_overlap": 8.5,
                "partnership_history": 7.0,
                "activation_potential": 8.5,
                "exclusivity_value": 7.0
            }
        },
        {
            "name": "LuxuryBrands Global",
            "industry": "Luxury Retail",
            "description": "High-end luxury retail conglomerate with multiple premium brands",
            "annual_revenue": "$3.8B",
            "previous_sports_partnerships": ["Tennis Tournaments", "Golf Championships"],
            "criteria_scores": {
                "brand_alignment": 6.5,
                "financial_health": 8.5,
                "audience_overlap": 5.0,
                "partnership_history": 6.0,
                "activation_potential": 7.0,
                "exclusivity_value": 9.0
            }
        }
    ]
    
    # Create calculator
    calculator = PartnerFitScoreCalculator()
    
    # Calculate scores for each partner
    results = []
    for partner in sample_partners:
        score_result = calculator.calculate_score(partner)
        results.append(score_result)
    
    # Sort results by overall score (descending)
    results.sort(key=lambda x: x["overall_score"], reverse=True)
    
    return results

if __name__ == "__main__":
    # Run the example
    evaluation_results = example_partner_evaluation()
    
    # Print the results
    print("\n========================")
    print("PARTNER FIT SCORE RESULTS:")
    print("========================\n")
    
    for i, result in enumerate(evaluation_results, 1):
        print(f"#{i}: {result['partner_name']}")
        print(f"Overall Score: {result['overall_score']}/10")
        print(f"Recommendation: {result['recommendation']}")
        print("\nScore Breakdown:")
        
        for criterion, details in result['score_breakdown'].items():
            print(f"  - {criterion.replace('_', ' ').title()}: {details['raw_score']} " +
                  f"(weight: {details['weight']}, weighted: {details['weighted_score']:.2f})")
        
        print("\n" + "-" * 50 + "\n")
    
    # Example of how this would be used in the full system
    print("In the full MLSE Partnership Crew system:")
    print("1. The Research Agent would gather detailed information on potential partners")
    print("2. The Partner Fit Score Agent would evaluate each partner using this scoring system")
    print("3. The results would be used by other agents to create presentations and recommendations")