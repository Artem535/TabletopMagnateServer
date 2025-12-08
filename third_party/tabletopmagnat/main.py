import asyncio
from tabletopmagnat.application.application import Application  # type: ignore

if __name__ == "__main__":
    asyncio.run(Application().run("Расскажи правила игры Подземелье и Песики"))