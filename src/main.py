"""main.py"""
import json
import logging

import click

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option(
    "--temp_list1",
    type=str,
    required=True,
)
@click.option(
    "--temp_list2",
    type=str,
    required=True,
)
def main(temp_list1: str, temp_list2: str) -> None:
    logging.info(f"{temp_list1}: type: {type(temp_list1)}")
    logging.info(f"{temp_list2}: type: {type(temp_list2)}")

    _temp_list1 = json.loads(temp_list1)
    for _temp in _temp_list1:
        logging.info(f"{_temp}: type: {type(_temp)}")
    _temp_list2 = json.loads(temp_list2)
    for _temp in _temp_list2:
        logging.info(f"{_temp}: type: {type(_temp)}")


if __name__ == "__main__":
    main()
