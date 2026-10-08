# ====== SharedKernel BUSINESS LOGIC ======

> Опис стабільного концептуального змісту `SharedKernel`: спільне ядро для всіх Bounded Contexts. Містить лише те, що використовується більш ніж одним BC.

## Purpose

`SharedKernel` володіє:
- базовими абстракціями доменних елементів (Value Object, Entity, EntityId);
- фундаментальними контрактами, обов'язковими для всіх BC;
- спільними Value Objects (ідентифікатори, обгортки типів);
- спільними енумами (VulnerabilityType, Severity, Language, SourceType);
- базовою абстракцією винятків проєкту;
- кор-реєстром винятків (`CoreExceptionRegistry`).

**NOT here:**
- будь-яка бізнес-логіка, специфічна для одного BC (`Scan`, `Report`, `Rule`) — залишається у відповідному BC;
- інфраструктурні реалізації — `Infrastructure`;
- юзкейси — `Application`.

> До SharedKernel потрапляє лише справді крос-БК-шне. Це не склад для довільної логіки, і воно не повинно розростатись.

## Structure

```text
Domain/SharedKernel/
├── Abstracts/      # базові абстракції доменних елементів
├── Contract/       # фундаментальні інтерфейси
├── ValueObject/    # спільні VO
├── Enum/           # спільні енуми
└── Exception/      # опційно: CoreExceptionRegistry, ACoreException
```

## Abstracts

| Abstract | Description | Invariants |
|---|---|---|
| `AValueObject` | База всіх Value Objects проєкту. | - Іммутабельний.<br>- Порівняння за значенням (`equals()`).<br>- Реалізує `IValueObject`. |
| `AEntity` | База всіх Entity проєкту (не Aggregate Root). | - Має `uuid`.<br>- Реалізує `IEntity`. |
| `AAggregateRoot` | База Aggregate Roots. | - Розширює `AEntity`.<br>- Містить чергу доменних івентів. |
| `AEntityUuidVO` | База типізованих UUID Value Objects. | - Іммутабельний.<br>- Валідація UUID у конструкторі. |
| `ASecureScanException` | База всіх винятків проєкту. | - Розширює `\Exception`.<br>- Реалізує `ISecureScanException`.<br>- Має метод `getCodeEnum()`. |
| `ADomainEvent` | База доменних івентів. | - Має UUID івента, UUID ентіті-джерела, timestamp, версію схеми.<br>- Декларує `getEventName()` та `getEventDataClass()`. |

## Contracts

| Contract | Description |
|---|---|
| `IValueObject` | Фундаментальний інтерфейс VO. Декларує `equals(IValueObject $other): bool`. |
| `IEntity` | Фундаментальний інтерфейс Entity. Декларує `getUuid()`. |
| `ISecureScanException` | Контракт усіх винятків проєкту. Декларує `getCodeEnum(): IExceptionCodeRegistry`. |
| `IExceptionCodeRegistry` | Контракт реєстрів винятків. Декларує `getSegment(): string`, `getList(): array`. |
| `IPolicy` | Контракт доменних політик (якщо використовуються). |

## Value Objects

| Value Object | Description | Invariants |
|---|---|---|
| `UuidVO` | Спільний VO UUID (для ентіті без власного типізованого UUID). | - Іммутабельний.<br>- Валідність UUID v4. |
| `TimestampVO` | Обгортка для таймстемпу (UTC). | - Іммутабельний.<br>- Завжди UTC. |
| `CountVO` | Невід'ємне ціле число. | - Іммутабельний.<br>- Значення ≥ 0. |
| `PathVO` | Відносний шлях до файлу. | - Іммутабельний.<br>- Не порожній.<br>- Без `..` для безпеки. |

## Enums

| Enum | Values | Description |
|---|---|---|
| `VulnerabilityType` | `SQL_INJECTION`, `XSS`, `SECRET_LEAK`, `INSECURE_DESERIALIZATION`, `PATH_TRAVERSAL` | Типи вразливостей, які виявляє система. |
| `Severity` | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` | Рівні критичності. |
| `Language` | `PHP`, `JS` | Підтримувані мови для аналізу. |
| `SourceType` | `ARCHIVE`, `GIT` | Тип джерела для сканування. |

## Exceptions

```text
SharedKernel/Exception/
├── Abstracts/
│   └── ACoreException.php
├── Registry/
│   └── CoreExceptionRegistry.php
└── <кор-винятки>
```

- `CoreExceptionRegistry` — сегмент `CORE`, числові кейси, реалізує `IExceptionCodeRegistry`.
- `ACoreException` — розширює `ASecureScanException`, прив'язується до `CoreExceptionRegistry`.
- Кор-винятки: усе, що не належить жодному BC чи інфраструктурі.

## Traits

| Trait | Description |
|---|---|
| `TEventQueue` | Черга доменних івентів для Aggregate Root. Методи: `triggerEvent()`, `pullEvents()`. Дедуплікація за семантичним ключем у межах одного виклику. |

## Правила наповнення SharedKernel

- Додавання нового елемента в SharedKernel потребує попереднього апруву власника.
- Елемент має бути використаний (або фундаментальний) у більш ніж одному BC.
- Елементи специфічні для одного BC — залишаються в тому BC.

## Infrastructure

`SharedKernel` не має власних моделей персистенсу. Він надає абстракції для інших BC.