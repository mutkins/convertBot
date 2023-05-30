import logging
from aiogram.utils import executor
from create_bot import dp
from handlers import common, covnert

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


# Register handlers from handlers folder
common.register_handlers(dp)
covnert.register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
