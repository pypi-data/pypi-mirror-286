#!/usr/bin/env python3
#    pbskids-dl
#    Copyright (C) 2024 The pbskids-dl Team
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import libpbskids_dl.api
def download(url, argument=None):
    args = libpbskids_dl.api.download_gen_args(url, argument)
    script, soup = libpbskids_dl.api.download_fetch_script(args["url"])
    libpbskids_dl.api.download_check_drm(soup)
    assets, videos = libpbskids_dl.api.download_find_assets(script)
    if (args["filename"] != None):
        vid_title = args["filename"]
    else:
        vid_title = assets['title'].replace('/','+').replace('\\','+') + '.mp4'
    print(vid_title)
    for video in videos:
        if (video['profile'] == 'mp4-16x9-baseline'):
            libpbskids_dl.api.download_dl_video(vid_title, video, args["filename"])
            print("\nDownload Complete!")
            return True
    print("\nThe operation failed...")
    return False