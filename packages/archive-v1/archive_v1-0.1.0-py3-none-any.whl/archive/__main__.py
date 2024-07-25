import pathlib
import datetime
import shutil
from pathlib import Path
import argparse
import toml
from dataclasses import dataclass

CWD = Path().resolve()

@dataclass
class Config:
    root: Path
    archive_path: Path
    timezone: int

def get_config() -> Config:
    d = CWD
    config_file = 'archive.toml'
    while True:
        path = d / config_file
        if path.exists():
            break
        p = d.parent
        print(d, p)
        if p == d:
            raise f"{config_file} not found."
        d = p

    root = d
    with path.open() as f:
        data = toml.load(f)
        archive_path = root / data['path']
        timezone = data['timezone']
    return Config(root, archive_path, timezone)


# def main(targets: list[str], tz: int):
def main(targets: list[str]):
    config = get_config()
    TZ = datetime.timezone(datetime.timedelta(hours=config.timezone))
    TODAY = datetime.datetime.now(TZ).strftime("%Y%m%d")
    print(f"Today: {TODAY}")
    ROOT = config.root
    ARCHIVE = config.archive_path / TODAY

    for t in targets:
        t = pathlib.Path(t)
        if not t.exists():
            print(f"{t} does not exist.")
            continue
        # t_rel = t.resolve().relative_to(ROOT, walk_up=True)
        t_rel = t.resolve().relative_to(ROOT) # python 3.8
        out = ARCHIVE / t_rel
        ver = 1
        while out.exists():
            ver += 1
            out = ARCHIVE / f"{t_rel}_v{ver}"
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(t, out)
        print(f"Moved {t} to {out}")


def cli() -> None:
    p = argparse.ArgumentParser('archive')
    # p.add_argument(
    #     '-t', '--timezone',
    #     type=int, default=0,
    #     help='e.g. GMT+9 -> 9',
    # )
    p.add_argument('targets', nargs='+')
    a = p.parse_args()
    # main(a.targets, a.timezone)
    main(a.targets)

if __name__ == "__main__":
    cli()
