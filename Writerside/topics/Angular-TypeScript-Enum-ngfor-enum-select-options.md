# Angular TypeScript Enum ngfor-enum-select-options

> 首次發表：2019-05-30

---

ngfor-enum-select-options

```

export enum Symbols {
  equals = '\u003D',
  notEquals = '!='
}

@Component({
  selector: 'my-app',
  template: `
    <p>
      Having the name as label and symbol as value:
      <select>
        <option *ngFor="let symbol of keys(symbols)"
            [ngValue]="symbols[symbol]">{{symbol}}
        </option>
      </select>
    </p>
    <p>
      Having the symbol as label and name as value:
      <select>
        <option *ngFor="let symbol of keys(symbols)"
            [ngValue]="symbol">{{symbols[symbol]}}
        </option>
      </select>
    </p>
  `
})
export class AppComponent  {
  keys = Object.keys;
  symbols = Symbols;
}
```

Ref: <https://stackblitz.com/edit/ngfor-enum-select-options?file=app%2Fapp.component.ts>
{ignore-vars="true"}
