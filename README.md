# Adventures with LLMs

## Setup

#### Create and activate the virtual environment

```powershell
python -m venv venv

# This command is different for Mac and Linux (look it up)
venv\Scripts\activate
```

All dependencies are in your `requirements.txt`. Install them after activating your virtual environment:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Initializing the Debug for first run

- Ensure you have the Python debugger installed with `CTRL+SHIFT+X` and typing `@installed python debugger`.
- Set a breakpoint on your code's entry point and press F5.
- A configuration menu will open from Command Palette. Select "Python File" or "Python File with Arguments".
- The debugger will run, and stop on the breakpoint.

> Note: For the debugger to work correctly you must be in the directory of your solution's environment.

## Auto formatting in VS Code

In VS Code, prefer the "Black Formatter" extension from Microsoft. Install the extension and then paste the following into your workspace `settings.json` or simply select the formatter as the default formatter in Settings.

```json
{
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.black-formatter"
    }
}
```

## Setting up a new subfolder project with its own venv

1. Navigate to your subfolder (e.g., `three-way-convos`).
2. Create a virtual environment:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. In VS Code, select the correct Python interpreter:
   - Open Command Palette (`Ctrl+Shift+P`)
   - Type and select **Python: Select Interpreter**
   - Choose the interpreter from your subfolder's `venv` (e.g., `three-way-convos/venv/Scripts/python.exe`)
5. Debugging:
   - Use the provided `.vscode/launch.json` or run/debug directly from the subfolder.
   - Ensure breakpoints are set and the correct interpreter is selected.

## Setting environment variables for API keys

- Create a `.env` file in your subfolder (e.g., `three-way-convos/.env`) and add your API key:
  ```
  OPENAI_API_KEY=your-key-here
  ```
- In your VS Code debug configuration (`.vscode/launch.json`), add:
  ```json
  "envFile": "${workspaceFolder}/three-way-convos/.env"
  ```
- This ensures your API key is available when running or debugging from the workspace directory.

## Troubleshooting
- If you see `ModuleNotFoundError`, make sure your virtual environment is activated and VS Code is using the correct interpreter.
- You can always check which interpreter is active in the bottom left of VS Code.

## References

- See [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial) for more details on how setup and debug Python applications in VS Code.
