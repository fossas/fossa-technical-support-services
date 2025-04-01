# 📦 FOSSA SBOM Upload Script

This Python script automates the process of uploading a Software Bill of Materials (SBOM) file to [FOSSA](https://fossa.com) using their public API.

It:
1. Requests a signed upload URL from FOSSA.
2. Uploads your SBOM file to that signed URL.
3. Triggers a build in FOSSA to analyze the uploaded SBOM.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/fossas/fossa-technical-support-services.git
cd sboms/upload
```

### 2. Set Your FOSSA API Token

You need a [FOSSA API token](https://docs.fossa.com/docs/api-access).

```bash
export FOSSA_TOKEN=your_fossa_api_token
```

### 3. Place Your SBOM File

Ensure your SBOM file is named `file.spdx` and placed in the root of this directory (same directory as the script).

> You can rename your actual SBOM file or modify the script to point to a different filename.

### 4. Run the Script

```bash
python3 upload-sbom.py
```

If everything is successful, you'll see:

```
SBOM uploaded and build triggered successfully.
```

---

## ⚙️ Customizing Project Info

You can change the project `packageSpec` and `revision` by modifying these lines in `upload-sbom.py`:

```python
PACKAGE_SPEC = "your-project-name"
REVISION = "v1.0.0"  # commit SHA or version tag
```

---

## 🧪 Requirements

- Python 3.6+
- `requests` library

Install `requests` if needed:

```bash
pip install requests
```

---

## 🛠 Troubleshooting

- **Token not set?** Make sure `FOSSA_TOKEN` is exported in your terminal.
- **Invalid SBOM file?** Make sure `file.spdx` exists and is a valid SBOM format.
- **Wrong project name or revision?** FOSSA may reject malformed or conflicting inputs.

---

## 📄 License

MIT — free to use and modify.
