# Реєстр модулів / Bounded Contexts

> Точка входу в мапу модулів проєкту. Повний перелік усіх Bounded Contexts з короткими описами, межами відповідальності, статусом та залежностями.

## Перелік BC

| BC | Призначення | Межі (що НЕ робить) | Залежності | Статус |
|---|---|---|---|---|
| `Scan` | Життєвий цикл сканування: прийом коду, запуск SAST, агрегація вразливостей | Не формує звіти; не зберігає каталог правил | `Rule` (через `IRuleProvider`), `SharedKernel` | У розробці |
| `Report` | Формування, збереження та експорт звітів у JSON/HTML | Не запускає сканування; не виконує аналіз | `Scan` (читає результати), `SharedKernel` | У розробці |
| `Rule` | Каталог правил безпеки (SQL-ін'єкції, XSS, витік секретів) | Не виконує сканування; не формує звіти | `SharedKernel` | У розробці |
| `SharedKernel` | Спільні абстракції, контракти, VO, енуми, базові винятки | Не містить бізнес-логіки конкретного BC | — | Стабільний |

## Міжмодульні залежності

```text
Scan ──(IRuleProvider)──► Rule
  │
  ▼
Report ──(читає результати сканування)──► Scan

Усі BC ──(Abstracts, Contracts, VO)──► SharedKernel
```

## Сегменти винятків

| BC / Шар | Сегмент | Реєстр |
|---|---|---|
| `Scan` | `SCAN` | `ScanExceptionRegistry` |
| `Report` | `REPT` | `ReportExceptionRegistry` |
| `Rule` | `RULE` | `RuleExceptionRegistry` |
| Infrastructure | `INF` | `InfrastructureExceptionRegistry` |
| SharedKernel / все інше | `CORE` | `CoreExceptionRegistry` |

## Правила взаємодії

- Крос-БК зв'язність дозволена лише через **стабільні** посилання (мініфікований id + назва), ніколи — через вбудови змінної глибини.
- Кожен BC має власний `ExceptionRegistry` зі своїм сегментом.
- Додавання елемента в `SharedKernel` потребує попереднього апруву власника проєкту.
- Domain ніколи не залежить від Infrastructure напряму — лише через `OutsourceContract`.

## Посилання на бізнес-логіку

- [`Scan`](internal_spec/Scan/business_logic.md)
- [`Report`](internal_spec/Report/business_logic.md)
- [`Rule`](internal_spec/Rule/business_logic.md)
- [`SharedKernel`](internal_spec/SharedKernel/business_logic.md)