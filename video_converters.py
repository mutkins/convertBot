import subprocess
import os
import logging
from dotenv import load_dotenv
from my_exceptions import ImagickException
from tools import get_filepaths_from_folder


log = logging.getLogger("main")
load_dotenv()
ffmpeg_path = os.environ.get('ffmpeg_path')


async def do_convert_video_folder(folder_name, target_format):
    """This func convert all files target_format in folder_name and put new files in same folder"""
    for source_file_path in await get_filepaths_from_folder(folder_name=folder_name, file_format='*'):
        result_file_path = source_file_path.split(sep='.')[-2] + f'.{target_format}'
        try:
            result = subprocess.run(f'{ffmpeg_path} -i {source_file_path} {result_file_path}', capture_output=True)
            if result.returncode:
                raise ImagickException(message=result.stderr)
            else:
                pass
        except ImagickException as e:
            log.error(e)
            raise Exception(e)