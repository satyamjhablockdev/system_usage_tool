# 🚀 Advanced System Monitor

**Made by Satyam Jha**

A stunning, full-screen terminal-based system monitoring dashboard with real-time animated charts, beautiful UI, and comprehensive system information display.

![System Monitor Preview](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 📊 **Comprehensive Monitoring**
- **CPU Performance**: Usage percentage, per-core monitoring, frequency, history charts
- **Memory Status**: RAM usage, swap information, availability with sparkline trends
- **Storage Overview**: Real disk drives only (excludes loop devices), usage bars, free space
- **GPU Performance**: NVIDIA GPU support with temperature, VRAM usage, utilization
- **System Information**: Uptime, real-time timestamps, system statistics

### 🔧 **Technical Features**
- **Cross-platform compatibility** (Linux, macOS, Windows)
- **Intelligent filtering** - excludes virtual filesystems and loop devices
- **Real-time updates** every 2 seconds
- **Error handling** for missing hardware or permissions
- **Clean exit** with Ctrl+C

## 📸 Screenshots

```
◢═══════════════════════════════════════════════════════════════════════════════◢
║                          ADVANCED SYSTEM MONITOR                              ║
║                               Made by Satyam Jha                              ║
◢═══════════════════════════════════════════════════════════════════════════════◢

🔥 CPU PERFORMANCE
─────────────────────────────────────────────
Overall Usage:  85.4%
[████████████████████████████░░░░░░░░░░░░] 85.4%
History: ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅
Cores: 4 physical | Threads: 8 | Frequency: 2400 MHz

🧠 MEMORY STATUS  
─────────────────────────────────────────────
RAM Usage:  67.2% (5.4 GB / 8.0 GB)
[██████████████████████████░░░░░░░░░░░░░░] 67.2%
History: ▃▄▅▆▇█▇▆▅▄▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇█▇▆
Available: 2.6 GB
```

## 🚀 Quick Start
**Direct download and run:**

### Prerequisites
- Python 3.6 or higher
- `psutil` library
## Installation
### Automatic 
```bash
wget https://raw.githubusercontent.com/satyamjhablockdev/system_usage_tool/main/system_monitor.py
pip install psutil
python3 system_monitor.py
```
### Manual

1. **Clone the repository:**
   ```bash
   git clone https://github.com/satyamjhablockdev/system_usage_tool.git
   cd system_usage_tool
   ```

2. **Install dependencies:**
   ```bash
   pip install psutil
   ```
   
   Or using the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the monitor:**
   ```bash
   python3 system_monitor.py
   ```

## 💡 Usage

### Basic Usage
```bash
python3 system_monitor.py
```

### Exit
Press `Ctrl+C` to exit gracefully.

## 🖥️ Compatibility

| Feature | Linux | macOS | Windows |
|---------|--------|--------|---------|
| CPU Monitoring | ✅ | ✅ | ✅ |
| Memory Monitoring | ✅ | ✅ | ✅ |
| Disk Monitoring | ✅ | ✅ | ✅ |
| NVIDIA GPU | ✅ | ✅ | ✅ |
| AMD GPU | ⚠️ | ⚠️ | ⚠️ |
| Colors/Unicode | ✅ | ✅ | ✅* |

*Windows: Use Windows Terminal or WSL for best experience

## 🔧 Configuration

The monitor automatically adapts to your system, but you can modify these settings in the code:

- **Update interval**: Change `time.sleep(2)` in the main loop
- **History length**: Modify the history list size (default: 50 data points)
- **Progress bar width**: Adjust `width//3` in progress bar calls
- **Color thresholds**: Modify the percentage values in `get_gradient_color()`

## 🎯 GPU Support

### NVIDIA GPUs
- Requires `nvidia-smi` to be installed and accessible
- Shows: Usage, Temperature, VRAM, Power consumption
- Supports multiple GPUs

### AMD GPUs
- Limited support (requires `rocm-smi`)
- Shows: Basic usage information

### Intel GPUs
- Currently not supported (contributions welcome!)

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

1. **Bug Reports**: Open an issue with detailed information
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Submit pull requests with new features or fixes
4. **Documentation**: Help improve the README or add comments
5. **Testing**: Test on different systems and report compatibility


## 🐛 Known Issues

- AMD GPU monitoring requires additional setup
- Some terminals may not support all Unicode characters
- Windows Command Prompt has limited color support (use Windows Terminal)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [psutil](https://github.com/giampaolo/psutil) for system information
- Inspired by modern terminal applications
- Unicode characters for beautiful visual elements

---

⭐ **Star this repository if you found it helpful!** ⭐

Made with ❤️ by Satyam Jha
