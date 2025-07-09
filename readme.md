# CanIRun - Steam Game Compatibility Checker

**CanIRun** is a Python tool that checks if your PC meets the minimum requirements to run a specific Steam game.

## Features

- Fetches minimum requirements for any Steam game by its AppID.
- Detects your system's storage, CPU frequency, GPU memory, and RAM.
- Compares your hardware with the game's requirements.
- Displays a detailed, color-coded report with pass/fail status and performance bars.
- Offers upgrade recommendations and gaming tips.

## How It Works

1. Enter the Steam AppID of the game you want to check.
2. The tool retrieves the game's minimum requirements from the Steam API.
3. Your system's hardware is automatically detected.
4. The results are displayed in a user-friendly format, showing which components pass or fail.

## Requirements

- Python 3.8+
- See [`requirements.txt`](requirements.txt) for all dependencies.

## Installation

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

```vscode
API_KEY=your_google_genai_api_key
```

Set your API_KEY for Google GenAI in a `.env` file:

```
API_KEY=your_google_genai_api_key
```

## Usage

Run the main script and enter the Steam AppID when prompted:

```bash
python main.py
```

**Example AppID:** 271590 (GTA V)

## Example Output

```
=========================================================
                CAN I RUN THIS GAME?
=========================================================
💾 Storage Space
   Your System: 500 GB
   Required:    72 GB
   Status:      ✅ PASSED
   Performance: [████████████████████] 100.0%
...
🎮 FULLY COMPATIBLE
Components Passed: 4/4
=========================================================
🎯 You're all set to play this game!
```

## Notes

• The tool uses Google GenAI to extract GPU and GPU details from text.
• For best results, keep your system drivers up to date.
• Some features (like GPU detection) may require additional permissions or libraries depending on your OS.

## License

MIT License

---

*Created for educational and personal use.*