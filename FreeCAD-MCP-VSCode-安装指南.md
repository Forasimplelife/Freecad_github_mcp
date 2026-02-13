# FreeCAD MCP VS Code GitHub Copilot 安装指南

本指南详细介绍如何在 **VS Code GitHub Copilot Chat** 下配置 FreeCAD MCP（模型上下文协议），让你可以直接在 VS Code 中远程控制 FreeCAD。

> **注意：** 本文档专为 **VS Code + GitHub Copilot** 用户编写，官方 README 针对 Claude Desktop，很多内容并不适用 VS Code。

---

## 前置条件

- 已安装 **FreeCAD**（建议最新版）
- 已安装并激活 **VS Code** 和 **GitHub Copilot** 扩展
- 已安装 **Git**
- 能联网下载依赖

---

## 步骤1：安装 FreeCAD MCP 插件

FreeCAD MCP 插件**无法通过 FreeCAD 自带的插件管理器安装**，需手动安装。

### 1.1 克隆仓库

打开终端，执行：

```bash
git clone https://github.com/neka-nat/freecad-mcp.git
cd freecad-mcp
```

### 1.2 复制插件到 FreeCAD 插件目录

不同操作系统插件目录如下：

#### Windows

```powershell
# PowerShell 命令
xcopy /E /I addon\FreeCADMCP %APPDATA%\FreeCAD\Mod\FreeCADMCP
```

或手动：
1. 打开 `%APPDATA%\FreeCAD\Mod\`（可在资源管理器地址栏粘贴）
2. 将 `addon/FreeCADMCP` 文件夹复制进去

#### macOS

```bash
cp -r addon/FreeCADMCP ~/Library/Application\ Support/FreeCAD/Mod/
```

#### Linux

**Ubuntu（标准安装）：**
```bash
cp -r addon/FreeCADMCP ~/.FreeCAD/Mod/
```

**Ubuntu（snap 安装）：**
```bash
cp -r addon/FreeCADMCP ~/snap/freecad/common/Mod/
```

**Debian：**
```bash
cp -r addon/FreeCADMCP ~/.local/share/FreeCAD/Mod/
```

### 1.3 重启 FreeCAD

复制完成后，**彻底重启 FreeCAD**。

### 1.4 启用 MCP 插件

1. 打开 FreeCAD
2. 顶部工具栏 Workbench 下拉选择 **MCP Addon**
3. 点击 FreeCAD MCP 工具栏的 **Start RPC Server**
4. 确认提示：`RPC Server started at 0.0.0.0:9875`

---

## 步骤2：安装 UV 包管理器

**UV 是 FreeCAD MCP 在 VS Code 下运行的关键依赖。**

> **为什么要用 UV？** UV 负责管理 FreeCAD MCP 的 Python 依赖和运行环境，没有它 MCP 服务器无法启动。

### 2.1 安装 UV

#### Windows（PowerShell）

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2.2 验证安装

安装后**重启终端**，执行：

```bash
uv --version
```

应输出类似：`uv 0.10.2 (a788db7e5 2026-02-10)`

### 2.3 获取 UV 的完整路径（VS Code 必须）

**Windows（PowerShell）：**
```powershell
(Get-Command uv).Source
```

**macOS/Linux：**
```bash
which uv
```

**记下此路径**，下一步要用。例如：
- Windows: `C:/Users/<你的用户名>/.local/bin/uv.exe`
- macOS: `/Users/<你的用户名>/.local/bin/uv`
- Linux: `/home/<你的用户名>/.local/bin/uv`

---

## 步骤3：配置 VS Code MCP

**重点：** 配置写在 `mcp.json`，**不是** `settings.json`！

### 3.1 找到 mcp.json 文件

**Windows：**
```
%APPDATA%\Code\User\mcp.json
```
（完整路径：`C:\Users\<你的用户名>\AppData\Roaming\Code\User\mcp.json`）

**macOS：**
```
~/Library/Application Support/Code/User/mcp.json
```

**Linux：**
```
~/.config/Code/User/mcp.json
```

### 3.2 编辑 mcp.json

在 `"servers"` 节点下添加 FreeCAD MCP 配置：

```json
"freecad-mcp": {
    "type": "stdio",
    "command": "C:/Users/<你的用户名>/.local/bin/uv.exe",
    "args": [
        "--directory",
        "C:/Users/<你的用户名>/freecad-mcp",
        "run",
        "freecad-mcp"
    ]
}
```

**注意事项：**
1. `<你的用户名>` 替换为实际用户名
2. `uv.exe` 路径用上一步查到的完整路径
3. `freecad-mcp` 路径为你克隆仓库的位置
4. Windows 路径可用 `/` 或 `\\`
5. macOS/Linux 不要 `.exe`

### 3.3 重载 VS Code

保存后：
1. `Ctrl+Shift+P`（Win/Linux）或 `Cmd+Shift+P`（Mac）
2. 输入并选择：**Developer: Reload Window**

---

## 步骤4：验证配置

### 4.1 检查 MCP 服务器状态

1. 打开 VS Code Copilot Chat
2. 查看 MCP 服务器列表
3. 应看到 **freecad-mcp**，状态为 Running，11 tools，1 prompt

### 4.2 检查 FreeCAD RPC Server

1. FreeCAD 选择 MCP Addon 工作台
2. 点击 **Start RPC Server**
3. Report View 看到：`RPC Server started at 0.0.0.0:9875`

### 4.3 测试连接

在 Copilot Chat 输入：
```
@freecad-mcp create_document name=TestModel
```
如成功会返回：`Document 'TestModel' created successfully`

---

## 步骤5：创建第一个 3D 模型

### 5.1 创建文档
```
@freecad-mcp create_document name=MyModel
```

### 5.2 添加立方体
```
@freecad-mcp create_object doc_name=MyModel obj_type=Part::Box obj_name=Box obj_properties={"Length":100,"Width":50,"Height":30}
```

### 5.3 添加圆柱体
```
@freecad-mcp create_object doc_name=MyModel obj_type=Part::Cylinder obj_name=Cylinder obj_properties={"Radius":20,"Height":80}
```

### 5.4 添加球体
```
@freecad-mcp create_object doc_name=MyModel obj_type=Part::Sphere obj_name=Sphere obj_properties={"Radius":30}
```

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `@freecad-mcp create_document` | 创建新文档 |
| `@freecad-mcp create_object` | 创建 3D 对象（立方体、圆柱、球等）|
| `@freecad-mcp edit_object` | 编辑对象属性 |
| `@freecad-mcp delete_object` | 删除对象 |
| `@freecad-mcp execute_code` | 执行 FreeCAD Python 代码 |
| `@freecad-mcp get_objects` | 列出文档所有对象 |
| `@freecad-mcp get_object` | 获取对象详情 |
| `@freecad-mcp list_documents` | 列出所有文档 |
| `@freecad-mcp get_parts_list` | 获取零件库列表 |
| `@freecad-mcp insert_part_from_library` | 插入零件库零件 |

---

## 常见问题排查

### 问题1：spawn uv ENOENT

**现象：** MCP 报错 `Error spawn uv ENOENT`

**解决：**
1. 确认已安装 UV：`uv --version`
2. 用完整路径写在 mcp.json
3. 例：`"C:/Users/Zhang/.local/bin/uv.exe"`

### 问题2：命令一直转圈无响应

**现象：** 命令无响应

**解决：**
1. 重启 FreeCAD 的 RPC Server
2. 检查 Report View 是否有报错
3. 重载 VS Code

### 问题3：Unknown document

**现象：** `NameError: Unknown document 'MyModel'`

**解决：** 先创建文档再创建对象

### 问题4：MCP Server 显示 Error

**解决：**
1. 检查 VS Code Output 面板
2. 检查 mcp.json 路径
3. 检查 freecad-mcp 目录是否存在

### 问题5：settings.json 配置无效

**解决：**
不要用 settings.json，必须用 mcp.json

---

## 远程连接（进阶）

FreeCAD 支持远程控制：
1. FreeCAD MCP 工具栏勾选 Remote Connections
2. 配置 Allowed IPs
3. mcp.json 增加 --host 参数

---

## 参考资料

- [FreeCAD MCP GitHub](https://github.com/neka-nat/freecad-mcp)
- [UV 官方文档](https://docs.astral.sh/uv/)
- [FreeCAD 官方文档](https://wiki.freecad.org/)
- [GitHub Copilot Chat](https://docs.github.com/copilot/using-github-copilot/using-github-copilot-chat-in-your-ide)

---

**祝你用 FreeCAD + VS Code 玩得开心！**
