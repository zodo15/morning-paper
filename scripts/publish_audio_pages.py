#!/usr/bin/env python3
"""Publish converted audio (audio/*.m4a, audio/*.times.json) to the gh-pages
branch, which GitHub Pages serves at https://zodo15.github.io/morning-paper/audio/.
The Vercel rewrite in vercel.json maps /audio/* there, so site URLs stay
same-origin and data files keep their relative audio/... paths.

Run AFTER publish_day.py has converted the day's audio, e.g.:
  python3 scripts/publish_audio_pages.py --push

Uses a temporary worktree of gh-pages; commits and pushes only audio changes.
Needs the repo's push credentials on the origin remote (or pass --no-push).
"""
import argparse, os, subprocess, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WT = '/tmp/morning-paper-gh-pages'

def run(cmd, cwd=None):
    print('+', ' '.join(cmd))
    subprocess.run(cmd, cwd=cwd or ROOT, check=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--push', action='store_true', help='push gh-pages to origin')
    a = ap.parse_args()

    if not os.path.isdir(os.path.join(ROOT, 'audio')):
        sys.exit('no audio/ directory - run publish_day.py first')
    if os.path.exists(WT):
        shutil.rmtree(WT)
    run(['git', 'worktree', 'add', '--force', WT, 'gh-pages'])
    os.makedirs(os.path.join(WT, 'audio'), exist_ok=True)
    copied = 0
    for f in sorted(os.listdir(os.path.join(ROOT, 'audio'))):
        if f.endswith('.m4a') or f.endswith('.times.json'):
            shutil.copy2(os.path.join(ROOT, 'audio', f), os.path.join(WT, 'audio', f))
            copied += 1
    print(f'copied {copied} audio files into gh-pages worktree')
    run(['git', 'add', 'audio'], cwd=WT)
    if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=WT).returncode == 0:
        print('no audio changes on gh-pages')
    else:
        run(['git', 'commit', '-m', 'Publish audio to Pages host'], cwd=WT)
        if a.push:
            run(['git', 'push', 'origin', 'gh-pages'], cwd=WT)
        else:
            print('committed locally; rerun with --push to publish')
    run(['git', 'worktree', 'remove', '--force', WT])

if __name__ == '__main__':
    main()
