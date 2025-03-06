from crewai import Agent
import json
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import os

class PartnershipGapAnalyzer:
    """
    A utility class to analyze partnership data and identify gaps
    
    This class demonstrates how the Gap Identification Agent might
    analyze current partnerships to identify opportunities.
    """
    
    def __init__(self):
        """Initialize the gap analyzer with industry categories and benchmarks"""
        
        # Define industry categories for partnership analysis
        self.industry_categories = [
            "Financial Services",
            "Telecommunications",
            "Technology",
            "Automotive",
            "Apparel & Sportswear",
            "Food & Beverage",
            "Health & Wellness",
            "Travel & Hospitality",
            "Insurance",
            "Energy",
            "Entertainment",
            "Retail",
            "Luxury Goods"
        ]
        
        # Define benchmark data for sports partnership portfolios
        # This represents the typical distribution of partnerships for major sports organizations
        self.industry_benchmarks = {
            "Financial Services": 0.15,  # 15% of partnerships
            "Telecommunications": 0.10,
            "Technology": 0.12,
            "Automotive": 0.08,
            "Apparel & Sportswear": 0.10,
            "Food & Beverage": 0.12,
            "Health & Wellness": 0.08,
            "Travel & Hospitality": 0.06,
            "Insurance": 0.05,
            "Energy": 0.04,
            "Entertainment": 0.05,
            "Retail": 0.03,
            "Luxury Goods": 0.02
        }
        
        # Define partnership types
        self.partnership_types = [
            "Naming Rights",
            "Jersey Sponsor",
            "Official Partner",
            "Media Partner",
            "Technology Partner",
            "Community Partner",
            "Event Sponsor"
        ]
    
    def analyze_current_partners(self, current_partners: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze current partners to identify industry distribution
        
        Args:
            current_partners: List of current partner data
            
        Returns:
            Analysis of current partnership distribution
        """
        # Count partners by industry
        industry_counts = {category: 0 for category in self.industry_categories}
        other_industries = []
        
        for partner in current_partners:
            industry = partner.get("industry", "Unknown")
            if industry in industry_counts:
                industry_counts[industry] += 1
            else:
                other_industries.append(industry)
        
        # Calculate percentages
        total_partners = len(current_partners)
        industry_percentages = {}
        
        if total_partners > 0:
            for industry, count in industry_counts.items():
                industry_percentages[industry] = count / total_partners
        
        return {
            "total_partners": total_partners,
            "industry_counts": industry_counts,
            "industry_percentages": industry_percentages,
            "other_industries": other_industries
        }
    
    def identify_gaps(self, current_partners: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify gaps in the current partnership portfolio
        
        Args:
            current_partners: List of current partner data
            
        Returns:
            Analysis of partnership gaps and opportunities
        """
        # Analyze current partners
        current_analysis = self.analyze_current_partners(current_partners)
        
        # Identify industry gaps
        industry_gaps = {}
        for industry, benchmark in self.industry_benchmarks.items():
            current_percentage = current_analysis["industry_percentages"].get(industry, 0)
            gap = benchmark - current_percentage
            
            if gap > 0:
                industry_gaps[industry] = {
                    "current_percentage": current_percentage,
                    "benchmark_percentage": benchmark,
                    "gap": gap,
                    "opportunity_score": gap * 10  # Scale to 0-10
                }
        
        # Sort gaps by opportunity score
        sorted_gaps = sorted(
            industry_gaps.items(),
            key=lambda x: x[1]["opportunity_score"],
            reverse=True
        )
        
        # Identify partnership type gaps
        partnership_type_counts = {ptype: 0 for ptype in self.partnership_types}
        for partner in current_partners:
            ptype = partner.get("partnership_type", "Unknown")
            if ptype in partnership_type_counts:
                partnership_type_counts[ptype] += 1
        
        # Create recommendations
        recommendations = []
        for industry, gap_data in sorted_gaps[:3]:  # Top 3 opportunities
            recommendations.append({
                "industry": industry,
                "opportunity_score": gap_data["opportunity_score"],
                "recommendation": f"Pursue partnerships in the {industry} sector to address significant gap of {gap_data['gap']:.1%}"
            })
        
        return {
            "current_analysis": current_analysis,
            "industry_gaps": dict(sorted_gaps),
            "partnership_type_distribution": partnership_type_counts,
            "top_recommendations": recommendations
        }
    
    def generate_gap_visualization(self, gap_analysis: Dict[str, Any], output_dir: str = "."):
        """
        Generate visualizations of partnership gaps
        
        Args:
            gap_analysis: The gap analysis data
            output_dir: Directory to save visualizations
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create industry gap chart
        plt.figure(figsize=(12, 8))
        
        industries = []
        current = []
        benchmark = []
        
        for industry, data in gap_analysis["industry_gaps"].items():
            industries.append(industry)
            current.append(data["current_percentage"] * 100)
            benchmark.append(data["benchmark_percentage"] * 100)
        
        x = range(len(industries))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], current, width, label='Current %')
        plt.bar([i + width/2 for i in x], benchmark, width, label='Benchmark %')
        
        plt.xlabel('Industry')
        plt.ylabel('Percentage of Partnerships')
        plt.title('Partnership Gaps by Industry')
        plt.xticks(x, industries, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        
        # Save the chart
        plt.savefig(os.path.join(output_dir, "partnership_gaps.png"))
        plt.close()
        
        # Create opportunity score chart
        plt.figure(figsize=(10, 6))
        
        industries = []
        scores = []
        
        for industry, data in gap_analysis["industry_gaps"].items():
            industries.append(industry)
            scores.append(data["opportunity_score"])
        
        # Sort by score
        sorted_data = sorted(zip(industries, scores), key=lambda x: x[1], reverse=True)
        sorted_industries, sorted_scores = zip(*sorted_data) if sorted_data else ([], [])
        
        plt.barh(range(len(sorted_industries)), sorted_scores, align='center')
        plt.yticks(range(len(sorted_industries)), sorted_industries)
        plt.xlabel('Opportunity Score')
        plt.title('Partnership Opportunity Scores by Industry')
        plt.tight_layout()
        
        # Save the chart
        plt.savefig(os.path.join(output_dir, "opportunity_scores.png"))
        plt.close()

def create_gap_identification_agent():
    """Create the Gap Identification Agent"""
    
    gap_identification_agent = Agent(
        role="Gap Identification Agent",
        goal="Analyze research data to identify gaps and opportunities in current partnerships",
        backstory="You are a strategic analyst specialized in identifying partnership gaps and opportunities. With your expertise in market trends and industry analysis, you excel at comparing current partner portfolios against industry benchmarks to highlight missing partnership categories.",
        verbose=True
    )
    
    return gap_identification_agent

def example_gap_analysis():
    """Example of how the Gap Identification Agent might analyze partnership data"""
    
    # Sample current partners (in a real system, this would come from the Partner Knowledge Agent)
    sample_current_partners = [
        {
            "name": "Scotia Bank",
            "industry": "Financial Services",
            "partnership_type": "Naming Rights",
            "partnership_start": "2018-07-01",
            "annual_value": "$8M"
        },
        {
            "name": "Rogers Communications",
            "industry": "Telecommunications",
            "partnership_type": "Media Partner",
            "partnership_start": "2015-01-15",
            "annual_value": "$12M"
        },
        {
            "name": "Bell Canada",
            "industry": "Telecommunications",
            "partnership_type": "Official Partner",
            "partnership_start": "2017-03-22",
            "annual_value": "$5M"
        },
        {
            "name": "Nike",
            "industry": "Apparel & Sportswear",
            "partnership_type": "Jersey Sponsor",
            "partnership_start": "2016-09-01",
            "annual_value": "$7M"
        },
        {
            "name": "Coca-Cola",
            "industry": "Food & Beverage",
            "partnership_type": "Official Partner",
            "partnership_start": "2019-05-10",
            "annual_value": "$4M"
        },
        {
            "name": "Molson Canadian",
            "industry": "Food & Beverage",
            "partnership_type": "Official Partner",
            "partnership_start": "2018-10-15",
            "annual_value": "$3.5M"
        }
    ]
    
    # Create analyzer
    analyzer = PartnershipGapAnalyzer()
    
    # Perform gap analysis
    gap_analysis = analyzer.identify_gaps(sample_current_partners)
    
    # Generate visualizations
    analyzer.generate_gap_visualization(gap_analysis, output_dir="gap_analysis_output")
    
    return gap_analysis

if __name__ == "__main__":
    # Run the example
    print("\n========================")
    print("GAP IDENTIFICATION ANALYSIS")
    print("========================\n")
    
    analysis_results = example_gap_analysis()
    
    # Print current partnership analysis
    current = analysis_results["current_analysis"]
    print(f"Current Partners: {current['total_partners']}")
    print("\nIndustry Distribution:")
    for industry, count in current["industry_counts"].items():
        if count > 0:
            percentage = current["industry_percentages"][industry] * 100
            print(f"  - {industry}: {count} partners ({percentage:.1f}%)")
    
    # Print gap analysis
    print("\nPartnership Gaps:")
    for industry, data in analysis_results["industry_gaps"].items():
        print(f"  - {industry}:")
        print(f"    Current: {data['current_percentage']*100:.1f}%")
        print(f"    Benchmark: {data['benchmark_percentage']*100:.1f}%")
        print(f"    Gap: {data['gap']*100:.1f}%")
        print(f"    Opportunity Score: {data['opportunity_score']:.1f}/10")
    
    # Print recommendations
    print("\nTop Recommendations:")
    for i, rec in enumerate(analysis_results["top_recommendations"], 1):
        print(f"{i}. {rec['recommendation']} (Score: {rec['opportunity_score']:.1f}/10)")
    
    print("\nVisualizations saved to 'gap_analysis_output' directory")
    
    print("\n========================")
    print("In the full MLSE Partnership Crew system:")
    print("1. The Partner Knowledge Agent would provide current partner data")
    print("2. The Gap Identification Agent would analyze this data to identify opportunities")
    print("3. The Research Agent would then focus on researching potential partners in gap areas")
    print("4. The Partner Fit Score Agent would evaluate these potential partners")
    print("========================")