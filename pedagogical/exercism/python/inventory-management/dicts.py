"""Functions to keep track and alter inventory."""


def create_inventory(items: list[str]) -> dict:
    inventory: dict[str, int] = {}
    for item in items:
        inventory[item] = inventory.get(item, 0) + 1
    return inventory


def add_items(inventory: dict[str, int], items: list[str]) -> dict:
    for item in items:
        inventory[item] = inventory.get(item, 0) + 1
    return inventory


def decrement_items(inventory: dict[str, int], items: list[str]) -> dict:
    for item in items:
        if inventory.get(item, 0) > 0:
            inventory[item] -= 1
    return inventory


def remove_item(inventory: dict[str, int], item: str) -> dict:
    inventory.pop(item, None)
    return inventory


def list_inventory(inventory: dict[str, int]) -> list[tuple]:
    return [(item, count) for item, count in inventory.items() if count > 0]
