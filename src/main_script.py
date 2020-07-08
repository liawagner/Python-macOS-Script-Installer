#!/usr/bin/env python3
import os
import sys
import glob
import tqdm
import requests
import validators
#import appdirs
from pathlib import Path

# clear Terminal screen first
# in pyCharm enable 'Emulate terminal in output console' option in the run configuration
def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux (here, os.name is 'posix')
    else:
        _ = os.system('clear')
clear()

appname = 'downloader-demo'
appauthor = 'author-name'
#cachedir = appdirs.user_cache_dir(appname, appauthor)
cachedir = str(os.path.join(Path.home(), "Downloads/" + appname))

if not os.path.exists(cachedir):
    try:
        os.mkdir(cachedir)
    except OSError:
        print ("Creation of the directory %s failed " % cachedir)
    else:
        print ("Successfully created the directory %s " % cachedir)

#  Copyright 2019 tiptapcode Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  from https://medium.com/better-programming/python-progress-bars-with-tqdm-by-example-ce98dbbc9697

# -*- coding: utf-8 -*-

class FileDownloader(object):

    def get_url_filename(self, url):
        """
        Discover file name from HTTP URL, If none is discovered derive name from http redirect HTTP content header Location
        :param url: Url link to file to download
        :type url: str
        :return: Base filename
        :rtype: str
        """
        try:
            if not validators.url(url):
                raise ValueError('Invalid url')
            filename = os.path.basename(url)
            basename, ext = os.path.splitext(filename)
            if ext:
                return filename
            header = requests.head(url, allow_redirects=False).headers
            return os.path.basename(header.get('Location')) if 'Location' in header else filename
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            raise errh
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            raise errc
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            raise errt
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            raise err

    def download_file(self, url, filename=None, target_dir=None):
        """
        Stream downloads files via HTTP
        :param url: Url link to file to download
        :type url: str
        :param filename: filename overrides filename defined in Url param
        :type filename: str
        :param target_dir: target destination directory to download file to
        :type target_dir: str
        :return: Absolute path to target destination where file has been downloaded to
        :rtype: str
        """
        if target_dir and not os.path.isdir(target_dir):
            raise ValueError('Invalid target_dir={} specified'.format(target_dir))
        local_filename = self.get_url_filename(url) if not filename else filename

        req = requests.get(url, stream=True)
        file_size = int(req.headers['Content-Length'])
        chunk_size = 1024  # 1 MB
        num_bars = int(file_size / chunk_size)

        base_path = os.path.abspath(os.path.dirname(__file__))
        target_dest_dir = os.path.join(base_path, local_filename) if not target_dir else os.path.join(target_dir, local_filename)
        with open(target_dest_dir, 'wb') as fp:
            for chunk in tqdm.tqdm(req.iter_content(chunk_size=chunk_size), total=num_bars, unit='KB', desc=local_filename, leave=True, file=sys.stdout):
                fp.write(chunk)

        return target_dest_dir


if __name__== "__main__":

    links = ['https://github.com/mdbergmann/Eloquent/releases/download/2.6.3/Eloquent-2.6.3.app.zip', 'https://www.python.org/ftp/python/3.8.3/python-3.8.3-macosx10.9.pkg']

    downloader = FileDownloader()

    for url in links:
        downloader.download_file(url, downloader.get_url_filename(url) ,cachedir)

    answer = None
    while answer not in ("yes", "no"):
        answer = input("Delete the downloaded files? [yes|no] ")
        if answer == "yes":
            files = glob.glob(cachedir + "/*")
            for f in files:
                os.remove(f)
            print("Deleted downloaded files.")
        elif answer == "no":
            print("Downloaded files are in " + cachedir)
        else:
            print("Please enter yes or no!")

    print('\nThis is just a demo for this template for creating a macOS app and an installer dmg')
    print('with a Python script that runs in a terminal window. Replace the script with your own script.')
