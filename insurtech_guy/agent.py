# ============================================
# 🤖 THE INSURTECH GUY - AI-POWERED INSURANCE CONCIERGE
# ============================================
# Google ADK Agents Intensive Capstone Project
# Author: Hazem Abdallah
# ============================================

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search
from google.genai import types
from typing import List

# ============================================
# RETRY CONFIGURATION
# ============================================
# Handles API rate limits and transient errors

retry_config = types.HttpRetryOptions(
    attempts=5,          # Maximum retry attempts
    exp_base=7,          # Delay multiplier
    initial_delay=1,     # Initial delay in seconds
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

# ============================================
# 1. INSURERS DATA
# ============================================
# 5 major US auto insurers with different pricing multipliers
# and available add-on packages

INSURERS = {
    "GEICO": {
        "name": "GEICO",
        "multiplier": 0.95,  # Budget-friendly pricing
        "reputation": "Budget-friendly, fast quotes",
        "available_add_ons": ["roadside_assistance", "rental_car"],
        "special_features": []
    },
    "Progressive": {
        "name": "Progressive",
        "multiplier": 0.98,
        "reputation": "Innovative, name-your-price",
        "available_add_ons": ["roadside_assistance", "rental_car", "accident_forgiveness"],
        "special_features": []
    },
    "StateFarm": {
        "name": "StateFarm",
        "multiplier": 1.0,  # Baseline pricing
        "reputation": "Like a good neighbor, reliable",
        "available_add_ons": ["roadside_assistance", "rental_car", "gap_insurance", "accident_forgiveness"],
        "special_features": []
    },
    "Allstate": {
        "name": "Allstate",
        "multiplier": 1.05,
        "reputation": "You're in good hands",
        "available_add_ons": ["roadside_assistance", "gap_insurance", "accident_forgiveness"],
        "special_features": []
    },
    "Travelers": {
        "name": "Travelers",
        "multiplier": 1.08,  # Premium pricing
        "reputation": "Premium service, established since 1853",
        "available_add_ons": ["roadside_assistance", "rental_car", "gap_insurance", "accident_forgiveness", "oem_parts_guarantee"],
        "special_features": ["concierge_claims_service"]
    }
}

# ============================================
# 2. COVERAGE TIERS
# ============================================
# Three levels of coverage with different price points

COVERAGE_TIERS = {
    "liability": {
        "name": "Liability Only",
        "price_multiplier": 0.30,  # 30% of standard price
        "minimum_annual": 700,     # Minimum $700/year
        "includes": ["Bodily Injury Liability", "Property Damage Liability"]
    },
    "standard": {
        "name": "Standard Coverage",
        "price_multiplier": 1.0,
        "minimum_annual": 2000,    # Minimum $2,000/year
        "includes": ["Bodily Injury Liability", "Property Damage Liability", 
                     "Collision Coverage", "Comprehensive Coverage", "Uninsured Motorist"]
    },
    "premium": {
        "name": "Premium Coverage",
        "price_multiplier": 1.0,
        "minimum_annual": 2500,    # Minimum $2,500/year
        "includes": ["Everything in Standard", "Plus selected add-ons"]
    }
}

# ============================================
# 3. ADD-ONS
# ============================================
# Optional coverage add-ons with annual costs

ADD_ONS = {
    "roadside_assistance": {"name": "Roadside Assistance", "annual_cost": 50},
    "rental_car": {"name": "Rental Car Coverage", "annual_cost": 75},
    "gap_insurance": {"name": "Gap Insurance", "annual_cost": 100},
    "accident_forgiveness": {"name": "Accident Forgiveness", "annual_cost": 150},
    "oem_parts_guarantee": {"name": "OEM Parts Guarantee", "annual_cost": 75},
    "concierge_claims": {"name": "Concierge Claims Service", "annual_cost": 0}  # Free with Travelers Premium
}

# ============================================
# 4. PRICING PARAMETERS
# ============================================
# Base rates by car brand category (percentage of car value)

BRAND_RATES = {
    "american": 0.05,   # 5% - Ford, Chevy, etc.
    "japanese": 0.055,  # 5.5% - Toyota, Honda, etc.
    "german": 0.06,     # 6% - BMW, Mercedes, etc.
    "other": 0.065      # 6.5% - All other brands
}

# Car brand to category mapping
CAR_BRANDS = {
    "american": ["Ford", "Chevrolet", "Chevy", "Dodge", "GMC", "Jeep", 
                 "Cadillac", "Lincoln", "Buick", "Chrysler", "Ram"],
    "japanese": ["Toyota", "Honda", "Nissan", "Mazda", "Subaru", 
                 "Lexus", "Acura", "Infiniti", "Mitsubishi"],
    "german": ["BMW", "Mercedes", "Mercedes-Benz", "Audi", 
               "Volkswagen", "VW", "Porsche", "Mini"]
    # Any brand not listed above defaults to "other" category
}

# Age-based risk adjustments
AGE_ADJUSTMENT = {
    "18-25": 1.15,   # +15% for young drivers
    "26-60": 1.0,    # Standard rate
    "60+": 0.90      # -10% for experienced seniors
}

# License experience adjustments
EXPERIENCE_ADJUSTMENT = {
    "0-2": 1.20,     # +20% for new drivers
    "3-5": 1.10,     # +10% for newer drivers
    "5+": 1.0        # Standard rate for experienced
}

# ============================================
# 5. HELPER FUNCTIONS
# ============================================

def get_brand_category(brand: str) -> str:
    """
    Determine the category of a car brand for pricing.
    Returns 'american', 'japanese', 'german', or 'other'.
    """
    brand_lower = brand.lower().strip()
    for category, brands in CAR_BRANDS.items():
        if any(b.lower() == brand_lower for b in brands):
            return category
    return "other"  # Default for unlisted brands


def get_age_bracket(age: int) -> str:
    """Determine age bracket for risk adjustment."""
    if age < 18:
        return None
    elif age <= 25:
        return "18-25"
    elif age <= 60:
        return "26-60"
    else:
        return "60+"


def get_experience_bracket(years: int) -> str:
    """Determine license experience bracket for risk adjustment."""
    if years < 0:
        return None
    elif years <= 2:
        return "0-2"
    elif years <= 5:
        return "3-5"
    else:
        return "5+"


def get_addon_names(insurer_name: str) -> list:
    """Get list of add-on names available for an insurer."""
    insurer = INSURERS.get(insurer_name)
    if not insurer:
        return []
    names = []
    for addon_id in insurer["available_add_ons"]:
        if addon_id in ADD_ONS:
            names.append(ADD_ONS[addon_id]["name"])
    if "concierge_claims_service" in insurer.get("special_features", []):
        names.append("Concierge Service (FREE)")
    return names


def get_addon_total(insurer_name: str) -> int:
    """Calculate total cost of all add-ons for an insurer."""
    insurer = INSURERS.get(insurer_name)
    if not insurer:
        return 0
    total = 0
    for addon_id in insurer["available_add_ons"]:
        if addon_id in ADD_ONS:
            total += ADD_ONS[addon_id]["annual_cost"]
    return total


def calculate_premium(car_brand: str, car_value: float, driver_age: int, 
                      license_years: int, insurer_name: str, tier: str = "standard") -> dict:
    """
    Calculate insurance premium based on all factors.
    
    Returns a dictionary with premium details or error message.
    """
    # Validate driver age
    if driver_age < 18:
        return {"error": "Driver must be at least 18 years old"}
    
    # Get brand category and base rate
    brand_category = get_brand_category(car_brand)
    base_rate = BRAND_RATES[brand_category]
    base_premium = car_value * base_rate
    
    # Apply age adjustment
    age_bracket = get_age_bracket(driver_age)
    age_multiplier = AGE_ADJUSTMENT[age_bracket]
    
    # Apply experience adjustment
    exp_bracket = get_experience_bracket(license_years)
    exp_multiplier = EXPERIENCE_ADJUSTMENT[exp_bracket]
    
    # Get insurer details
    insurer = INSURERS.get(insurer_name)
    if not insurer:
        return {"error": f"Unknown insurer: {insurer_name}"}
    insurer_multiplier = insurer["multiplier"]
    
    # Get tier details
    tier_info = COVERAGE_TIERS.get(tier)
    if not tier_info:
        return {"error": f"Unknown tier: {tier}"}
    
    # Calculate adjusted premium
    adjusted_premium = base_premium * age_multiplier * exp_multiplier * tier_info["price_multiplier"]
    
    # Apply minimum premium for tier
    adjusted_premium = max(adjusted_premium, tier_info["minimum_annual"])
    
    # Apply insurer multiplier
    final_premium = adjusted_premium * insurer_multiplier
    
    # Add add-ons for premium tier
    add_on_total = 0
    add_on_details = []
    
    if tier == "premium":
        add_on_total = get_addon_total(insurer_name)
        for addon_id in insurer["available_add_ons"]:
            if addon_id in ADD_ONS:
                addon = ADD_ONS[addon_id]
                add_on_details.append({"name": addon["name"], "cost": addon["annual_cost"]})
        if insurer_name == "Travelers":
            add_on_details.append({"name": "Concierge Claims Service", "cost": 0})
    
    final_premium += add_on_total
    
    return {
        "success": True,
        "insurer": insurer_name,
        "reputation": insurer["reputation"],
        "tier": tier,
        "tier_name": tier_info["name"],
        "brand_category": brand_category,
        "annual_premium": round(final_premium, 2),
        "monthly_premium": round(final_premium / 12, 2),
        "add_ons": add_on_details,
        "coverage_includes": tier_info["includes"]
    }

# ============================================
# 6. AGENT TOOLS
# ============================================
# These functions are exposed to the agent for use during conversation

def get_insurance_quotes(car_brand: str, car_value: float, driver_age: int, 
                         license_years: int, coverage_tier: str) -> dict:
    """
    Get car insurance quotes from all insurers.
    
    Args:
        car_brand: The brand of the car (e.g., Ford, Toyota, BMW)
        car_value: The value of the car in dollars
        driver_age: Age of the driver (must be 18+)
        license_years: Years the driver has held a license
        coverage_tier: "liability", "standard", "premium", or "all"
    
    Returns:
        Dictionary with quotes organized by tier
    """
    # Input validation
    if driver_age < 18:
        return {"error": "Driver must be at least 18 years old."}
    if car_value <= 0:
        return {"error": "Car value must be positive."}
    
    # Determine which tiers to calculate
    if coverage_tier.lower() == "all":
        tiers = ["liability", "standard", "premium"]
    elif coverage_tier.lower() in ["liability", "standard", "premium"]:
        tiers = [coverage_tier.lower()]
    else:
        return {"error": f"Unknown tier: {coverage_tier}"}
    
    # Calculate quotes for each tier
    results = {}
    for tier in tiers:
        quotes = []
        for insurer_name in INSURERS.keys():
            quote = calculate_premium(car_brand, car_value, driver_age, 
                                      license_years, insurer_name, tier)
            if quote.get("success"):
                quotes.append({
                    "insurer": quote["insurer"],
                    "reputation": quote["reputation"],
                    "annual_premium": quote["annual_premium"],
                    "monthly_premium": quote["monthly_premium"],
                    "add_ons": get_addon_names(quote["insurer"]) if tier == "premium" else []
                })
        # Sort by price
        quotes.sort(key=lambda x: x["annual_premium"])
        results[tier] = quotes
    
    return {
        "success": True, 
        "car_brand": car_brand, 
        "car_value": car_value, 
        "quotes": results
    }


def get_available_addons(insurer_name: str) -> dict:
    """
    Get available add-ons for a specific insurer.
    
    Args:
        insurer_name: Name of the insurer (GEICO, Progressive, StateFarm, Allstate, Travelers)
    
    Returns:
        List of available add-ons with costs
    """
    if insurer_name not in INSURERS:
        return {"error": f"Unknown insurer: {insurer_name}"}
    
    insurer = INSURERS[insurer_name]
    addons = []
    
    for addon_id in insurer["available_add_ons"]:
        if addon_id in ADD_ONS:
            addon = ADD_ONS[addon_id]
            addons.append({"name": addon["name"], "cost": addon["annual_cost"]})
    
    # Add special features
    if "concierge_claims_service" in insurer.get("special_features", []):
        addons.append({
            "name": "Concierge Claims Service", 
            "cost": 0, 
            "note": "FREE with Premium"
        })
    
    return {"insurer": insurer_name, "available_add_ons": addons}


def purchase_policy(insurer_name: str, coverage_tier: str, annual_premium: float,
                    car_brand: str, car_model: str, car_year: int, license_plate: str,
                    full_name: str, date_of_birth: str, address: str, 
                    phone: str, email: str, driver_license_number: str,
                    payment_method: str, policy_start_date: str) -> dict:
    """
    Complete purchase of an insurance policy (simulated).
    
    Args:
        insurer_name: Selected insurer
        coverage_tier: Selected tier (liability, standard, premium)
        annual_premium: Annual premium amount
        car_brand: Car brand
        car_model: Car model
        car_year: Car year
        license_plate: License plate number
        full_name: Customer full name
        date_of_birth: DOB (YYYY-MM-DD)
        address: Full address
        phone: Phone number
        email: Email address
        driver_license_number: Driver license number
        payment_method: credit_card, debit_card, or bank_transfer
        policy_start_date: Start date (YYYY-MM-DD)
    
    Returns:
        Policy confirmation with policy number
    """
    import random
    import string
    
    # Validate insurer
    if insurer_name not in INSURERS:
        return {"error": f"Unknown insurer: {insurer_name}"}
    
    # Generate policy number
    policy_number = f"{insurer_name[:3].upper()}-{''.join(random.choices(string.digits, k=8))}"
    
    return {
        "success": True,
        "message": "🎉 Policy purchased successfully!",
        "policy_number": policy_number,
        "insurer": insurer_name,
        "coverage": coverage_tier,
        "annual_premium": annual_premium,
        "monthly_premium": round(annual_premium / 12, 2),
        "vehicle": f"{car_year} {car_brand} {car_model}",
        "customer": full_name,
        "email": email,
        "start_date": policy_start_date
    }

# ============================================
# 7. SUB-AGENT FOR WEB SEARCH
# ============================================
# Specialized agent for searching insurer reviews and information

google_search_agent = LlmAgent(
    name="google_search_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Searches for information about insurance companies",
    instruction="""Use the google_search tool to find information about insurance companies.
    Search for reviews, ratings, and customer feedback about the specified insurer.
    Return the search results to help the customer make an informed decision.""",
    tools=[google_search]
)

# ============================================
# 8. ROOT AGENT
# ============================================
# Main conversational agent that orchestrates the insurance buying experience

root_agent = LlmAgent(
    name="insurtech_guy",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Expert auto insurance advisor with 34 years of experience",
    instruction="""You are THE INSURTECH GUY - an expert auto insurance advisor with 34 years of experience.

## YOUR ROLE
Help customers find car insurance from 5 insurers: GEICO, Progressive, StateFarm, Allstate, and Travelers.

## REQUIRED INFO FOR QUOTES
Before showing quotes, you need:
1. Car brand (Ford, Toyota, BMW, etc.)
2. Car value (dollar amount)
3. Driver age (must be 18+)
4. License years (how long they've had a license)

Listen naturally to what the customer shares. Ask only for missing info.

## COVERAGE TIERS
- Liability: ~30% of standard, minimum $700/year
- Standard: Full coverage, minimum $2,000/year  
- Premium: Standard + add-ons, minimum $2,500/year

## ADD-ONS
- Roadside Assistance: $50/year
- Rental Car: $75/year
- Gap Insurance: $100/year
- Accident Forgiveness: $150/year
- OEM Parts (Travelers only): $75/year
- Concierge Service (Travelers Premium): FREE

## TOOLS
- get_insurance_quotes: Get quotes from all insurers (pass coverage_tier as "all" to see all tiers)
- get_available_addons: Show add-ons for an insurer
- purchase_policy: Complete purchase (simulated)
- google_search_agent: Search for insurer reviews and reputation

## YOUR STYLE
- Friendly and helpful
- Simple language, no jargon
- Always use tools for real quotes - never make up numbers!
- When customer wants to know about an insurer's reputation, use google_search_agent

## PURCHASE FLOW
When customer selects an offer, collect:
- Full name, date of birth, address
- Phone, email
- Driver license number
- Car model, year, license plate
- Payment method (credit_card, debit_card, bank_transfer)
- Policy start date (YYYY-MM-DD)

Then use purchase_policy tool to complete.
""",
    tools=[
        AgentTool(agent=google_search_agent), 
        get_insurance_quotes, 
        get_available_addons, 
        purchase_policy
    ]
)

# ============================================
# 9. MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("🚗 THE INSURTECH GUY - AI-Powered Insurance Concierge")
    print("=" * 60)
    print("\nAgent ready! Use 'adk web' to start the web UI.")
    print("\nCapabilities:")
    print("  • Multi-agent architecture (root + search sub-agent)")
    print("  • Custom tools (quotes, add-ons, purchase)")
    print("  • Real-time insurer research via Google Search")
    print("  • Dynamic pricing based on 8 factors")
    print("=" * 60)
