# How to Disable TLS 1.0 /1.1 in Apache Server

> 首次發表：2022-06-20

---

筆記一下禁用 TLS 1.0 與 1.1

結論

Apche

sudo vi /etc/apache2/httpd.conf

```
#   SSL Protocol support:
# List the enable protocol levels with which clients will be able to
# connect.  Disable SSLv2 access by default:
SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
```

Windows

[Nartac Software - IIS Crypto](https://www.nartac.com/Products/IISCrypto/)

![Nartac Software - IIS Crypto](dotblogs-09b94ce6-1655716824.jpg)

參照

[How to Disable TLS 1.0 /1.1 in Apache Server - Fedingo](https://fedingo.com/how-to-disable-tls-1-0-1-1-in-apache/)

延伸閱讀

[Azure VPN Windows Server 2012 R2 Error 812](Azure-VPN-Windows-Server-2012-R2-Error-812.md)

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Apache

- 回首頁

---

*本文章從點部落遷移至 Writerside*
