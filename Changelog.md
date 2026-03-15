# Changelog

All notable changes to DeltaForge are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [1.4] — October 19, 2025

### Added
- `/groupinfo` command: shows group type (Addon or System Commands), command count, and command list. `/groupinfo` lists all groups; `/groupinfo(Text Addons)` details a specific group.
- `/groupinfo` added to the exempt commands list (always available regardless of active group).

### Changed
- **Command keys standardized:** all underscores removed from `commands` dictionary keys (`"num_random"` → `"numrandom"`, `"flip_coin"` → `"flipcoin"`, `"remove_group"` → `"removegroup"`, etc.).
- **Group names updated:** `System Tools` → `System Commands`, `All` → `All Commands`. Text Addons, Random Tools, and Note Tools classified as "Addon" groups.
- `cmd_groups`, `cmd_load_group`, `cmd_cmds`, `cmd_search_cmd` updated to reflect new group names.
- Main loop parameter handling updated to support `/groupinfo` and `/datetime` edge cases.

### Fixed
- `/cmds`, `/searchcmd`, `/removegroup` were sometimes affected by group restrictions due to key inconsistencies — resolved, these commands are now always available.

---

## [1.3] — October 12, 2025

### Added
- `/rng(max)` — tests 1/max probability.
- `/timer(seconds)` — countdown timer.
- `/toupper(text)` — converts text to uppercase.
- `/reverse(text)` — reverses text.
- `/randomchoice(items)` — picks a random item from a list.
- `/tolower(text)` — converts text to lowercase.
- `/randomcolor` — generates a random hex color code.
- `/datetime(format)` — displays date and time in a specified format.
- `/shuffle(text)` — shuffles words in text.
- `/listnotes` — lists all notes from the notes file.
- `/charcount(text)` — counts characters in text.

### Fixed
- `load_user_data` and `save_user_data` improved to handle `JSONDecodeError` and missing file cases.
- Inconsistencies between `/loadgroup` and `/cmds` resolved.

---

## [1.2] — October 11, 2025

### Added
- `/flipcoin(count)` — flips a coin multiple times.
- `/randomword(length)` — generates a random word.
- `/countwords(text)` — counts words in text.
- `/generatepassword(length)` — generates a random password.
- `/rolldice(sides;count)` — rolls dice with a specified number of sides.
- `/numrandom(min,max;count)` — generates random numbers in a specified range.
- Group-based command system introduced: `Text Addons`, `Random Tools`, `Note Tools`, `System Tools`.
- `commands` dictionary structure standardized to make adding new commands easier.

### Changed
- Error messages and input handling logic improved across existing commands.

### Fixed
- Command parameter validation errors resolved.
- Error handling strengthened for `deltaforge_notes.txt` and `user_data.json` file operations.

---

## [1.1] — October 11, 2025

### Added
- **Full update system:** `/setversion`, `/checklatestversion`, `/setlatestversion`, `/update`. Version checking and auto-update via GitHub Gist.
- Automatic backup on update with restore on failure.
- Persistent user data support via `user_data.json`.
- Group management foundation: `/loadgroup`, `/groups`.
- `/restart`, `/exit` system commands.
- User confirmation (`y/n`) for update operations.
- Emoji support in output messages (`✅`, `❌`, `⚠️`, etc.).

---

## [1.0.1] — October 11, 2025

> ⚠️ This version contains an incomplete update system. Version switching may be unreliable.

### Added
- `/setversion`, `/checklatestversion` commands (partially functional).
- Basic command processing loop established.
- `commands` dictionary structure introduced.

---

## [1.0] — October 11, 2025

> ⚠️ Initial release. Update system untested — version switching may be unreliable.

### Added
- **DeltaForge** first release — modular command-line toolkit.
- Dependencies: `json`, `random`, `string`, `datetime`, `os`, `sys`, `shutil`, `time`.
- `/savenote(text)` — save a note to file.
- `/clearnotes` — clear the notes file.
- `/listnotes` — list all saved notes.
- `/timestamp` — display Unix timestamp.
