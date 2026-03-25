	# Ubuntu系统 OpenClaw 语音集成方案
## （2026-02-25 修订版 - 根据实际情况）

---

# 一、当前情况（已具备）

| 项目          | 状态                                      |
| ----------- | --------------------------------------- |
| Ubuntu 系统   | ✅ Lenovo XiaoXin Pro 13 (2020) AMD 版本 |
| OpenClaw    | ✅ 2026.2.23，已开机自启                       |
| Python 3.13 | ✅ 已安装                                   |
| 麦克风         | ⚠️ 需测试                                  |
| 扬声器         | ✅ 内置                                    |

---

# 二、目标

实现"**唤醒 → 语音输入 → 执行 → 语音输出**"全闭环

---

# 三、需要的组件

| 模块 | 工具 | 模型大小 | 用途 |
|------|------|----------|------|
| 唤醒 | Porcupine | ~20KB | 检测"嘿，小小海" |
| 语音识别 | Whisper.cpp | ~75MB (small) | 本地转文字 |
| 语音合成 | Piper | ~150MB | 中文语音输出 |
| 执行 | OpenClaw | - | 执行命令 |

---

# 四、执行步骤

## 第一步：测试麦克风

```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

## 第二步：安装依赖

```bash
# 音频库
pip3 install --break-system-packages sounddevice numpy scipy soundfile

# Whisper.cpp Python 绑定
pip3 install --break-system-packages whispercpp

# Piper TTS
pip3 install --break-system-packages piper-tts

# Porcupine 唤醒
pip3 install --break-system-packages pvporcupine pvrecorder
```

## 第三步：下载模型

```bash
# 创建模型目录
mkdir -p ~/.openclaw/models/{whisper,piper,porcupine}

# Whisper 中文小模型（推荐 small，速度快）
# 下载：https://huggingface.co/ggerganov/whisper.cpp/tree/main/models
# 文件：ggml-small-zh-q4_0.bin

# Piper 中文模型
# 下载：https://github.com/rhasspy/piper-voices
# 文件：zh_CN-huayan-medium.onnx + .json
```

## 第四步：编写核心脚本

编写 `voice_agent.py`，实现：
1. 监听唤醒词
2. 录音
3. Whisper 识别
4. 调用 OpenClaw 执行
5. Piper 输出语音

## 第五步：测试全流程

```bash
python3 ~/.openclaw/scripts/voice_agent.py
```

---

# 五、简化版 vs 完整版

| 版本 | 唤醒 | ASR | TTS | 复杂度 |
|------|------|-----|-----|--------|
| 简化版 | 按钮 | API | TTS工具 | ⭐ |
| 完整版 | Porcupine | Whisper | Piper | ⭐⭐⭐ |

---

# 六、建议

**先做简化版**：
1. 用按钮/关键词触发（不用唤醒词）
2. 用现有 TTS 工具输出
3. 验证流程后再升级完整版

---

# 七、待确认

| 项目 | 状态 |
|------|------|
| 麦克风测试 | ⏳ 待做 |
| 模型下载 | ⏳ 待做 |
| 脚本开发 | ⏳ 待做 |

---

*修订日期：2026-02-25*
*修订人：小小海*
