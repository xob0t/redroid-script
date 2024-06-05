import os
import shutil
from stuffs.general import General
from tools.helper import get_download_dir, host, print_color, run, bcolors

class Gp_unlim(General):
    dl_link = "https://gitlab.com/cuynu/gphotos-unlimited-zygisk/uploads/0447f2d3e9426bad0caa7621c4218ea4/gphoto-unlimited-zygisk-v1.1-stable.zip"
    arch = host()
    download_loc = get_download_dir()
    dl_file_name = os.path.join(download_loc, "gphoto-unlimited.zip")
    copy_dir = "./gp_unlim"
    extract_to = "/tmp/gp_unlim/extract"
    act_md5 = "95c5413f173aac9bc5f321b791c951f2"

    def download(self):
        print_color("Downloading gphoto-unlimited now .....", bcolors.GREEN)
        super().download()

    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        run(["chmod", "+x", self.extract_to, "-R"])
    
        print_color("Copying gphoto-unlimited files ...", bcolors.GREEN)
        shutil.copytree(os.path.join(self.extract_to, "system"), os.path.join(self.copy_dir, "system"), dirs_exist_ok=True)