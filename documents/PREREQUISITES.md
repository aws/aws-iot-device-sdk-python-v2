# Prerequisites

## Quick Setup

**Requirements:**
- Python 3.8+

**Installation:**
```bash
# macOS/Linux
python3 -m pip install awsiotsdk

# Windows  
python -m pip install awsiotsdk
```

Precompiled wheels are automatically downloaded for most platforms (macOS, Windows, Linux).

## Compilation Dependencies

### When Compilation is Needed

Precompiled wheels are downloaded when installing on major platforms (Mac, Windows, Linux). If wheels are unavailable for your platform, your machine must compile AWS Common Runtime C libraries.

### Requirements for Compilation

- C compiler (Clang 6+, GCC 5+, or MSVC 15+)
- CMake 3.9+
- Python development headers

<details>
<summary><strong>Windows Compilation Setup</strong></summary>

### C Compiler (MSVC)

1. Download [Visual Studio Installer](https://visualstudio.microsoft.com/downloads/)
2. Run installer and select **Desktop development with C++** workload
3. Verify installation:
   - Open "Developer Command Prompt for VS" from Start Menu
   - Run `cl.exe` - should show compiler version

**Note:** Use Developer Command Prompt (not regular terminal) when building.

### C Compiler (MinGW-w64)

Alternative to MSVC using GCC on Windows:

1. Download and run MSYS2 installer from [msys2.org](https://www.msys2.org/)
2. Follow MSYS2 instructions to update database and base packages
3. Install MinGW-w64 toolchain:
   ```bash
   pacman -S --needed base-devel mingw-w64-x86_64-toolchain
   ```
4. Add to Windows PATH: `C:\msys64\mingw64\bin`
5. Verify: `gcc --version`

### CMake

1. Download [CMake 3.9+](https://cmake.org/download/) for Windows
2. Run installer and check "Add CMake to system PATH" option
3. Restart terminal and verify: `cmake --version`

### Python Headers
Automatically installed with Python on Windows.

</details>

<details>
<summary><strong>macOS Compilation Setup</strong></summary>

### C Compiler (Xcode Command Line Tools)

**Using Homebrew:**
1. During brew installation, it will prompt to install Xcode Command Line Tools
2. Type `y` to install
3. Verify: `clang --version`

**Manual Installation:**
1. Go to [developer.apple.com/downloads](https://developer.apple.com/download/all/)
2. Sign in with Apple ID
3. Download "Command Line Tools for Xcode"
4. Install and verify: `clang --version`

### CMake

**Using Homebrew:**
```bash
brew install cmake
cmake --version
```

**Manual Installation:**
1. Download from [cmake.org](https://cmake.org/install/)
2. Drag CMake.app to Applications folder
3. Add to PATH:
   ```bash
   sudo "/Applications/CMake.app/Contents/bin/cmake-gui" --install
   ```
4. Restart terminal and verify: `cmake --version`

### Python Headers
Automatically installed with Python on macOS.

</details>

<details>
<summary><strong>Linux Compilation Setup</strong></summary>

### C Compiler

Check if already installed:
```bash
clang --version
gcc --version
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install build-essential  # for GCC
# OR
sudo apt install clang           # for Clang
```

**Arch Linux:**
```bash
sudo pacman -S gcc    # for GCC
# OR  
sudo pacman -S clang  # for Clang
```

### CMake

**Ubuntu:**
```bash
# Via Software Center: search for "cmake"
# OR via command line:
sudo snap install cmake
```

**Arch Linux:**
```bash
sudo pacman -S cmake
```

### Python Headers

**Ubuntu:**
```bash
sudo apt install python3-dev
```

**Arch Linux:**
```bash
sudo pacman -S python3-dev
```

**RHEL/CentOS/Fedora:**
```bash
sudo dnf install python3-devel
# OR
sudo yum install python3-devel
```

</details>

---

## Advanced Troubleshooting

**Compilation Issues:**
- **Compilation fails**: Ensure you have C compiler, CMake, and Python headers installed
- **CMake not found**: Add CMake to your system PATH
- **Permission errors**: Use `sudo` on Linux/macOS or run as Administrator on Windows
- **Python version**: Verify you're using Python 3.8+ with `python --version`

**Getting Help:**
- Check our [FAQ](./FAQ.md)
- Search [existing issues](https://github.com/aws/aws-iot-device-sdk-python-v2/issues)
- Create a [new issue](https://github.com/aws/aws-iot-device-sdk-python-v2/issues/new/choose)
