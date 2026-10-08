# PayGuard AI
**The AI Safety Layer for Autonomous Commerce**

## Problem
AI agents can act faster than humans can verify them. What happens when an AI makes a bad financial decision? Traditional payment systems ask "Can this payment be processed?". PayGuard AI asks "Should this payment happen?".

## Solution
PayGuard AI acts as an intelligent layer between the user and PayPal. Every transaction passes through three levels:
1. Risk Assessment
2. Policy Check
3. Authorization Rules
Only after passing these checks does the system allow the payment to proceed through PayPal.

## Architecture
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Backend**: Python, Flask
- **Database**: MySQL
- **Payments**: PayPal API (Sandbox)
- **AI**: Google Generative AI (Gemini)

## Setup
1. Create a MySQL database named `pay_pal`.
2. Execute `database/schema.sql` to initialize tables.
3. Add your credentials to `.env`.
4. Install dependencies: `pip install -r requirements.txt`
5. Run backend: `python -m backend.app` (from root folder)
6. Open `frontend/index.html` in your browser.

## Core Differentiator
"PayPal moves the money. PayGuard makes sure the money should move."
