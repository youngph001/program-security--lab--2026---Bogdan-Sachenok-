# Документація проєкту SecureScan

> SecureScan — система автоматизованого статичного аналізу вихідного коду на наявність вразливостей безпеки.

## Швидкий старт

- [Межі проєкту](specification/scope.md)
- [Вимоги](specification/requirements.md)
- [Архітектура](specification/architecture.md)
- [Політика проєкту](policy/project_policy.md)
- [Реєстр модулів](contexts_registry.md)
- [Журнал змін документації](changelog.md)

## Структура документації

```text
docs/
├── README.md                          # цей файл
├── contexts_registry.md               # реєстр усіх Bounded Contexts
├── changelog.md                       # журнал змін документації
├── specification/
│   ├── scope.md                       # межі проєкту
│   ├── requirements.md                # функціональні та нефункціональні вимоги
│   └── architecture.md                # архітектурний опис
├── policy/
│   ├── project_policy.md              # політика проєкту
│   └── project_documentation_policy.md # правила ведення документації
├── guide/
│   └── getting_started.md             # як почати роботу
└── internal_spec/
    ├── Scan/
    │   ├── business_logic.md
    │   ├── changelog.md
    │   └── tech_notes.md
    ├── Report/
    │   ├── business_logic.md
    │   ├── changelog.md
    │   └── tech_notes.md
    ├── Rule/
    │   ├── business_logic.md
    │   ├── changelog.md
    │   └── tech_notes.md
    └── SharedKernel/
        ├── business_logic.md
        ├── changelog.md
        └── tech_notes.md
```

## Призначення

SecureScan приймає вихідний код (архів або Git-URL), виконує статичний аналіз на наявність типових вразливостей (SQL-ін'єкції, XSS, витік секретів) та формує звіт у форматах JSON і HTML.

## Межі

Проєкт **НЕ робить**: динамічний аналіз (DAST), автоматичне виправлення коду, управління користувачами, написання власних правил безпеки.

## Правила ведення документації

- Документація — повноцінний деліверабл; застаріла чи відсутня документація вважається дефектом.
- Зміни в коді супроводжуються змінами в `docs/`.
- Деталі — у [політиці документації](policy/project_documentation_policy.md).