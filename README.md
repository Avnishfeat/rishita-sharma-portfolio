# Rishita Sharma Portfolio

Live site: https://freekit.dev/s/rishita-sharma/

This is a static portfolio site. The main editable file is `index.html`, and all images/resume files are inside the `Portfolio` folder.

## Simple Editing Guide

1. Open `index.html` on GitHub.
2. Press the pencil icon to edit.
3. Use `Ctrl + F` to find the text you want to change.
4. Make the edit.
5. Click `Commit changes`.

After a commit, GitHub Actions republishes the FreeKit website automatically. It can take a minute or two for the live site to refresh.

## Replacing Images

Open the `Portfolio` folder, then upload a new file with the same filename as the old one.

Important files:

- Profile photo: `Portfolio/ME.jpeg`
- Resume PDF: `Portfolio/CV_Rishita Sharma.pdf`
- Portfolio screenshots and logos: everything else inside `Portfolio`

Keeping the same filename means the website updates without needing to edit code.

## What Not To Edit

Do not upload or edit these local-only files:

- `deploy/`
- any `.zip` file
- `pagedrop-deploy.json`

They are intentionally ignored by git.

## Hosting

The live website is deployed to FreeKit automatically from GitHub Actions whenever the `main` branch changes.
