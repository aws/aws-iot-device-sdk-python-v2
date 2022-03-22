# PREREQUISITES

## Python 3.6 of higher

* On Windows:
  * Download the Python installer from the official Python website: [Python Website](https://www.python.org/downloads/windows/)
* On MacOS:
  * Using `brew` (steps to [install `brew`](##cmake-31-on-mac)): `brew install python`.
  * Download the Python installer from the official Python website: [Python Website](https://www.python.org/downloads/macos/)
* On Linux:
  * Ubuntu: `sudo apt-get install python3`
  * Arch Linux: `sudo pacman -S python3`
  * Linux Distros that support `yum`: `sudo yum install python3`

# Installation Issues

`awsiotsdk` depends on [awscrt](https://github.com/awslabs/aws-crt-python), which makes use of C extensions. Precompiled wheels are downloaded when installing on major platforms (Mac, Windows, Linux, Raspberry Pi OS). If wheels are unavailable for your platform, your machine must compile some C libraries. If you encounter issues, please install the following dependencies:

* CMake 3.1+
* Python headers and development libraries
* You may also need to install a C/C++ compiler to compile the C code

Steps to install these dependencies per platform are listed below.


## Cmake 3.1+
### Cmake 3.1+ on Windows

1. Download CMake3.1+ for your platform: https://cmake.org/download/
2. Run the Cmake Installer. Make sure you add CMake into **PATH**.
3. Restart the command prompt / terminal.

### Cmake 3.1+ on Mac

You can install CMake easily using `brew` and it is the recommended workflow for most usecases. [Brew](https://brew.sh/) is a command line package manager that makes it easy to install packages and software dependencies.

1. Open a new terminal and input the following command:
``` sh
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. If XCode Command Line Tools are not installed, the `brew` install process will ask if you want to install. Type `y` to install.
3. Wait for `brew` to install the XCode Command Line Tools. This make take some time.
4. Once `brew` is finished, confirm the XCode Command Line Tools have installed by opening a new terminal and inputting `clang --version`.

Once `brew` is installed, you can install CMake using these steps:
1. Install CMake by running `brew install cmake`.
2. Once the install is finished, close the terminal and reopen it.
3. Confirm CMake is installed by running `cmake --version`.

If stuck waiting for `brew` to install XCode Command Line Tools for over 15-20 minutes, you many need to cancel the installation (`CTRL-C` in the terminal)
and install XCode Command Line Tools though the installer. You can find steps to install the XCode Command Line tools here: [Install XCode Command Line Tools](#macos-xcode-command-line-tools)

#### CMake using official precompiled download

You can also install CMake using a precompiled binary using the following steps:

1. Go to [cmake.org/install](https://cmake.org/install/).
2. Follow the install instructions for MacOS on the website page.
3. Once CMake is installed and added to the path, confirm it's working by running `cmake --version`.

### Cmake 3.1 on Linux

#### Install CMake on Ubuntu

1. Open the Ubuntu Software Center
2. In the search bar enter `cmake` and select `CMake - cross-platform build system` from the list
3. Press the `install` button
4. After CMake has installed open a new terminal
5. Type `cmake --version` to confirm CMake is installed

Or using the command line:

1. Open a new terminal
2. Run `sudo snap install cmake` to install CMake from the snap store
3. After CMake has installed, close the terminal and reopen it
4. Type `cmake --version` to confirm CMake is installed

#### Install CMake on Arch Linux

1. Open a new terminal.
2. Run `sudo pacman -S cmake` to install Cmake
3. After CMake has installed, close the terminal and reopen it
4. Type `cmake --version` to confirm CMake is installed.


## Python headers and libraries

For Windows and MacOS, the development headers and libraries should be installed automatically.

On Linux, the development headers and libaries are installed seperately and can be installed using the following commands depending on your Linux distro:
* Ubuntu: `sudo apt-get install python3-dev`
* Arch Linux: `sudo pacman -S python3-dev`
* Distros supporting `yum`: `sudo yum install python3-devel`


## C/C++ Compiler

First, check if you need to install a C/C++ compiler by running one of the following commands:

``` sh
g++ --version
```

``` sh
clang --version
```

If you get a message with a version number, then you already have a C/C++ compiler and do not need to install anything else.

### Windows

You can compile C and C++ code through MSVC. To install Visual Studio with MSVC, follow these steps:
1. Download **Visual Studio Installer** https://visualstudio.microsoft.com/downloads/
2. Run the installer, check the **Desktop development with C++** workload and select Install.
3. Verify your MSVC installation
   * In Windows Start up Menu, try open "Developer Command Prompt for VS"

### MacOS (XCode Command Line Tools)

To compile C/C++ code on MacOS, you will need to install the Command Line Tools using the following steps:

1. Go to [developer.apple.com/downloads](https://developer.apple.com/download/all/).
2. Input your AppleID to access the developer downloads.
3. From the presented list, scroll until you find `Command Line Tools for Xcode <version>`.
4. Select `view more details` and then select `Additionals Tools for Xcode <version>.dmg`.
5. Once downloaded, double click the `.dmg` and follow the installer instructions.
6. Confirm XCode Command Line Tools have installed by opening a new terminal and inputting `clang --version`.

### Linux
#### Install GCC or Clang on Ubuntu

To compile C/C++ code on Ubuntu Linux, you will need to follow these steps:

1. Open a new terminal
2. (optional) Run `sudo apt-get update` to get latest package updates.
3. (optional) Run `sudo apt-get upgrade` to install latest package updates.
4. Run `sudo apt-get install build-essential` to install GCC or `sudo apt-get install clang` to install Clang.
5. Once the install is finished, close the terminal and reopen it.
6. Confirm GCC is installed by running `gcc --version` or Clang is installed by running `clang --version`.

#### Install GCC or Clang on Arch Linux

To compile C/C++ code on Arch Linux, you will need to follow these steps:

1. Open a new terminal.
2. Run `sudo pacman -S gcc` to install GCC or `sudo pacman -S clang` to install Clang.
3. Once the install is finished, close the terminal and reopen it.
4. Confirm Clang is installed by running `gcc --version`.
