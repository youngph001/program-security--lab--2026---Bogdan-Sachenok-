# Getting Started — SecureScan

> Короткий посібник для розробника: як встановити проєкт, перевірити якість коду та запустити тести.

## Вимоги до середовища

- **PHP 8.3+**
- **Composer 2.x**
- **Git**
- (опційно) **MySQL 8** або **PostgreSQL 15** — для запуску повного стека
- (опційно) **Redis** — для черги асинхронних сканувань

## Встановлення

```bash
git clone https://github.com/youngph001/program-security--lab--2026---Bogdan-Sachenok-.git
cd program-security--lab--2026---Bogdan-Sachenok-
composer install
```

## Перевірка якості коду

### Лінтер (Laravel Pint)

```bash
vendor/bin/pint --test
```

Для авто-виправлення:

```bash
vendor/bin/pint
```

### Статичний аналіз (PHPStan, level max)

```bash
vendor/bin/phpstan analyse
```

### Контроль меж шарів (Deptrac)

```bash
vendor/bin/deptrac analyse
```

### Повний набір перевірок

```bash
composer check
```

(Якщо в `composer.json` визначено скрипт `check`, він виконує всі три перевірки підряд.)

## Тести

### Запуск усіх тестів

```bash
vendor/bin/phpunit
```

### Запуск тестів конкретного шару

```bash
vendor/bin/phpunit --group domain
vendor/bin/phpunit --group application
vendor/bin/phpunit --group infrastructure
```

### Запуск тестів конкретного BC

```bash
vendor/bin/phpunit --group scan.domain
vendor/bin/phpunit --group report.domain
vendor/bin/phpunit --group rule.domain
```

### Покриття

```bash
vendor/bin/phpunit --coverage-html coverage/
```

Звіт буде у `coverage/index.html`.

## Запуск системи

### HTTP-сервер (dev)

```bash
php -S localhost:8000 -t public/
```

Приклад запиту на створення сканування:

```bash
curl -X POST http://localhost:8000/api/scans \
  -H "Content-Type: application/json" \
  -d '{"sourceType":"GIT","repositoryUrl":"https://github.com/user/repo"}'
```

### CLI

```bash
bin/console scan:start --source=archive --path=/path/to/code.zip
bin/console scan:start --source=git --url=https://github.com/user/repo
```

Перевірка статусу сканування:

```bash
bin/console scan:status <scanId>
```

## Структура проєкту

```text
src/
├── EntryPoint.php
├── Infrastructure/
├── Domain/
│   ├── Scan/
│   ├── Report/
│   ├── Rule/
│   └── SharedKernel/
├── Application/
└── Framework/
```

Детальніше — в [архітектурному описі](../specification/architecture.md).

## Документація

- [README документації](../README.md)
- [Межі проєкту](../specification/scope.md)
- [Вимоги](../specification/requirements.md)
- [Архітектура](../specification/architecture.md)
- [Політика проєкту](../policy/project_policy.md)
- [Реєстр модулів](../contexts_registry.md)

## Правила роботи

Перед початком роботи ознайомся з [політикою проєкту](../policy/project_policy.md). Ключове:

- Строго типізоване ООП, SOLID, чистий код.
- Шарова архітектура з жорсткими межами.
- PHPDoc обов'язковий для кожного метода та властивості.
- Усі винятки — від `ASecureScanException`.
- Тести без реальних мережевих викликів.
- Коміти з префіксом `[DEV-XXX]`, `[FIX-XXX]`, `[DOCS]`, `[POLICY]`.