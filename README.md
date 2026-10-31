# Firebase Unity SDK — UPM git mirror

Unmodified Firebase Unity SDK packages from Google's UPM archive
(<https://developers.google.com/unity/archive#firebase>), unpacked so Unity can install them
from a git URL. No LFS: every file stays under GitHub's 100 MiB limit, and `sync.py` refuses a
release that breaks that.

## Install in a project

Each package lives in its own folder; a tag pins the SDK version.

```json
"com.google.firebase.app": "https://github.com/ByteTeknoloji/firebase-unity-upm.git?path=/com.google.firebase.app#14.1.0",
"com.google.firebase.analytics": "https://github.com/ByteTeknoloji/firebase-unity-upm.git?path=/com.google.firebase.analytics#14.1.0",
"com.google.firebase.remote-config": "https://github.com/ByteTeknoloji/firebase-unity-upm.git?path=/com.google.firebase.remote-config#14.1.0"
```

The packages depend on `com.google.external-dependency-manager`, which comes from OpenUPM:

```json
"scopedRegistries": [
  {
    "name": "package.openupm.com",
    "url": "https://package.openupm.com",
    "scopes": ["com.google.external-dependency-manager"]
  }
]
```

## Update to a new SDK version

```bash
python sync.py 14.2.0 app analytics remote-config
git add -A
git commit -m "Firebase Unity SDK 14.2.0"
git tag 14.2.0
git push origin main --tags
```

Then change the `#tag` of every Firebase entry in the project's `Packages/manifest.json` together;
the packages require matching versions.
