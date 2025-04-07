# 🧹 Docker Volume Cleaner

**Docker Volume Cleaner** is a lightweight Python tool that helps you identify and remove unused anonymous Docker volumes — including symlinks and their targets 🗑️

Keep your Docker environment tidy, automated, and efficient 🚀

---

## 📦 Installation

Install it using [Kevin’s Package Manager](https://github.com/kevinveenbirkenbach/package-manager) with the alias:

```bash
pkgmgr install dockreap
```

> `dockreap` is the alias for this tool within `pkgmgr`.  
> Repository: [github.com/kevinveenbirkenbach/docker-volume-cleaner](https://github.com/kevinveenbirkenbach/docker-volume-cleaner)

---

## ⚙️ Features

- Detects all anonymous Docker volumes (64-character hashes)
- Skips whitelisted volumes
- Skips bootstrap mounts (`/var/www/bootstrap`)
- Cleans up symlinks **and** their target directories
- Optional confirmation prompt via `--no-confirmation`
- Pure Python — **no dependencies**

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🤖 Built with ChatGPT

Developed with the help of [ChatGPT]([https://chat.openai.com/share/7b177eef-b97f-4e63-b2ef-cfdc69c2337e](https://chatgpt.com/share/67f3c910-2ea0-800f-85db-71ec39a713f2)) 🤝

---

## 👤 Author

**Kevin Veen-Birkenbach**  
🌍 [https://www.veen.world/](https://www.veen.world/)
