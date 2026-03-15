import time
import json
import os
import sys
import urllib.request
import random
import shutil
import string
from datetime import datetime

# ========== AYARLAR ==========
current_version = "1.4"
gist_id = "3f96f83b995b625459972c12469e372e"
latest_url = f"https://gist.githubusercontent.com/Scriptionz/{gist_id}/raw/latest.txt"

print("Welcome to Axis Python v1.4")
time.sleep(2)
print("Axis Python by Emir Karadağ, Special OS Commands")
time.sleep(2)

# Başlatmada otomatik güncelleme kontrolü
def auto_check_update():
    print("AUS: Checking For New Version...")
    cmd_check_latest(auto=True)

# Sürüm karşılaştırma fonksiyonu
def version_greater(new, current):
    try:
        new_parts = tuple(map(int, new.split('.')))
        current_parts = tuple(map(int, current.split('.')))
        return new_parts > current_parts
    except Exception:
        return False

# ========== KOMUT FONKSİYONLARI ==========
USER_DATA_FILE = "user_data.json"

def load_user_data(user_id="default_user"):
    """Load user data"""
    try:
        with open(USER_DATA_FILE, "r") as f:
            data = json.load(f)
        return data.get(user_id, {})
    except (FileNotFoundError, json.JSONDecodeError):
        # Dosya yoksa veya bozuksa, sıfırla ve boş döndür
        print("⚠️ user_data.json not found or corrupted, resetting to default.")
        save_user_data(user_id, {})  # Boş veriyle yeni dosya oluştur
        return {}

def save_user_data(user_id, data):
    """Save user data"""
    try:
        try:
            with open(USER_DATA_FILE, "r+") as f:
                users = json.load(f)
                users[user_id] = data
                f.seek(0)
                f.truncate()  # Dosyayı sıfırla
                json.dump(users, f, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(USER_DATA_FILE, "w") as f:
                json.dump({user_id: data}, f, indent=4)
    except Exception as e:
        print(f"❌ Error saving user data: {e}")

def cmd_to_upper(params):
    """Make all the text upper"""
    try:
        if not params.strip():
            raise ValueError("Text cannot be empty")
        print(f"Uppercase: {params.upper()}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /toupper(text) e.g., /toupper(hello)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /toupper(text) e.g., /toupper(hello)")

def cmd_dice_game(params):
    """Roll the dice and show the total score"""
    try:
        count = int(params.strip())
        if count < 1:
            raise ValueError("Count must be positive")
        results = [random.randint(1, 6) for _ in range(count)]
        total = sum(results)
        print(f"Rolled: {', '.join(map(str, results))}, Total: {total}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /dicegame(count) e.g., /dicegame(3)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /dicegame(count) e.g., /dicegame(3)")

def cmd_rng(params):
    """Test the chance %1 with any max number"""
    try:
        max_num = int(params.strip())
        if max_num < 1:
            raise ValueError("Max number must be positive")
        result = random.randint(1, max_num)
        probability = 1 / max_num * 100
        if result == 1:
            print(f"🎉 RNG Success Result: {result} (1/{max_num})")
        else:
            print(f"🚩 Result: {result} (Failed to hit 1/{max_num}, {probability:.2f}% chance)")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /rng(max) e.g., /rng(100)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /rng(max) e.g., /rng(100)")

def cmd_flip_text(params):
    """Invert text and replace characters with custom reverse appearance"""
    try:
        if not params.strip():
            raise ValueError("Text cannot be empty")
        flip_map = str.maketrans(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'ɐqɔpǝɟɓɥıɾʞlɯuodbɹsʇnʌʍxʎzɐqɔpǝɟɓɥıɾʞlɯuodbɹsʇnʌʍxʎz'
        )
        flipped = params[::-1].translate(flip_map)
        print(f"Flipped Text: ({flipped})")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /fliptext(text) e.g., /fliptext(hello)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /fliptext(text) e.g., /fliptext(hello)")

def cmd_timer(params):
    """Set a timer"""
    try:
        seconds = int(params.strip())
        if seconds < 1:
            raise ValueError("Seconds must be positive")
        print(f"Starting {seconds}-second timer...")
        for i in range(seconds, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        print("✅ Timer finished!")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /timer(seconds) e.g., /timer(10)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /timer(seconds) e.g., /timer(10)")

def cmd_load_group(params):
    """Load the selected group"""
    try:
        # Girişi temizle: fazladan boşlukları kaldır, büyük/küçük harf duyarlılığını yok et
        group = ' '.join(params.split()).strip()
        if not group:
            raise ValueError("Group name cannot be empty")
        valid_groups = ["All", "Text Addons", "Random Tools", "Note Tools", "System Tools"]
        # Grup adını karşılaştırmak için büyük/küçük harf duyarlılığını kaldır
        if group.lower() not in [g.lower() for g in valid_groups]:
            print(f"❌ Invalid group: '{group}'. Available groups: {', '.join(valid_groups)}")
            return
        # Orijinal grup adını bul (büyük/küçük harf korunarak)
        group = next(g for g in valid_groups if g.lower() == group.lower())
        user_data = load_user_data()
        user_data["active_group"] = group
        save_user_data("default_user", user_data)
        print(f"✅ Loaded group: {group}. Use /cmds to see active commands.")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /loadgroup(group) e.g., /loadgroup(Text Addons)")
    except Exception as e:
        print(f"❌ Error: {e}. Input was: '{params}'. Usage: /loadgroup(group) e.g., /loadgroup(Text Addons)")

def cmd_remove_group():
    """Remove the active command group"""
    try:
        user_data = load_user_data()
        if "active_group" not in user_data:
            print("✅ No active group to remove.")
            return
        del user_data["active_group"]
        save_user_data("default_user", user_data)
        print("✅ Active group removed. Please load a group with /loadgroup.")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /remove_group")

def cmd_groups():
    """List all available command groups"""
    try:
        valid_groups = ["All", "Text Addons", "Random Tools", "Note Tools", "System Tools"]
        print(f"Available groups: {', '.join(valid_groups)}")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /groups")

def cmd_random_word(params):
    """Generate random text"""
    try:
        length = int(params.strip())
        if length < 1:
            raise ValueError("Length must be positive")
        chars = string.ascii_lowercase
        word = ''.join(random.choice(chars) for _ in range(length))
        print(f"Random Word: {word}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /randomword(length) e.g., /randomword(5)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /randomword(length) e.g., /randomword(5)")

def cmd_timestamp():
    """Show current Unix timestamp"""
    try:
        timestamp = int(datetime.now().timestamp())
        print(f"Unix Timestamp: {timestamp}")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /timestamp")

def cmd_reverse(params):
    """Reverse the text"""
    try:
        if not params.strip():
            raise ValueError("Text cannot be empty")
        print(f"Reversed: {params[::-1]}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /reverse(text) e.g., /reverse(hello)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /reverse(text) e.g., /reverse(hello)")

def cmd_random_choice(params):
    """Select one of the items in the list"""
    try:
        items = [item.strip() for item in params.split(',')]
        if not items or not params.strip():
            raise ValueError("At least one item required")
        chosen = random.choice(items)
        print(f"Chosen: {chosen}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /randomchoice(items) e.g., /randomchoice(apple,banana,orange)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /randomchoice(items) e.g., /randomchoice(apple,banana,orange)")

def cmd_clear_notes():
    """Clean the notes"""
    try:
        if os.path.exists("axis_notes.txt"):
            open("axis_notes.txt", "w").close()
            print("✅ Notes file (axis_notes.txt) cleared.")
        else:
            print("✅ No notes file found to clear.")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /clearnotes")

def cmd_char_count(params):
    """Count the number of characters in the text"""
    try:
        if not params.strip():
            raise ValueError("Text cannot be empty")
        print(f"Character Count: {len(params)}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /charcount(text) e.g., /charcount(hello world)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /charcount(text) e.g., /charcount(hello world)")

def cmd_search_cmd(params):
    """Search for patterns in command names or descriptions"""
    try:
        pattern = params.strip().lower()
        if not pattern:
            raise ValueError("Search pattern cannot be empty")
        user_data = load_user_data()
        active_group = user_data.get("active_group")
        if not active_group:
            print("❌ No command group loaded. Please load a group first.")
            print("Available groups: All, Text Addons, Random Tools, Note Tools, System Tools")
            print("Usage: /loadgroup(group) e.g., /loadgroup(Text Addons)")
            return
        matches = []
        for cmd in commands.values():
            if (active_group == "All" or cmd["group"] == active_group or cmd["name"] in ["/loadgroup", "/groups", "/cmds", "/searchcmd", "/remove_group"]) and \
               (pattern in cmd["name"].lower() or pattern in cmd["desc"].lower()):
                matches.append(cmd)
        if not matches:
            print(f"❌ No commands found matching '{pattern}' in group '{active_group}'.")
            return
        print(f"Commands matching '{pattern}' (Group: {active_group}):")
        for cmd in matches:
            print(f"  {cmd['name']}: {cmd['desc']}")
            if cmd["example"]:
                print(f"    Example: {cmd['example']}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /searchcmd(pattern) e.g., /searchcmd(random)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /searchcmd(pattern) e.g., /searchcmd(random)")

def cmd_num_random(params):
    """Generate random number"""
    try:
        parts = params.split(';')
        if len(parts) != 2:
            raise ValueError("Exactly two parts (min,max;count) required")
        min_max = parts[0].strip().split(',')
        if len(min_max) != 2:
            raise ValueError("Min and max values required")
        min_val = int(min_max[0].strip())
        max_val = int(min_max[1].strip())
        count = int(parts[1].strip())
        if min_val > max_val:
            raise ValueError("Min cannot be greater than max")
        if count < 1:
            raise ValueError("Count must be positive")
        numbers = [random.randint(min_val, max_val) for _ in range(count)]
        print(f"Input: {', '.join(map(str, numbers))}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /numrandom(min, max; count) e.g., /numrandom(1, 10; 2)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /numrandom(min, max; count) e.g., /numrandom(1, 10; 2)")

def cmd_roll_dice(params):
    """Throw a dice"""
    try:
        parts = params.split(';')
        if len(parts) != 2:
            raise ValueError("Exactly two parts (sides;count) required")
        sides = int(parts[0].strip())
        count = int(parts[1].strip())
        if sides < 1:
            raise ValueError("Sides must be positive")
        if count < 1:
            raise ValueError("Count must be positive")
        results = [random.randint(1, sides) for _ in range(count)]
        print(f"Rolled {count} {sides}-sided dice: {', '.join(map(str, results))}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /rolldice(sides;count) e.g., /rolldice(6;2)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /rolldice(sides;count) e.g., /rolldice(6;2)")

def cmd_gen_pass(length):
    """Generate a random password"""
    try:
        length = int(length)
        if length < 4:
            raise ValueError("Length must be at least 4")
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        print(f"Generated Password: {password}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /genpass(length) e.g., /genpass(12)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /genpass(length) e.g., /genpass(12)")

def cmd_count_words(text):
    """Count the number of words in the text"""
    try:
        words = text.strip().split()
        if not words:
            raise ValueError("Text cannot be empty")
        print(f"Word Count: {len(words)}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /countwords(text) e.g., /countwords(Hello world)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /countwords(text) e.g., /countwords(Hello world)")

def cmd_save_note(note):
    """Save the note to a file"""
    try:
        if not note.strip():
            raise ValueError("Note cannot be empty")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note_entry = f"[{timestamp}] {note}\n"
        with open("axis_notes.txt", "a", encoding="utf-8") as f:
            f.write(note_entry)
        print(f"✅ Saved note: {note_entry.strip()}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /savenote(note) e.g., /savenote(Test note)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /savenote(note) e.g., /savenote(Test note)")

def cmd_flip_coin(count):
    """Coin toss"""
    try:
        count = int(count)
        if count < 1:
            raise ValueError("Count must be positive")
        results = [random.choice(["Heads", "Tails"]) for _ in range(count)]
        print(f"Flipped {count} coin(s): {', '.join(results)}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /flipcoin(count) e.g., /flipcoin(3)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /flipcoin(count) e.g., /flipcoin(3)")

def cmd_set_version(params):
    """Download any version of the Axis Phyton"""
    try:
        version = params.strip()
        if not version:
            raise ValueError("Version number required")
        download_version(version)
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /setversion(version) e.g., /setversion({current_version})")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /setversion(version) e.g., /setversion({current_version})")

def cmd_check_latest(auto=False):
    """Check the latest version"""
    try:
        with urllib.request.urlopen(latest_url) as res:
            latest = res.read().decode().strip()
        print(f"Current: v{current_version}")
        print(f"Latest: v{latest}")
        if version_greater(latest, current_version):
            print("⚠️ Update available! Use /setlatestversion or /update to install.")
        else:
            print("✅ Up to date.")
        return latest
    except Exception as e:
        print(f"❌ Couldn't check version: {e}")
        return None

def download_version(version, confirm=True):
    """Select any version and download"""
    warning_versions = ["1.0.1", "1.0a"]
    if version in warning_versions:
        print(f"⚠️ Warning: Version {version} may be outdated or problematic (e.g., missing update_system validation). Continue?")
        approval = input("(y/n): ").strip().lower()
        if approval != 'y':
            print("❌ Operation cancelled.")
            return

    if confirm:
        approval = input(f"Download and switch to v{version}? (y/n): ").strip().lower()
        if approval != 'y':
            print("❌ Update cancelled.")
            return

    try:
        update_url = f"https://gist.githubusercontent.com/Scriptionz/{gist_id}/raw/axis_{version}.py"
        with urllib.request.urlopen(update_url) as res:
            new_code = res.read().decode()

        fname = os.path.basename(__file__)
        backup_fname = "axis_backup.py"
        shutil.copy(fname, backup_fname)

        with open("axis_new.py", "w", encoding="utf-8") as f:
            f.write(new_code)
        os.remove(fname)
        os.rename("axis_new.py", fname)
        print(f"✅ Successfully switched to version {version}! Use /restart to reload.")
    except Exception as e:
        print(f"❌ Failed to download version {version}: {e}")
        if os.path.exists(backup_fname):
            os.remove(fname) if os.path.exists(fname) else None
            shutil.copy(backup_fname, fname)
            print("🔄 Restored from backup.")

def cmd_set_latest_version():
    """Download and set the latest version of the system"""
    try:
        latest = cmd_check_latest()
        if latest is None:
            return
        if not version_greater(latest, current_version):
            print("Already on the latest version.")
            return
        download_version(latest)
    except Exception as e:
        print(f"❌ Failed to set latest version: {e}")

def cmd_update():
    """Update and restart"""
    cmd_set_latest_version()
    cmd_restart()

def cmd_restart():
    """Restart the system"""
    print("🔄 Restarting Axis...")
    time.sleep(1)
    python = sys.executable
    os.execl(python, python, *sys.argv)

def cmd_exit():
    """Exit from Axis"""
    print("Exiting Axis...")
    time.sleep(1)
    sys.exit()

def cmd_cmds():
    """List all the available commands"""
    try:
        user_data = load_user_data()
        active_group = user_data.get("active_group")
        if not active_group:
            print("❌ No command group loaded. Please load a group first.")
            print("Available groups: All, Text Addons, Random Tools, Note Tools, System Tools")
            print("Usage: /loadgroup(group) e.g., /loadgroup(Text Addons)")
            return
        print(f"Available commands (Group: {active_group}):")
        for cmd in commands.values():
            if active_group == "All" or cmd["group"] == active_group or cmd["name"] in ["/loadgroup", "/groups", "/cmds", "/searchcmd", "/remove_group"]:
                print(f"  {cmd['name']:<20} → {cmd['desc']}")
                if cmd['example']:
                    print(f"    Example: {cmd['example']}")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /cmds")

# ========== KOMUT FONKSİYONLARI ==========
def cmd_to_lower(params):
    """Turn text to lowercase"""
    try:
        if not params.strip():
            raise ValueError("Text cannot be empty")
        print(f"Lowercase: {params.lower()}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /tolower(text) e.g., /tolower(HELLO)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /tolower(text) e.g., /tolower(HELLO)")

def cmd_random_color():
    """Generate random color"""
    try:
        color = ''.join(random.choice('0123456789ABCDEF') for _ in range(6))
        print(f"Random Color: #{color}")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /randomcolor")

def cmd_list_notes():
    """List all the notes in note file"""
    try:
        if not os.path.exists("axis_notes.txt"):
            print("✅ No notes file found.")
            return
        with open("axis_notes.txt", "r", encoding="utf-8") as f:
            notes = f.readlines()
        if not notes:
            print("✅ Notes file is empty.")
            return
        print("Notes in axis_notes.txt:")
        for note in notes:
            print(f"  {note.strip()}")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /listnotes")

def cmd_shuffle(params):
    """Mix the words"""
    try:
        words = params.strip().split()
        if not words:
            raise ValueError("Text cannot be empty")
        random.shuffle(words)
        print(f"Shuffled: {' '.join(words)}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /shuffle(text) e.g., /shuffle(hello world test)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /shuffle(text) e.g., /shuffle(hello world test)")

def cmd_date_time(params):
    """Show current date and time"""
    try:
        if not params.strip():
            raise ValueError("Format cannot be empty")
        formatted_time = datetime.now().strftime(params)
        print(f"DateTime: {formatted_time}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}. Usage: /datetime(format) e.g., /datetime(%Y-%m-%d %H:%M:%S)")
    except Exception as e:
        print(f"❌ Error: {e}. Usage: /datetime(format) e.g., /datetime(%Y-%m-%d %H:%M:%S)")

# ========== KOMUT TANIMLARI ==========
commands = {
    "numrandom": {
        "name": "/numrandom",
        "func": cmd_num_random,
        "desc": "Generate random numbers",
        "params": "(min, max; count)",
        "example": "/numrandom(1, 10; 2)",
        "group": "Random Tools"
    },
    "rng": {
        "name": "/rng",
        "func": cmd_rng,
        "desc": "Test 1/max probability with random number",
        "params": "(max)",
        "example": "/rng(100)",
        "group": "Random Tools"
    },
    "searchcmd": {
        "name": "/searchcmd",
        "func": cmd_search_cmd,
        "desc": "Search for commands by name or description",
        "params": "(pattern)",
        "example": "/searchcmd(random)",
        "group": "System Tools"
    },
    "randomword": {
        "name": "/randomword",
        "func": cmd_random_word,
        "desc": "Generate a random word",
        "params": "(length)",
        "example": "/randomword(5)",
        "group": "Random Tools"
    },
    "rolldice": {
        "name": "/rolldice",
        "func": cmd_roll_dice,
        "desc": "Roll dice with specified sides",
        "params": "(sides;count)",
        "example": "/rolldice(6;2)",
        "group": "Random Tools"
    },
    "timer": {
        "name": "/timer",
        "func": cmd_timer,
        "desc": "Start a countdown timer",
        "params": "(seconds)",
        "example": "/timer(10)",
        "group": "System Tools"
    },
    "dicegame": {
        "name": "/dicegame",
        "func": cmd_dice_game,
        "desc": "Roll dice and show total score",
        "params": "(count)",
        "example": "/dicegame(3)",
        "group": "Random Tools"
    },
    "timestamp": {
        "name": "/timestamp",
        "func": cmd_timestamp,
        "desc": "Show current Unix timestamp",
        "params": None,
        "example": None,
        "group": "System Tools"
    },
    "generatepassword": {
        "name": "/generatepassword",
        "func": cmd_gen_pass,
        "desc": "Generate a random password",
        "params": "(length)",
        "example": "/generatepassword(12)",
        "group": "Random Tools"
    },
    "countwords": {
        "name": "/countwords",
        "func": cmd_count_words,
        "desc": "Count words in text",
        "params": "(text)",
        "example": "/countwords(Hello world)",
        "group": "Text Addons"
    },
    "savenote": {
        "name": "/savenote",
        "func": cmd_save_note,
        "desc": "Save a note to file",
        "params": "(note)",
        "example": "/savenote(Test note)",
        "group": "Note Tools"
    },
    "flipcoin": {
        "name": "/flipcoin",
        "func": cmd_flip_coin,
        "desc": "Flip a coin multiple times",
        "params": "(count)",
        "example": "/flipcoin(3)",
        "group": "Random Tools"
    },
    "setversion": {
        "name": "/setversion",
        "func": cmd_set_version,
        "desc": "Switch to a specific version",
        "params": "(version)",
        "example": f"/setversion({current_version})",
        "group": "System Tools"
    },
    "checklatestversion": {
        "name": "/checklatestversion",
        "func": cmd_check_latest,
        "desc": "Check the latest Axis version online",
        "params": None,
        "example": None,
        "group": "System Tools"
    },
    "setlatestversion": {
        "name": "/setlatestversion",
        "func": cmd_set_latest_version,
        "desc": "Download and install the latest Axis version",
        "params": None,
        "example": None,
        "group": "System Tools"
    },
    "update": {
        "name": "/update",
        "func": cmd_update,
        "desc": "Update to latest and restart",
        "params": None,
        "example": None,
        "group": "System Tools"
    },
    "restart": {
        "name": "/restart",
        "func": cmd_restart,
        "desc": "Restart Axis system",
        "params": None,
        "example": None,
        "group": "System Tools"
    },
    "exit": {
        "name": "/exit",
        "func": cmd_exit,
        "desc": "Exit Axis Python",
        "params": None,
        "example": None,
        "group": "System Tools"
    },
    "cmds": {
        "name": "/cmds",
        "func": cmd_cmds,
        "desc": "List all available commands",
        "params": None,
        "example": None,
        "group": "System Tools"
    },
    "toupper": {
        "name": "/toupper",
        "func": cmd_to_upper,
        "desc": "Convert text to uppercase",
        "params": "(text)",
        "example": "/toupper(hello)",
        "group": "Text Addons"
    },
    "reverse": {
        "name": "/reverse",
        "func": cmd_reverse,
        "desc": "Reverse the text",
        "params": "(text)",
        "example": "/reverse(hello)",
        "group": "Text Addons"
    },
    "randomchoice": {
        "name": "/randomchoice",
        "func": cmd_random_choice,
        "desc": "Choose a random item from a list",
        "params": "(items)",
        "example": "/randomchoice(apple,banana,orange)",
        "group": "Random Tools"
    },
    "clearnotes": {
        "name": "/clearnotes",
        "func": cmd_clear_notes,
        "desc": "Clear the notes file",
        "params": None,
        "example": None,
        "group": "Note Tools"
    },
    "charcount": {
        "name": "/charcount",
        "func": cmd_char_count,
        "desc": "Count characters in text",
        "params": "(text)",
        "example": "/charcount(hello world)",
        "group": "Text Addons"
    },
    "tolower": {
        "name": "/tolower",
        "func": cmd_to_lower,
        "desc": "Convert text to lowercase",
        "params": "(text)",
        "example": "/tolower(HELLO)",
        "group": "Text Addons"
    },
    "randomcolor": {
        "name": "/randomcolor",
        "func": cmd_random_color,
        "desc": "Generate a random hex color code",
        "params": None,
        "example": None,
        "group": "Random Tools"
    },
    "listnotes": {
        "name": "/listnotes",
        "func": cmd_list_notes,
        "desc": "List all notes in the notes file",
        "params": None,
        "example": None,
        "group": "Note Tools"
    },
    "shuffle": {
        "name": "/shuffle",
        "func": cmd_shuffle,
        "desc": "Shuffle words in text",
        "params": "(text)",
        "example": "/shuffle(hello world test)",
        "group": "Text Addons"
    },
    "datetime": {
        "name": "/datetime",
        "func": cmd_date_time,
        "desc": "Show current date and time in specified format",
        "params": "(format)",
        "example": "/datetime(%Y-%m-%d %H:%M:%S)",
        "group": "System Tools"
    },
    "fliptext": {
        "name": "/fliptext",
        "func": cmd_flip_text,
        "desc": "Flip text with special reversed characters",
        "params": "(text)",
        "example": "/fliptext(hello)",
        "group": "Text Addons"
    },
    "loadgroup": {
        "name": "/loadgroup",
        "func": cmd_load_group,
        "desc": "Load a specific command group",
        "params": "(group)",
        "example": "/loadgroup(Text Addons)",
        "group": "System Tools"
    },
    "groups": {
        "name": "/groups",
        "func": cmd_groups,
        "desc": "List all available command groups",
        "params": None,
        "example": None,
        "group": "System Tools"
    },
    "removegroup": {
        "name": "/removegroup",
        "func": cmd_remove_group,
        "desc": "Remove the active command group",
        "params": None,
        "example": None,
        "group": "System Tools"
    },
}

# ========== ANA DÖNGÜ ==========
user_data = load_user_data()
active_group = user_data.get("active_group")

auto_check_update()

while True:
    cmd_input = input("Type your command: ").strip().lower()
    
    # Komutları işle
    cmd_name = cmd_input.split("(")[0][1:]  # / kaldırılır
    if cmd_name in commands:
        cmd = commands[cmd_name]
        # /loadgroup, /groups, /cmds, /searchcmd, /removegroup her zaman çalışabilir
        if active_group is None and cmd["name"] not in ["/loadgroup", "/groups", "/cmds", "/searchcmd", "/removegroup"]:
            print("❌ No command group loaded. Please load a group first.")
            print("Available groups: All, Text Addons, Random Tools, Note Tools, System Tools")
            print("Usage: /loadgroup(group) e.g., /loadgroup(Text Addons)")
            continue
        if active_group != "All" and cmd["group"] != active_group and cmd["name"] not in ["/loadgroup", "/groups", "/cmds", "/searchcmd", "/removegroup"]:
            print(f"❌ Command '{cmd['name']}' is not in active group '{active_group}'. Use /loadgroup to change group.")
            continue
        if cmd["params"]:  # Parametreli komut
            if "(" not in cmd_input or ")" not in cmd_input:
                print(f"Usage: {cmd['name']}{cmd['params']} e.g., {cmd['example']}")
                continue
            params = cmd_input[cmd_input.find("(")+1:cmd_input.rfind(")")].strip()
            if not params and cmd["params"] != "(format)":  # /datetime için özel durum
                print(f"Usage: {cmd['name']}{cmd['params']} e.g., {cmd['example']}")
                continue
            cmd["func"](params)
        else:  # Parametresiz komut
            if "(" in cmd_input or ")" in cmd_input:
                print(f"❌ Command '{cmd['name']}' does not take parameters. Usage: {cmd['name']}")
                continue
            cmd["func"]()
    else:
        print(f"❌ Unknown command: /{cmd_name}. Type /cmds to see all commands.")
