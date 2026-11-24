# GCP VPC Peering

> 首次發表：2024-02-19

---

筆記下誤刪 虛擬私有雲網路對等互連 後的處理

結論

```
gcloud services vpc-peerings update --service=servicenetworking.googleapis.com --ranges=default-ip-range --network=default --project=my-test-project-20240219 --force
```

說明

Cloud SQL 設定私有 IP 時會需要建立 VPC peering 來連線

![Cloud SQL 設定私有 IP 時會需要建立 VPC peering 來連線](dotblogs-ea03c786-1708311279.jpg)

否則好像連 IP 白名單都開不了

但是直接從 Cloud SQL 網路設定重建會失敗

只能用指令來更新

更新後會在 VPC peering 畫面看到原本刪除的 `servicenetworking.googleapis.com`

![更新後會在 VPC peering 畫面看到原本刪除的 servicenetworking.googleapis.com](dotblogs-ea03c786-1708314114.jpg)

參照

https://stackoverflow.com/a/56743836/4104545

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- CloudSQL
- GCP
- VPC

- 回首頁

---

*本文章從點部落遷移至 Writerside*
