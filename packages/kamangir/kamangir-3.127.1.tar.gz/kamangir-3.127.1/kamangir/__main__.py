import argparse
from kamangir import NAME, VERSION, DESCRIPTION, ICON
from kamangir import README
from kamangir.logger import logger
from blueness.argparse.generic import main

success, message = main(
    __file__,
    NAME,
    VERSION,
    DESCRIPTION,
    ICON,
    {
        "build_README": lambda _: README.build(),
    },
)
if not success:
    logger.error(message)
