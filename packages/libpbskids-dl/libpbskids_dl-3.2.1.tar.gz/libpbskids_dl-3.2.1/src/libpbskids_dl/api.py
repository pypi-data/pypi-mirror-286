import sys
pbskids_dl_version = '3.2'
class DependenciesNeeded(Exception):
    "libpbskids-dl needs these modules:\n\targparse, urllib (urllib3), and BeautifulSoup4 (bs4)"
    pass
class DownloadFetchScriptError(Exception):
    "The link failed to load properly. Is it a PBS KIDS Video link?"
    pass
class DownloadFindAssetsError(Exception):
    "The video was not found! Is the link a PBS KIDS Video link?"
    pass
class DownloadUnsupportedStandard(Exception):
    "DRM Content is not available in pbskids-dl..."
    pass
class DownloadDLVideoError(Exception):
    "The video cannot be downloaded!"
    pass
def version():
    return pbskids_dl_version
try:
    import argparse
    import urllib.request, urllib.error, urllib
    from bs4 import BeautifulSoup
    import json
except:
    raise DependenciesNeeded
def download_fetch_script(url):
    try:
        response = urllib.request.urlopen(url)
        webContent = response.read().decode('UTF-8')
        soup = BeautifulSoup(webContent, features="lxml")
        script = soup.find('script', type='application/json').text
    except:
        raise DownloadFetchScriptError
    return script,soup
def download_find_assets(script):
    try:
        data = json.loads(script)
        assets = data['props']['pageProps']['videoData']['mediaManagerAsset']
        videos = assets['videos']
    except:
        raise DownloadFindAssetsError
    return assets,videos
def download_check_drm(soup):
    isdrm = soup.find('\"drm_enabled\"\:true')
    if str(isdrm) != "None":
        raise DownloadUnsupportedStandard
def download_dl_video(vid_title, video, filename):
    try:
        global realvid
        realvid = video['url']
        print('Downloading Video...')
        print(realvid)
        urllib.request.urlretrieve(realvid, vid_title)
    except:
        raise DownloadDLVideoError
def download_gen_args(args_url, args_dict):
    args = {}
    args["url"] = args_url
    try:
        args["filename"] = args_dict["filename"]
    except TypeError:
        args["filename"] = None
    return args
# No, the script is not designed to be readable.
# It's an API, silly.