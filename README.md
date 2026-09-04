Tourist Translator AI
A browser-based, two-way voice translator built for tourists communicating with locals in real time — no app download required.
🔗 Live app: https://touristtranslator.streamlit.app/
What It Does
Set your destination language (currently: French, Spanish, Italian, German).
Speak, and the AI transcribes and translates what the other person says into English.
Reply in English, and the AI translates and displays it back in the local language.
Built for face-to-face tourist conversations — directions, ordering food, hotel check-in — where typing into an app mid-conversation isn't practical.
Tech Stack
App framework: Streamlit
Speech-to-text: AssemblyAI API
Translation: Python translation API
Language: Python
Hosting: Streamlit Community Cloud (zero-infrastructure deployment)
Setup
1. Clone the repo
Bash

3. Install dependencies
Bash

5. Add your API key
Create a .streamlit/secrets.toml file in the project root:
Toml
An AssemblyAI API key is required to run speech-to-text. Sign up for a free key at assemblyai.com.
6. Run locally
Bash
Deployment
This app is deployed on Streamlit Community Cloud. To deploy your own copy:
Push this repo to GitHub.
Connect the repo in Streamlit Community Cloud.
Add ASSEMBLYAI_API_KEY under the app's Secrets settings.
Deploy — no server or infrastructure setup needed.
Supported Languages
English ↔ French, Spanish, Italian, German
Known Limitations
Requires a valid AssemblyAI API key to function (speech-to-text will not work without one).
Currently supports a fixed set of four languages.
Turn-by-turn translation (not continuous streaming) — see roadmap below.
Roadmap
Phase 2: Migrate backend to a decoupled FastAPI/WebSocket engine for high-concurrency, real-time streaming translation.
Phase 3: Expand supported languages.
Phase 4: Add offline/cached common-phrase mode for low-connectivity situations.
License
(Add your license here, e.g. MIT)
