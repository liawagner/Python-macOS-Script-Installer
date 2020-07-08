# Python-macOS-Script-Installer - work in progress

A template to quickly create a macOS app bundle and dmg installer from a Python script, which will be launched in a Terminal session.

---

#### Background



### Usage

1. First ...

2. Then download the [CC_Offline_Package_Generator.dmg](https://github.com/chriswayg/CC-Offline-Package-Generator/releases/), mount it and copy `CC_Offline_Package_Generator` to Applications. Run the app and it will open a Terminal window. Then follow the on-screen instructions. Tested on High Sierra, Mojave and Catalina.

Download location: https://github.com/chriswayg/CC-Offline-Package-Generator/releases/

![](https://raw.githubusercontent.com/chriswayg/CC-Offline-Package-Generator/master/screenshots/Usage00.png)

### Technical notes:
The *CC_Offline_Package_Generator* binary file was built with via `pyinstaller pyinstall.spec`on macOS High Sierra 10.13.6. This means it should theoretically be compatible with High Sierra, Mojave, Catalina, and Big Sur. The python virtual environment was created with `pipenv`. The binary already includes Python inside, so there is no need to install Python to run CC_Offline_Package_Generator.

To build the binary, Homebrew and Python 3 needs to be installed. This has been tested with Python 3.7 from Homebrew. The build_prerequisites.sh` script will setup everything that is required. Some familiarity with configuring Python would be helpful. - Issue the following commands in a Terminal:

```
git clone https://github.com/chriswayg/CC-Offline-Package-Generator.git
cd CC-Offline-Package-Generator
./build_prerequisites.sh
pipenv shell
./build_app.sh
```

This will produce the `CC_Offline_Package_Generator.dmg` installer in the `/dmg` directory.

---

- Lincense: GPL 3.0 for my portions of the code
