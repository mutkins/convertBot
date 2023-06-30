import subprocess
import os
import logging
from dotenv import load_dotenv
from my_exceptions import ImagickException

log = logging.getLogger("main")
load_dotenv()
imagick_path = os.environ.get('imagick_path')


async def do_convert_folder(folder_name, target_format):
    """This func convert all files target_format in folder_name and put new files in same folder"""
    try:
        result = subprocess.run(f'mogrify -format {target_format} temp/{folder_name}/*.*',
                                capture_output=True, shell=True)  # FOR LINUX
        # result = subprocess.run(f'{imagick_path} mogrify -format {target_format} temp/{folder_name}/*.*', capture_output=True) - FOR WINDOWS
        if result.stderr:
            raise ImagickException(message=result.stderr)
        else:
            return None
    except ImagickException as e:
        log.error(e)
        raise Exception(e)
