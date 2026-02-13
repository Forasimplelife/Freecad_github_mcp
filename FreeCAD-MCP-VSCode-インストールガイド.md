# FreeCAD MCP VS Code GitHub Copilot インストールガイド

このガイドは、**VS Code GitHub Copilot Chat** で FreeCAD MCP（モデルコンテキストプロトコル）をセットアップし、VS Code から FreeCAD を直接操作する方法を説明します。

> **注意：** 本ガイドは **VS Code + GitHub Copilot** 専用です。公式 README は Claude Desktop 用であり、多くの手順は VS Code には適用されません。

---

## 前提条件

- **FreeCAD**（最新版推奨）
- **VS Code** と **GitHub Copilot** 拡張機能がインストール・有効化されていること
- **Git** がインストールされていること
- インターネット接続

---

## ステップ1：FreeCAD MCP アドオンのインストール

FreeCAD MCP アドオンは FreeCAD のアドオンマネージャーにはありません。**手動でインストール**する必要があります。

### 1.1 リポジトリのクローン

ターミナルで以下を実行：

```bash
git clone https://github.com/neka-nat/freecad-mcp.git
cd freecad-mcp
```

### 1.2 アドオンを FreeCAD のアドオンディレクトリにコピー

OSごとのアドオンディレクトリ：

#### Windows

```powershell
# PowerShell
xcopy /E /I addon\FreeCADMCP %APPDATA%\FreeCAD\Mod\FreeCADMCP
```

または手動で：
1. `%APPDATA%\FreeCAD\Mod\` に移動（エクスプローラーのアドレスバーに貼り付け）
2. `addon/FreeCADMCP` フォルダをコピー

#### macOS

```bash
cp -r addon/FreeCADMCP ~/Library/Application\ Support/FreeCAD/Mod/
```

#### Linux

**Ubuntu（標準インストール）：**
```bash
cp -r addon/FreeCADMCP ~/.FreeCAD/Mod/
```

**Ubuntu（snap）：**
```bash
cp -r addon/FreeCADMCP ~/snap/freecad/common/Mod/
```

**Debian：**
```bash
cp -r addon/FreeCADMCP ~/.local/share/FreeCAD/Mod/
```

### 1.3 FreeCAD を再起動

コピー後、**FreeCAD を完全に再起動**してください。

### 1.4 MCP アドオンを有効化

1. FreeCAD を開く
2. ワークベンチで **MCP Addon** を選択
3. FreeCAD MCP ツールバーで **Start RPC Server** をクリック
4. `RPC Server started at 0.0.0.0:9875` と表示されることを確認

---

## ステップ2：UV パッケージマネージャのインストール

**UV は VS Code で FreeCAD MCP を動かすために必須です。**

> **なぜ UV？** UV は FreeCAD MCP サーバーの Python 依存関係と実行を管理します。UV がないと MCP サーバーは起動できません。

### 2.1 UV のインストール

#### Windows（PowerShell）

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2.2 インストール確認

インストール後、**ターミナルを再起動**し：

```bash
uv --version
```

例：`uv 0.10.2 (a788db7e5 2026-02-10)`

### 2.3 UV のフルパスを取得（VS Code 用）

**Windows（PowerShell）：**
```powershell
(Get-Command uv).Source
```

**macOS/Linux：**
```bash
which uv
```

**このパスをメモ**してください。例：
- Windows: `C:/Users/<ユーザー名>/.local/bin/uv.exe`
- macOS: `/Users/<ユーザー名>/.local/bin/uv`
- Linux: `/home/<ユーザー名>/.local/bin/uv`

---

## ステップ3：VS Code MCP 設定

**重要：** 設定は `mcp.json` に記述し、`settings.json` には書かないでください。

### 3.1 mcp.json ファイルの場所

**Windows：**
```
%APPDATA%\Code\User\mcp.json
```
（例：`C:\Users\<ユーザー名>\AppData\Roaming\Code\User\mcp.json`）

**macOS：**
```
~/Library/Application Support/Code/User/mcp.json
```

**Linux：**
```
~/.config/Code/User/mcp.json
```

### 3.2 mcp.json の編集

`"servers"` セクションに FreeCAD MCP を追加：

```json
"freecad-mcp": {
    "type": "stdio",
    "command": "C:/Users/<ユーザー名>/.local/bin/uv.exe",
    "args": [
        "--directory",
        "C:/Users/<ユーザー名>/freecad-mcp",
        "run",
        "freecad-mcp"
    ]
}
```

**注意：**
1. `<ユーザー名>` を実際のユーザー名に置き換え
2. uv.exe のフルパスを使う
3. freecad-mcp ディレクトリもフルパス
4. Windows は `/` または `\\` でOK
5. macOS/Linux は `.exe` 不要

### 3.3 VS Code をリロード

保存後：
1. `Ctrl+Shift+P`（Win/Linux）または `Cmd+Shift+P`（Mac）
2. **Developer: Reload Window** を選択

---

## ステップ4：セットアップ確認

### 4.1 MCP サーバーの状態確認

1. VS Code Copilot Chat を開く
2. MCP サーバーリストを確認
3. **freecad-mcp** が Running、11 tools、1 prompt で表示されていること

### 4.2 FreeCAD RPC サーバーの確認

1. FreeCAD で MCP Addon ワークベンチを選択
2. **Start RPC Server** をクリック
3. Report View で `RPC Server started at 0.0.0.0:9875` を確認

### 4.3 接続テスト

Copilot Chat で：
```
@freecad-mcp create_document name=TestModel
```
成功すれば：`Document 'TestModel' created successfully` と返る

---

## ステップ5：3D モデルを作成

### 5.1 ドキュメント作成
```
@freecad-mcp create_document name=MyModel
```

### 5.2 ボックス追加
```
@freecad-mcp create_object doc_name=MyModel obj_type=Part::Box obj_name=Box obj_properties={"Length":100,"Width":50,"Height":30}
```

### 5.3 シリンダー追加
```
@freecad-mcp create_object doc_name=MyModel obj_type=Part::Cylinder obj_name=Cylinder obj_properties={"Radius":20,"Height":80}
```

### 5.4 スフィア追加
```
@freecad-mcp create_object doc_name=MyModel obj_type=Part::Sphere obj_name=Sphere obj_properties={"Radius":30}
```

---

## 主なコマンド

| コマンド | 説明 |
|----------|------|
| `@freecad-mcp create_document` | 新規ドキュメント作成 |
| `@freecad-mcp create_object` | 3Dオブジェクト作成（ボックス、シリンダー、スフィア等）|
| `@freecad-mcp edit_object` | オブジェクトのプロパティ編集 |
| `@freecad-mcp delete_object` | オブジェクト削除 |
| `@freecad-mcp execute_code` | FreeCAD Python コード実行 |
| `@freecad-mcp get_objects` | ドキュメント内の全オブジェクト一覧 |
| `@freecad-mcp get_object` | オブジェクト詳細取得 |
| `@freecad-mcp list_documents` | 全ドキュメント一覧 |
| `@freecad-mcp get_parts_list` | パーツライブラリ一覧取得 |
| `@freecad-mcp insert_part_from_library` | パーツライブラリから挿入 |

---

## トラブルシューティング

### 問題1：spawn uv ENOENT

**現象：** MCP サーバーが `Error spawn uv ENOENT` を表示

**対策：**
1. UV がインストールされているか確認：`uv --version`
2. mcp.json でフルパスを指定
3. 例：`"C:/Users/Zhang/.local/bin/uv.exe"`

### 問題2：コマンドが無反応

**現象：** コマンドが応答しない

**対策：**
1. FreeCAD の RPC Server を再起動
2. Report View でエラー確認
3. VS Code をリロード

### 問題3：Unknown document

**現象：** `NameError: Unknown document 'MyModel'`

**対策：** 先にドキュメントを作成してからオブジェクトを作成

### 問題4：MCP Server が Error

**対策：**
1. VS Code Output パネルでエラー確認
2. mcp.json のパス確認
3. freecad-mcp ディレクトリの存在確認

### 問題5：settings.json 設定が効かない

**対策：**
settings.json ではなく mcp.json を使う

---

## リモート接続（上級）

FreeCAD をネットワーク越しに操作する場合：
1. FreeCAD MCP ツールバーで Remote Connections を有効化
2. Allowed IPs を設定
3. mcp.json に --host オプションを追加

---

## 参考リンク

- [FreeCAD MCP GitHub](https://github.com/neka-nat/freecad-mcp)
- [UV 公式ドキュメント](https://docs.astral.sh/uv/)
- [FreeCAD 公式ドキュメント](https://wiki.freecad.org/)
- [GitHub Copilot Chat](https://docs.github.com/copilot/using-github-copilot/using-github-copilot-chat-in-your-ide)

---

**FreeCAD + VS Code で楽しい 3D モデリングを！**
