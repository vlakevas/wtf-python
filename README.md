# wtf-python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)

**wtf-python** is a developer-centric CLI tool designed to transform cryptic Python tracebacks into friendly, jargon-free, and actionable explanations. Powered by Google Gemini AI, it doesn't just tell you *what* went wrong—it helps you understand *why* and offers to fix it for you.

## 🚀 Overview

Stop wasting time deciphering "ZeroDivisionError" or "AttributeError." When your script crashes, just run it with `wtf`. The tool intercepts the crash, analyzes your code and the error message, and provides a beautifully formatted explanation in your terminal.

## ✨ Features

- **AI-Powered Explanations:** Get clear, conversational breakdowns of complex errors.
- **Smart Auto-Fixer:** Automatically generates and applies corrections to your source code.
- **Safety First:** Automatically creates `.bak` backups before modifying any files.
- **Rate-Limit Resilient:** Built-in exponential backoff to handle Gemini API quotas gracefully.
- **AI Personalities:** Change the "vibe" of your debugger:
  - `--socrates`: A wise mentor who asks guiding questions.
  - `--dummy`: Simplifies concepts using real-world analogies.
  - `--roast`: Harsh, sarcastic feedback from a "Gordon Ramsay" persona.
  - `--bro`: Hyper-caffeinated Silicon Valley startup energy.
  - `--wizard`: Medieval sorcery and counter-spell incantations.

## 📦 Installation

Ensure you have [uv](https://github.com/astral-sh/uv) installed, then run:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/wtf-python.git
cd wtf-python

# Install globally as a tool
uv tool install .
```

## ⚙️ Configuration

1. Get a free Gemini API key from the [Google AI Studio](https://aistudio.google.com/).
2. Set the `GEMINI_API_KEY` environment variable:

```bash
# In your .env file or shell profile
export GEMINI_API_KEY="your_api_key_here"
```

## 🛠 Usage

Simply prefix your script execution with `wtf`:

```bash
# Standard usage
wtf script.py

# With a specific personality
wtf script.py --roast
wtf script.py --wizard
```

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
