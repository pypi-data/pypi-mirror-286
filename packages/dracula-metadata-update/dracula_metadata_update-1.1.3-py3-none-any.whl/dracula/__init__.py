import sys
from .dracula import main

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_metadata.py <folder_path> [image_path]")
        sys.exit(1)

    folder_path = sys.argv[1]
    image_path = sys.argv[2] if len(sys.argv) > 2 else None
    album_name = "드라큘라 10주년 스튜디오 OST"

    main(folder_path, album_name, image_path)