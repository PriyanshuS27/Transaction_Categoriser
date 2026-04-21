# Transaction Categorization Service

An AI-powered Django REST API that automatically categorizes financial transactions into accounting categories using **Groq API** with **Llama 3.1 8B** LLM.

## Project Overview

This service accepts financial transaction details and uses the Groq API (fast, efficient LLM inference) to suggest the most appropriate accounting category from a provided chart of accounts. It provides confidence scores, reasoning, and alternative suggestions to support accounting workflows.

**Key Features:**
- ✅ **Groq API Integration** - Fast LLM inference (Llama 3.1 8B)
- ✅ **Intelligent Categorization** - AI-powered financial classification
- ✅ **Confidence Scoring** - Quantified certainty with reasoning
- ✅ **Few-Shot Learning** - Historical transaction context
- ✅ **Production-Ready** - Retry logic, error handling, logging
- ✅ **Type Safety** - Full type hints throughout
- ✅ **Comprehensive Tests** - Unit tests and integration tests
- ✅ **No Database** - Stateless, scalable API

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- **Groq API key** (free tier available at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone or navigate to the project directory:**

```bash
cd c:\Users\Admin\PythonProjects\App_Deft_Assignment\transaction_categorizer
```

2. **Create a Python virtual environment:**

```bash
python -m venv venv
```

3. **Activate the virtual environment:**

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Or Windows Command Prompt
venv\Scripts\activate.bat
```

4. **Install dependencies:**

```bash
pip install -r requirements.txt
```

5. **Create .env file from .env.example:**

```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your Groq API key
# Open .env in your editor and replace:
# GROQ_API_KEY=your_api_key_here
# with your actual Groq API key from https://console.groq.com
```

6. **Create logs directory (for logging):**

```bash
mkdir logs
```

## Running the Server

1. **Run the development server:**

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

2. **Verify the server is running:**

```bash
curl http://localhost:8000/api/categorize/ -X OPTIONS
```

## API Endpoint Documentation

### Endpoint: POST /api/categorize/

Categorizes a financial transaction into an accounting category using AI analysis.

### Request Headers

```
Content-Type: application/json
```

### Request Body

```json
{
  "description": "Paid for AWS server subscription",
  "vendor": "Amazon Web Services",
  "amount": 15000.00,
  "company_id": "C001",
  "industry": "IT Services",
  "chart_of_accounts": [
    "Office Supplies",
    "Software & Subscriptions",
    "Travel & Entertainment",
    "Payroll",
    "Marketing",
    "Utilities",
    "Professional Services"
  ],
  "historical_transactions": [
    {
      "description": "GitHub Pro subscription",
      "category": "Software & Subscriptions"
    },
    {
      "description": "Zoom monthly plan",
      "category": "Software & Subscriptions"
    },
    {
      "description": "Team lunch at restaurant",
      "category": "Travel & Entertainment"
    }
  ]
}
```

### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | String | Yes | Transaction description (max 1000 chars) |
| `vendor` | String | Yes | Vendor or payee name (max 200 chars) |
| `amount` | Decimal | No | Transaction amount |
| `company_id` | String | Yes | Company identifier (max 100 chars) |
| `industry` | String | Yes | Company industry (max 100 chars) |
| `chart_of_accounts` | Array | Yes | List of valid account categories (non-empty) |
| `historical_transactions` | Array | No | Previous transactions for context |

### Response Body (Success - 200)

```json
{
  "suggested_category": "Software & Subscriptions",
  "confidence_score": 0.91,
  "reasoning": "Transaction matches historical SaaS subscription patterns and vendor is a known cloud provider",
  "alternatives": [
    {
      "category": "Office Supplies",
      "confidence": 0.05
    },
    {
      "category": "Utilities",
      "confidence": 0.04
    }
  ],
  "status": "success"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `suggested_category` | String | Recommended accounting category |
| `confidence_score` | Float | Confidence level (0.0 to 1.0) |
| `reasoning` | String | Explanation for the categorization |
| `alternatives` | Array | Alternative category suggestions with confidence scores |
| `status` | String | Response status ("success" or "error") |

### Response Body (Validation Error - 400)

```json
{
  "status": "error",
  "message": "Invalid request data",
  "errors": {
    "chart_of_accounts": [
      "chart_of_accounts must not be empty"
    ]
  }
}
```

### Response Body (LLM Service Error - 503)

```json
{
  "status": "error",
  "message": "Failed to get categorization from LLM service"
}
```

## Testing with cURL

### Test 1: Successful AWS Subscription Categorization

```bash
curl -X POST http://localhost:8000/api/categorize/ \
  -H "Content-Type: application/json" \
  -d '{
  "description": "AWS monthly subscription charge for server resources",
  "vendor": "Amazon Web Services",
  "amount": 15000.00,
  "company_id": "C001",
  "industry": "IT Services",
  "chart_of_accounts": [
    "Office Supplies",
    "Software & Subscriptions",
    "Travel & Entertainment",
    "Payroll",
    "Marketing",
    "Utilities",
    "Professional Services"
  ],
  "historical_transactions": [
    {
      "description": "GitHub Pro subscription",
      "category": "Software & Subscriptions"
    },
    {
      "description": "Zoom monthly plan",
      "category": "Software & Subscriptions"
    }
  ]
}'
```

### Test 2: Office Furniture Purchase

```bash
curl -X POST http://localhost:8000/api/categorize/ \
  -H "Content-Type: application/json" \
  -d '{
  "description": "Executive ergonomic office chair purchase from Herman Miller",
  "vendor": "Herman Miller",
  "amount": 45000.00,
  "company_id": "C001",
  "industry": "IT Services",
  "chart_of_accounts": [
    "Office Supplies",
    "Software & Subscriptions",
    "Travel & Entertainment",
    "Payroll",
    "Marketing",
    "Utilities",
    "Professional Services"
  ],
  "historical_transactions": [
    {
      "description": "Stapler and paper clips bulk purchase",
      "category": "Office Supplies"
    }
  ]
}'
```

### Test 3: Validation Error (Missing Required Field)

```bash
curl -X POST http://localhost:8000/api/categorize/ \
  -H "Content-Type: application/json" \
  -d '{
  "description": "Test transaction",
  "vendor": "Test Vendor",
  "chart_of_accounts": []
}'
```

Expected response with error about empty chart_of_accounts.

## Testing with Postman

1. **Open Postman**

2. **Create a new POST request** with URL: `http://localhost:8000/api/categorize/`

3. **Set Headers:**
   - Key: `Content-Type`
   - Value: `application/json`

4. **Set Body (raw JSON):**
   - Select "raw" and choose "JSON"
   - Paste the request body from the examples above

5. **Click Send** to execute the request

## Sample Transaction Test Cases

The service includes 5 pre-configured sample transactions in `categorization/sample_data/mock_transactions.py`:

### Sample 1: AWS Cloud Services
- **Description:** AWS monthly subscription charge for server resources
- **Vendor:** Amazon Web Services
- **Amount:** 15,000.00
- **Expected Category:** Software & Subscriptions
- **Expected Confidence:** ~0.90

### Sample 2: Office Furniture
- **Description:** Executive ergonomic office chair purchase
- **Vendor:** Herman Miller
- **Amount:** 45,000.00
- **Expected Category:** Office Supplies
- **Expected Confidence:** ~0.85

### Sample 3: Client Entertainment
- **Description:** Client dinner at upscale restaurant
- **Vendor:** The Ritz Carlton Restaurant
- **Amount:** 8,500.00
- **Expected Category:** Travel & Entertainment
- **Expected Confidence:** ~0.88

### Sample 4: Freelancer Payment
- **Description:** Payment to independent contractor for UI/UX design
- **Vendor:** Jane Smith (Freelancer)
- **Amount:** 25,000.00
- **Expected Category:** Professional Services
- **Expected Confidence:** ~0.92

### Sample 5: Electricity Bill
- **Description:** Monthly electricity bill for office building
- **Vendor:** State Electricity Board
- **Amount:** 12,000.00
- **Expected Category:** Utilities
- **Expected Confidence:** ~0.95

## Architecture

### Project Structure

```
transaction_categorizer/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
├── config/
│   ├── __init__.py
│   ├── settings.py          # Django settings with API key config
│   └── urls.py              # Project URL routing
├── categorization/
│   ├── __init__.py
│   ├── views.py             # DRF API view
│   ├── serializers.py       # Input/output validation
│   ├── urls.py              # App URL routing
│   ├── exceptions.py        # Custom exception handler
│   ├── services/
│   │   ├── __init__.py
│   │   ├── context_builder.py    # Builds structured prompts
│   │   ├── llm_wrapper.py        # Gemini API abstraction
│   │   └── response_parser.py    # Parses LLM output
│   └── sample_data/
│       ├── __init__.py
│       └── mock_transactions.py  # Sample data for testing
└── logs/                    # Application logs directory
```

### Data Flow

1. **Request** → API receives transaction data
2. **Validation** → Serializer validates all fields
3. **Context Building** → Creates structured prompt with transaction data and historical examples
4. **LLM Call** → Sends prompt to Google Gemini API
5. **Parsing** → Extracts and validates JSON response
6. **Response** → Returns categorization with confidence score

## Error Handling

The service implements comprehensive error handling:

- **400 Bad Request:** Invalid input data (validation errors)
- **503 Service Unavailable:** LLM API not configured or unreachable
- **500 Internal Server Error:** Unexpected application errors

All errors include a JSON response with status, message, and error details.

## Logging

Application logs are written to `logs/categorization.log` with the following information:

- Request processing status
- LLM API calls and responses
- Validation errors
- Parsing errors
- Performance metrics

View logs:

```bash
# Tail the log file
Get-Content -Path logs/categorization.log -Wait

# Or search for specific patterns
Get-Content logs/categorization.log | Select-String "error" -CaseSensitive
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Generative AI API key | `AIzaSy...` |
| `DEBUG` | Django debug mode | `True` or `False` |
| `SECRET_KEY` | Django secret key | `your-secret-key-here` |
| `ALLOWED_HOSTS` | Allowed host names | `localhost,127.0.0.1` |

## Dependencies

- **Django 4.2.11** - Web framework
- **djangorestframework 3.14.0** - REST API framework
- **google-generativeai 0.3.0** - Gemini API client
- **python-dotenv 1.0.0** - Environment variable management
- **requests 2.31.0** - HTTP library

## Production Deployment Checklist

- [ ] Set `DEBUG = False` in `.env`
- [ ] Generate a strong `SECRET_KEY`
- [ ] Add production domain to `ALLOWED_HOSTS`
- [ ] Set up proper logging to files/monitoring
- [ ] Use environment-based configuration for all secrets
- [ ] Implement rate limiting for API endpoints
- [ ] Add authentication/API keys for production access
- [ ] Configure CORS if serving frontend from different domain
- [ ] Set up database backups if needed
- [ ] Monitor Gemini API usage and costs
- [ ] Implement request/response caching where appropriate

## Troubleshooting

### "GEMINI_API_KEY not configured"

**Solution:** Ensure `.env` file exists and contains a valid API key:

```bash
# Check if .env exists
Test-Path .env

# Verify API key is set
Get-Content .env | Select-String GEMINI_API_KEY
```

### "Module not found" errors

**Solution:** Ensure virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

### "Failed to connect to Gemini API"

**Solution:** 
- Verify your internet connection
- Check API key validity at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Verify your account has free tier quota remaining

### Server won't start on port 8000

**Solution:** Use a different port:

```bash
python manage.py runserver 8080
```

## Support

For issues, questions, or feature requests, check the logs for error details:

```bash
Get-Content logs/categorization.log | Select-Object -Last 50
```

## License

This project is provided as-is for educational and business use.

---

**Last Updated:** April 2026
