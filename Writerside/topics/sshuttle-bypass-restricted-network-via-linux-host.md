# 用 sshuttle 透過第二台 Linux 主機的乾淨外網,繞過受限網路封鎖

<web-summary>受限網路擋掉遊戲或特定服務的連線時,若有一台同時連著受限網路與另一條乾淨外網的 Linux 主機,可用 sshuttle 把本機流量透明導出去,只需 SSH、不用在主機上安裝或設定。</web-summary>

如果你的電腦在一個會封鎖特定連線(某些線上遊戲、特定 port 或被 DNS 過濾的網域)的受限網路裡,但你能 SSH 到一台**同時接著「受限網路」和「另一條不受過濾的外網」**的 Linux 主機,最快的解法是在本機用 sshuttle:

```bash
sshuttle --dns -r user@linux-host 0/0 -x 10.0.0.0/8
```

它會把電腦的 TCP 與 DNS 透明地導到那台主機、從它的乾淨外網出去;伺服器端不用裝任何東西、不用 sudo,只走已經通的 SSH(port 22)。

> 本文中的主機名稱、使用者名稱、IP、網段與對外 IP 皆為示意值,請替換成你自己的環境。範例 IP 使用文件保留範圍(RFC 5737:`192.0.2.0/24`、`198.51.100.0/24`、`203.0.113.0/24`)。

## 情境

- 本機(例如 macOS)在受限網路內,對外 IP 走受過濾的 gateway,連某些服務會逾時,甚至連網域都解析不出來。
- 受限網路裡有一台 Linux 主機,你有它的 SSH 金鑰登入。
- 這台 Linux 主機有**第二張網卡接另一條外網**(家用線、獨立 ISP、行動熱點等),而且它的預設路由就走那條線,對外 IP 不經過受限網路的過濾。

典型例子:連線型遊戲(例如 Battle.net 類的登入加上遊戲連線 port 1119 / 3724)在受限網路被擋,但那台 Linux 主機能正常上網。

## 為什麼這樣可行

sshuttle 在本機設定 pf/iptables,把去往目標的 TCP 連線透明攔截,改用 SSH 通道送到遠端主機,再由遠端主機**以它自己的身分**向目標建立連線。那台主機的連線遵循它自己的路由表——既然它的預設路由走那條乾淨外網,導過去的流量就從那條線出去,繞過了本機所在受限網路的封鎖。

它只用已經通的 SSH port 22,遠端端只需要 Python(以你的 SSH 身分執行、不用 sudo、不改動遠端防火牆),所以對共用主機幾乎零干擾、關掉即無痕。

## 前置檢查

先確認那台 Linux 主機真的從乾淨外網出去,而不是繞回受限 gateway:

```bash
# 在 Linux 主機上:預設路由應指向乾淨外網那張網卡
ip route show default
ip route get 1.1.1.1

# 對外 IP 應是那條乾淨線的,而不是受限網路的
curl -s https://ifconfig.co
```

如果主機有兩條預設路由,`metric` 較小者優先;確認 `ip route get 1.1.1.1` 走的是乾淨外網那張介面。

## 操作步驟

<procedure>
<step>
<p>本機安裝 sshuttle(macOS 用 Homebrew):</p>
<code-block lang="bash">
brew install sshuttle
</code-block>
</step>
<step>
<p>啟動隧道。`0/0` 代表其餘流量全導,`-x` 把受限網段排除、維持直連,`--dns` 讓 DNS 查詢也走遠端解析:</p>
<code-block lang="bash">
sshuttle --dns -r user@linux-host 0/0 -x 10.0.0.0/8
</code-block>
<p>第一次會要求輸入本機密碼(macOS 用 pfctl 設定攔截規則)。sshuttle 會自動把 SSH 目標主機本身排除,不會把連到它的流量繞進隧道。</p>
</step>
<step>
<p>隧道開著時再啟動你要用的應用或遊戲。不玩時按 <code>Ctrl-C</code>(或 <code>sshuttle --stop</code>)即回復原本網路。</p>
</step>
</procedure>

想轉背景執行可加 `--daemon`,收掉用 `sshuttle --stop`。

## 驗證方式

隧道開著時,在本機確認對外 IP 已改走乾淨外網:

```bash
curl -s https://ifconfig.co
# 應回那條乾淨外網的對外 IP(例如 203.0.113.10),而非受限網路的(例如 198.51.100.20)
```

確認原本被擋的服務 port 現在連得通。注意 `nc -z` 這種半開探測在 sshuttle 下常誤報 fail,請用實際連線測試:

```bash
# 用真實 TCP 連線測試(以遊戲登入 / 連線 port 為例)
python3 - <<'PY'
import socket
for host, port in [("example-service.net", 1119), ("example-service.net", 443)]:
    ip = socket.gethostbyname(host)
    s = socket.socket(); s.settimeout(6)
    try:
        s.connect((ip, port)); print(f"{host}:{port} OPEN ({ip})")
    except Exception as e:
        print(f"{host}:{port} fail: {e}")
    finally:
        s.close()
PY
```

同時確認受限網路內部資源仍直連(因為 `-x` 排除了那個網段),例如還能 SSH 到內網主機、開內部服務。

若 hostname 一開始就解析不出來,可先參考 [macOS mDNS 與 SSH hostname](macos-mdns-ssh-hostname-resolution.md) 區分「解析不到」與「連不上」。

## 限制與注意

- **只帶 TCP 與 DNS,不帶 UDP。** 多數遊戲的核心連線是 TCP,可正常玩;但 UDP 語音(例如語音聊天)不會通。
- **隧道開著時,所有未被 `-x` 排除的流量都走那條外網**,包含一般瀏覽,對外 IP 會變。只在需要時開啟。
- 每次啟動要輸入一次本機密碼(pfctl)。
- 若那台 Linux 是共用主機,sshuttle 不在上面留任何設定、也不影響其他人的服務;但仍應避免佔用過多頻寬。

## 進階:需要 UDP 時改用 WireGuard

若需要 UDP(語音、其他遊戲)或想要常駐、免每次輸密碼,改在那台 Linux 架 WireGuard,TCP/UDP 全包。代價是:

- 伺服器端要一次性 `sudo` 安裝 `wireguard-tools`、建立介面、加 NAT(`MASQUERADE` 由 wg 網段出乾淨外網那張網卡);若主機上的 Docker 把 `FORWARD` chain 預設設成 `DROP`,PostUp 要明確補上 wg 網段的 `FORWARD ACCEPT`。
- 需要本機到伺服器之間有一個 UDP port 能通;受限網路若把它擋掉,得再用 `udp2raw` 或 `wstunnel` 把 WireGuard 包成 TCP。

一般只是要讓 TCP 遊戲能玩,sshuttle 就足夠,不需要動到伺服器設定。

## 參考資料

- [sshuttle 官方文件](https://sshuttle.readthedocs.io/)
- [WireGuard 官方網站](https://www.wireguard.com/)
