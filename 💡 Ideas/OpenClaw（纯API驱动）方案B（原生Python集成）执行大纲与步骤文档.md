# Ubuntu系统 OpenClaw（纯API驱动）方案B（原生Python集成）执行大纲与步骤文档

本文档对应方案B（原生Python集成），核心目标是实现“唤醒词+语音指令+语音回复”全闭环（对标小爱同学），全程采用原生Python集成Porcupine（唤醒）、Whisper.cpp（本地ASR）、Piper（本地TTS），无缝对接已部署的OpenClaw（纯API驱动），无需依赖Docker，兼顾灵活性、稳定性与隐私安全，完全衔接现有OpenClaw插件（缓存、屏幕OCR）及中断处理逻辑。

# 一、文档前置说明（衔接现有部署，明确前提）

## 1.1 基础前提（已完成，核对确认）

- 1.1.1 环境：Ubuntu桌面系统（Intel NUC/i5及以上，确保性能达标），已部署OpenClaw（纯API驱动，无本地模型），API Key（如Minimax）可正常使用。

- 1.1.2 现有配置：OpenClaw已加载缓存、屏幕OCR插件，具备系统命令执行、文件读写权限，已配置中断处理逻辑。

- 1.1.3 硬件：麦克风（优先外接，减少噪音）、扬声器可正常使用，无硬件故障。

- 1.1.4 依赖基础：Python 3.10+已安装，已升级pyaudio、sounddevice等音频库（之前语音优化已完成，可直接复用）。

## 1.2 核心目标

- 实现全离线语音交互核心模块（唤醒、ASR），仅复杂决策走OpenClaw关联的API，降低token消耗、提升响应速度。

- 达成小爱同学级体验：唤醒延迟<100ms、语音识别准确率≥95%、语音合成自然流畅，全闭环响应时间<2s。

- 深度对接OpenClaw，将语音模块封装为独立插件，与现有缓存、屏幕OCR插件联动，上下文流畅，可复用现有代码。

## 1.3 核心工具与版本（避坑关键）

- Porcupine：最新稳定版（支持中文唤醒词，footprint仅20KB，延迟低）。

- Whisper.cpp：最新版（推荐加载small中文模型，平衡速度与准确率；硬件充足可选用medium模型）。

- Piper：最新版（选用zh_CN-huayan-medium中文音色，自然度接近小爱同学）。

- Python依赖：确保whisper-cpp-python、piper-tts、pvporcupine等依赖版本兼容，避免版本冲突。

# 二、执行大纲（整体流程，贴合现有部署）

1. 前期准备：下载所需模型（Whisper中文模型、Piper中文模型），确认硬件与依赖兼容性。

2. 核心依赖安装：安装Porcupine、Whisper.cpp、Piper的Python依赖，与现有OpenClaw环境适配。

3. 唤醒词定制：在Picovoice Console训练自定义唤醒词（如“嘿，OpenClaw”），下载唤醒词模型。

4. Python脚本开发：编写核心桥接脚本，集成唤醒、ASR、TTS功能，对接OpenClaw API，复用现有音频降噪、异常处理逻辑。

5. 插件封装：将语音交互模块封装为OpenClaw独立插件（voice_offline.py），替换原有语音插件，加载到OpenClaw配置中。

6. 联动优化：对接现有缓存插件，实现TTS结果本地缓存；优化资源占用，避免影响OpenClaw运行。

7. 全流程测试：逐一测试唤醒、ASR、TTS、OpenClaw执行、语音反馈全闭环，排查异常。

8. 后期维护：制定模型更新、插件维护、异常排查流程，衔接现有OpenClaw维护逻辑。

# 三、详细执行步骤（可直接操作，避坑重点标注）

## 第一步：前期准备（10分钟，避坑核心）

### 1.1 模型下载（本地存储，避免运行卡顿）

- 1.1.1 Whisper中文模型：
       
下载地址：https://huggingface.co/ggerganov/whisper.cpp/tree/main/models
推荐下载：ggml-small-zh-q4_0.bin（体积小、速度快，适配Intel i5级别硬件），下载后放入 ~/.openclaw/models/whisper/ 目录（新建对应文件夹）。
      

- 1.1.2 Piper中文模型：
        
下载地址：https://github.com/rhasspy/piper-voices/releases
        
下载：zh_CN-huayan-medium.onnx（华艳音色，接近小爱同学）和 zh_CN-huayan-medium.onnx.json，放入 ~/.openclaw/models/piper/ 目录（新建对应文件夹）。
      

### 1.2 硬件兼容性验证（避免后期踩坑）

```bash
# 验证麦克风是否正常（复用之前的音频检测逻辑）
python3 -c "import sounddevice as sd; print(sd.query_devices()); sd.rec(10, samplerate=16000, channels=1); sd.wait()"
# 验证扬声器是否正常
mpg123 /usr/share/sounds/alsa/Front_Center.wav

```

说明：若麦克风/扬声器异常，先排查Ubuntu系统权限（设置→声音），优先切换外接麦克风/扬声器。

## 第二步：核心依赖安装（15分钟，适配现有OpenClaw环境）

注意：安装前先激活OpenClaw对应的Python环境（若有），避免依赖安装到全局环境，导致版本冲突。

```bash
# 升级pip，确保安装兼容性
pip3 install --upgrade pip

# 安装Porcupine依赖（唤醒词检测）
pip3 install pvporcupine pvrecorder  # pvrecorder用于音频采集，替代原生pyaudio，更稳定

# 安装Whisper.cpp依赖（本地ASR）
pip3 install whisper-cpp-python

# 安装Piper依赖（本地TTS）
pip3 install piper-tts

# 安装辅助依赖（复用之前的降噪、异常处理逻辑）
pip3 install scipy numpy soundfile

```

避坑提示：若安装whisper-cpp-python失败，先安装依赖库：sudo apt install -y build-essential cmake

## 第三步：唤醒词定制（10分钟，实现“嘿，OpenClaw”唤醒）

1. 访问Picovoice Console（免费注册）：https://console.picovoice.ai/

2. 创建应用，选择Porcupine，自定义唤醒词：输入“嘿，OpenClaw”，录制3-5条不同语气的语音样本（正常语速、稍慢语速、略带噪音），提升唤醒准确率。

3. 下载唤醒词模型（.ppn格式），选择Ubuntu系统适配版本，放入 ~/.openclaw/models/porcupine/ 目录。

4. 记录API Key（Picovoice Console中获取），用于后续脚本中加载唤醒词模型（仅首次加载验证，无网络依赖）。

## 第四步：Python核心桥接脚本开发（30分钟，复用现有代码，对接OpenClaw）

核心逻辑：持续监听→唤醒词检测→语音录制→本地ASR识别→调用OpenClaw执行→本地TTS合成→语音反馈，复用之前voice_stable.py的降噪、音频采集逻辑，衔接OpenClaw现有API。

### 4.1 新建脚本文件（封装为OpenClaw插件）

```bash
nano ~/.openclaw/plugins/voice_offline.py

```

### 4.2 编写脚本内容（完整可直接复制，标注处需替换为你的实际路径/Key）

```python
import os
import numpy as np
import sounddevice as sd
import whispercpp as wcpp
from piper.tts import PiperVoice
import pvporcupine
import pvrecorder
from scipy.io import wavfile
from datetime import datetime

# -------------------------- 配置参数（需替换为你的实际配置）--------------------------
# 模型路径（对应第一步下载的模型）
WHISPER_MODEL_PATH = "~/.openclaw/models/whisper/ggml-small-zh-q4_0.bin"
PIPER_MODEL_PATH = "~/.openclaw/models/piper/zh_CN-huayan-medium.onnx"
PIPER_CONFIG_PATH = "~/.openclaw/models/piper/zh_CN-huayan-medium.onnx.json"
PORCUPINE_MODEL_PATH = "~/.openclaw/models/porcupine/你的唤醒词模型.ppn"
PORCUPINE_ACCESS_KEY = "你的Picovoice API Key"  # 仅首次加载使用

# OpenClaw配置
OPENCLAW_WORK_DIR = "~/Desktop"
CACHE_PATH = "~/.openclaw/tts_cache/"  # 对接现有缓存插件，存储TTS结果
os.makedirs(CACHE_PATH, exist_ok=True)

# 音频参数（固定，适配所有模块）
SAMPLERATE = 16000
CHANNELS = 1
RECORD_DURATION = 5  # 唤醒后录制5秒语音指令
DEVICE = 0  # 麦克风设备编号（可通过sd.query_devices()查看）

# -------------------------- 初始化核心模块（复用现有逻辑，避免重复开发）--------------------------
# 初始化唤醒词检测（Porcupine）
porcupine = pvporcupine.create(
    access_key=PORCUPINE_ACCESS_KEY,
    model_path=os.path.expanduser(PORCUPINE_MODEL_PATH),
    keywords=["嘿，OpenClaw"]
)

# 初始化本地ASR（Whisper.cpp）
whisper_model = wcpp.Whisper(os.path.expanduser(WHISPER_MODEL_PATH))

# 初始化本地TTS（Piper）
piper_voice = PiperVoice(
    model_path=os.path.expanduser(PIPER_MODEL_PATH),
    config_path=os.path.expanduser(PIPER_CONFIG_PATH)
)

# 初始化音频采集（复用之前的降噪逻辑）
recorder = pvrecorder.PvRecorder(
    device_index=DEVICE,
    frame_length=porcupine.frame_length
)

# -------------------------- 辅助函数（缓存、降噪、异常处理，衔接现有配置）--------------------------
def get_cache_key(text):
    """生成TTS缓存键，对接现有缓存插件逻辑"""
    import hashlib
    return hashlib.md5(text.encode("utf-8")).hexdigest() + ".wav"

def tts_cache(text):
    """TTS结果缓存，避免重复合成，降低资源消耗"""
    cache_key = get_cache_key(text)
    cache_file = os.path.join(os.path.expanduser(CACHE_PATH), cache_key)
    if os.path.exists(cache_file):
        return cache_file
    # 合成语音并保存到缓存
    with open(cache_file, "wb") as f:
        for audio_bytes in piper_voice.synthesize(text):
            f.write(audio_bytes)
    return cache_file

def denoise_audio(audio_data):
    """降噪处理（复用之前voice_stable.py的逻辑）"""
    audio_data = audio_data / np.max(np.abs(audio_data))
    noise_threshold = 0.01
    audio_data[np.abs(audio_data)< noise_threshold] = 0
    return audio_data

def play_audio(audio_path):
    """播放语音（Ubuntu原生工具，稳定无依赖）"""
    os.system(f"mpg123 {audio_path} > /dev/null 2>&1")

# -------------------------- 核心逻辑（唤醒+ASR+OpenClaw执行+TTS反馈）--------------------------
def voice_interaction_loop():
    """语音交互全闭环，持续运行，对接OpenClaw"""
    print("等待唤醒词「嘿，OpenClaw」...（按Ctrl+C退出）")
    recorder.start()
    try:
        while True:
            # 1. 持续监听，检测唤醒词
            pcm = recorder.read()
            result = porcupine.process(pcm)
            if result >= 0:
                # 检测到唤醒词，播放提示音
                print("检测到唤醒词，准备接收指令...")
                play_audio("/usr/share/sounds/alsa/Front_Right.wav")

                # 2. 录制语音指令（带降噪）
                audio = sd.rec(
                    int(RECORD_DURATION * SAMPLERATE),
                    samplerate=SAMPLERATE,
                    channels=CHANNELS,
                    dtype='int16'
                )
                sd.wait()
                audio = denoise_audio(audio)
                temp_audio_path = "/tmp/voice_cmd.wav"
                wavfile.write(temp_audio_path, SAMPLERATE, audio)

                # 3. 本地ASR识别（无网络，不消耗token）
                result = whisper_model.transcribe(
                    temp_audio_path,
                    language="zh",
                    n_threads=4  # 限制CPU核心数，避免影响OpenClaw
                )
                os.remove(temp_audio_path)
                voice_cmd = result["text"].strip()
                print(f"识别到指令：{voice_cmd}")
                if not voice_cmd:
                    play_audio(tts_cache("未识别到有效指令，请重试"))
                    continue

                # 4. 调用OpenClaw执行指令（对接现有OpenClaw API）
                try:
                    import subprocess
                    # 调用OpenClaw执行指令，获取执行结果
                    openclaw_cmd = f"openclaw run --prompt '{voice_cmd}'"
                    response = subprocess.check_output(openclaw_cmd, shell=True, text=True)
                    print(f"OpenClaw执行结果：{response}")
                    # 5. 本地TTS合成反馈（使用缓存）
                    tts_file = tts_cache(f"已完成指令：{voice_cmd}，结果：{response[:50]}")
                    play_audio(tts_file)
                except Exception as e:
                    error_msg = f"指令执行失败：{str(e)[:30]}"
                    print(error_msg)
                    play_audio(tts_cache(error_msg))
    except KeyboardInterrupt:
        print("退出语音交互")
    finally:
        recorder.stop()
        porcupine.delete()
        recorder.delete()

# -------------------------- OpenClaw插件注册（衔接现有插件体系）--------------------------
def register_to_openclaw():
    return {
        "name": "voice_offline",
        "description": "原生Python集成的离线语音交互插件（Porcupine+Whisper+Piper），对标小爱同学",
        "functions": {
            "start_voice_interaction": voice_interaction_loop  # 启动语音交互全闭环
        }
    }

```

避坑提示：1. 替换所有标注“需替换”的路径和Key；2. 若硬件性能一般，将whisper_model.transcribe中的n_threads改为2，减少CPU占用。

## 第五步：插件集成与OpenClaw配置优化（10分钟，衔接现有配置）

### 5.1 加载新插件，替换原有语音插件

```bash
nano ~/.openclaw/config.yaml

```

更新plugins配置，删除原有voice_stable.py，添加新的离线语音插件，保留缓存、屏幕OCR插件：

```yaml
plugins:
  - ~/.openclaw/plugins/cache.py
  - ~/.openclaw/plugins/screen_ocr.py
  - ~/.openclaw/plugins/voice_offline.py  # 新增离线语音插件

# 保留原有其他配置（API、权限、记忆等），补充语音交互优化配置
voice:
  offline_mode: true  # 开启离线语音模式
  tts_cache_path: ~/.openclaw/tts_cache/  # 对接缓存插件
  whisper_threads: 4  # 适配硬件的CPU核心数

```

### 5.2 权限补充（避免执行失败）

```bash
# 给插件和模型目录赋予执行权限
sudo chmod -R 755 ~/.openclaw/plugins/
sudo chmod -R 755 ~/.openclaw/models/
# 确保OpenClaw能调用系统音频工具
sudo chmod +x /usr/bin/mpg123

```

## 第六步：联动优化（10分钟，提升体验，衔接现有缓存）

- 6.1 缓存联动：脚本中已实现TTS结果缓存，与现有OpenClaw缓存插件目录一致，无需额外配置，重复指令可直接调用缓存，提升响应速度。

- 6.2 资源优化：调整脚本中whisper的n_threads参数（根据CPU核心数，如i5为4核，设置为2-4），避免语音模块占用过多资源，导致OpenClaw卡顿。

- 6.3 异常处理衔接：脚本中已集成异常捕获（如指令执行失败、ASR识别失败），与你之前的OpenClaw中断处理逻辑一致，确保闭环不中断。

## 第七步：全流程测试（20分钟，验证对标小爱同学）

### 7.1 基础功能测试（逐一验证）

```bash
# 启动OpenClaw语音交互闭环
openclaw run --prompt "调用voice_offline插件的start_voice_interaction函数"

```

- 测试1：唤醒词测试——距离5米内说“嘿，OpenClaw”，验证是否能快速响应（延迟<100ms），无漏唤醒/误唤醒。

- 测试2：ASR识别测试——唤醒后说指令（如“帮我在桌面创建test文件夹”“关闭Chrome窗口”），验证识别准确率≥95%，环境噪音下≥90%。

- 测试3：TTS输出测试——验证语音合成自然流畅，无卡顿、无断音，音色接近小爱同学。

### 7.2 全闭环测试（核心）

- 测试场景1：唤醒→说“整理桌面文件，按类型分类”→OpenClaw执行→语音反馈执行结果，验证全流程≤2s，无中断。

- 测试场景2：唤醒→说“截取屏幕，识别当前窗口名称”→OpenClaw执行（调用屏幕OCR）→语音反馈结果，验证插件联动正常。

- 测试场景3：重复指令测试——连续2次说“列出桌面文件”，验证第二次TTS使用缓存，响应速度更快。

### 7.3 异常测试（避坑关键）

- 测试1：麦克风中断——拔掉麦克风，验证脚本提示异常，不崩溃，重新插上后可正常使用。

- 测试2：指令执行失败——说“删除系统文件夹”（无权限指令），验证语音反馈失败信息，OpenClaw不崩溃。

- 测试3：资源占用测试——同时执行语音交互+OpenClaw文件操作，验证CPU/内存占用正常，无卡顿。

## 第八步：后期维护（长期稳定运行，衔接现有维护逻辑）

- 8.1 模型维护：定期更新Whisper、Piper模型（每月1次），优化识别准确率和音色；唤醒词模型可根据使用场景，补充语音样本优化。

- 8.2 缓存维护：每周清理一次TTS缓存（rm -rf ~/.openclaw/tts_cache/*），避免缓存文件过多占用存储。

- 8.3 异常排查：
       
- 唤醒不灵敏：检查麦克风位置、唤醒词模型，补充语音样本重新训练；
        
- ASR识别不准：更新Whisper模型，调整降噪阈值；
        
- TTS卡顿：检查Piper模型路径，优化CPU核心数配置；
        
- 与OpenClaw联动失败：检查config.yaml插件加载配置，重启OpenClaw服务（openclaw restart）。
      

- 8.4 开机自启：将语音交互启动命令添加到OpenClaw开机自启脚本中（衔接之前的systemd服务），无需手动启动。

# 四、关键注意事项（避坑重点，上下文衔接）

- 1.  模型路径必须正确：所有模型（Whisper、Piper、Porcupine）的路径的路径需与脚本中配置一致，否则会导致模块初始化失败，建议使用绝对路径。

- 2.  版本兼容性：严格按照步骤安装依赖，避免版本冲突（尤其是whisper-cpp-python和Piper，版本不兼容会导致ASR/TTS失败）。

- 3.  资源占用控制：避免Whisper使用过多CPU核心，否则会影响OpenClaw正常执行，根据硬件情况调整n_threads参数。

- 4.  衔接现有配置：脚本中已复用之前的音频降噪、异常处理逻辑，缓存路径与现有缓存插件一致，无需大幅修改现有OpenClaw配置。

- 5.  隐私安全：唤醒、ASR、TTS全本地运行，仅OpenClaw的复杂决策走API，语音数据不上传，隐私性拉满，符合个人使用需求。

- 6.  唤醒词优化：若环境噪音较大，可在Picovoice Console补充更多带噪音的语音样本，提升唤醒准确率，对标小爱同学的唤醒可靠性。

# 五、验收标准（对标小爱同学，确保效果达标）

- 1.  唤醒：延迟<100ms，5米内唤醒准确率≥98%，无明显误唤醒（普通说话不触发）。

- 2.  ASR识别：正常环境下准确率≥95%，环境噪音下≥90%，无断音、识别错误。

- 3.  TTS输出：音色自然，接近小爱同学，无卡顿、无断音，延迟≤1s。

- 4.  全闭环：唤醒→识别→执行→反馈，总响应时间<2s，与OpenClaw、缓存插件联动正常。

- 5.  稳定性：连续运行1小时无崩溃，异常场景（麦克风中断、指令失败）可正常反馈，不影响OpenClaw整体运行。
> （注：文档部分内容可能由 AI 生成）