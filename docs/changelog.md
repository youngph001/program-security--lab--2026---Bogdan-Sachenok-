# Changelog — документація SecureScan

> Журнал змін документації проєкту. Строго append-only: нові записи додаються на початок файлу.
>
> Формат запису:
> ```
> ## [YYYY-MM-DD] [TICKET-XXX] Назва зміни
> - зміна 1
> - зміна 2
> ```

## [2026-10-08] [LAB2] Створення документації проєкту

### Додано

- Структура `docs/` (`specification/`, `policy/`, `guide/`, `internal_spec/`).
- `README.md` — точка входу в документацію.
- `contexts_registry.md` — реєстр усіх Bounded Contexts.

### Специфікація (`docs/specification/`)

- `scope.md` — призначення системи, межі (In Scope / Out of Scope), зацікавлені сторони.
- `requirements.md` — 12 функціональних вимог (FR), 12 нефункціональних вимог (NFR), обмеження (C), припущення (A). Складено за ISO/IEC/IEEE 29148:2018.
- `architecture.md` — архітектурний опис за ISO/IEC/IEEE 42010:2022: шари, BC, взаємодія, дані, розгортання, ключові рішення.

### Політики (`docs/policy/`)

- `project_policy.md` — політика проєкту: технології, фундаментальні принципи, архітектура, неймінг, PHPDoc, винятки, NULL-less, тестування, Git workflow, анти-патерни.
- `project_documentation_policy.md` — правила ведення документації.

### Бізнес-логіка (`docs/internal_spec/`)

- `Scan/business_logic.md` — Entities, Status Lifecycle, VO, Policies, Services, Events, AC/AQ.
- `Scan/changelog.md`, `Scan/tech_notes.md`.
- `Report/business_logic.md` — Entities, VO, Policies, Services, Events, AC/AQ.
- `Report/changelog.md`, `Report/tech_notes.md`.
- `Rule/business_logic.md` — Entities, Status Lifecycle, VO, Policies, Services, Events, AC/AQ.
- `Rule/changelog.md`, `Rule/tech_notes.md`.
- `SharedKernel/business_logic.md` — Abstracts, Contracts, VO, Enums, Exceptions, Traits.
- `SharedKernel/changelog.md`, `SharedKernel/tech_notes.md`.

### Посібник (`docs/guide/`)

- `getting_started.md` — встановлення, перевірка якості, запуск тестів, запуск системи.