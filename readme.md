# macOS Python Script App Installer

A template to quickly create a macOS app bundle and dmg installer from a Python script, which will be launched in a Terminal session. This is intended for python scripts which run in a Terminal and require some user interaction. 

### Background
A python script that runs in a terminal should be able to run anywhere, just like a bash shell script, but its not really that straighforward. On macOS only an outdated version of Python is installed by default. To run a recent script, Python 3 needs to be installed usually with additional modules via pip3. Packaging the script with pyinstaller together with Python allows it to run out of the box. 

Still a binary file like that does not integrate well with macOS in the Applications directory. Platypus can create a nice app bundle for python scripts which do not need much user interaction. For bi-directional user interaction the script needs to be launched in a terminal rather than just a log window. Therefore to run the script in the macOS Terminal app from Platypus, I added an applescript launcher. Then the app gets packaged by create-dmg to make it easy to distribute and install the app bundle.

I previously used this approach for the [CC-Offline-Package-Generator](https://github.com/chriswayg/CC-Offline-Package-Generator) script. This template project is intended to have a straightforward way to drop in a python script and package it quickly.

This is primarily intended for macOS Python terminal applications which require user interactions in the terminal. PyQt apps can be packaged with fbs (fman build system) easily or by pyqtdeploy for cross platform use. For many use cases creating a macOS app bundle with pyinstaller or py2app alone will get the job done.

### Usage

1. Try the [Downloader_Demo.dmg](https://github.com/liawagner/Python-macOS-Script-Installer/releases), mount it and copy `Downloader_Demo` to Applications. Run the app and it will open a Terminal window. Then follow the on-screen instructions. Tested on High Sierra, Mojave and Catalina.

2. Use your own python script code, adapt the names and add your app icon. 

Download location: https://github.com/chriswayg/Python-macOS-Script-Installer/releases/

![](https://raw.githubusercontent.com/chriswayg/Python-macOS-Script-Installer/master/screenshots/Usage00.png)

### Technical notes
If the *Downloader_Demo* binary file is built with via `pyinstaller pyinstall.spec`on macOS High Sierra 10.13.6, then it should be compatible with High Sierra, Mojave, Catalina, and Big Sur. The python virtual environment was created with `pipenv`. The binary already includes Python inside, so there is no need to install Python to run Downloader_Demo.

### Build
To build the binary, Homebrew and Python 3 needs to be installed. This has been tested with Python 3.7 from Homebrew. The build_prereqs.sh` script will setup everything that is required. Some familiarity with configuring Python is expected. - Issue the following commands in a Terminal:

```
git clone https://github.com/chriswayg/Python-macOS-Script-Installer.git
cd Python-macOS-Script-Installer
./build_prereqs.sh
pipenv shell
./build_app.sh
```

This will produce the `Downloader_Demo.dmg` installer in the `/dist` directory.

### Pyinstaller

Look here: https://pyinstaller.readthedocs.io/en/stable/index.html

Adapt the specfile as needed. Use the following command, which will also create a new specfile
```
pyinstaller --onefile --hidden-import 'pkg_resources.py2_warn' src/main_script.py
```

---

- Lincense: GPL 3.0 for my portions of the code
