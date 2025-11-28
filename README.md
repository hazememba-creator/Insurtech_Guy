# 🚗 The Insurtech Guy - AI-Powered Insurance Concierge

> Replacing Rigid Insurance Forms with Natural Conversation

[![Google ADK](https://img.shields.io/badge/Google-ADK-blue)](https://google.github.io/adk-docs/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5-orange)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Kaggle](https://img.shields.io/badge/Kaggle-Capstone-20BEFF)](https://www.kaggle.com/competitions/agents-intensive-capstone-project)

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Why Agents?](#-why-agents)
- [Solution Architecture](#-solution-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Demo](#-demo)
- [Course Capabilities Demonstrated](#-course-capabilities-demonstrated)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)
- [License](#-license)

---

## 🎯 Problem Statement

Buying car insurance today is a frustrating experience. Customers face:

- **Rigid online forms** with dozens of fields
- **Confusing terminology** and complex coverage options
- **No personalized guidance** - everyone gets the same impersonal experience
- **Multiple website visits** to compare insurers

According to industry studies, **over 40% of online insurance quotes are never completed** due to form complexity.

As someone with 34 years of experience in digital services and having recently managed a regional Insurtech project in MEA region, I've witnessed this problem firsthand. Everyone deserves access to clear, personalized guidance when making these important decisions.

---

## 🤖 Why Agents?

Traditional software cannot solve this problem. Rule-based chatbots fail because insurance conversations are nuanced—customers express their needs in countless ways.

**AI agents are the right solution because they can:**

| Capability | How It Helps |
|------------|--------------|
| **Understand Natural Language** | Extract data from "I just got my license" or "driving for 5 years" |
| **Maintain Context** | Remember earlier conversation, ask only missing info |
| **Use Tools Dynamically** | Calculate quotes, search reviews, process purchases |
| **Provide Personalized Guidance** | Tailor explanations to each customer's situation |
| **Scale Expertise** | Deliver advisor knowledge 24/7 without human cost |

The agent paradigm transforms insurance buying from **"fill out this form"** to **"tell me about yourself and I'll help you find the right coverage."**

---

## 🏗 Solution Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CUSTOMER                              │
│                    (Natural Language)                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                 ROOT AGENT (insurtech_guy)                   │
│                   Gemini 2.5 Flash Lite                      │
│                                                              │
│  • Understands customer needs                                │
│  • Collects required information naturally                   │
│  • Presents quotes and recommendations                       │
│  • Guides purchase process                                   │
└───────┬─────────────────┬─────────────────┬─────────────────┘
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────────────┐
│ CUSTOM TOOLS  │ │ CUSTOM TOOLS  │ │    SUB-AGENT          │
│               │ │               │ │ (google_search_agent) │
│ • get_quotes  │ │ • get_addons  │ │                       │
│ • purchase    │ │               │ │ • google_search tool  │
└───────────────┘ └───────────────┘ └───────────────────────┘
        │                 │                 │
        ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                               │
│                                                              │
│  • 5 Insurers (GEICO, Progressive, StateFarm, Allstate,     │
│                Travelers)                                    │
│  • 3 Coverage Tiers (Liability, Standard, Premium)          │
│  • 6 Add-ons with varying availability                      │
│  • Dynamic pricing based on car, driver, coverage           │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### Core Functionality

- **Natural Conversation** - No rigid forms, just talk naturally
- **Multi-Insurer Quotes** - Compare 5 insurers across 3 coverage tiers
- **Dynamic Pricing** - Based on car brand, value, driver age, experience
- **Real-time Research** - Search for insurer reviews via Google
- **Add-on Customization** - View and understand available add-ons
- **Simulated Purchase** - Complete end-to-end purchase flow

### Pricing Model

| Brand Category | Base Rate |
|----------------|-----------|
| American (Ford, Chevy, etc.) | 5.0% |
| Japanese (Toyota, Honda, etc.) | 5.5% |
| German (BMW, Mercedes, etc.) | 6.0% |
| Other brands | 6.5% |

**Adjustments applied for:**
- Driver age (18-25: +15%, 60+: -10%)
- License experience (0-2 years: +20%, 3-5 years: +10%)
- Insurer multiplier (GEICO 0.95x to Travelers 1.08x)

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | Google ADK (Agent Development Kit) |
| LLM | Gemini 2.5 Flash Lite |
| Development | Kaggle Notebooks |
| Language | Python 3.11 |
| Testing UI | ADK Web UI |
| Observability | DEBUG logging + Tracing |

---

## 📦 Installation

### Prerequisites

- Python 3.10+
- Google API Key (Gemini access)

### Setup

```bash
# Clone the repository
git clone https://github.com/hazememba-creator/insurtech-guy.git
cd insurtech-guy

# Install dependencies
pip install -r requirements.txt

# Set your API key
export GOOGLE_API_KEY="your-api-key-here"
```

---

## 🚀 Usage

### Option 1: Run on Kaggle (Recommended)

1. Open the notebook on Kaggle
2. Add your `GOOGLE_API_KEY` to Kaggle Secrets
3. Run all cells
4. Click the ADK Web UI button to interact

### Option 2: Run Locally

```bash
# Navigate to agent directory
cd insurtech_guy

# Start ADK Web UI
adk web --log_level DEBUG
```

Then open `http://localhost:8000` in your browser.

---

## 🎬 Demo

### Conversation Flow

**1. Customer starts conversation:**
> "Hello, I need car insurance"

**2. Agent asks for missing info:**
> "I'd be happy to help! Could you tell me about your car and yourself?"

**3. Customer provides details:**
> "Ford Explorer, worth about $50,000. I'm 54 and been driving for 35 years"

**4. Agent presents quotes:**
> "Here are your options across all coverage levels..."

| Tier | GEICO | Progressive | StateFarm | Allstate | Travelers |
|------|-------|-------------|-----------|----------|-----------|
| Liability | $712 | $735 | $750 | $787 | $810 |
| Standard | $2,375 | $2,450 | $2,500 | $2,625 | $2,700 |
| Premium | $2,500 | $2,725 | $2,875 | $2,925 | $3,150 |

**5. Customer asks about insurer:**
> "Do you have customer reviews about GEICO?"

**6. Agent searches and responds:**
> "GEICO is often praised for affordability and digital tools..."

**7. Customer purchases:**
> "I'll take the StateFarm Standard"

**8. Agent completes purchase:**
> "🎉 Congratulations! Policy STA-43594990 confirmed. $2,500/year."

---

## 📚 Course Capabilities Demonstrated

This project demonstrates **3 key capabilities** from the Google ADK Agents Intensive course:

### 1. Multi-Agent Architecture

- **Root Agent** (`insurtech_guy`): Main conversational agent
- **Sub-Agent** (`google_search_agent`): Specialized for web search
- Uses `AgentTool` wrapper pattern for agent composition

### 2. Custom Tools

| Tool | Purpose |
|------|---------|
| `get_insurance_quotes` | Calculate quotes from all 5 insurers |
| `get_available_addons` | Show add-ons and costs per insurer |
| `purchase_policy` | Simulate policy purchase |
| `google_search` | Real-time insurer research (built-in) |

### 3. Observability

- DEBUG-level logging for full prompt/response visibility
- ADK Web UI with real-time tracing
- Events tab for step-by-step inspection

---

## 🔮 Future Enhancements

Given more time, I would add:

- [ ] **Sessions & Memory** - Continue previous conversations
- [ ] **Agent Evaluation** - Systematic testing framework
- [ ] **Custom Quote Tool** - Add/remove specific add-ons
- [ ] **Real Insurer APIs** - Live quotes instead of simulated
- [ ] **Document OCR** - Extract info from license photos
- [ ] **Cloud Deployment** - Deploy via Agent Engine
- [ ] **Multi-Line Insurance** - Home, life, health products

---

## 👨‍💻 Author

**Hazem Ali Abdallah**

- 34 years experience in digital services
- Recently managed regional Insurtech project in MEA region
- Kaggle: [@hazemaliabdallah](https://www.kaggle.com/hazemaliabdallah)
- GitHub: [@hazememba-creator](https://github.com/hazememba-creator)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Google ADK Team for the excellent Agent Development Kit
- Kaggle for hosting the 5-Day AI Agents Intensive
- The Gemini team for powerful language models

---

**Built with ❤️ for the Google ADK Agents Intensive Capstone Project 2025**
