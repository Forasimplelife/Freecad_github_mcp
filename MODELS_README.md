---
noteId: "24d70af008bd11f1b1eaf70624350159"
tags: []

---

# FreeCAD MCP 精美模型脚本集

## 📋 概述

这个项目包含多个通过 VS Code 和 FreeCAD MCP Server 生成精美 3D 模型的 Python 脚本。每个脚本都可以独立运行，生成特定的 3D 模型。

## ⚙️ 工作原理

### 关于 MCP 连接方式

这些脚本使用 XML-RPC 协议与 FreeCAD MCP Server 通信：

```python
server = xmlrpc.client.ServerProxy("http://localhost:9875")
```

**重要说明**：
- ✅ **必须先启动 FreeCAD MCP Server**，脚本才能正常运行
- ❌ **如果没有 MCP Server 运行**，连接会失败并报错
- 🔄 MCP Server 作为中间层，接收 Python 代码并在 FreeCAD 中执行

### VS Code 脚本 vs 直接在 FreeCAD 中运行

| 方式 | 说明 | 优势 |
|------|------|------|
| **VS Code + MCP** | 通过 XML-RPC 远程调用 FreeCAD | ✅ 可在 VS Code 中编写和调试<br>✅ 更好的代码管理<br>✅ 可集成到其他应用 |
| **FreeCAD 直接运行** | 在 FreeCAD 控制台或宏中运行 | ✅ 无需 MCP Server<br>✅ 更直接的执行 |

## 🎨 模型列表

### 1. Gear.py - 齿轮 ⚙️
生成一个精密的齿轮模型，包含：
- 20 个齿
- 可调节的模数和齿高
- 中心孔
- 金色外观

**特点**：适合机械设计和工程项目

### 2. Vase.py - 花瓶 🏺
生成一个优雅的花瓶模型，包含：
- 光滑的曲线轮廓
- 空心内部结构
- 自然的腹部膨胀和颈部收缩
- 陶瓷白色外观

**特点**：展示旋转建模和曲线设计

### 3. Spiral_Staircase.py - 螺旋楼梯 🌀
生成一个精美的螺旋楼梯，包含：
- 16 级台阶
- 中心支撑柱
- 螺旋扶手
- 木纹色台阶渐变效果

**特点**：适合建筑可视化和室内设计

### 4. Diamond.py - 钻石 💎
生成一个切割钻石模型，包含：
- 多刻面设计
- 亭部（下部）和冠部（上部）
- 透明晶体材质
- 8 刻面对称结构

**特点**：展示精密建模和材质设置

### 5. Coffee_Cup.py - 咖啡杯 ☕
生成一个逼真的咖啡杯，包含：
- 空心杯体
- 曲线把手
- 咖啡色陶瓷外观
- 平滑的连接点

**特点**：适合产品设计和渲染

### 6. Spring.py - 弹簧 🌸
生成一个螺旋弹簧模型，包含：
- 10 圈线圈
- 可调节的螺距和直径
- 金属银色外观
- 顶部和底部支撑平面

**特点**：展示螺旋线扫掠技术

## 🚀 使用方法

### 前置条件

1. **安装 FreeCAD**
   - 下载并安装 FreeCAD：https://www.freecad.org/

2. **安装 FreeCAD MCP Server**
   - 在 VS Code 中配置 FreeCAD MCP
   - 确保 MCP Server 监听在 `http://localhost:9875`

3. **Python 环境**
   - Python 3.x
   - 无需额外的 Python 包（使用标准库）

### 运行步骤

1. **启动 FreeCAD MCP Server**
   ```bash
   # 确保 FreeCAD MCP Server 正在运行
   # 可以通过 @freecad-mcp 在 VS Code 中激活
   ```

2. **运行任意脚本**
   ```bash
   # 在 VS Code 终端中运行
   python Gear.py
   python Vase.py
   python Spiral_Staircase.py
   python Diamond.py
   python Coffee_Cup.py
   python Spring.py
   ```

3. **查看结果**
   - 模型将在 FreeCAD 窗口中自动生成
   - 可以在 FreeCAD 中进一步编辑和导出

## 🔧 自定义参数

每个脚本都包含可调节的参数。例如在 `Gear.py` 中：

```python
# 齿轮参数
num_teeth = 20  # 齿数（可修改）
module = 3  # 模数（可修改）
thickness = 10  # 齿轮厚度（可修改）
```

您可以修改这些参数来生成不同规格的模型。

## ⚠️ 常见问题

### 问题 1：连接失败
```
❌ 连接或执行失败: [Errno 10061] No connection could be made...
```

**解决方案**：
1. 确认 FreeCAD MCP Server 已启动
2. 检查端口 9875 是否被占用
3. 尝试重启 FreeCAD MCP Server

### 问题 2：模型未显示
**解决方案**：
1. 检查 FreeCAD 窗口是否打开
2. 在 FreeCAD 中点击 "View" → "Fit All" 查看完整模型
3. 检查脚本输出的错误信息

### 问题 3：执行缓慢
**解决方案**：
1. 复杂模型（如螺旋楼梯）需要更多计算时间
2. 减少参数值（如台阶数、刻面数）可提高速度
3. 等待 `doc.recompute()` 完成

## 📚 进阶学习

### 修改模型

每个脚本都有详细的注释。您可以：
- 调整几何参数
- 修改颜色和材质
- 添加新的特征
- 组合多个模型

### FreeCAD API 参考

- [FreeCAD Python 脚本教程](https://wiki.freecad.org/Python_scripting_tutorial)
- [Part 模块文档](https://wiki.freecad.org/Part_Module)
- [Draft 模块文档](https://wiki.freecad.org/Draft_Module)

## 🤝 贡献

欢迎提交新的模型脚本！请确保：
- 代码有清晰的注释
- 参数可以轻松调整
- 包含模型的简要说明

## 📄 许可证

MIT License - 自由使用和修改

---

**享受 3D 建模的乐趣！** 🎉
