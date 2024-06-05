#!/usr/bin/env python3

import argparse
import subprocess
from stuffs.gapps import Gapps
from stuffs.gp_unlim import Gp_unlim
from stuffs.magisk import Magisk
from stuffs.ndk import Ndk
from stuffs.widevine import Widevine
import tools.helper as helper


def main():
    dockerfile = ""
    tags = []
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-a', '--android-version',
                        dest='android',
                        help='Specify the Android version to build',
                        default='11.0.0',
                        choices=['13.0.0', '12.0.0', '12.0.0_64only', '11.0.0', '10.0.0', '9.0.0', '8.1.0'])
    parser.add_argument('-g', '--install-gapps',
                        dest='gapps',
                        help='Install OpenGapps to ReDroid',
                        action='store_true')
    parser.add_argument('-u', '--install-gp-unlim',
                    dest='gp_unlim',
                    help='Install gphoto-unlimited to ReDroid',
                    action='store_true')
    parser.add_argument('-n', '--install-ndk-translation',
                        dest='ndk',
                        help='Install libndk translation files',
                        action='store_true')
    parser.add_argument('-m', '--install-magisk', dest='magisk',
                        help='Install Magisk ( Bootless )',
                        action='store_true')
    parser.add_argument('-w', '--install-widevine', dest='widevine',
                        help='Integrate Widevine DRM (L3)',
                        action='store_true')
    parser.add_argument('-c', '--container', 
                        dest='container',
                        default='docker',
                        help='Specify container type', 
                        choices=['docker', 'podman'])

    args = parser.parse_args()
    dockerfile = dockerfile + \
        "FROM redroid/redroid:{}-latest\n".format(
            args.android)
    tags.append(args.android)
    if args.gapps:
        Gapps().install()
        dockerfile = dockerfile + "COPY gapps /\n"
        tags.append("gapps")
    if args.gp_unlim:
        Gp_unlim().install()
        dockerfile = dockerfile + "COPY gp_unlim /\n"
        tags.append("gp-unlim")
    if args.ndk:
        if args.android in ["11.0.0", "12.0.0", "12.0.0_64only"]:
            arch = helper.host()[0]
            if arch == "x86" or arch == "x86_64":
                Ndk().install()
                dockerfile = dockerfile+"COPY ndk /\n"
                tags.append("ndk")
        else:
            helper.print_color(
                "WARNING: Libndk seems to work only on redroid:11.0.0 or redroid:12.0.0", helper.bcolors.YELLOW)
    if args.magisk:
        Magisk().install()
        dockerfile = dockerfile+"COPY magisk /\n"
        tags.append("magisk")
    if args.widevine:
        Widevine(args.android).install()
        dockerfile = dockerfile+"COPY widevine /\n"
        tags.append("widevine")
    print("\nDockerfile\n"+dockerfile)
    with open("./Dockerfile", "w", encoding="utf-8") as f:
        f.write(dockerfile)
    new_image_name = "redroid/redroid:"+"_".join(tags)
    subprocess.run([args.container, "build", "-t", new_image_name, "."])
    helper.print_color("Successfully built {}".format(
        new_image_name), helper.bcolors.GREEN)


if __name__ == "__main__":
    main()
