# Sunrise Crops Wiki Bot 🌾🌽🍋  
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://aiogram.dev)
[![OpenAI](https://a11ybadges.com/badge?logo=openai)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
Telegram bot for agricultural crop information based on Wikipedia data.
## 🌟 Features
- Answers questions about agricultural crops
- Uses OpenAI's GPT models for natural language processing
- Rate limiting: 5 requests per hour, 20 per day
- Context-aware responses based on Wikipedia data
## 🚀 Quick Start
### Requirements
- Python 3.11+  
- Telegram account with Telegram Bot Token from [@BotFather](https://t.me/BotFather)  
### Setup
```bash
git clone https://github.com/iM1k33/Crops_bot.git
cd Quiz_bot
# Creating virtual environment 
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
# Install dependencies
pip install -r requirements.txt
```
### Bot Setup
1. Create api file:
```bash
cp crops_bot/api_example.py crops_bot/api.py
```
2. Open `crops_bot/api.py` and edit variables:
```python
OPENAI_API_KEY = "your_openai_api_key"
TELEGRAM_TOKEN = "your_telegram_bot_token"
```
### Runing the bot
```bash
python run.py
```
3. Download crops.csv to /data
You can use manual download via link https://drive.google.com/file/d/1T1wWJsuI6hGSgAdxfaIp1O7BfoewVc-l
OR
using gdown
```bash
pip install gdown
gdown 1T1wWJsuI6hGSgAdxfaIp1O7BfoewVc-l -O crops.csv
```


## 🎮 Usage
- `/start` - Start the bot
- `/help` - Show help information
- `/stats` - Show your usage statistics

## 🗂️ Project Structure
```
Crops_bot/
├── data/
│   └── crops.csv *excluded from repo, link provided
├── crops_bot/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── main.py
│   ├── handlers.py
│   ├── commands.py
│   ├── limiter.py
│   └── gpt_client.py
├── run.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```
## ⚙️ Technologia
- [aiogram](https://aiogram.dev/) - Asinc framework for Telegram Bot API
- [openai](https://openai.com/api) - The fastest and most powerful platform for building AI products
## 🤝 Contribution
1. Fork repo  
2. Create branch: `git checkout -b feature/your-feature`  
3. Make commit: `git commit -m 'Add some feature'`  
4. Push branch: `git push origin feature/your-feature`  
5. Open Pull Request  
## 📜 License
This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
