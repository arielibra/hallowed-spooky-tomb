"""Download story videos from an Instagram user.

Usage:
    python download_story.py YOUR_USERNAME TARGET_USERNAME

Stories always require login. You can only see stories that your own
account can see (public accounts, or private accounts you follow).
Videos are saved to downloads/<target_username>/.
"""
import sys
from pathlib import Path

import instaloader


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    my_username, target = sys.argv[1], sys.argv[2]
    out_dir = Path("downloads") / target

    L = instaloader.Instaloader(
        dirname_pattern=str(out_dir),
        download_pictures=False,      # videos only
        download_video_thumbnails=False,
        save_metadata=False,
        compress_json=False,
    )

    # Reuse a saved session if there is one, otherwise log in (asks for password).
    try:
        L.load_session_from_file(my_username)
    except FileNotFoundError:
        L.interactive_login(my_username)
        L.save_session_to_file()

    profile = instaloader.Profile.from_username(L.context, target)

    count = 0
    for story in L.get_stories(userids=[profile.userid]):
        for item in story.get_items():
            if item.is_video:
                L.download_storyitem(item, target=target)
                count += 1

    if count:
        print(f"Downloaded {count} story video(s) to {out_dir}/")
    else:
        print(f"No story videos found for {target} (no active story, or you can't see it).")


if __name__ == "__main__":
    main()
