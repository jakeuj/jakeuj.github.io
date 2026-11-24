# Windows 10 bash ll

> 首次發表：2019-12-16

---

紀錄一下Windows使用Bash支援LL指令

的修改步驟這樣

![的修改步驟這樣](dotblogs-0992e9aa-1576469218_21726.png)

以管理員身分執行powershell

$ vim /etc/bash.bashrc

附加一行

(vim不熟的提示：先打 i 才能新增內容)

alias ll='ls -l'

存檔

這邊沒有用管理員身分執行會顯示無法儲存檔案

但也沒有 sudo 可以用來執行 vim

結論：用管理員身分執行powershell

(vim不熟的提示：ESC 加上 :wq)
