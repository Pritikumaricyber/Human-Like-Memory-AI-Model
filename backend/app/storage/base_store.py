from typing import Generic, TypeVar

T = TypeVar("T")


class BaseStore(Generic[T]):
    """
    Generic in-memory storage repository.
    """

    def __init__(self):
        self._items: list[T] = []

    def add(self, item: T) -> None:
        """
        Add an item.
        """
        self._items.append(item)

    def get_all(self) -> list[T]:
        """
        Return all items.
        """
        return self._items

    def get_by_id(self, item_id: str):
        """
        Find an item by ID.
        """
        for item in self._items:
            if getattr(item, "id", None) == item_id:
                return item

        return None

    def update(self, updated_item: T) -> bool:
        """
        Update an existing item.
        """
        for index, item in enumerate(self._items):
            if getattr(item, "id", None) == getattr(updated_item, "id", None):
                self._items[index] = updated_item
                return True

        return False

    def delete(self, item_id: str) -> bool:
        """
        Delete an item by ID.
        """
        for index, item in enumerate(self._items):
            if getattr(item, "id", None) == item_id:
                del self._items[index]
                return True

        return False

    def count(self) -> int:
        """
        Return the total number of items.
        """
        return len(self._items)

    def clear(self) -> None:
        """
        Remove all items.
        """
        self._items.clear()