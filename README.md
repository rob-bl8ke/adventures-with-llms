# Adventures with LLMs

## Setup

This repository uses a **single virtual environment** at the root level for all Python projects in the subdirectories. This approach saves storage space and simplifies dependency management.

#### Create and activate the virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **Note:** On Mac/Linux, use `source venv/bin/activate` instead.

All dependencies are in the root `requirements.txt`. Install them after activating your virtual environment:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Deactivate the virtual environment

```powershell
deactivate
```

## Debugging

- Ensure you have the Python debugger installed with `CTRL+SHIFT+X` and typing `@installed python debugger`.
- Select the Python interpreter from the root `venv`:
  - Open Command Palette (`Ctrl+Shift+P`)
  - Type and select **Python: Select Interpreter**
  - Choose `.\venv\Scripts\python.exe` (or similar path for your root venv)
- Set a breakpoint on your code's entry point and press F5.
- A configuration menu will open from Command Palette. Select "Python File" or "Python File with Arguments".
- The debugger will run and stop on the breakpoint.

> **Note:** Since all projects share the same root-level virtual environment, you only need to select the interpreter once.

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

## Adding new dependencies

When you need to add a new Python package:

1. Make sure the root virtual environment is activated:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
2. Install the package:
   ```powershell
   pip install package-name
   ```
3. Update the `requirements.txt`:
   ```powershell
   pip freeze > requirements.txt
   ```

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

- If you see `ModuleNotFoundError`, make sure your virtual environment is activated and VS Code is using the root venv interpreter.
- You can always check which interpreter is active in the bottom left of VS Code.
- All subdirectory projects now share the same dependencies from the root `requirements.txt`
This setup makes switching between environments seamless and avoids manual interpreter changes.

## References

- See [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial) for more details on how setup and debug Python applications in VS Code.
