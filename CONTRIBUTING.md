# Welcome to the Instagram Safe Unfollower Community! 👋

First off, thank you for considering contributing to this project. It's people like you that make the open-source community such an amazing place to learn, inspire, and create.

We want to keep this project safe, simple, and effective for everyone.

## 💬 How to Communicate

* **Have a Question?** Please check the [Closed Issues](../../issues?q=is%3Aissue+is%3Aclosed) first to see if it has already been answered. If not, feel free to open a new Issue with the label `question`.
* **Found a Bug?** Open a new Issue and try to include:
    * Your OS (Windows/Mac/Linux).
    * The error message you see in the terminal.
    * A screenshot (if safe/relevant).
    * **IMPORTANT:** Do not share your `config.json` or Session IDs in issues!

## 🛠️ Development Setup

If you want to modify the code or add features, you need to set up your own "Virtual Environment" (since we don't upload ours to GitHub).

**Step 1: Fork and Clone**
Fork this repository to your own GitHub account, then clone it to your machine.

**Step 2: Create a Virtual Environment**
This keeps your project libraries separate from your computer's global libraries.

* **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
* **Mac/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Create Config**
Copy `config.example.json` to `config.json` and add your test credentials.

## 📥 Submitting a Pull Request (PR)

1.  **Code:** Make your changes.
2.  **Test:** Run `python main.py` with `"dry_run": true` to ensure it doesn't crash.
3.  **Clean Up:** Remove any `print()` statements you used for debugging.
4.  **Submit:** Push to your fork and submit a Pull Request.
    * Describe exactly what you changed.
    * Explain *why* this change is needed.

## ⚠️ Safety Guidelines for Contributors

* **No API Spam:** Do not add loops that query Instagram's API rapidly without `time.sleep()`.
* **No Password Collection:** Never add code that asks for or saves the user's password.
* **Keep it Local:** This tool must remain local-execution only. Do not add cloud database connections.

Thank you for helping us keep Instagram Unfollower clean and safe! 🚀
