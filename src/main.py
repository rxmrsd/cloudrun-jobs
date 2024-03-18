"""main.py"""
import json

import click


@click.command()
@click.option(
    "--store_list",
    type=str,
    required=True,
)
@click.option(
    "--category_list",
    type=str,
    required=True,
)
def main(store_list: str, category_list: str) -> None:
    print(f"{store_list}: type: {type(store_list)}")
    print(f"{category_list}: type: {type(category_list)}")

    _store_list = json.loads(store_list)
    for _store in _store_list:
        print(f"{_store}: type: {type(_store)}")
    _category_list = json.loads(category_list)
    for _category in _category_list:
        print(f"{_category}: type: {type(_category)}")


if __name__ == "__main__":
    main()
