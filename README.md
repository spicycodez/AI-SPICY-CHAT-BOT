# 🚀 AI-SPICY-CHAT-BOT

A **FREE**, **AI-powered Telegram chat bot** using the **Groq API** with a clean, modular ANNIECHATBOT-style architecture.

## ✨ Features

- 🤖 **Free AI** - Powered by Groq (completely free!)
- 💬 **Smart Chat** - Natural conversations with context memory
- 👥 **Groups & DMs** - Works everywhere!
- ⚡ **Lightning Fast** - Groq provides ultra-fast inference
- 🎨 **Customizable** - Easy to modify personality and behavior
- 📦 **Modular** - Clean plugin-based architecture (ANNIECHATBOT style)
- 🐳 **Docker Ready** - Easy deployment
- ☁️ **Cloud Deployment** - Heroku, VPS, or Docker

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Framework:** Pyrogram (Telegram API)
- **AI:** Groq API (Free)
- **Database:** MongoDB (optional)
- **Deployment:** Docker, Heroku, VPS

## 📋 Setup

### 1️⃣ Prerequisites

- Python 3.11 or higher
- A Telegram account
- Groq API key (free from [console.groq.com](https://console.groq.com))

### 2️⃣ Get Telegram Credentials

1. Go to [https://my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Click "API Development Tools"
4. Create an app and get your `API_ID` and `API_HASH`

### 3️⃣ Create Bot with @BotFather

1. Open [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Follow the steps to get your `BOT_TOKEN`
4. **Important:** Send `/setprivacy` → select your bot → choose **Disable**

### 4️⃣ Get Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for free
3. Create an API key

### 5️⃣ Local Setup

```bash
# Clone repo
git clone https://github.com/spicycodez/AI-SPICY-CHAT-BOT.git
cd AI-SPICY-CHAT-BOT

# Install dependencies
pip install -r requirements.txt

# Copy example env file
cp .env.example .env

# Fill in your credentials in .env
# nano .env  (or use your favorite editor)

# Run the bot
python -m SPICYBOT
```

## 🐳 Docker Setup

```bash
# Build and run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🚀 Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set GROQ_API_KEY=your_groq_key

# Deploy
git push heroku main

# Scale worker
heroku ps:scale worker=1

# View logs
heroku logs --tail
```

## 📖 Commands

| Command | Usage |
|---------|-------|
| `/start` | Show welcome menu |
| `/help` | Show help message |
| `/reset` | Clear chat memory |

## 💬 Usage

### In Groups
- **Tag the bot:** `@your_bot_name your message`
- **Reply to bot:** Reply to any message from the bot

### In Private DM
- Just type any message!

## ⚙️ Configuration

Edit `.env` file to customize:

```env
# Bot personality
BOT_NAME=Pari

# Memory (how many previous messages to remember)
MEMORY_LIMIT=10

# AI Model (see Groq docs for options)
GROQ_MODEL=mixtral-8x7b-32768

# Optional - Panel image
START_IMG=https://your-image-url.jpg
```

## 🧠 Available Groq Models

- `mixtral-8x7b-32768` - Fast & capable (default)
- `llama2-70b-4096` - Large & powerful
- `gemma-7b-it` - Lightweight

See [Groq docs](https://console.groq.com/docs/models) for latest models.

## 📁 Project Structure

```
SPICYBOT/
├── __init__.py          # Bot client & config
├── __main__.py          # Entry point
├── modules/             # Plugins
│   ├── start.py         # /start command
│   ├── chat.py          # Chat handler
│   ├── welcome.py       # Welcome messages
│   └── callbacks.py     # Button callbacks
└── utils/
    └── ai.py            # Groq API integration

config.py               # Configuration
requirements.txt        # Dependencies
Dockerfile              # Docker image
app.json                # Heroku config
```

## 🤝 Contributing

Feel free to fork, modify, and improve!

## 📝 License

MIT License - Use freely for any purpose

## 🐛 Troubleshooting

### Bot not responding
- Check if bot is added to the group
- Check if privacy is disabled (`/setprivacy` in @BotFather)
- Make sure all env vars are set correctly

### API errors
- Verify your Groq API key is valid
- Check your Telegram credentials
- Ensure bot token is correct

## 💬 Support

- 📧 Issues? Open a GitHub issue
- 🤝 PRs welcome!

---

**Made with ❤️ by spicycodez**

⭐ Star this repo if you found it useful!
