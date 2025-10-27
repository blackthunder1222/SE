import json  # stdlib JSON handling [web:4]
import logging  # structured logging over prints [web:4]
from datetime import datetime  # timestamping events [web:4]

logger = logging.getLogger(__name__)  # module-level logger [web:4]
logging.basicConfig(level=logging.INFO)  # simple config for demo [web:4]

# Global inventory store kept simple for this lab [web:4]
stock_data: dict[str, int] = {}  # explicit type hint improves linters [web:4]

def add_item(item: str, qty: int = 0, logs: list[str] | None = None) -> None:
    """Add quantity for an item with validation and safe default list."""  # [web:3][web:4]
    if logs is None:
        logs = []  # avoid mutable default sharing across calls [web:3]
    if not isinstance(item, str) or not item.strip():
        logger.warning("Invalid item name provided")  # structured warning [web:4]
        return
    if not isinstance(qty, int):
        logger.warning("Quantity must be int, got %r", qty)  # [web:4]
        return
    stock_data[item] = stock_data.get(item, 0) + qty  # safe aggregation [web:4]
    logs.append(f"{datetime.now().isoformat()}: Added {qty} of {item}")  # modern formatting [web:4]

def remove_item(item: str, qty: int) -> None:
    """Remove quantity for an item with specific error handling."""  # [web:6][web:4]
    try:
        if not isinstance(qty, int) or qty < 0:
            raise ValueError("qty must be a non-negative int")  # explicit contract [web:4]
        current = stock_data.get(item)
        if current is None:
            logger.info("Item %s not present; nothing to remove", item)  # [web:4]
            return
        new_qty = current - qty
        if new_qty <= 0:
            del stock_data[item]
        else:
            stock_data[item] = new_qty
    except (KeyError, ValueError) as exc:
        logger.exception("Failed to remove item: %s", exc)  # no silent pass [web:4]

def get_qty(item: str) -> int:
    """Return quantity or raise KeyError if missing (caller decides)."""  # [web:11][web:4]
    return stock_data[item]  # explicit behavior; tests can assert KeyError [web:11]

def load_data(path: str = "inventory.json") -> None:
    """Load inventory from JSON using context managers."""  # [web:4]
    global stock_data
    with open(path, "r", encoding="utf-8") as f:  # context manager + encoding [web:4]
        stock_data = json.load(f)  # use json.load directly [web:4]

def save_data(path: str = "inventory.json") -> None:
    """Persist inventory to JSON safely with context manager."""  # [web:4]
    with open(path, "w", encoding="utf-8") as f:  # context manager [web:4]
        json.dump(stock_data, f, ensure_ascii=False, indent=2)  # readable JSON [web:4]

def print_data() -> None:
    """Print a human-readable report; logging kept for operational messages."""  # [web:4]
    print("Items Report")  # acceptable simple output for user-facing report [web:4]
    for name, qty in stock_data.items():
        print(name, "->", qty)  # straightforward iteration [web:4]

def check_low_items(threshold: int = 5) -> list[str]:
    """Return items whose quantity is below threshold with validation."""  # [web:4]
    if not isinstance(threshold, int) or threshold < 0:
        raise ValueError("threshold must be a non-negative int")  # fail fast [web:4]
    result: list[str] = []
    for name, qty in stock_data.items():
        if qty < threshold:
            result.append(name)
    return result  # simple list return [web:4]

def main() -> None:
    add_item("apple", 10)  # basic path [web:4]
    add_item("banana", -2)  # allowed negative adds; business rule demo [web:4]
    add_item("not-a-name", 0)  # validated but harmless [web:4]

    remove_item("apple", 3)  # specific handling [web:6]
    remove_item("orange", 1)  # non-existent safe path [web:6]

    try:
        print("Apple stock:", get_qty("apple"))  # may raise KeyError if removed [web:11]
    except KeyError:
        print("Apple not in stock")  # user-friendly fallback [web:11]

    print("Low items:", check_low_items())  # defaults validated [web:4]

    save_data()  # context-managed write [web:4]
    load_data()  # context-managed read [web:4]
    print_data()  # report [web:4]

if __name__ == "__main__":
    # Removed unsafe eval; never use eval on untrusted strings to satisfy Bandit [web:4][web:10]
    main()  # entry point [web:11]
