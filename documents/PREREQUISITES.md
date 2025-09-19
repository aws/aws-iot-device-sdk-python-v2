# PREREQUISITES

## Python 3.8 or higher

How you install Python varies from platform to platform. Below are the instructions for Windows, macOS, and Linux:

* On Windows:
  * Download the Python installer from the official Python website: [Python Website](https://www.python.org/downloads/windows/)
* On macOS:
  * Using `brew` (steps to [install `brew`](#brew-installation)): `brew install python`.
  * Download the Python installer from the official Python website: [Python Website](https://www.python.org/downloads/macos/)
* On Linux:
  * Ubuntu: `sudo apt install python3`
  * Arch Linux: `sudo pacman -S python3`
  * Linux Distros that support `dnf`: `sudo dnf install python3`
  * Linux Distros that support `yum`: `sudo yum install python3`

## Installation Issues

`awsiotsdk` depends on [awscrt](https://github.com/awslabs/aws-crt-python), which makes use of C extensions. Precompiled wheels are downloaded when installing on major platforms (Mac, Windows, Linux, Raspberry Pi OS). If wheels are unavailable for your platform, your machine must compile some C libraries. If you encounter issues, please install the following dependencies:

* C++ 11 or higher
  * Clang 3.9+ or GCC 4.8+ or MSVC 2015+
* CMake 3.9+
* Python headers and development libraries

Steps to install these dependencies are below, as well as per platform instructions for [Windows](#windows-instructions), [macOS](#macos-instructions), and [Linux](#linux-instructions).

## C++ 11 Compiler

To build the SDK, you will need a compiler that can compile C++ 11 code or higher. C++ compilers vary based on platform, but listed below are a few of the most common and the minimum version required:

* Clang: 3.9 or higher
* GCC: 4.8 or higher
* MSVC: 2015 or higher

Listed below are ways to install C++ 11 compilers on [Windows](#windows-c-compilers), [macOS](#macos-c-compiler), and [Linux](#linux-c-compilers).

## CMake 3.9+

You will also need CMake to build the SDK. The minimum required version is CMake 3.9.

Below are the instructions to install CMake in a non-platform specific way:

1. Download CMake3.9+ for your platform: https://cmake.org/download/
2. Run the Cmake Installer. Make sure you add CMake into **PATH**.
3. Restart the command prompt / terminal.

Listed below are also instructions to install CMake on [Windows](#windows-cmake), [macOS](#macos-cmake), and [Linux](#linux-cmake).

## Python headers and development libraries

For Windows and macOS, the development headers and libraries should be installed automatically.

On Linux, the development headers and libraries are installed separately and can be installed using the following commands depending on your Linux distro:
* Ubuntu: `sudo apt install python3-dev`
* Arch Linux: `sudo pacman -S python3-dev`
* Distros supporting `dnf`: `sudo dnf install python3-devel`
* Distros supporting `yum`: `sudo yum install python3-devel`

## Windows Instructions

### Windows C++ Compilers

#### MSVC

Microsoft Visual C++ (MSVC) is a C++ compiler that is supported and maintained by Microsoft, and is supported by the C++ SDK. To install MSVC, you will need to install Visual Studio using the instructions below.

Install Visual Studio with MSVC
1. Download **Visual Studio Installer** https://visualstudio.microsoft.com/downloads/
2. Run the installer, check the **Desktop development with C++** workload and select Install.
3. Verify your MSVC installation
   * In Windows Start up Menu, try open "Developer Command Prompt for VS".
   * In the opened terminal/console window, type `cl.exe` and it *should* output the compiler version.
   * You can also find the compiler version by opening Visual Studio by selecting `help` and then `about`.

If using MSVC, you will need to use the Developer Command Prompt instead of the standard terminal when compiling the SDK and samples.

### Windows CMake

#### Manual Install

You can also install CMake manually by following the installation instructions on the CMake website:

1. Download CMake3.9+ for Windows: https://cmake.org/download/
2. Run the Cmake Installer.
3. Next you need to add CMake to your windows `PATH` environment variables so you can run it from the terminal.
   * Note: The installer should include an option to add CMake to the system path for all users. If you have checked this box, you can skip steps `4` through `8`.
4. Open the Windows Settings. You can do this by typing `settings` into the search bar or by opening the Windows start menu and navigating to the Windows Settings (should be called "Settings") application.
5. Once the Windows Settings window is open, search for `Edit environment variables for your account`.
6. Select the `Path` variable in the `User variables` property and press the `Edit` button.
7. Select `New` and then add the CMake `bin` folder to this path. If you do not modify the install path, it should be located around `C:\Program Files (x86)\CMake.x.x` where `x.x` is the version. If you installed CMake to a different directory, then you will need to modify the path accordingly.
8. Once you have added the path to the `Path` variable in the `User variables` property, select `OK` and save.
9. Close any console/terminal windows you have open. This is because the console/terminal will not see the updated `PATH` variable unless it is restarted by closing and reopening.
10. Run `cmake --version` to check that CMake is properly installed.

### Windows Python headers and development libraries

You will need to install Python to get the development libraries, if you do not already have Python installed. To download Python on Windows, go to the official website and download the Python installer for Windows: [Python Website](https://www.python.org/downloads/windows/)

The development headers and libraries should be installed automatically when you install Python.


## macOS Instructions

### Brew Installation

[Brew](https://brew.sh/) is a command line package manager that makes it easy to install packages and software dependencies.

To install `brew` use the following command:
``` sh
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### macOS C++ Compiler

#### XCode Command Line Tools using `brew`

XCode Command Line Tools is the easiest way to install C++ compilers on macOS, as it is officially supported and maintained by Apple. By installing the XCode Command Line tools, you will automatically install `clang`, which can compile C++ 11 code. One way to install XCode Command Line Tools is using `brew`.

1. If XCode Command Line Tools are not installed, the `brew` install process will ask if you want to install. Type `y` to install.
2. Wait for `brew` to install the XCode Command Line Tools. This make take some time.
3. Once `brew` is finished, confirm the XCode Command Line Tools have installed by opening a new terminal and inputting `clang --version`.

If stuck waiting for `brew` to install XCode Command Line Tools for over 15-20 minutes, you many need to cancel the installation (`CTRL-C` in the terminal) and install XCode Command Line Tools though the installer.

##### XCode Command Line Tools using installer

You can also install XCode Command Line Tools manually through an installer download on Apple's website. The instructions to install through the installer are below:

1. Go to [developer.apple.com/downloads](https://developer.apple.com/download/all/).
2. Input your AppleID to access the developer downloads.
3. From the presented list, scroll until you find `Command Line Tools for Xcode <version>`.
4. Select `view more details` and then select `Additionals Tools for Xcode <version>.dmg`.
5. Once downloaded, double click the `.dmg` and follow the installer instructions.
6. Confirm XCode Command Line Tools have installed by opening a new terminal and inputting `clang --version`.

### macOS CMake

#### CMake using `brew`

CMake can easily be installed using `brew`, so if you installed `brew` for XCode Command Line Tools, you can run the following to install CMake:

1. Confirm you have `brew` installed:
    ``` sh
    brew --version
    ```
2. Install CMake by running `brew install cmake`.
3. Close any console/terminal windows you have open. This is to refresh the console/terminal so it uses the latest changes.
4. Confirm CMake is installed by running `cmake --version`.

#### Manual Install

You can also install CMake manually by following the installation instructions on the CMake website:

1. Go to [cmake.org/install](https://cmake.org/install/).
2. Follow the installation instructions for macOS on the website page.
3. Drag and drop the CMake application from the downloaded installer into your Applications folder. A window should open once you have mounted the CMake installer that easily allows you to do this via drag-and-drop.
4. You may need to manually add CMake to your `PATH` so you can run it in the terminal. To do this, run the following command:
    ``` sh
    sudo "/Applications/CMake.app/Contents/bin/cmake-gui" --install
    ```
5. This will create the symlinks so you can run CMake from the terminal.
6. Close any console/terminal windows you have open. This is to refresh the console/terminal so it uses the latest changes.

### macOS Python headers and development libraries

You will need to install Python to get the development libraries, if you do not already have Python installed. There are two ways to install Python on macOS, depending on how you want to install it:
* Using `brew` (steps to [install `brew`](#brew-installation)): `brew install python`.
* Download the Python installer from the official Python website: [Python Website](https://www.python.org/downloads/macos/)

The development headers and libraries should be installed automatically when you install Python.


## Linux instructions

### Linux C++ Compilers

Many Linux operating systems have C++ compilers installed by default, so you might already `clang` or `gcc` preinstalled.
To test, try running the following in a new terminal:

``` sh
clang --version
```
``` sh
gcc --version
```

If both these commands fail, then please follow the instructions below for installing a C++ compiler on your Linux operating system.

If your Linux operating system is not in the list, please use a search engine to find out how to install either `clang` or `gcc` on your Linux operating system.

#### Install GCC or Clang on Ubuntu

1. Open a new terminal
2. (optional) Run `sudo apt update` to get latest package updates.
3. (optional) Run `sudo apt upgrade` to install latest package updates.
4. Run `sudo apt install build-essential` to install GCC or `sudo apt install clang` to install Clang.
5. Once the installation is finished, close the terminal and reopen it.
6. Confirm GCC is installed by running `gcc --version` or Clang is installed by running `clang --version`.

#### Install GCC or Clang on Arch Linux

1. Open a new terminal.
2. Run `sudo pacman -S gcc` to install GCC or `sudo pacman -S clang` to install Clang.
3. Once the installation is finished, close the terminal and reopen it.
4. Confirm Clang is installed by running `gcc --version`.

### Linux CMake

There are several ways to install CMake depending on the Linux operating system. Several Linux operating systems include CMake in their software repository applications, like the Ubuntu Software Center for example, so you may want to check there first. Below are the instructions to install CMake for Ubuntu and Arch Linux.

If your Linux operating system is not in the list below, please use a search engine to find out how to install CMake on your Linux operating system. You can also always try to install CMake manually using the generic install instructions at the top of this page.

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

### Linux Python headers and development libraries

You will need to install Python to get the development libraries, if you do not already have Python installed. How you install Linux varies from operating system to operating system, but common operating system commands to install Python are listed below:
* Ubuntu: `sudo apt install python3`
* Arch Linux: `sudo pacman -S python3`
* Linux Distros that support `yum`: `sudo yum install python3`

On Linux, the development headers and libraries are installed separately from Python and can be installed using the following commands depending on your Linux distro:
* Ubuntu: `sudo apt install python3-dev`
* Arch Linux: `sudo pacman -S python3-dev`
* Distros supporting `dnf`: `sudo dnf install python3-devel`
* Distros supporting `yum`: `sudo yum install python3-devel`
