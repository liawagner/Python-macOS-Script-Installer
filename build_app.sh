#!/usr/bin/env bash
set -o errexit

# TODO use templating with j2cli to make $appname and $binaryname substitutions in the other files
binaryname="downloader-demo"
appname="Downloader_Demo"

color="$(tput bold; tput setaf 5)"
reset="$(tput sgr0)"

printf "${color}*** Checking for build prerequisites${reset}\n"

[[ -d "$(xcode-select -p)" ]]  || { echo "${color}Xcode tools are missing! Run build_prereqs.sh first.${reset}\n" && exit 1; }

checkPrereqs=("python3.7" \
              "brew" \
              "platypus" \
              "create-dmg" \
              "pipenv")

for prereq in ${checkPrereqs[@]}; do
    command -v $prereq > /dev/null 2>&1  || { printf "${color}$prereq is missing! Run build_prereqs.sh first.${reset}\n" && exit 1; }
done

[[ -z $VIRTUAL_ENV ]] && printf "${color}Run 'pipenv shell' first, as this build script needs to run in a virtual environment.${reset}\n" && exit 1

if [[ -d /Volumes/$appname/$appname.app ]]; then
    hdiutil detach /Volumes/$appname  || { printf  "${color}*** Ensure that $appname.dmg is unmounted!${reset}\n" && exit 1; }
fi

printf  "${color}*** cleaning up before build...${reset}\n"
rm -rf build/ dist/
[[ -f app/$binaryname ]] && rm app/$binaryname

printf  "${color}*** creating the binary python '$binaryname' with pyinstaller...${reset}\n"
pipenv install
pyinstaller pyinstall.spec

{
date +"Date: %Y-%m-%d %H:%M"
printf "\n$ sw_vers -productVersion\n"
sw_vers -productVersion
printf "\n$ python -V\n"
python -V
printf "\n$ pipenv --version\n"
pipenv --version
printf "\n$ pipenv graph\n"
pipenv graph
printf "\n$ pip list\n"
pip list
printf "\n$ brew list --versions\n"
brew list --versions
} > app/build_env.txt

printf  "${color}*** creating the .app bundle with Platypus...${reset}\n"
mkdir -p dmg/createdmg
mv dist/$binaryname app/
cd app
rm -rf "../dmg/createdmg/$appname.app"
platypus -P app_bundle_config.platypus "../dmg/createdmg/$appname.app"

printf  "${color}*** creating the DMG installer with create-dmg...${reset}\n"
cd ../dmg
[[ -f "$appname.dmg" ]] && rm "$appname.dmg"
[[ -f "rw.$appname.dmg" ]] && rm "rw.$appname.dmg"

# Create a DMG installer
create-dmg \
  --volname "$appname" \
  --background "installer_background.png" \
  --window-pos 200 120 \
  --window-size 500 360 \
  --icon-size 80 \
  --icon "$appname.app" 120 155 \
  --hide-extension "$appname.app" \
  --app-drop-link 350 155 \
  "$appname.dmg" \
  "createdmg"

# move all created files to the dist directory
mv ../app/build_env.txt ../dist/
mv ../app/$binaryname ../dist/
mv createdmg/$appname.app/ ../dist/
mv $appname.dmg ../dist/
rm -rf createdmg

printf  "${color}*** The installer has been created in dist/$appname.dmg${reset}\n"
