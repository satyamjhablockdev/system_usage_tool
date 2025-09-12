#!/usr/bin/env python3
"""
Advanced System Monitor Dashboard
Made by Satyam Jha

A stunning terminal-based system monitoring dashboard with:
- Full-screen display
- Real-time animated charts
- Beautiful UI with gradients and animations
- Accurate system information
"""

import psutil
import time
import os
import shutil
import subprocess
from datetime import datetime
import sys

# Enhanced color codes and styling
class Style:
    # Colors
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Bright colors
    BRIGHT_RED = '\033[1;91m'
    BRIGHT_GREEN = '\033[1;92m'
    BRIGHT_YELLOW = '\033[1;93m'
    BRIGHT_BLUE = '\033[1;94m'
    BRIGHT_MAGENTA = '\033[1;95m'
    BRIGHT_CYAN = '\033[1;96m'
    BRIGHT_WHITE = '\033[1;97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Text formatting
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    STRIKETHROUGH = '\033[9m'
    
    # Reset
    RESET = '\033[0m'
    CLEAR = '\033[2J'
    HOME = '\033[H'

class SystemMonitor:
    def __init__(self):
        self.running = True
        self.cpu_history = []
        self.memory_history = []
        self.animation_frame = 0
        
    def get_terminal_size(self):
        """Get terminal dimensions"""
        return shutil.get_terminal_size((80, 24))
    
    def clear_screen(self):
        """Clear screen and move cursor to top"""
        print(Style.CLEAR + Style.HOME, end='')
    
    def get_gradient_color(self, percentage, reverse=False):
        """Get gradient color based on percentage"""
        if reverse:
            percentage = 100 - percentage
            
        if percentage < 25:
            return Style.BRIGHT_GREEN
        elif percentage < 50:
            return Style.BRIGHT_YELLOW
        elif percentage < 75:
            return Style.YELLOW
        elif percentage < 90:
            return Style.RED
        else:
            return Style.BRIGHT_RED
    
    def create_progress_bar(self, percentage, width=40):
        """Create beautiful progress bars"""
        filled = int(percentage / 100 * width)
        color = self.get_gradient_color(percentage)
        
        if filled == 0:
            bar = Style.DIM + '░' * width + Style.RESET
        else:
            bar = color + '█' * filled + Style.DIM + '░' * (width - filled) + Style.RESET
        
        return bar
    
    def create_spark_line(self, data, width=30):
        """Create sparkline chart"""
        if not data or len(data) == 0:
            return Style.DIM + '─' * width + Style.RESET
        
        # Ensure we have valid numeric data
        valid_data = [x for x in data if isinstance(x, (int, float))]
        if not valid_data:
            return Style.DIM + '─' * width + Style.RESET
        
        # Normalize data
        max_val = max(valid_data) if len(valid_data) > 0 else 1
        min_val = min(valid_data) if len(valid_data) > 0 else 0
        
        if max_val == min_val:
            max_val = min_val + 1
        
        spark_chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        spark_line = ''
        
        data_slice = valid_data[-width:] if len(valid_data) >= width else valid_data
        
        for value in data_slice:
            try:
                normalized = (value - min_val) / (max_val - min_val)
                char_index = min(int(normalized * (len(spark_chars) - 1)), len(spark_chars) - 1)
                
                # Color based on value
                if value > 80:
                    color = Style.BRIGHT_RED
                elif value > 60:
                    color = Style.RED
                elif value > 40:
                    color = Style.YELLOW
                else:
                    color = Style.BRIGHT_GREEN
                
                spark_line += color + spark_chars[char_index] + Style.RESET
            except (ValueError, ZeroDivisionError):
                spark_line += Style.DIM + '─' + Style.RESET
        
        # Pad with dashes if needed
        remaining = width - len(data_slice)
        if remaining > 0:
            spark_line = Style.DIM + '─' * remaining + Style.RESET + spark_line
        
        return spark_line
    
    def get_cpu_info(self):
        """Get comprehensive CPU information"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        
        # Store history
        self.cpu_history.append(cpu_percent)
        if len(self.cpu_history) > 50:
            self.cpu_history.pop(0)
        
        return {
            'usage': cpu_percent,
            'per_core': cpu_per_core,
            'cores': cpu_count,
            'threads': cpu_count_logical,
            'frequency': cpu_freq.current if cpu_freq else 0,
            'history': self.cpu_history
        }
    
    def get_memory_info(self):
        """Get comprehensive memory information"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        self.memory_history.append(memory.percent)
        if len(self.memory_history) > 50:
            self.memory_history.pop(0)
        
        return {
            'total': memory.total,
            'used': memory.used,
            'available': memory.available,
            'percentage': memory.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_percentage': swap.percent,
            'history': self.memory_history
        }
    
    def get_disk_info(self):
        """Get only real disk information, excluding loop devices"""
        disks = []
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            # Skip loop devices, snap mounts, and other virtual filesystems
            if (partition.device.startswith('/dev/loop') or 
                partition.mountpoint.startswith('/snap') or
                partition.fstype in ['squashfs', 'tmpfs', 'devtmpfs'] or
                partition.device.startswith('/dev/ram')):
                continue
                
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                if usage.total > 100 * 1024 * 1024:  # Only drives > 100MB
                    disks.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'filesystem': partition.fstype,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percentage': (usage.used / usage.total) * 100
                    })
            except (PermissionError, FileNotFoundError, OSError):
                continue
        
        return disks
    
    def get_gpu_info(self):
        """Get GPU information"""
        gpu_info = []
        
        # Try NVIDIA first
        try:
            nvidia_smi = subprocess.run([
                'nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu,name',
                '--format=csv,noheader,nounits'
            ], capture_output=True, text=True, timeout=3)
            
            if nvidia_smi.returncode == 0:
                for line in nvidia_smi.stdout.strip().split('\n'):
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 5:
                            try:
                                gpu_info.append({
                                    'vendor': 'NVIDIA',
                                    'name': parts[4],
                                    'usage': float(parts[0]) if parts[0] != '[N/A]' else 0,
                                    'memory_used': int(parts[1]) if parts[1] != '[N/A]' else 0,
                                    'memory_total': int(parts[2]) if parts[2] != '[N/A]' else 0,
                                    'temperature': int(parts[3]) if parts[3] != '[N/A]' else 0
                                })
                            except (ValueError, IndexError):
                                continue
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return gpu_info
    
    def format_bytes(self, bytes_value):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} EB"
    
    def draw_header(self, width):
        """Draw animated header"""
        title = "ADVANCED SYSTEM MONITOR"
        subtitle = "Made by Satyam Jha"
        
        # Animated border
        border_chars = ['◢', '◣', '◤', '◥']
        border_char = border_chars[self.animation_frame % len(border_chars)]
        
        # Center the title
        title_padding = (width - len(title)) // 2
        subtitle_padding = (width - len(subtitle)) // 2
        
        print(f"{Style.BRIGHT_CYAN}{Style.BOLD}")
        print(f"{border_char}" + "═" * (width - 2) + f"{border_char}")
        print(f"║{' ' * title_padding}{title}{' ' * (width - title_padding - len(title) - 2)}║")
        print(f"║{' ' * subtitle_padding}{Style.BRIGHT_YELLOW}{subtitle}{Style.BRIGHT_CYAN}{' ' * (width - subtitle_padding - len(subtitle) - 2)}║")
        print(f"{border_char}" + "═" * (width - 2) + f"{border_char}")
        print(Style.RESET)
    
    def draw_cpu_section(self, cpu_info, width):
        """Draw CPU monitoring section"""
        print(f"\n{Style.BRIGHT_BLUE}{Style.BOLD}🔥 CPU PERFORMANCE{Style.RESET}")
        print("─" * (width // 2))
        
        # Main CPU usage
        color = self.get_gradient_color(cpu_info['usage'])
        print(f"Overall Usage: {color}{Style.BOLD}{cpu_info['usage']:6.1f}%{Style.RESET}")
        
        # Progress bar
        bar = self.create_progress_bar(cpu_info['usage'], width//3)
        print(f"[{bar}]")
        
        # Sparkline history
        if cpu_info['history']:
            sparkline = self.create_spark_line(cpu_info['history'])
            print(f"History: {sparkline}")
        
        # System info
        print(f"Cores: {Style.BRIGHT_WHITE}{cpu_info['cores']} physical{Style.RESET} | "
              f"Threads: {Style.BRIGHT_WHITE}{cpu_info['threads']}{Style.RESET} | "
              f"Frequency: {Style.BRIGHT_WHITE}{cpu_info['frequency']:.0f} MHz{Style.RESET}")
        
        # Per-core usage (show up to 16 cores)
        if len(cpu_info['per_core']) <= 16:
            print("Per Core: ", end="")
            for i, core_usage in enumerate(cpu_info['per_core']):
                color = self.get_gradient_color(core_usage)
                print(f"{color}{core_usage:4.0f}%{Style.RESET}", end=" ")
                if (i + 1) % 8 == 0:
                    print()
            if len(cpu_info['per_core']) % 8 != 0:
                print()
    
    def draw_memory_section(self, memory_info, width):
        """Draw memory monitoring section"""
        print(f"\n{Style.BRIGHT_GREEN}{Style.BOLD}🧠 MEMORY STATUS{Style.RESET}")
        print("─" * (width // 2))
        
        # RAM Usage
        color = self.get_gradient_color(memory_info['percentage'])
        print(f"RAM Usage: {color}{Style.BOLD}{memory_info['percentage']:6.1f}%{Style.RESET} "
              f"({self.format_bytes(memory_info['used'])} / {self.format_bytes(memory_info['total'])})")
        
        bar = self.create_progress_bar(memory_info['percentage'], width//3)
        print(f"[{bar}]")
        
        # Memory sparkline
        if memory_info['history']:
            sparkline = self.create_spark_line(memory_info['history'])
            print(f"History: {sparkline}")
        
        print(f"Available: {Style.BRIGHT_WHITE}{self.format_bytes(memory_info['available'])}{Style.RESET}")
        
        # Swap information
        if memory_info['swap_total'] > 0:
            swap_color = self.get_gradient_color(memory_info['swap_percentage'])
            print(f"Swap: {swap_color}{memory_info['swap_percentage']:5.1f}%{Style.RESET} "
                  f"({self.format_bytes(memory_info['swap_used'])} / {self.format_bytes(memory_info['swap_total'])})")
    
    def draw_storage_section(self, disk_info, width):
        """Draw storage monitoring section"""
        print(f"\n{Style.BRIGHT_YELLOW}{Style.BOLD}💾 STORAGE OVERVIEW{Style.RESET}")
        print("─" * (width // 2))
        
        if not disk_info:
            print(f"{Style.DIM}No storage devices found{Style.RESET}")
            return
        
        for disk in disk_info[:4]:  # Limit to 4 disks for space
            color = self.get_gradient_color(disk['percentage'])
            
            # Device name and mount point
            device_name = disk['device'].split('/')[-1] if '/' in disk['device'] else disk['device']
            mount_display = disk['mountpoint'] if len(disk['mountpoint']) < 20 else f"...{disk['mountpoint'][-17:]}"
            
            print(f"{Style.BRIGHT_WHITE}{device_name}{Style.RESET} → {Style.DIM}{mount_display}{Style.RESET}")
            print(f"Usage: {color}{Style.BOLD}{disk['percentage']:5.1f}%{Style.RESET} "
                  f"({self.format_bytes(disk['used'])} / {self.format_bytes(disk['total'])})")
            
            # Progress bar
            bar = self.create_progress_bar(disk['percentage'], width//4)
            print(f"[{bar}] Free: {self.format_bytes(disk['free'])}")
            print()
    
    def draw_gpu_section(self, gpu_info, width):
        """Draw GPU monitoring section"""
        print(f"\n{Style.BRIGHT_MAGENTA}{Style.BOLD}🎮 GPU PERFORMANCE{Style.RESET}")
        print("─" * (width // 2))
        
        if not gpu_info:
            print(f"{Style.DIM}No compatible GPU detected{Style.RESET}")
            print(f"{Style.DIM}Install nvidia-smi for NVIDIA GPU monitoring{Style.RESET}")
            return
        
        for gpu in gpu_info:
            color = self.get_gradient_color(gpu['usage'])
            print(f"{Style.BRIGHT_WHITE}{gpu['name']}{Style.RESET}")
            print(f"Usage: {color}{Style.BOLD}{gpu['usage']:5.1f}%{Style.RESET}")
            
            if gpu['temperature'] > 0:
                temp_color = Style.BRIGHT_GREEN if gpu['temperature'] < 70 else Style.YELLOW if gpu['temperature'] < 85 else Style.BRIGHT_RED
                print(f"Temperature: {temp_color}{gpu['temperature']}°C{Style.RESET}")
            
            if gpu['memory_total'] > 0:
                mem_percent = (gpu['memory_used'] / gpu['memory_total']) * 100
                mem_color = self.get_gradient_color(mem_percent)
                print(f"VRAM: {mem_color}{mem_percent:5.1f}%{Style.RESET} "
                      f"({gpu['memory_used']} MB / {gpu['memory_total']} MB)")
    
    def draw_footer(self, width):
        """Draw footer with system info"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
            uptime_str = str(uptime).split('.')[0]
        except:
            uptime_str = "Unknown"
        
        print(f"\n{Style.BRIGHT_CYAN}{'═' * width}")
        print(f"{Style.DIM}Last Update: {timestamp} | "
              f"Uptime: {uptime_str} | "
              f"Press Ctrl+C to exit{Style.RESET}")
        print(f"{Style.BRIGHT_CYAN}{'═' * width}{Style.RESET}")
    
    def run(self):
        """Main monitoring loop"""
        try:
            while self.running:
                # Get terminal size
                term_size = self.get_terminal_size()
                width = min(term_size.columns, 120)
                
                # Clear screen
                self.clear_screen()
                
                # Get all system information
                cpu_info = self.get_cpu_info()
                memory_info = self.get_memory_info()
                disk_info = self.get_disk_info()
                gpu_info = self.get_gpu_info()
                
                # Draw all sections
                self.draw_header(width)
                self.draw_cpu_section(cpu_info, width)
                self.draw_memory_section(memory_info, width)
                self.draw_storage_section(disk_info, width)
                self.draw_gpu_section(gpu_info, width)
                self.draw_footer(width)
                
                # Update animation frame
                self.animation_frame += 1
                
                # Wait before next update
                time.sleep(2)
                
        except KeyboardInterrupt:
            self.clear_screen()
            print(f"\n{Style.BRIGHT_GREEN}{Style.BOLD}System Monitor Closed{Style.RESET}")
            print(f"{Style.BRIGHT_CYAN}Thanks for using Advanced System Monitor by Satyam Jha!{Style.RESET}\n")

def main():
    """Main function"""
    # Check dependencies
    try:
        import psutil
    except ImportError:
        print(f"{Style.BRIGHT_RED}Error: psutil is required{Style.RESET}")
        print(f"{Style.BRIGHT_YELLOW}Install with: pip install psutil{Style.RESET}")
        sys.exit(1)
    
    print(f"{Style.BRIGHT_CYAN}Starting Advanced System Monitor...{Style.RESET}")
    time.sleep(1)
    
    # Run the monitor
    monitor = SystemMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
