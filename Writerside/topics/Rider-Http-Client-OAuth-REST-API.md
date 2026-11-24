# Rider Http Client OAuth REST API

> 首次發表：2022-12-21

---

筆記下 Rider 的 Http Client 使用 OAuth 驗證並呼叫 REST API

![筆記下 Rider 的 Http Client 使用 OAuth 驗證並呼叫 REST API](dotblogs-9ba91063-1671594530.jpg)

結論

`rest-api.http`

```
### Getting a Machine-to-Machine Application Access Token
POST https://auth.spscommerce.com/oauth/token
Content-Type: application/json

{
  "grant_type": "client_credentials",
  "client_id": "{{client_id}}",
  "client_secret": "{{client_secret}}",
  "audience": "api://api.spscommerce.com/"
}

> {%
    client.test("Request executed successfully", function() {
        client.assert(response.status === 200, "Response status is not 200");
    });
    client.global.set("auth_token", response.body.access_token);
%}

### Using an Access Token
GET https://api.spscommerce.com/auth-check
Authorization: Bearer {{auth_token}}

> {%
    client.test("Request executed successfully", function() {
        client.assert(response.status === 204, "Response status is not 204");
    });
%}

### Filter Transactions
GET https://api.spscommerce.com/transactions/v5/data/
Authorization: Bearer {{auth_token}}

> {%
    client.test("Request executed successfully", function() {
        client.assert(response.status === 200, "Response status is not 200");
    });
%}
```

`http-client.private.env.json`

```
{
  "development": {
    "client_id": "YOUR_APP_ID",
    "client_secret": "YOUR_APP_SECRET"
  },
  "production": {
    "client_id": "YOUR_APP_ID",
    "client_secret": "YOUR_APP_SECRET"
  }
}
```

REF

[Dev Center: Docs | new authentication docs | machine2machine applications (spscommerce.com)](https://developercenter.spscommerce.com/#/docs/new-authentication-docs/machine2machine-applications)

[Exploring the HTTP request syntax | JetBrains Rider Documentation](https://www.jetbrains.com/help/rider/Exploring_HTTP_Syntax.html#example-working-with-environment-files)
