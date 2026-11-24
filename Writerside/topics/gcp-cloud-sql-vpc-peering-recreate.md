# GCP 誤刪 VPC Peering 後恢復 Cloud SQL 私人 IP

<web-summary>誤刪 servicenetworking 的 VPC Peering 後，Cloud SQL 無法從介面重建私人 IP 連線，改用 gcloud services vpc-peerings update --force 恢復。</web-summary>

> 首次發表：2024-02-19

誤刪「虛擬私有雲網路對等互連」後，直接從 Cloud SQL 的網路設定重建會失敗，要用指令強制更新：

```bash
gcloud services vpc-peerings update \
  --service=servicenetworking.googleapis.com \
  --ranges=default-ip-range \
  --network=default \
  --project=<project-id> \
  --force
```

`--ranges` 和 `--network` 換成當初建立私人服務存取權時用的 IP 範圍與 VPC 名稱。

## 為什麼需要這條 Peering

Cloud SQL 設定私人 IP 時，會透過 VPC Peering 連到 Google 管理的服務網路。我遇到的情況是 Peering 被刪除後，連 IP 白名單都沒辦法設定。

![Cloud SQL 私人 IP 設定](dotblogs-ea03c786-1708311279.jpg)

## 驗證

更新後回到 VPC Peering 畫面，會看到原本刪除的 `servicenetworking-googleapis-com`：

![VPC Peering 已恢復](dotblogs-ea03c786-1708314114.jpg)

## 參照

[Stack Overflow：Cloud SQL private services access](https://stackoverflow.com/a/56743836/4104545)
