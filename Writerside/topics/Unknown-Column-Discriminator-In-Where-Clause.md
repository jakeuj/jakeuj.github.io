# Unknown column &#x27;Discriminator&#x27; in &#x27;where clause&#x27; {id="Unknown-Column-Discriminator-In-Where-Clause"}

> 首次發表：2019-06-10

---

Unknown column 'Discriminator' in 'where clause'

結論是實體裡面設定了關聯性

但實際資料庫中的資料表卻沒有該關聯

檢查巡覽屬性與外部索引鍵

是否與資料庫不一致

修正後可以正常
