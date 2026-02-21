import instaloader
import json
import time
import random
import sys
import os

# --- CONSTANTS ---
CONFIG_FILE = 'config.json'
CUSTOM_TARGETS_FILE = 'ig_unfollowers_2026-02-15T22-32-02.json'
PROCESSED_FILE = 'processed_unfollows.txt'  # ← new: remembers who was attempted
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"[ERROR] {CONFIG_FILE} not found!")
        sys.exit(1)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_processed():
    """Load usernames that were already attempted (successful or failed)"""
    processed = set()
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                username = line.strip()
                if username:
                    processed.add(username)
    print(f"[INFO] Loaded {len(processed)} previously processed users")
    return processed

def save_processed(username):
    """Append a processed username to the file"""
    with open(PROCESSED_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{username}\n")

def unfollow_via_api(L, user_id, csrf_token):
    url = f"https://www.instagram.com/web/friendships/{user_id}/unfollow/"
    L.context._session.headers.update({'X-CSRFToken': csrf_token})
    try:
        response = L.context._session.post(url)
        if response.status_code == 200:
            return True
        else:
            print(f" [API ERROR] Status: {response.status_code} | Msg: {response.text[:200]}")
            return False
    except Exception as e:
        print(f" [REQUEST ERROR] {e}")
        return False

def load_custom_targets(filename):
    targets = []
    if not os.path.exists(filename):
        print(f"[INFO] Custom {filename} not found → falling back")
        return targets

    print(f"[INFO] Loading custom {filename}...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'users' in data and isinstance(data['users'], list):
            for user in data['users']:
                if 'username' in user and 'id' in user:
                    targets.append({
                        'username': user['username'],
                        'id': user['id']
                    })
        print(f"  → Loaded {len(targets)} targets with IDs")
    except Exception as e:
        print(f"[ERROR] Failed to load custom targets: {e}")
    return targets

def main():
    print("--- Instagram Unfollower - with skip already processed & non-existent users ---")
   
    config = load_config()
    username = config['username']
    session_id = config['session_id']
    csrf_token = config['csrf_token']
    max_unfollows = config['max_unfollows_per_day']
    dry_run = config['dry_run']
    whitelist = set(config['whitelist'])

    if "PASTE_" in session_id:
        print("[ERROR] Update config.json with real credentials.")
        return

    # Load previously processed users
    processed = load_processed()

    # Load targets (prefer custom file with IDs)
    print("\nLoading targets...")
    targets = load_custom_targets(CUSTOM_TARGETS_FILE)

    if not targets:
        print("[WARNING] No custom targets loaded – script will skip unfollows without IDs.")
        return

    print(f"\nStats:")
    print(f" - Total targets: {len(targets)}")
    print(f" - Already processed: {len(processed)}")
    print(f" - Remaining to process: {len(targets) - len(processed)}")

    # Initialize session
    print("\nInitializing connection...")
    L = instaloader.Instaloader(user_agent=USER_AGENT)
    try:
        L.context._session.cookies.set("sessionid", session_id, domain=".instagram.com")
        L.context._session.cookies.set("csrftoken", csrf_token, domain=".instagram.com")
        user = L.test_login()
        if user:
            print(f"SUCCESS! Logged in as: {user}")
        else:
            print("[ERROR] Login failed.")
            return
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return

    # 5. EXECUTION LOOP
    count = 0
    print(f"\nStarting process... (Max per day: {max_unfollows})")
   
    if dry_run:
        print("\n[DRY RUN MODE - no unfollows]")
        for t in targets[:10]:
            print(f"  Would process: {t['username']} (ID: {t['id']})")
        print(f"  ... and {len(targets)-10} more")
        return

    for target in targets:
        target_user = target['username']
        user_id = target['id']

        # Skip already processed
        if target_user in processed:
            print(f"[{count+1}/{max_unfollows}] {target_user}... Already processed → skipping")
            continue

        print(f"[{count+1}/{max_unfollows}] {target_user}...", end=" ")

        if not user_id:
            print("No ID – skipping")
            save_processed(target_user)
            continue

        try:
            # Attempt unfollow
            if unfollow_via_api(L, user_id, csrf_token):
                print("UNFOLLOWED.")
                save_processed(target_user)
            else:
                print("FAILED (API error).")
                save_processed(target_user)  # still mark as attempted

            # Short test delay – 30s to 2 min
            sleep_time = random.randint(30, 120)
            print(f" Waiting {sleep_time} seconds...", end="\r")
            time.sleep(sleep_time)

        except Exception as e:
            print(f"ERROR: {e}")
            # Mark as processed even on error (so we don't retry forever)
            save_processed(target_user)

            if '429' in str(e):
                print("Rate limit → pausing 60 minutes")
                time.sleep(3600)
            elif count > 5:
                print("Too many errors → stopping")
                break

        count += 1
        if count >= max_unfollows:
            print(f"\n[STOP] Daily limit reached.")
            break

    print("\nJob Done.")

if __name__ == "__main__":
    main()

