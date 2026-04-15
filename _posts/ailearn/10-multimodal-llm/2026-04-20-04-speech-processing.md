---
layout: post
title: "语音处理 - ASR与TTS"
date: 2026-04-20
categories: ailearn
tags: [AI, 多模态, 语音识别, 语音合成]
keywords: ASR, TTS, Whisper, 语音识别, 语音合成
---

* content
{:toc}

> **前置知识**：需要先掌握 Transformer基础
>
> **本文重点**：语音识别与语音合成

---

## 一、语音识别 (ASR)

### 1.1 Whisper模型

```python
import whisper

# 加载模型
model = whisper.load_model("base")  # tiny/base/small/medium/large

# 转录音频
result = model.transcribe("audio.mp3")
print(result["text"])

# 获取详细结果
for segment in result["segments"]:
    print(f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}")

# 指定语言
result = model.transcribe("audio.mp3", language="zh")
```

### 1.2 使用HuggingFace

```python
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torchaudio

# 加载模型
processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

# 加载音频
waveform, sample_rate = torchaudio.load("audio.mp3")

# 重采样到16kHz
if sample_rate != 16000:
    resampler = torchaudio.transforms.Resample(sample_rate, 16000)
    waveform = resampler(waveform)

# 预处理
input_features = processor(
    waveform.squeeze().numpy(),
    sampling_rate=16000,
    return_tensors="pt"
).input_features

# 推理
predicted_ids = model.generate(input_features)
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print(transcription[0])
```

---

## 二、语音合成 (TTS)

### 2.1 使用Edge TTS

```python
import edge_tts
import asyncio

async def text_to_speech(text, output_file):
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(output_file)

# 使用
asyncio.run(text_to_speech("你好，欢迎使用语音合成", "output.mp3"))

# 列出可用声音
voices = await edge_tts.list_voices()
for voice in voices:
    if voice["Locale"].startswith("zh"):
        print(f"{voice['ShortName']}: {voice['FriendlyName']}")
```

### 2.2 使用Coqui TTS

```python
from TTS.api import TTS

# 初始化
tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC", progress_bar=True)

# 合成
tts.tts_to_file(text="你好，世界", file_path="output.wav")

# 多语言模型
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")
tts.tts_to_file("Hello world", speaker="en_0", language="en", file_path="output.wav")
```

### 2.3 使用Bark

```python
from transformers import BarkModel, BarkProcessor

# 加载模型
processor = BarkProcessor.from_pretrained("suno/bark-small")
model = BarkModel.from_pretrained("suno/bark-small")

# 合成
inputs = processor("Hello, my name is Suno.", voice_preset="v2/en_speaker_6")

audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()

# 保存
import scipy.io.wavfile as wavfile
sample_rate = model.generation_config.sample_rate
wavfile.write("bark_output.wav", rate=sample_rate, data=audio_array)
```

---

## 三、语音助手

```python
import whisper
import edge_tts
import asyncio

class VoiceAssistant:
    """语音助手"""
    
    def __init__(self):
        self.asr_model = whisper.load_model("base")
    
    def listen(self, audio_path):
        """语音识别"""
        result = self.asr_model.transcribe(audio_path)
        return result["text"]
    
    def speak(self, text, output_path):
        """语音合成"""
        async def _speak():
            communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
            await communicate.save(output_path)
        asyncio.run(_speak())
    
    def process(self, audio_path):
        """处理语音"""
        # 识别
        text = self.listen(audio_path)
        print(f"用户: {text}")
        
        # 生成回复（这里可以接入LLM）
        response = f"你说的是: {text}"
        
        # 合成
        self.speak(response, "response.mp3")
        return response

# 使用
assistant = VoiceAssistant()
assistant.process("input.mp3")
```

---

## 四、实时语音识别

```python
import pyaudio
import wave
import threading

class RealTimeASR:
    """实时语音识别"""
    
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)
        self.is_recording = False
    
    def record_audio(self, duration=5, sample_rate=16000):
        """录音"""
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            input=True,
            frames_per_buffer=1024
        )
        
        frames = []
        for _ in range(0, int(sample_rate / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # 保存临时文件
        wf = wave.open("temp.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))
        wf.close()
        
        return "temp.wav"
    
    def transcribe_realtime(self, duration=5):
        """实时转录"""
        audio_file = self.record_audio(duration)
        result = self.model.transcribe(audio_file)
        return result["text"]
```

---

## 参考资源

> - [Whisper论文](https://arxiv.org/abs/2212.04356)
> - [Edge TTS](https://github.com/rany2/edge-tts)
> - [Coqui TTS](https://github.com/coqui-ai/TTS)

---

**返回**：[多模态大模型]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-10-multimodal-llm %})

*最后更新: 2026年4月20日*