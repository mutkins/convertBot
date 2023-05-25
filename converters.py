import subprocess
import os
import logging
import io
from dotenv import load_dotenv
from my_exceptions import ImagickException

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")

load_dotenv()
imagick_path = os.environ.get('imagick_path')


def do_convert(input_filepath, target_format):
    output_filepath = input_filepath.rsplit(sep=".", maxsplit=1)[0] + f".{target_format}"
    result = subprocess.run(f"{imagick_path} {input_filepath} {output_filepath}", capture_output=True)
    try:
        if result.stderr:
            raise ImagickException(message=result.stderr)
        else:
            return output_filepath
    except ImagickException as e:
        log.error(e)
        raise Exception(e)
