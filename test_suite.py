"""
Test suite for transaction categorization API.

Tests the Groq API integration with real transactions.
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:8000/api/categorize/"

# Test data
TEST_CASES = [
    {
        "name": "AWS Subscription",
        "data": {
            "description": "AWS monthly cloud subscription",
            "vendor": "Amazon Web Services",
            "industry": "Technology",
            "company_id": "TECH-001",
            "amount": 1500.00,
            "chart_of_accounts": [
                "Software & Subscriptions",
                "Utilities",
                "Office Supplies",
                "Travel & Entertainment"
            ],
            "historical_transactions": [
                {
                    "description": "GitHub Pro subscription",
                    "category": "Software & Subscriptions"
                }
            ]
        }
    },
    {
        "name": "Office Chair Purchase",
        "data": {
            "description": "Ergonomic office chair from Herman Miller",
            "vendor": "Herman Miller",
            "industry": "Furniture",
            "company_id": "FURN-001",
            "amount": 1200.00,
            "chart_of_accounts": [
                "Software & Subscriptions",
                "Office Supplies",
                "Travel & Entertainment",
                "Utilities"
            ],
            "historical_transactions": [
                {
                    "description": "Office desk purchase",
                    "category": "Office Supplies"
                }
            ]
        }
    },
    {
        "name": "Client Dinner",
        "data": {
            "description": "Client entertainment dinner at upscale restaurant",
            "vendor": "The Capital Grille",
            "industry": "Restaurant",
            "company_id": "REST-001",
            "amount": 450.00,
            "chart_of_accounts": [
                "Software & Subscriptions",
                "Office Supplies",
                "Travel & Entertainment",
                "Utilities"
            ],
            "historical_transactions": [
                {
                    "description": "Team lunch at cafe",
                    "category": "Travel & Entertainment"
                }
            ]
        }
    },
    {
        "name": "Electricity Bill",
        "data": {
            "description": "Monthly electricity bill for office building",
            "vendor": "City Power Company",
            "industry": "Utilities",
            "company_id": "UTIL-001",
            "amount": 800.00,
            "chart_of_accounts": [
                "Software & Subscriptions",
                "Office Supplies",
                "Travel & Entertainment",
                "Utilities"
            ],
            "historical_transactions": [
                {
                    "description": "Water bill payment",
                    "category": "Utilities"
                }
            ]
        }
    }
]


def run_tests():
    """Run all test cases against the API."""
    print("=" * 80)
    print("TRANSACTION CATEGORIZATION TEST SUITE".center(80))
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"[Test {i}] {test_case['name']}")
        print("-" * 80)
        
        try:
            # Make API request
            response = requests.post(
                API_URL,
                json=test_case['data'],
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Print result
                print(f"✓ Status: SUCCESS")
                print(f"  Category: {result.get('suggested_category')}")
                print(f"  Confidence: {result.get('confidence_score')}")
                print(f"  Reasoning: {result.get('reasoning')}")
                
                # Print alternatives
                alternatives = result.get('alternatives', [])
                if alternatives:
                    alt_str = ', '.join([f"{alt['category']} ({alt['confidence']})" for alt in alternatives])
                    print(f"  Alternatives: {alt_str}")
                
                passed += 1
            else:
                print(f"✗ Error: HTTP {response.status_code}")
                print(f"  Response: {response.text}")
                failed += 1
        
        except requests.exceptions.ConnectionError:
            print(f"✗ Error: Could not connect to API at {API_URL}")
            print("  Make sure Django server is running: python manage.py runserver")
            failed += 1
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            failed += 1
        
        print()
    
    # Summary
    print("=" * 80)
    print("TEST SUITE COMPLETE".center(80))
    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(TEST_CASES)} tests")
    print()
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
