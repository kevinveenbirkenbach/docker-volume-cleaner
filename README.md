# 🧹 Docker Volume Cleaner (dockreap)

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-blue?logo=github)](https://github.com/sponsors/kevinveenbirkenbach)
[![Patreon](https://img.shields.io/badge/Support-Patreon-orange?logo=patreon)](https://www.patreon.com/c/kevinveenbirkenbach)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20Coffee-Funding-yellow?logo=buymeacoffee)](https://buymeacoffee.com/kevinveenbirkenbach)
[![PayPal](https://img.shields.io/badge/Donate-PayPal-blue?logo=paypal)](https://s.veen.world/paypaldonate)

**dockreap** is a lightweight Python CLI tool that helps you identify and remove unused **anonymous Docker volumes** — including symlinks and their targets 🗑️

Keep your Docker environment tidy, automated, and efficient 🚀

---

## ⚙️ Features

- Detects anonymous Docker volumes (64-character hash names)
- Skips whitelisted volumes
- Skips bootstrap mounts (`/var/www/bootstrap`)
- Cleans up symlinks **and** their target directories
- Optional confirmation prompt via `--no-confirmation`
- Pure Python — **no external dependencies**

---

## 📦 Installation

### Install from PyPI (recommended)

```bash
pip install dockreap
```

or with an isolated environment:

```bash
pipx install dockreap
```

### Install from source (development)

```bash
git clone https://github.com/kevinveenbirkenbach/dockreap.git
cd dockreap
pip install .
```

---

## 🧪 Usage

```bash
# Basic usage (with confirmation prompt)
dockreap

# Skip confirmation
dockreap --no-confirmation

# Skip specific volumes by adding them to the whitelist
dockreap "volumeid1 volumeid2"

# Skip confirmation + whitelist
dockreap "volumeid1 volumeid2" --no-confirmation
```

📝 Notes:

* Only volumes with **64-character hash names** (anonymous volumes) are considered.
* Volumes mounted at `/var/www/bootstrap` are automatically excluded.
* If a volume’s `_data` directory is a **symlink**, both the symlink **and its target directory** are removed.
* Volumes referenced by **any container (running or stopped)** are not deleted.

---

## 🔐 Requirements

* Python ≥ 3.9
* Docker CLI available and configured
* Sufficient permissions to remove Docker volumes
  (usually requires `root` or membership in the `docker` group)

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Kevin Veen-Birkenbach**
🌍 [https://www.veen.world/](https://www.veen.world/)

```
