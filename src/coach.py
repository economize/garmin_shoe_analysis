import ollama
import duckdb
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
MODEL = "deepseek-r1:14b"
HISTORY_FILE = "chat_history.json"

# --- 1. LOAD HEALTH DATA (ACWR/Stats) ---
current_acwr = 0.99
current_status = "GREEN LIGHT"
current_date = datetime.now().strftime("%Y-%m-%d")

try:
    conn = duckdb.connect('garmin_analysis.db', read_only=True)
    tables = conn.execute("SHOW TABLES").fetchall()
    if tables and ('analysis' in [t[0] for t in tables]):
        stats = conn.execute("SELECT date, acwr, status FROM analysis ORDER BY date DESC LIMIT 1").fetchone()
        if stats:
            current_date = str(stats[0])
            current_acwr = stats[1]
            current_status = stats[2]
    conn.close()
except Exception:
    pass # Use defaults if DB fails

data_context = f"""
Current Date: {current_date}
ACWR (Acute Chronic Workload Ratio): {current_acwr:.2f}
Status: {current_status}
Recent Issues: Recovering from Groin Strain (Sept 2025).
Shoes Available: Saucony Speed 3 (Good for low risk), Stability Shoes (Good for recovery).
"""

# --- 2. DEFINE SYSTEM PROMPT ---
system_prompt_content = f"""
You are an expert running coach and physiologist.
Your athlete has the following current stats:
{data_context}

RULES:
1. Always base advice on the ACWR and injury history provided above.
2. If ACWR > 1.3, be conservative. If < 0.8, encourage consistency.
3. Keep responses concise and actionable.
4. You have access to past conversations. Use them to track progress.
"""

# --- 3. MANAGE CHAT HISTORY ---
def load_history():
    messages = []
    # Always start with the FRESH system prompt (updated stats)
    messages.append({'role': 'system', 'content': system_prompt_content})
    
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                old_messages = json.load(f)
                # Filter out old system prompts so we don't confuse the model with old stats
                user_assistant_msgs = [m for m in old_messages if m['role'] != 'system']
                messages.extend(user_assistant_msgs)
                print(f"📂 Loaded {len(user_assistant_msgs)} past messages from history.")
        except Exception as e:
            print(f"⚠️ Could not load history: {e}")
    
    return messages

def save_history(messages):
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(messages, f, indent=2)
    except Exception as e:
        print(f"⚠️ Failed to save history: {e}")

# --- 4. THE CHAT LOOP ---
def chat_loop():
    messages = load_history()
    
    print("---------------------------------------------------------")
    print(f"🏃 COACH DEEPSEEK ({MODEL})")
    print(f"📊 Context: ACWR {current_acwr} | {current_status}")
    print("   (History loaded. Type 'clear' to wipe memory)")
    print("---------------------------------------------------------")

    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            # Commands
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Session saved.")
                break
            
            if user_input.lower() == 'clear':
                if os.path.exists(HISTORY_FILE):
                    os.remove(HISTORY_FILE)
                messages = [{'role': 'system', 'content': system_prompt_content}]
                print("🧹 Memory wiped!")
                continue

            if not user_input:
                continue
            
            # Add user message
            messages.append({'role': 'user', 'content': user_input})

            # Stream Response
            print("\n🤖 Coach: ", end="", flush=True)
            full_response = ""
            
            stream = ollama.chat(model=MODEL, messages=messages, stream=True)
            for chunk in stream:
                content = chunk['message']['content']
                print(content, end="", flush=True)
                full_response += content
            
            print() # Newline

            # Add AI response and Save immediately
            messages.append({'role': 'assistant', 'content': full_response})
            save_history(messages)

        except KeyboardInterrupt:
            print("\n👋 Session ended.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            break

if __name__ == "__main__":
    chat_loop()