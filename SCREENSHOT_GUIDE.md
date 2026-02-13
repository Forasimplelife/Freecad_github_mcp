# FreeCAD 模型截图功能说明

## 📸 自动截图功能

所有脚本现在都会在生成模型后自动保存截图到 `images` 文件夹！

### 功能说明

1. **自动创建文件夹**：如果 `images` 文件夹不存在，会自动创建
2. **高分辨率截图**：保存为 1920x1080 像素的 PNG 图片
3. **白色背景**：使用白色背景，适合展示和文档使用
4. **自动命名**：每个模型都有对应的图片名称

### 截图文件列表

运行脚本后，将在 `images` 文件夹中生成以下截图：

- `Gear.png` - 齿轮模型
- `Vase.png` - 花瓶模型
- `Spiral_Staircase.png` - 螺旋楼梯模型
- `Diamond.png` - 钻石模型
- `Coffee_Cup.png` - 咖啡杯模型
- `Spring.png` - 弹簧模型
- `FancyBox.png` - 基础盒子模型

### 技术实现

脚本使用以下 FreeCAD 命令保存截图：

```python
import FreeCADGui as Gui

# 自动调整视图以显示完整模型
Gui.SendMsgToActiveView("ViewFit")

# 保存截图
Gui.activeDocument().activeView().saveImage(
    image_path,  # 保存路径
    1920,        # 宽度（像素）
    1080,        # 高度（像素）
    'White'      # 背景颜色
)
```

### 自定义截图设置

您可以在脚本中修改以下参数：

1. **分辨率**：修改 `1920, 1080` 为其他尺寸
2. **背景颜色**：将 `'White'` 改为 `'Black'`、`'Transparent'` 等
3. **保存路径**：修改 `image_dir` 变量

### 示例：修改截图分辨率

```python
# 4K 分辨率
Gui.activeDocument().activeView().saveImage(image_path, 3840, 2160, 'White')

# HD 分辨率
Gui.activeDocument().activeView().saveImage(image_path, 1280, 720, 'White')

# 方形截图
Gui.activeDocument().activeView().saveImage(image_path, 1080, 1080, 'White')
```

### 示例：修改背景颜色

```python
# 黑色背景
Gui.activeDocument().activeView().saveImage(image_path, 1920, 1080, 'Black')

# 透明背景（PNG）
Gui.activeDocument().activeView().saveImage(image_path, 1920, 1080, 'Transparent')

# 当前背景（使用 FreeCAD 设置的背景）
Gui.activeDocument().activeView().saveImage(image_path, 1920, 1080, 'Current')
```

## 🎯 使用方法

运行任意模型脚本，截图会自动保存：

```bash
python Gear.py
# 输出：✅ 齿轮模型已生成！去 FreeCAD 窗口查看效果！
#       截图已保存到: c:\...\images\Gear.png
```

## 📂 文件夹结构

```
Freecad_github_mcp/
├── images/                  # 自动生成的截图文件夹
│   ├── Gear.png
│   ├── Vase.png
│   ├── Spiral_Staircase.png
│   ├── Diamond.png
│   ├── Coffee_Cup.png
│   ├── Spring.png
│   └── FancyBox.png
├── Gear.py                  # 脚本文件
├── Vase.py
├── ...
└── SCREENSHOT_GUIDE.md      # 本文档
```

## 💡 注意事项

1. **FreeCAD GUI 必须运行**：截图功能需要 FreeCAD 的图形界面，无法在纯命令行模式下使用
2. **MCP Server 必须启动**：确保 FreeCAD MCP Server 正在运行
3. **截图会覆盖**：每次运行脚本都会覆盖同名的截图文件
4. **路径问题**：如果您的工作目录不同，请修改脚本中的 `script_dir` 变量

## 🔧 故障排除

### 问题：截图未保存

**可能原因**：
- FreeCAD GUI 未运行
- 权限不足，无法创建文件夹或写入文件
- 路径配置错误

**解决方案**：
1. 确认 FreeCAD 窗口已打开
2. 检查文件系统权限
3. 验证控制台输出的截图路径是否正确

### 问题：截图为空白或不完整

**解决方案**：
- 在 `saveImage` 之前添加延迟：
  ```python
  import time
  time.sleep(1)  # 等待渲染完成
  Gui.activeDocument().activeView().saveImage(...)
  ```
- 确保 `doc.recompute()` 已执行
- 使用 `ViewFit` 确保模型在视图中可见

---

**享受自动化截图功能！** 📸✨
