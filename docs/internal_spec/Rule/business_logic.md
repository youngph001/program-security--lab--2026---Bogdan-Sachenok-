# ====== Rule BUSINESS LOGIC ======

> Опис стабільного концептуального змісту модуля `Rule`: призначення, межі, доменні елементи та інваріанти.

## Purpose

`Rule` володіє:
- каталогом правил безпеки (SQL-ін'єкції, XSS, витік секретів тощо);
- класифікацією правил за типом уразливості та рівнем критичності;
- наданням правил для виконання під час сканування;
- життєвим циклом правила (активне / застаріле / вимкнене).

**NOT here:**
- виконання сканування — `Scan`;
- формування звітів — `Report`;
- написання власних правил користувачем — свідомо не реалізується (тільки вбудований каталог);
- динамічне завантаження правил з зовнішніх джерел — не входить у скоуп.

## Entities

| Entity | Basic Fields | Description | Invariants |
|---|---|---|---|
| `Rule` *(Aggregate Root)* | uuid, code, type, severity, pattern, status, language | Правило безпеки. Містить шаблон для пошуку вразливості та метадані. | - `uuid` іммутабельний.<br>- `code` унікальний, формат `SS-<TYPE>-<NUM>`.<br>- `type` — одне зі значень енума `VulnerabilityType`.<br>- `severity` — одне зі значень енума `Severity`.<br>- `language` — одне зі значень енума `Language` (`PHP`, `JS`).<br>- `pattern` не порожній.<br>- `status` змінюється лише за політикою. |

## Status Lifecycle

- Нове правило створюється в статусі `ACTIVE`.

Дозволені переходи:

| From | Self-initiated | System/admin-initiated |
|---|---|---|
| `ACTIVE` | → `DISABLED` | → `DEPRECATED` |
| `DISABLED` | → `ACTIVE` | → `DEPRECATED` |
| `DEPRECATED` | — (terminal) | — (terminal) |

- **Self-initiated:** зміна адміністратором через `DisableRuleAC` / `EnableRuleAC`.
- **System/admin-initiated:** позначення правила як застарілого через `DeprecateRuleAC`.
- Прямий перехід `DEPRECATED → ACTIVE` заборонений — застаріле правило залишається історичним.

## Value Objects

| Value Object | Description | Invariants |
|---|---|---|
| `RuleUuidVO` | Типізований UUID правила. | - Іммутабельний.<br>- Валідність UUID з базового класу. |
| `RuleCodeVO` | Код правила у форматі `SS-<TYPE>-<NUM>`. | - Іммутабельний.<br>- Відповідає регулярному виразу `^SS-[A-Z]+-\d{3}$`. |
| `VulnerabilityTypeVO` | Обгортка енума `VulnerabilityType`. | - Іммутабельний. |
| `SeverityVO` | Обгортка енума `Severity`. | - Іммутабельний. |
| `PatternVO` | Шаблон пошуку (regex або AST-патерн). | - Іммутабельний.<br>- Валідний regex / AST-патерн. |
| `LanguageVO` | Обгортка енума `Language`. | - Іммутабельний. |
| `RuleStatusVO` | Обгортка енума `RuleStatus`. | - Іммутабельний. |

## Domain Policies

| Domain Policy | Description |
|---|---|
| `DisableRuleDPolicy` | Дозволяє `ACTIVE → DISABLED`. |
| `EnableRuleDPolicy` | Дозволяє `DISABLED → ACTIVE`. |
| `DeprecateRuleDPolicy` | Дозволяє `ACTIVE/DISABLED → DEPRECATED`. Блокує повернення з `DEPRECATED`. |

## Domain Services

| Domain Service | Operation |
|---|---|
| `RegisterRuleService` | Реєструє нове правило в каталозі; емить `RuleRegisteredDE`. |
| `DisableRuleService` | Вимикає правило за політикою; емить `RuleDisabledDE`. |
| `EnableRuleService` | Повертає правило в активний стан; емить `RuleEnabledDE`. |
| `DeprecateRuleService` | Позначає правило як застаріле; емить `RuleDeprecatedDE`. |
| `MatchRulesService` *(internal — no UC)* | Повертає активні правила для заданої мови. Викликається з `Scan.RunScanService` через `IRuleProvider` (OutsourceContract). |

## Domain Events

| Event | Carries | Notes |
|---|---|---|
| `RuleRegisteredDE` | rule uuid, code, type | |
| `RuleDisabledDE` | rule uuid, code | |
| `RuleEnabledDE` | rule uuid, code | |
| `RuleDeprecatedDE` | rule uuid, code | |

## Application Commands & Queries

**Commands (`AC`):**

| Area | Commands |
|---|---|
| Rule | `RegisterRuleAC`, `DisableRuleAC`, `EnableRuleAC`, `DeprecateRuleAC` |

**Queries (`AQ`):**

| Query | Purpose |
|---|---|
| `GetRuleAQ` | Повертає правило за `ruleId`. |
| `ListRulesAQ` | Список правил із фільтром за типом / критичністю / мовою / статусом. |
| `ListActiveRulesAQ` | Список активних правил для конкретної мови. |

## Infrastructure

### Models

- `RuleModel` — uuid, code, type, severity, pattern, language, status, created_at, updated_at.

### Cache

- Каталог активних правил кешується за ключем `rules:active:{language}` на 15 хвилин (правила рідко змінюються, але часто читаються під час сканування).