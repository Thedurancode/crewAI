from crewai import Agent
import json
import os
from typing import Dict, List, Any
import hashlib
import datetime

class PartnershipDataManager:
    """
    A utility class to manage partnership research data
    
    This class demonstrates how the Data Management Agent might handle
    data verification, deduplication, and storage.
    """
    
    def __init__(self, data_dir="partnership_data"):
        """
        Initialize the data manager
        
        Args:
            data_dir: Directory to store partnership data
        """
        self.data_dir = data_dir
        self.partners_file = os.path.join(data_dir, "partners.json")
        self.research_file = os.path.join(data_dir, "research_data.json")
        self.history_file = os.path.join(data_dir, "data_history.json")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Initialize data files if they don't exist
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Initialize data files with empty structures if they don't exist"""
        if not os.path.exists(self.partners_file):
            with open(self.partners_file, 'w') as f:
                json.dump({"current_partners": [], "potential_partners": []}, f, indent=2)
        
        if not os.path.exists(self.research_file):
            with open(self.research_file, 'w') as f:
                json.dump({"research_entries": []}, f, indent=2)
        
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump({"history": []}, f, indent=2)
    
    def _generate_data_hash(self, data: Dict) -> str:
        """
        Generate a hash for data to check for duplicates
        
        Args:
            data: The data to hash
            
        Returns:
            A hash string representing the data
        """
        # Create a stable string representation of the data
        data_str = json.dumps(data, sort_keys=True)
        # Generate hash
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _log_data_change(self, operation: str, data_type: str, data_id: str):
        """
        Log data changes to history
        
        Args:
            operation: The operation performed (add, update, delete)
            data_type: The type of data (partner, research)
            data_id: Identifier for the data
        """
        with open(self.history_file, 'r') as f:
            history_data = json.load(f)
        
        history_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "operation": operation,
            "data_type": data_type,
            "data_id": data_id
        }
        
        history_data["history"].append(history_entry)
        
        with open(self.history_file, 'w') as f:
            json.dump(history_data, f, indent=2)
    
    def add_partner(self, partner_data: Dict[str, Any], is_current: bool = False) -> Dict[str, Any]:
        """
        Add a partner to the database
        
        Args:
            partner_data: Partner information
            is_current: Whether this is a current partner (True) or potential partner (False)
            
        Returns:
            The added partner data with status information
        """
        # Verify required fields
        required_fields = ["name", "industry"]
        for field in required_fields:
            if field not in partner_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Load existing data
        with open(self.partners_file, 'r') as f:
            partners_data = json.load(f)
        
        # Check for duplicates
        partner_list_key = "current_partners" if is_current else "potential_partners"
        partner_list = partners_data[partner_list_key]
        
        # Generate a unique ID if not provided
        if "id" not in partner_data:
            partner_data["id"] = self._generate_data_hash(partner_data)
        
        # Check if partner already exists
        for existing_partner in partner_list:
            if existing_partner["name"] == partner_data["name"]:
                return {
                    "status": "error",
                    "message": f"Partner '{partner_data['name']}' already exists",
                    "data": existing_partner
                }
        
        # Add metadata
        partner_data["added_date"] = datetime.datetime.now().isoformat()
        partner_data["last_updated"] = partner_data["added_date"]
        
        # Add to appropriate list
        partner_list.append(partner_data)
        
        # Save updated data
        with open(self.partners_file, 'w') as f:
            json.dump(partners_data, f, indent=2)
        
        # Log the change
        self._log_data_change("add", "partner", partner_data["id"])
        
        return {
            "status": "success",
            "message": f"Added {partner_list_key.replace('_', ' ')} '{partner_data['name']}'",
            "data": partner_data
        }
    
    def add_research_data(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add research data to the database
        
        Args:
            research_data: Research information
            
        Returns:
            The added research data with status information
        """
        # Verify required fields
        required_fields = ["partner_id", "source", "data"]
        for field in required_fields:
            if field not in research_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Load existing data
        with open(self.research_file, 'r') as f:
            all_research_data = json.load(f)
        
        # Generate a hash for deduplication
        data_hash = self._generate_data_hash(research_data["data"])
        
        # Check for duplicates
        for entry in all_research_data["research_entries"]:
            if self._generate_data_hash(entry["data"]) == data_hash:
                return {
                    "status": "error",
                    "message": "Duplicate research data detected",
                    "data": entry
                }
        
        # Add metadata
        research_data["id"] = data_hash
        research_data["added_date"] = datetime.datetime.now().isoformat()
        
        # Add to research entries
        all_research_data["research_entries"].append(research_data)
        
        # Save updated data
        with open(self.research_file, 'w') as f:
            json.dump(all_research_data, f, indent=2)
        
        # Log the change
        self._log_data_change("add", "research", research_data["id"])
        
        return {
            "status": "success",
            "message": "Added new research data",
            "data": research_data
        }
    
    def get_partner_by_id(self, partner_id: str) -> Dict[str, Any]:
        """
        Get partner data by ID
        
        Args:
            partner_id: The partner ID to look up
            
        Returns:
            The partner data if found
        """
        with open(self.partners_file, 'r') as f:
            partners_data = json.load(f)
        
        # Search in both current and potential partners
        for partner_type in ["current_partners", "potential_partners"]:
            for partner in partners_data[partner_type]:
                if partner.get("id") == partner_id:
                    return {
                        "status": "success",
                        "data": partner,
                        "partner_type": partner_type
                    }
        
        return {
            "status": "error",
            "message": f"Partner with ID '{partner_id}' not found"
        }
    
    def get_research_for_partner(self, partner_id: str) -> Dict[str, Any]:
        """
        Get all research data for a specific partner
        
        Args:
            partner_id: The partner ID to look up
            
        Returns:
            All research entries for the partner
        """
        with open(self.research_file, 'r') as f:
            research_data = json.load(f)
        
        partner_research = [
            entry for entry in research_data["research_entries"]
            if entry["partner_id"] == partner_id
        ]
        
        return {
            "status": "success",
            "partner_id": partner_id,
            "research_count": len(partner_research),
            "research_entries": partner_research
        }
    
    def get_data_history(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get data operation history
        
        Args:
            limit: Maximum number of history entries to return
            
        Returns:
            Recent history entries
        """
        with open(self.history_file, 'r') as f:
            history_data = json.load(f)
        
        # Get the most recent entries
        recent_entries = history_data["history"][-limit:] if history_data["history"] else []
        
        return {
            "status": "success",
            "count": len(recent_entries),
            "history": recent_entries
        }

def create_data_management_agent():
    """Create the Data Management Agent"""
    
    data_management_agent = Agent(
        role="Data Management Agent",
        goal="Handle viewing, verifying, and saving research data to the database while preventing duplicates",
        backstory="You are an expert in data management systems with a focus on data integrity and organization. Your specialized skills allow you to verify data consistency, prevent duplicate entries, and maintain well-structured databases.",
        verbose=True
    )
    
    return data_management_agent

def example_data_management():
    """Example of how the Data Management Agent might handle partnership data"""
    
    # Create data manager
    data_manager = PartnershipDataManager(data_dir="example_partnership_data")
    
    # Example 1: Add current partners
    current_partners = [
        {
            "name": "Scotia Bank",
            "industry": "Financial Services",
            "partnership_type": "Arena Naming Rights",
            "partnership_start": "2018-07-01",
            "annual_value": "$8M",
            "contact_info": {
                "name": "Jane Smith",
                "email": "jane.smith@scotiabank.com"
            }
        },
        {
            "name": "Rogers Communications",
            "industry": "Telecommunications",
            "partnership_type": "Media Rights",
            "partnership_start": "2015-01-15",
            "annual_value": "$12M",
            "contact_info": {
                "name": "John Rogers",
                "email": "john.rogers@rogers.com"
            }
        }
    ]
    
    print("\n=== Adding Current Partners ===\n")
    for partner in current_partners:
        result = data_manager.add_partner(partner, is_current=True)
        print(f"{result['status'].upper()}: {result['message']}")
    
    # Example 2: Add potential partners
    potential_partners = [
        {
            "name": "TechCorp Inc.",
            "industry": "Technology",
            "potential_value": "$3-5M",
            "partnership_category": "Technology Partner",
            "notes": "Interested in innovation showcase opportunities"
        },
        {
            "name": "HealthFit Co.",
            "industry": "Health & Fitness",
            "potential_value": "$2-4M",
            "partnership_category": "Wellness Partner",
            "notes": "Looking for fan engagement opportunities"
        }
    ]
    
    print("\n=== Adding Potential Partners ===\n")
    for partner in potential_partners:
        result = data_manager.add_partner(partner, is_current=False)
        print(f"{result['status'].upper()}: {result['message']}")
    
    # Example 3: Add research data
    # First, get a partner ID
    with open(os.path.join(data_manager.data_dir, "partners.json"), 'r') as f:
        partners_data = json.load(f)
    
    if partners_data["potential_partners"]:
        partner_id = partners_data["potential_partners"][0]["id"]
        
        # Add research data for this partner
        research_entries = [
            {
                "partner_id": partner_id,
                "source": "EXA API Search",
                "search_query": "TechCorp Inc. sponsorship history",
                "data": {
                    "annual_revenue": "$5.2B",
                    "market_position": "Industry leader in consumer tech",
                    "previous_sponsorships": [
                        "NBA Team (2018-2021)",
                        "European Soccer League (2019-Present)"
                    ],
                    "recent_news": "Launching new product line in Q3 2025"
                }
            },
            {
                "partner_id": partner_id,
                "source": "Financial Database",
                "search_query": "TechCorp Inc. financial health",
                "data": {
                    "credit_rating": "AA",
                    "stock_performance": "+15% YTD",
                    "profit_margin": "22%",
                    "growth_forecast": "Positive"
                }
            }
        ]
        
        print("\n=== Adding Research Data ===\n")
        for entry in research_entries:
            result = data_manager.add_research_data(entry)
            print(f"{result['status'].upper()}: {result['message']}")
        
        # Example 4: Retrieve research for a partner
        print("\n=== Retrieving Partner Research ===\n")
        research_result = data_manager.get_research_for_partner(partner_id)
        print(f"Found {research_result['research_count']} research entries for partner")
    
    # Example 5: View data history
    print("\n=== Data Operation History ===\n")
    history_result = data_manager.get_data_history(limit=10)
    print(f"Recent operations: {history_result['count']}")
    for entry in history_result['history']:
        print(f"- {entry['timestamp']}: {entry['operation']} {entry['data_type']} ({entry['data_id']})")

if __name__ == "__main__":
    # Run the example
    print("\n========================")
    print("DATA MANAGEMENT EXAMPLE")
    print("========================\n")
    
    example_data_management()
    
    print("\n========================")
    print("In the full MLSE Partnership Crew system:")
    print("1. The Research Agent would gather data from various sources")
    print("2. The Data Management Agent would verify and store this data")
    print("3. Other agents would access this data for analysis and presentations")
    print("========================")