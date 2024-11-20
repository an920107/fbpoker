from datetime import datetime


def log(message: str, log_path: str = None, time: datetime = None) -> None:
    if time is None:
        time = datetime.now()
    print(f"[{time}] {message}")
    if log_path:
        with open(log_path, "a") as f:
            f.write(f"[{time}] {message}\n")
