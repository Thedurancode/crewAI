from crewai import Agent
from typing import Dict, List, Any, Tuple
import re

class PromptRefiner:
    """
    A utility class to refine search prompts and queries
    
    This class demonstrates how the Prompt Refinement Agent might
    optimize search queries to improve research outcomes.
    """
    
    def __init__(self):
        """Initialize the prompt refiner with optimization strategies"""
        
        # Define common search operators for different search engines
        self.search_operators = {
            "exact_match": '"{}',  # Exact phrase matching
            "exclude": '-{}',      # Exclude term
            "site": 'site:{}',     # Limit to specific site
            "filetype": 'filetype:{}',  # Limit to specific file type
            "date_range": 'after:{} before:{}',  # Date range
            "or": '{} OR {}',      # OR operator
            "intitle": 'intitle:{}',  # Term in title
        }
        
        # Define industry-specific terminology for partnerships
        self.partnership_terms = {
            "general": ["partnership", "sponsorship", "collaboration", "alliance", "sponsor"],
            "sports": ["sports sponsorship", "team sponsor", "arena naming rights", "jersey sponsor", 
                      "official partner", "sports marketing", "fan engagement"],
            "financial": ["financial services partner", "banking partner", "payment partner", 
                         "financial sponsor", "credit card partner"],
            "technology": ["technology partner", "tech sponsor", "innovation partner", 
                          "digital transformation", "tech alliance"],
            "media": ["media rights", "broadcast partner", "streaming partner", 
                     "content partnership", "media sponsor"]
        }
        
        # Define quality indicators for search results
        self.quality_indicators = {
            "relevance": ["partnership details", "sponsorship agreement", "deal terms", 
                         "partnership announcement", "sponsor agreement"],
            "recency": ["recent", "new", "announced", "latest", "updated"],
            "specificity": ["specific terms", "contract details", "partnership value", 
                           "agreement length", "specific benefits"]
        }
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze a search query to identify its components and potential issues
        
        Args:
            query: The search query to analyze
            
        Returns:
            Analysis of the query components and potential improvements
        """
        # Identify query components
        components = {
            "length": len(query),
            "word_count": len(query.split()),
            "has_quotes": '"' in query,
            "has_operators": any(op in query for op in ['-', 'site:', 'filetype:', 'intitle:']),
            "industry_terms": [],
            "partnership_terms": []
        }
        
        # Check for industry terms
        for term in self.partnership_terms["general"]:
            if term.lower() in query.lower():
                components["partnership_terms"].append(term)
        
        # Identify potential issues
        issues = []
        if components["word_count"] < 3:
            issues.append("Query is too short and may return overly broad results")
        if not components["has_quotes"] and components["word_count"] > 3:
            issues.append("Consider using quotes for key phrases to improve precision")
        if not components["has_operators"]:
            issues.append("Query lacks search operators that could improve results")
        if not components["partnership_terms"]:
            issues.append("Query lacks specific partnership-related terminology")
        
        return {
            "query": query,
            "components": components,
            "potential_issues": issues
        }
    
    def evaluate_results(self, results: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Evaluate search results to identify quality and relevance issues
        
        Args:
            results: List of search results (title, snippet, url)
            
        Returns:
            Evaluation of result quality and relevance
        """
        # Count quality indicators in results
        quality_counts = {category: 0 for category in self.quality_indicators}
        
        # Track relevance of each result
        result_relevance = []
        
        for result in results:
            # Combine title and snippet for analysis
            content = (result.get("title", "") + " " + result.get("snippet", "")).lower()
            
            # Check for quality indicators
            result_quality = {}
            for category, indicators in self.quality_indicators.items():
                category_matches = sum(1 for ind in indicators if ind.lower() in content)
                quality_counts[category] += category_matches
                result_quality[category] = category_matches > 0
            
            # Check for partnership terms
            partnership_relevance = 0
            for term_list in self.partnership_terms.values():
                for term in term_list:
                    if term.lower() in content:
                        partnership_relevance += 1
            
            # Calculate overall relevance score (0-10)
            relevance_score = min(10, (partnership_relevance * 2) + 
                                 (result_quality["relevance"] * 3) + 
                                 (result_quality["specificity"] * 3) + 
                                 (result_quality["recency"] * 2))
            
            result_relevance.append({
                "title": result.get("title", ""),
                "relevance_score": relevance_score,
                "quality_indicators": result_quality
            })
        
        # Calculate average relevance
        avg_relevance = sum(r["relevance_score"] for r in result_relevance) / len(result_relevance) if result_relevance else 0
        
        # Identify result issues
        result_issues = []
        if avg_relevance < 5:
            result_issues.append("Results have low overall relevance to partnership research")
        if quality_counts["specificity"] < len(results) * 0.3:
            result_issues.append("Results lack specific partnership details")
        if quality_counts["recency"] < len(results) * 0.3:
            result_issues.append("Results may not include recent partnership information")
        
        return {
            "result_count": len(results),
            "average_relevance": avg_relevance,
