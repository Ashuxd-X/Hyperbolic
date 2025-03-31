# 🤖 Hyperbolic Bot

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)](https://github.com/Ashuxd-X/Hyperbolic/commits/main)
[![Support](https://img.shields.io/badge/Support-Telegram-blue.svg)](https://telegram.me/lootersera_th)

An intelligent bot that generates and answers thought-provoking questions using the Hyperbolic API.

[Installation](#installation) • [Usage](#usage) • [Features](#features) • [Configuration](#configuration)

</div>

## 🌟 Features

- 🤔 Generates intelligent questions on various topics
- 💡 Provides concise, accurate answers
- 🎨 Beautiful colored console interface with ASCII art
- 📝 Automatically saves question history
- ⚡ Fast and efficient operation
- 🔄 Prevents question repetition
- 🛡️ Robust error handling

## 🚀 Installation

### Prerequisites

- Windows 10 or higher
- Python 3.8 or higher
- Internet connection

### Quick Start Guide

1. **Download the Repository**

   ```bash
   git clone https://github.com/Ashuxd-X/Hyperbolic.git
   cd Hyperbolic
   ```

2. **Run the Setup**

   - Double-click `run.bat`
   - If Python is not installed, you'll be prompted to install it
   - Follow the installation instructions for Python
   - Return to the bot folder and run `run.bat` again

3. **Enter Your API Key**
   - When prompted, paste your Hyperbolic API key
   - The key will be saved automatically
   - Required packages will be installed automatically

### Manual Installation

1. **Install Python**

   - Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Restart your computer after installation

2. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create key.txt**
   - Create a new file named `key.txt`
   - Or use command prompt: `notepad key.txt`
   - Paste your Hyperbolic API key into the file
   - Save the file

## 💻 Usage

### Windows Users

1. Double-click `run.bat`
2. The bot will start automatically
3. Press `Ctrl+C` to stop the bot

### Other Operating Systems

```bash
python hyper.py
```

## ⚙️ Configuration (Update If Required)

You can customize the bot's behavior by editing these variables in `hyper.py`:

```python
# Delay between questions (in seconds)
DELAY_BETWEEN_QUESTIONS = 30

# Maximum tokens for API responses
MAX_TOKENS = 2048

# Temperature for response generation (0.0 to 1.0)
TEMPERATURE = 0.7

# Top P for response generation (0.0 to 1.0)
TOP_P = 0.9

# Available topics
TOPICS = [
    "Technology", "Science", "History", "Art", "Literature",
    "Philosophy", "Economics", "Politics", "Environment",
    "Health", "Sports", "Entertainment", "Education",
    "Social Issues", "Innovation"
]

# Question types
QUESTION_TYPES = {
    "analysis": "Analyze the implications of",
    "prediction": "Predict the future of",
    "comparison": "Compare and contrast",
    "evaluation": "Evaluate the impact of",
    "explanation": "Explain how",
    "opinion": "Share your thoughts on",
    "solution": "Propose a solution for",
    "exploration": "Explore the possibilities of"
}
```

## 📁 Project Structure

```
hyperbolic-bot/
├── hyper.py           # Main bot code
├── run.bat           # Windows launcher
├── requirements.txt  # Python dependencies
├── key.txt          # API key (created automatically)
└── question_history.json  # Question history (created automatically)
```

## 🔍 Troubleshooting

### Common Issues

1. **Python Not Found**

   - Make sure Python is installed
   - Check if Python is added to PATH
   - Restart your computer after installation

2. **API Key Issues**

   - Delete `key.txt` and run `run.bat` again
   - Make sure your API key is valid
   - Check your internet connection

3. **Package Installation Failed**
   - Check your internet connection
   - Try running `pip install -r requirements.txt` manually
   - Make sure you have the latest pip version

### Getting Help

If you encounter any issues:

1. Check the error message in the console
2. Review the troubleshooting section
3. Contact support on Telegram: [Looters Era](https://telegram.me/lootersera_th)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

<div align="center">
Made with ❤️ by [Ashu](https://github.com/Ashuxd-X)
</div>
