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

## References

- See [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial) for more details on how setup and debug Python applications in VS Code.
