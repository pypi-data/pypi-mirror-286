import sys
from pathlib import Path

import uvicorn
from pydantic import ValidationError

from .settings import SETS


def main():
    uvicorn.run(
        app="cacheia_api.app:create_app",
        factory=True,
        host=SETS.CACHEIA_HOST,
        port=SETS.CACHEIA_PORT,
        reload=SETS.CACHEIA_RELOAD,
        workers=SETS.CACHEIA_WORKERS,
    )


if __name__ == "__main__":
    try:
        main()
    except ValidationError as e:
        directory = Path(".").absolute()
        print(
            f"The .env file is invalid or could not be "
            f"found on the current directory={directory}.\nValidation Error:\n{e}",
            file=sys.stderr,
        )
