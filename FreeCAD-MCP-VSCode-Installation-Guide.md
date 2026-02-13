# FreeCAD MCP Installation Guide for VS Code GitHub Copilot

This guide explains how to set up FreeCAD MCP (Model Context Protocol) with **VS Code GitHub Copilot Chat**, enabling you to control FreeCAD directly from VS Code.

> **Note**: This guide is specifically for **VS Code + GitHub Copilot**, not Claude Desktop. The official README is written for Claude Desktop and many instructions there don't apply to VS Code.

---

## Prerequisites

- **FreeCAD** installed (latest version recommended)
- **VS Code** with **GitHub Copilot** extension installed and activated
- **Git** installed
- **Internet connection** for downloading dependencies

---

## Step 1: Install FreeCAD MCP Addon

The FreeCAD MCP addon is **not available** in FreeCAD's built-in Addon Manager. You must install it **manually**.

### 1.1 Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/neka-nat/freecad-mcp.git
cd freecad-mcp
```

### 1.2 Copy the Addon to FreeCAD's Addon Directory

The FreeCAD Addon directory location varies by operating system:

#### Windows

```powershell
# Using PowerShell
xcopy /E /I addon\FreeCADMCP %APPDATA%\FreeCAD\Mod\FreeCADMCP
```

Or manually:
1. Navigate to: `%APPDATA%\FreeCAD\Mod\` (paste this in File Explorer address bar)
2. Copy the `addon/FreeCADMCP` folder there

#### macOS

```bash
cp -r addon/FreeCADMCP ~/Library/Application\ Support/FreeCAD/Mod/
```

#### Linux

**Ubuntu (standard install):**
```bash
cp -r addon/FreeCADMCP ~/.FreeCAD/Mod/
```

**Ubuntu (snap install):**
```bash
cp -r addon/FreeCADMCP ~/snap/freecad/common/Mod/
```

**Debian:**
```bash
cp -r addon/FreeCADMCP ~/.local/share/FreeCAD/Mod/
```

### 1.3 Restart FreeCAD

After copying the addon, **restart FreeCAD** completely.

### 1.4 Enable the MCP Addon

1. Open FreeCAD
2. From the **Workbench** dropdown (top toolbar), select **MCP Addon**
3. Click **Start RPC Server** in the FreeCAD MCP toolbar
4. Confirm you see: `RPC Server started at 0.0.0.0:9875`

---

## Step 2: Install UV Package Manager

**UV is critical** for running FreeCAD MCP with VS Code. It's a fast Python package and project manager.

> **Why UV?** UV manages the FreeCAD MCP server's Python dependencies and execution. Without it, the MCP server cannot start.

### 2.1 Install UV

#### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2.2 Verify Installation

After installation, **restart your terminal** and run:

```bash
uv --version
```

You should see output like: `uv 0.10.2 (a788db7e5 2026-02-10)`

### 2.3 Find UV's Full Path (Important for VS Code)

Run this command to get UV's full path:

**Windows (PowerShell):**
```powershell
(Get-Command uv).Source
```

**macOS/Linux:**
```bash
which uv
```

**Save this path** - you'll need it in the next step. Example output:
- Windows: `C:/Users/<YourUsername>/.local/bin/uv.exe`
- macOS: `/Users/<YourUsername>/.local/bin/uv`
- Linux: `/home/<YourUsername>/.local/bin/uv`

---

## Step 3: Configure VS Code MCP Settings

**Critical**: The configuration goes in `mcp.json`, **NOT** `settings.json`.

### 3.1 Locate the mcp.json File

The file is located at:

**Windows:**
```
%APPDATA%\Code\User\mcp.json
```
(Full path: `C:\Users\<YourUsername>\AppData\Roaming\Code\User\mcp.json`)

**macOS:**
```
~/Library/Application Support/Code/User/mcp.json
```

**Linux:**
```
~/.config/Code/User/mcp.json
```

### 3.2 Edit mcp.json

Open `mcp.json` in VS Code and add the FreeCAD MCP server configuration to the `"servers"` section:

```json
{
	"servers": {
		// ...existing servers like github/github-mcp-server...
		
		"freecad-mcp": {
			"type": "stdio",
			"command": "C:/Users/<YourUsername>/.local/bin/uv.exe",
			"args": [
				"--directory",
				"C:/Users/<YourUsername>/freecad-mcp",
				"run",
				"freecad-mcp"
			]
		}
	}
}
```

**Important notes:**

1. **Replace** `<YourUsername>` with your actual username
2. **Use the full path** to `uv.exe` (from Step 2.3)
3. **Use the full path** to your `freecad-mcp` directory (where you cloned the repo)
4. **Windows users**: Use forward slashes `/` or escaped backslashes `\\` in paths
5. **macOS/Linux users**: Remove `.exe` from the command path

**Example for Windows:**
```json
"freecad-mcp": {
	"type": "stdio",
	"command": "C:/Users/Zhang/.local/bin/uv.exe",
	"args": [
		"--directory",
		"C:/Users/Zhang/freecad-mcp",
		"run",
		"freecad-mcp"
	]
}
```

**Example for macOS/Linux:**
```json
"freecad-mcp": {
	"type": "stdio",
	"command": "/Users/zhang/.local/bin/uv",
	"args": [
		"--directory",
		"/Users/zhang/freecad-mcp",
		"run",
		"freecad-mcp"
	]
}
```

### 3.3 Reload VS Code

After saving `mcp.json`:
1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
2. Type and select: **Developer: Reload Window**

---

## Step 4: Verify the Setup

### 4.1 Check MCP Server Status

1. Open **GitHub Copilot Chat** in VS Code
2. Look at the MCP servers list in the chat interface
3. You should see **freecad-mcp** with status: **Running**, **11 tools**, **1 prompt**

### 4.2 Verify FreeCAD RPC Server

Make sure FreeCAD's RPC Server is running:
1. Open FreeCAD
2. Select **MCP Addon** workbench
3. Click **Start RPC Server**
4. Check the Report View for: `RPC Server started at 0.0.0.0:9875`

### 4.3 Test the Connection

In VS Code Copilot Chat, try creating a document:

```
@freecad-mcp create_document name=TestModel
```

If successful, you should see: `Document 'TestModel' created successfully`

---

## Step 5: Create Your First 3D Model

Now that everything is set up, create a simple 3D model:

### 5.1 Create a Document

```
@freecad-mcp create_document name=MyModel
```

### 5.2 Add a Box (Cube)

```
@freecad-mcp create_object doc_name=MyModel obj_type=Part::Box obj_name=Box obj_properties={"Length":100,"Width":50,"Height":30}
```

### 5.3 Add a Cylinder

```
@freecad-mcp create_object doc_name=MyModel obj_type=Part::Cylinder obj_name=Cylinder obj_properties={"Radius":20,"Height":80}
```

### 5.4 Add a Sphere

```
@freecad-mcp create_object doc_name=MyModel obj_type=Part::Sphere obj_name=Sphere obj_properties={"Radius":30}
```

---

## Available Commands

Here are the main FreeCAD MCP commands you can use in Copilot Chat:

| Command | Description |
|---------|-------------|
| `@freecad-mcp create_document` | Create a new FreeCAD document |
| `@freecad-mcp create_object` | Create a 3D object (Box, Cylinder, Sphere, etc.) |
| `@freecad-mcp edit_object` | Edit an existing object's properties |
| `@freecad-mcp delete_object` | Delete an object from the document |
| `@freecad-mcp execute_code` | Execute arbitrary Python code in FreeCAD |
| `@freecad-mcp get_objects` | List all objects in a document |
| `@freecad-mcp get_object` | Get details of a specific object |
| `@freecad-mcp list_documents` | List all open documents |
| `@freecad-mcp get_parts_list` | Get available parts from the library |
| `@freecad-mcp insert_part_from_library` | Insert a part from the library |

---

## Troubleshooting

### Issue 1: "spawn uv ENOENT" Error

**Symptom:** MCP server shows error: `Error spawn uv ENOENT`

**Solution:**
1. Make sure UV is installed: `uv --version`
2. Get UV's full path: `(Get-Command uv).Source` (Windows PowerShell)
3. Use the **full absolute path** in `mcp.json`, not just `uv`
4. Example: `"C:/Users/Zhang/.local/bin/uv.exe"`

### Issue 2: Commands Keep Spinning (No Response)

**Symptom:** Commands like `@freecad-mcp create_document` spin forever with no response.

**Solution:**
1. **Restart FreeCAD's RPC Server:**
   - In FreeCAD, click **Stop RPC Server**
   - Wait 3-5 seconds
   - Click **Start RPC Server**
   - Verify: `RPC Server started at 0.0.0.0:9875`

2. **Check FreeCAD's Report View** for errors:
   - View > Panels > Report view

3. **Reload VS Code:**
   - Press `Ctrl+Shift+P`
   - Select **Developer: Reload Window**

### Issue 3: "Unknown document" Error

**Symptom:** Error message: `NameError: Unknown document 'MyModel'`

**Solution:**
You must create the document first before creating objects:
```
@freecad-mcp create_document name=MyModel
```
Then create objects:
```
@freecad-mcp create_object doc_name=MyModel obj_type=Part::Box obj_name=Box
```

### Issue 4: MCP Server Shows "Error" Status

**Solution:**
1. Check VS Code's Output panel:
   - View > Output
   - Select **"MCP (Copilot)"** or **"GitHub Copilot Chat"** from dropdown
2. Look for error messages
3. Verify paths in `mcp.json` are correct and absolute
4. Ensure `freecad-mcp` directory exists at the specified path

### Issue 5: Configuration in settings.json Not Working

**Problem:** Adding `github.copilot.chat.mcp.remoteServers` in `settings.json` shows as grayed out.

**Solution:**
Don't use `settings.json`. Use `mcp.json` instead (see Step 3).

---

## Remote Connections (Advanced)

To control FreeCAD from another machine on your network:

### In FreeCAD:

1. Check **Remote Connections** in the FreeCAD MCP toolbar
2. Click **Configure Allowed IPs**
3. Enter allowed IP addresses or CIDR subnets:
   ```
   192.168.1.100, 10.0.0.0/24
   ```
4. Restart the RPC Server

### In mcp.json:

Add the `--host` flag:

```json
"freecad-mcp": {
	"type": "stdio",
	"command": "C:/Users/<YourUsername>/.local/bin/uv.exe",
	"args": [
		"--directory",
		"C:/Users/<YourUsername>/freecad-mcp",
		"run",
		"freecad-mcp",
		"--host", "192.168.1.100"
	]
}
```

Replace `192.168.1.100` with the IP address of the machine running FreeCAD.

---

## Additional Resources

- **FreeCAD MCP GitHub**: https://github.com/neka-nat/freecad-mcp
- **UV Documentation**: https://docs.astral.sh/uv/
- **FreeCAD Documentation**: https://wiki.freecad.org/
- **GitHub Copilot Chat**: https://docs.github.com/copilot/using-github-copilot/using-github-copilot-chat-in-your-ide

---

## FAQ

**Q: Can I use this with Claude Desktop?**  
A: Yes, but the configuration is different. See the [official README](https://github.com/neka-nat/freecad-mcp) for Claude Desktop setup.

**Q: Do I need a GitHub Copilot subscription?**  
A: Yes, GitHub Copilot (individual, business, or education) is required. The free tier doesn't support MCP servers.

**Q: Why does the command need `@freecad-mcp` and not `@freecad`?**  
A: The server name in `mcp.json` is `"freecad-mcp"`, so you must use the exact name with the hyphen.

**Q: Can I change the server name?**  
A: Yes, change `"freecad-mcp"` to any name you prefer in `mcp.json`, then use that name with `@`.

**Q: Where can I find more object types?**  
A: Check [FreeCAD's Part module documentation](https://wiki.freecad.org/Part_Module) for available primitives like `Part::Box`, `Part::Cylinder`, `Part::Sphere`, `Part::Cone`, `Part::Torus`, etc.

---

## License

FreeCAD MCP is licensed under the MIT License. See the [GitHub repository](https://github.com/neka-nat/freecad-mcp) for details.

---

**Happy 3D Modeling with FreeCAD and VS Code! 🚀**
