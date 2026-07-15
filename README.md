# FlirtyChatBot 💬✨

Telegram group/DM ke liye AI-powered flirty chat bot. Jab bhi koi tag kare ya
reply kare, ek sweet/romantic persona AI se reply generate hoke aata hai —
free Groq API use karke.

**Structure** AnonXMusic jaise modular pattern pe based hai (core / plugins / ai /
ui / utils), bas music ki jagah yahan sirf chatting hai — koi voice chat /
pytgcalls nahi hai.

## Kya kya milta hai

- `/start`, `/help`, `/reset` commands
- Group mein **@mention** ya **reply** karne par AI response
- Private DM mein har message ka AI reply (auto — mention ki zarurat nahi)
- Optional **Assistant/Userbot** — agar chahiye ki "BOT" tag na dikhe, apne
  personal account se bhi bot jaisa chat ho (bilkul AnonXMusic ke assistant jaisa)
- Har chat ki short memory (pichle messages yaad rakhta hai, natural context ke liye)
- Persona fully customizable — naam, tone, sab `.env` aur `bot/ai/persona.py` se
- **Premium /start panel** — photo + caption + inline buttons, private aur
  group ke liye alag-alag (Add to Group, DM, Help, Reset)
- Group mein add hote hi automatic **thank-you panel** (photo + caption + buttons)
- Ek hi repo mein backend + AI integration + Docker + Heroku config — kahin alag
  se kuch host nahi karna, same repo deploy karo aur sab chal jaayega

## Setup

### 1. Project install karo
```bash
cd FlirtyChatBot
pip install -r requirements.txt --break-system-packages
```
(Agar virtual environment use kar rahe ho toh `--break-system-packages` ki zarurat nahi)

> Windows par agar `tgcrypto` install mein error aaye, usse requirements.txt se
> hata do — bot bina uske bhi chalega, bas thoda slow.

### 2. Telegram API_ID / API_HASH lo
1. https://my.telegram.org par jao, apne number se login karo
2. **API Development Tools** → koi bhi naam/description daalke app create karo
3. `api_id` aur `api_hash` mil jayenge

### 3. Bot banao (@BotFather)
1. Telegram par [@BotFather](https://t.me/BotFather) kholo
2. `/newbot` bhejo, naam aur username set karo
3. Jo **token** milega, wahi `BOT_TOKEN` hai
4. **Zaroori:** `/setprivacy` bhejo → apna bot select karo → **Disable** choose karo
   (Isse bina ye kiye bot group ke normal messages nahi dekh payega, sirf commands dikhenge)

### 4. Groq API key lo (FREE)
1. https://console.groq.com par jao, sign up karo
2. **API Keys** section se naya key banao — `GROQ_API_KEY` yahi hai

### 5. `.env` file banao
`.env.example` ko copy karke `.env` banao, aur upar ke saare values bhar do:
```bash
cp .env.example .env
```

### 6. (Optional) Assistant/Userbot setup
Agar chahiye ki tumhara personal account bhi bot ki tarah chat kare (bina "BOT" tag ke):
```bash
python generate_session.py
```
Phone number + OTP maangega, phir ek **SESSION_STRING** dega — usse `.env` mein paste kar do.

⚠️ Note: Userbot automation Telegram ke ToS ke thoda grey-area mein aata hai
(spam-jaisa automated use disallowed hai), lekin apne khud ke group mein personal
chat ke liye use karna extremely common hai — yehi pattern AnonXMusic jaise bots
ke "assistant" mein bhi hota hai. Bas ise spam ya bahut saare unknown groups mein
mat daalo, apne account ka risk khud samjho.

### 7. Bot ko group mein add karo
- Bot (aur agar bana hai toh assistant/userbot account) ko group mein add karo
- Bot ko **admin** bana do (ya sirf privacy already disable kar di ho toh normal member bhi chalega)

### 8. Run karo (local testing ke liye)
```bash
python main.py
```
Production/VPS/Heroku pe deploy karna ho toh niche **"Deploy — Sab Kuch Isi Repo Se"**
section dekho — Docker se sab kuch isi ek repo se chal jaayega.

## Commands
| Command | Kaam |
|---|---|
| `/start` | Private ya group ke hisaab se alag intro panel |
| `/help` | Commands list |
| `/reset` | Us chat ki memory clear karo |

## Premium UI Panels 🎨
Teen jagah pe photo + caption + inline buttons wala panel aata hai:

1. **`/start` (private mein)** — Add Me To Your Group / Help / Reset buttons
2. **`/start` (group mein)** — chhota panel, Message Me Privately button
3. **Naye group mein add hote hi** — automatic thank-you panel, Help / Add To
   Another Group buttons

Photo dikhane ke liye `.env` mein `START_IMG` set karo (ek image URL — public
internet pe host hui koi bhi image, jaise apna banaya hua logo/banner imgbb ya
GitHub pe upload karke). **Khali chhod doge toh koi dikkat nahi** — bot khud
text-only panel pe fallback ho jaayega, kuch crash nahi hoga. Apni khud ki
image use karna — kahin se bhi random copyrighted image mat lena.

Buttons ka "Add Me To Your Group" wala link khud-ba-khud tumhare bot ke username
se ban jaata hai (koi manual config nahi chahiye).

## Customize kaise karo
- **Naam/tone:** `.env` mein `BOT_NAME` badlo, deeper personality `bot/ai/persona.py`
  mein `SYSTEM_PROMPT` edit karke
- **Panel wording:** `bot/ui/texts.py` — start/thank-you/help ka poora text yahan hai
- **Buttons:** `bot/ui/keyboards.py` — button add/remove/rename yahan se
- **AI model:** `.env` mein `GROQ_MODEL` — `openai/gpt-oss-20b` (fast) ya
  `openai/gpt-oss-120b` (zyada smart, thoda slow)
- **Memory length:** `.env` mein `MEMORY_LIMIT`
- Tip: Agar shayari wala touch chahiye, `persona.py` mein ek line add kar do jaise
  "kabhi kabhi Urdu shayari ka chhota sa touch bhi de sakti ho" — persona khud
  usko blend kar lega

## Deploy — Sab Kuch Isi Repo Se 🚀

**Important:** AI (Groq) alag se host nahi karna — wo already isi repo/process ke
andar hai. Jab container/dyno chalta hai, wahi ek process Telegram bot ko bhi
handle karta hai aur Groq ko seedha internet pe API call bhi karta hai. Ek repo,
ek deploy, sab kuch usi mein chalta hai — koi doosri jagah kuch host nahi karna.

Repo mein ye deployment files already hain:
- `Dockerfile` — image kaise banegi
- `docker-compose.yml` — VPS/local pe ek command mein chalane ke liye
- `heroku.yml` + `app.json` — Heroku (container stack) ke liye

### Option A: VPS pe (Docker)
```bash
git clone <tumhara-repo-url>
cd FlirtyChatBot
cp .env.example .env      # sab values bharo
docker compose up -d --build
```
Logs dekhne ke liye: `docker compose logs -f`
Rokne ke liye: `docker compose down`

VPS restart ho ya crash ho, `restart: unless-stopped` ki wajah se bot khud wapas
chalu ho jaayega.

### Option B: Heroku pe (Docker/container stack)
```bash
heroku login
heroku create tumhara-app-name
heroku stack:set container -a tumhara-app-name

# Heroku .env file use NAHI karta — config vars seedha set karne padte hain:
heroku config:set API_ID=xxxx API_HASH=xxxx BOT_TOKEN=xxxx GROQ_API_KEY=xxxx -a tumhara-app-name
heroku config:set SESSION_STRING=xxxx -a tumhara-app-name   # optional, assistant ke liye

git push heroku main

# Zaroori: worker dyno khud start nahi hota, manually scale karna padta hai
heroku ps:scale worker=1 -a tumhara-app-name
```
Logs: `heroku logs --tail -a tumhara-app-name`

⚠️ **Dyno type zaroor check karo:** Heroku ka free tier hai hi nahi ab (2022 mein
hi hata diya gaya tha). **Eco dyno ($5/month) inactivity par sleep ho jaata hai**
— ek continuously-running chat bot ke liye ye theek nahi, bot beech mein so
sakta hai. Isliye kam se kam **Basic dyno ($7/month, hamesha on)** use karo.
Budget tight hai toh VPS (DigitalOcean/Hetzner jaisi jagah ~$4-6/month ka droplet)
zyada reliable aur sasta padega, aur sleep wala issue bhi nahi hoga.

`app.json` mein saare zaroori config vars documented hain — GitHub pe push karne
ke baad (aur `repository` field apne asli repo URL se replace karke) chaho toh
README mein "Deploy to Heroku" button bhi laga sakte ho.

## Tech stack
- **Pyrogram** — Telegram MTProto client (bot + userbot dono)
- **Groq** — free, fast LLM inference (OpenAI-compatible API)
- **python-dotenv** — `.env` se config load karne ke liye
