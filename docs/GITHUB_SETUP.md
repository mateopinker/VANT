# GitHub Setup Notes

Target repository name: `VANT`

Target owner: `mateopinker`

## Repository Upload

Once an empty GitHub repository exists, add it as the remote and push:

```powershell
git remote add origin https://github.com/mateopinker/VANT.git
git push -u origin main
```

## GitHub Wiki Upload

GitHub Wikis are stored as a separate Git repository. After the main repository exists and Wiki is enabled in GitHub settings, publish the wiki seed pages:

```powershell
git clone https://github.com/mateopinker/VANT.wiki.git VANT.wiki
Copy-Item wiki\* VANT.wiki\ -Recurse -Force
git -C VANT.wiki add .
git -C VANT.wiki commit -m "Initialize VANT wiki"
git -C VANT.wiki push
```

The local `wiki/` folder remains the source template for future wiki updates.
