# 用 sshuttle 透過雙網卡 Linux：外網出口與公司內網分流

<web-summary>用 sshuttle 經雙網卡 Linux 切換兩種連線方式：在受限網路內使用獨立外網出口，或直接連外網、只把公司內網與 DNS 送進隧道，並驗證路由、服務連線與關閉清理。</web-summary>

大部分流量都是一般上網、只有少數連線需要公司跳板機或內部網站時，可以讓 Mac 直接接獨立外網，再用 sshuttle 只承接公司網段。Mac 留在公司網路時，則保留原本「內網直連、公開 TCP 經 Linux 出去」的方式，依目前網路選用。

| 模式 | Mac 所在網路 | 經過 Linux 的流量 | 維持直連的流量 |
| --- | --- | --- | --- |
| A：獨立外網出口 | 公司或其他受限網路 | 公開 IPv4 TCP 與一般 DNS | 被排除的公司／私有網段 |
| B：公司內網分流 | Linux 所在的獨立外網區網 | 指定公司網段 TCP、公司網域 DNS | 一般上網及其他 DNS |

> 主機名稱、帳號、IP、網域、介面與連線設定名稱皆為示意值，請替換成實際環境。公網與獨立區網示意位址使用 RFC 5737 文件範圍；公司範例使用私有網段，並不代表所有環境都應攔截整個 `10.0.0.0/8`。

## 網路條件與運作方式

假設 Linux 同時接著兩個網路：

| 項目 | 示意設定 |
| --- | --- |
| Linux 公司介面 | `wlan0`，`10.40.10.20/24` |
| 公司閘道／NetworkManager profile | `10.40.10.1`／`corp-wifi` |
| Linux 獨立外網介面 | `eth0`，`192.0.2.10/24` |
| 外網預設閘道 | `192.0.2.1`，metric 100 |
| Linux 在外網區網的 mDNS 名稱 | `relay.local` |
| 公司 DNS | `10.40.0.53` |
| RDP 跳板機／內部網站 | `10.40.20.10:3389`／`portal.corp.example.com`（`10.40.30.40`） |

sshuttle 在 Mac 以 pf 攔截指定目的地的 TCP，經 SSH 把資料送到 Linux，再由 Linux 重新向目標建立連線。因此 Linux 自己的路由表決定最後使用哪張網卡；Mac 上指定公司網段，不會自動替 Linux 補上公司路由。

代理本身只需要 Linux 上相容的 Python 與既有 SSH，不需遠端 root 或另外安裝 sshuttle。若缺公司路由，初始化該路由仍需要 Linux 管理權限；Mac 端設定 pf 也需要 sudo。

這裡的「獨立外網區網」是另一條線路上的 LAN。Mac 與 Linux 同在該區網時才可直接用 `.local`；Linux 能連外網，不代表從家中或手機熱點就能連進來。名稱解析問題可參考 [macOS mDNS 與 SSH hostname](macos-mdns-ssh-hostname-resolution.md)。

## 模式 A：從受限網路使用獨立外網出口 {#outbound}

```text
Mac（公司網路）
├─ 公司／私有網段 → 直連
└─ 公開 IPv4 TCP、一般 DNS → SSH → Linux → 獨立外網
```

先在 Linux 確認公開目的地走外網介面：

```bash
ip route show default
ip route get 1.1.1.1
curl -4 -s https://ifconfig.co/ip
```

兩張網卡都有預設路由時，較小的 metric 優先；同時要留意更具體的路由。範例預期公開目的地經 `eth0`、`192.0.2.1` 出去。

Mac 安裝並以前景啟動：

```bash
brew install sshuttle

sshuttle --dns -r user@10.40.10.20 0/0 \
  -x 10.0.0.0/8 -x 172.16.0.0/12 -x 192.168.0.0/16
```

`0/0` 代表所有 IPv4 位址，三個 `-x` 讓私有網段直連；`--dns` 把系統一般 DNS 查詢送到遠端。隧道開啟後再啟動應用程式，結束時按 Ctrl-C。

這個模式適合 Mac 必須留在受限網路的情況。若絕大多數流量都要連外、Mac 也能直接接獨立外網，模式 B 可以減少經過 SSH 的一般上網流量。

## 模式 B：直接上外網，只將公司網段送進隧道 {#inbound}

```text
Mac（獨立外網區網）
├─ 一般網站、遊戲、下載 → 直接上網
└─ 公司 TCP、公司網域 DNS → SSH → Linux → 公司網路
```

這裡調整的是要承接的目的網段，SSH 仍由 Mac 主動連 Linux，不需要改用 SSH `-R`。

### 確認兩端路由 {#inbound-routes}

先在 Mac 確認目前網路與 SSH：

```bash
route -n get default
ipconfig getifaddr en0
ssh -4 -o BatchMode=yes -o ConnectTimeout=5 user@relay.local 'hostname'
```

`en0` 請換成實際預設介面。接著在 Linux 查公司 DNS、跳板機與公開目的地：

```bash
ip route get 10.40.0.53
ip route get 10.40.20.10
ip route get 1.1.1.1
```

常見問題是 Linux 只有 `10.40.10.0/24` 的直連公司路由，其他公司 IP 都落到外網預設路由。此時即使 Mac 已設定 sshuttle，服務仍會逾時。

若實際公司資源確實都在 `10.0.0.0/8`，可在 Linux 的 NetworkManager profile 新增公司路由。先讀既有設定，確認沒有相同項目，再執行新增：

```bash
nmcli -g ipv4.routes connection show corp-wifi

sudo nmcli connection modify corp-wifi \
  +ipv4.routes "10.0.0.0/8 10.40.10.1 600"
sudo nmcli device reapply wlan0
```

`+ipv4.routes` 保留其他靜態路由；`device reapply` 嘗試將設定套用到已連線介面，不需為了這條路由重啟網卡。公司流量應改走 `wlan0`，公開目的地仍走外網預設路由。只需要少數公司網段時，就列出實際 CIDR，避免攔截其他私有網路或容器網段。

`nmcli -g` 會回傳 `10.0.0.0/8 10.40.10.1 600` 這種可解析格式；不要拿一般顯示模式的 `{ ip = ..., nh = ..., mt = ... }` 格式去驗證，否則可能把成功新增誤判成失敗。

### 啟動公司 TCP 與指定 DNS 的隧道 {#inbound-start}

Mac 的第一個終端機以前景執行：

```bash
sshuttle -v --method pf \
  -e 'ssh -4 -o BatchMode=yes -o ConnectTimeout=5 -o ServerAliveInterval=15 -o ServerAliveCountMax=3' \
  -r user@relay.local \
  --ns-hosts 10.40.0.53 --to-ns 10.40.0.53 \
  10.0.0.0/8
```

這裡沒有 `0/0`，所以公開 IPv4 TCP 不會被這條隧道攔截。`--ns-hosts` 只承接送往指定 DNS 伺服器的普通 DNS 查詢，`--to-ns` 指定遠端使用的 DNS。兩者要搭配後續 macOS 的公司網域設定，才是完整的 DNS 分流。

先確認公司 DNS 可經隧道查詢：

```bash
dig +time=2 +tries=1 @10.40.0.53 portal.corp.example.com A
```

只有 `Connected to server.` 還不足以代表 pf 已完成設定；先用實際查詢確認，再啟用系統 DNS 分流。

## 公司網域的 DNS 分流 {#split-dns}

只承接公司 TCP，並不能讓外網 DNS 自動解析公司網站。直接照搬模式 A 的 `--dns`，則會把一般 DNS 也送進 Linux。

在 Mac 第二個終端機開啟 `scutil`：

```bash
sudo scutil
```

接著在 scutil 提示符號輸入下列內容。這是 scutil 的指令，不是另開 shell 執行的 Bash：

```text
d.init
d.add ServerAddresses * 10.40.0.53
d.add SupplementalMatchDomains * corp.example.com internal.example.net
d.add SupplementalMatchDomainsNoSearch # 1
add State:/Network/Service/example-corp-tunnel/DNS temporary
```

保持這個 scutil 工作階段開著。`corp.example.com` 與 `internal.example.net` 才使用公司 DNS，其他網域沿用外網 DNS。請列出真正需要公司解析的網域；`.local` 仍交給原本的 mDNS。

`temporary` 設定屬於目前工作階段，輸入 `quit`、或該工作階段結束後就會撤除。若使用 heredoc 傳送上述內容後立刻結束 scutil，暫時設定也會立刻被撤除。

在另一個終端機確認系統已採用設定：

```bash
scutil --dns
sudo dscacheutil -flushcache
dscacheutil -q host -a name portal.corp.example.com
```

`dig @公司DNS` 是直接查指定伺服器，`dscacheutil` 才能用來確認 macOS 系統解析；瀏覽器若自訂 DNS over HTTPS，也要確認公司網域使用系統 DNS。

手動使用兩個工作階段時，停止前先在 scutil 輸入 `quit`，再對 sshuttle 按 Ctrl-C。若 SSH 提前中斷，也要結束仍開著的 scutil，撤除公司 DNS 分流。

### 整合為啟動器的生命週期 {#launcher-lifecycle}

要自動處理清理，可由同一個控制器管理 sshuttle 與 scutil 子程序：

1. 檢查目前區網、SSH、Linux 公司路由及重複啟動。
2. 取得 Mac sudo 驗證，啟動 sshuttle，確認經 pf 的公司 DNS 查詢成功。
3. 啟動 scutil 並持有 stdin，建立暫時 resolver，再確認系統解析。
4. 遇到 Ctrl-C、啟動失敗、SSH 中斷或 DNS 子程序退出，關閉 scutil 工作階段並停止本次隧道。

暫時工作階段結束即可撤除 DNS，不必在長時間連線後再次 sudo 才能清理，也不必留下永久的 `/etc/resolver` 檔案。只處理自己建立的子程序，保留既有連線與其他 pf 使用者的設定。

## 驗證服務與分流 {#verification}

以實際服務協定驗證連線：

```bash
# HTTPS 應建立 TLS，並收到目標服務的 HTTP 回應
curl -I --connect-timeout 5 --max-time 10 https://portal.corp.example.com/

# 公開 HTTPS 也應繼續可用
curl -4 -I --connect-timeout 5 --max-time 10 https://example.com/
```

RDP 請用遠端桌面工具連到 `10.40.20.10:3389`，確認能到登入流程。`nc -z` 或 Python `socket.connect()` 可能先被本機透明代理接受，因此成功建立 TCP 仍不能單獨證明 Linux 已連上真正目標。

網站回 HTTP 403 代表已收到伺服器回應，應再檢查網址、登入狀態與網站規則；不要把它等同於路由或 TLS 逾時。實際能否使用頁面，仍以使用者的瀏覽器操作確認。

模式 A 可比較隧道前後的對外 IP；模式 B 的 Mac 與 Linux 如果共用同一條外網，對外 IP 可能原本就相同，應改看 pf 的目的網段與 sshuttle 的 `Accept TCP` 日誌。

以日誌中的實際 anchor 名稱取代以下 `sshuttle-12300`：

```bash
sudo pfctl -a sshuttle-12300 -sn
sudo pfctl -a sshuttle-12300 -sr
sudo pfctl -s info
```

模式 B 的 TCP 攔截目的地應為指定公司網段，DNS 則限指定伺服器的 port 53。讀取本次規則時使用 `-sn`／`-sr`；`-s all` 即使指定 anchor，仍可能帶出全域連線狀態與計數器。

## 停止、故障與回復 {#cleanup}

驗證至少包括正常 Ctrl-C，以及只中斷測試隧道的 SSH 連線。兩者都應撤除公司 DNS 與本次攔截規則，讓公開上網持續正常；刻意模擬斷線時看到 `fatal: ssh connection ... exited` 是預期現象。

pf 的 anchor 名稱可能在規則被清空後仍保留。清理驗收應比對啟動前後的 NAT／過濾規則與 pf 啟用狀態，而不是要求所有 anchor 名稱消失。若啟動前已有其他程式使用 pf，關閉隧道後也可能仍維持 Enabled；應回復原先狀態，不要全域清空 pf 或強制關掉其他程式的防火牆。

本例使用前景 Ctrl-C。sshuttle 2.0.0 沒有 `--stop` 選項；需要背景執行時，應使用明確的 pidfile 管理該次程序，並另行管理 DNS 工作階段。

若只出現 `warning: closed channel 16 got cmd=TCP_STOP_SENDING len=0`，代表已關閉的 channel 又收到停止傳送通知，單憑這行不能判定整條 SSH 隧道故障；應搭配服務狀態、SSH 是否退出與清理結果判斷。

Linux 公司路由是持久設定，關閉 Mac 隧道不會自動移除。確定不再需要這條新增路由時，先關閉隧道，再在 Linux 移除精確項目：

```bash
sudo nmcli connection modify corp-wifi \
  -ipv4.routes "10.0.0.0/8 10.40.10.1 600"
sudo nmcli device reapply wlan0
```

只移除這次新增且仍相符的路由，保留其他項目；若要再次使用模式 B，先恢復公司路由。

## macOS pf 模式的範圍 {#limitations}

- 支援 TCP 與 DNS，不承接一般 UDP；RDP 的 UDP 加速、UDP 語音或其他協定要另外評估。
- `0/0` 只包含 IPv4；IPv6 需獨立規劃，不能據此宣稱全部流量都進入隧道。
- sshuttle 本身不需改遠端 NAT／FORWARD；必要的公司路由初始化則是另外的網路設定。
- Linux 是共用主機時，路由變更會影響它向公司網段發起的連線；新增前核對範圍，保留外網預設路由及既有服務設定。

## 進階：需要 UDP 時改用 WireGuard {#udp-wireguard}

若需要一般 UDP 或常駐 VPN，可另行評估 WireGuard。它需要 Linux 管理權限、轉送與路由／NAT 設定，並處理既有 Docker 防火牆規則；Mac 到伺服器之間也需要可用的傳輸路徑。僅需公司 RDP TCP 與內部網站時，先用已可驗證的 sshuttle 分流即可。

## 參考資料

- [sshuttle Usage](https://sshuttle.readthedocs.io/en/stable/usage.html)
- [sshuttle 選項與 DNS 說明](https://sshuttle.readthedocs.io/en/stable/manpage.html)
- [sshuttle 平台支援範圍](https://sshuttle.readthedocs.io/en/stable/requirements.html)
- [sshuttle 的 pf 清理實作](https://github.com/sshuttle/sshuttle/blob/master/sshuttle/methods/pf.py)
- [sshuttle channel 處理實作](https://github.com/sshuttle/sshuttle/blob/master/sshuttle/ssnet.py)
- [NetworkManager nmcli](https://networkmanager.dev/docs/api/latest/nmcli.html)
- [Apple SystemConfiguration 暫時工作階段](https://github.com/apple-oss-distributions/configd/blob/main/SystemConfiguration.fproj/SCDynamicStore.h)
- [WireGuard 官方網站](https://www.wireguard.com/)
