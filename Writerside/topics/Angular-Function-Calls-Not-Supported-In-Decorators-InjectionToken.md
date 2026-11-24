# Angular Function calls are not supported in decorators but &#x27;InjectionToken&#x27; was called in {id="Angular-Function-Calls-Not-Supported-In-Decorators-InjectionToken"}

> 首次發表：2019-08-26

---

Angular ng build --prod 時報錯的解決方法紀錄

Function calls are not supported in decorators but 'InjectionToken' was called in 'OWL\_MOMENT\_DATE\_TIME\_ADAPTER\_OPTIONS'

tsconfig.json

```

"paths": {
    //...

    "@angular/*": ["../node_modules/@angular/*"]
}
```

參照：<https://github.com/angular/angular/issues/16762>
