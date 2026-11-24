# Git Credential Manager for Windows 登入失敗處理

<web-summary>Windows 上 Git 一直登入失敗時，確認裝的是新版 git-credential-manager，並清除舊版殘留的 credential 設定。</web-summary>

> 首次發表：2024-03-06

Git 一直登入失敗時，先確認裝的是新版 Git Credential Manager，再清除舊版留下的 `credential` 設定。

## 安裝新版

[Releases · git-ecosystem/git-credential-manager (github.com)](https://github.com/git-ecosystem/git-credential-manager/releases)

上面是支援 MFA 的新版；下面是已停止維護的舊版，誤裝會一直登入失敗。

[~~Releases · microsoft/Git-Credential-Manager-for-Windows (github.com)~~](https://github.com/microsoft/Git-Credential-Manager-for-Windows/releases)

## 清除舊設定

舊版留下的 `credential` 區段要刪掉。可以用 TortoiseGit 的設定頁依序檢查本地、全域和系統三層 `.gitconfig`，以下是清除後的樣子。

### .gitconfig

- 本地
  - 清空
- 全域

```
[user]
name = <your-name>
email = <your-email>
```

- 系統

```
[diff "astextplain"]
textconv = astextplain
[filter "lfs"]
clean = git-lfs clean -- %f
smudge = git-lfs smudge -- %f
process = git-lfs filter-process
required = true
[http]
sslBackend = openssl
sslCAInfo = C:/Program Files/Git/mingw64/etc/ssl/certs/ca-bundle.crt
[core]
autocrlf = true
fscache = true
symlinks = false
[pull]
rebase = false
[credential]
helper = manager
[credential "https://dev.azure.com"]
useHttpPath = true
[init]
defaultBranch = master
```

## 參照

[介紹好用工具：Git Credential Manager for Windows (記憶 Git 常用密碼) | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2016/02/01/Useful-tool-Git-Credential-Manager-for-Windows)
