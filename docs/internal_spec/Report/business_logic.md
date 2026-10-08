# ====== Report BUSINESS LOGIC ======

> Опис стабільного концептуального змісту модуля `Report`: призначення, межі, доменні елементи та інваріанти.

## Purpose

`Report` володіє:
- формуванням звіту про сканування на основі агрегованих вразливостей;
- збереженням звітів у форматах JSON та HTML;
- наданням історії сканувань для конкретного проєкту;
- агрегацією статистики (кількість вразливостей за рівнями критичності).

**NOT here:**
- запуск сканування — `Scan`;
- каталог правил безпеки — `Rule`;
- управління користувачами — поза межами проєкту;
- автоматичне виправлення — не реалізується.

## Entities

| Entity | Basic Fields | Description | Invariants |
|---|---|---|---|
| `Report` *(Aggregate Root)* | uuid, scanRef, format, payload, createdAt | Звіт про конкретне сканування. Один звіт = одне сканування. | - `uuid` іммутабельний.<br>- `scanRef` не може бути змінений після створення.<br>- `format` — одне зі значень енума `ReportFormat` (`JSON`, `HTML`).<br>- `payload` не порожній.<br>- Новий звіт завжди створюється в форматі, заданому при ініціалізації. |
| `ReportStatistics` *(internal Entity)* | totalCount, lowCount, mediumCount, highCount, criticalCount | Статистика за звітом. | - Сума `lowCount + mediumCount + highCount + criticalCount = totalCount`.<br>- Усі значення ≥ 0. |

## Value Objects

| Value Object | Description | Invariants |
|---|---|---|
| `ReportUuidVO` | Типізований UUID звіту. | - Іммутабельний.<br>- Валідність UUID з базового класу. |
| `ReportFormatVO` | Обгортка енума `ReportFormat`. | - Іммутабельний.<br>- Значення валідне через енум. |
| `ScanReferenceVO` | Посилання на сканування (мініфіковане: uuid + назва). | - Іммутабельний.<br>- NULL-less: завжди або реальне посилання, або явний «відсутній» ref. |

## Domain Policies

| Domain Policy | Description |
|---|---|
| `CreateReportDPolicy` | Дозволяє створення звіту лише для сканування у статусі `COMPLETED`. Блокує для `PENDING`, `RUNNING`, `FAILED`, `CANCELLED`. |
| `ChangeReportFormatDPolicy` | Дозволяє зміну формату звіту лише до першого збереження. |

## Domain Services

| Domain Service | Operation |
|---|---|
| `CreateReportService` | Створює звіт на основі завершеного сканування; агрегує вразливості; емить `ReportCreatedDE`. |
| `BuildStatisticsService` *(internal — no UC)* | Обчислює статистику звіту. Викликається з `CreateReportService`. |
| `ExportReportService` | Експортує звіт у заданому форматі (JSON / HTML); емить `ReportExportedDE`. |

## Domain Events

| Event | Carries | Notes |
|---|---|---|
| `ReportCreatedDE` | report uuid, scan uuid, format | |
| `ReportExportedDE` | report uuid, format | |
| `ReportDeletedDE` | report uuid, reason | |

## Application Commands & Queries

**Commands (`AC`):**

| Area | Commands |
|---|---|
| Report | `CreateReportAC`, `ExportReportAC`, `DeleteReportAC` |

**Queries (`AQ`):**

| Query | Purpose |
|---|---|
| `GetReportAQ` | Повертає звіт за `reportId`. |
| `GetReportByScanAQ` | Повертає звіт за `scanId`. |
| `ListReportsAQ` | Список звітів із фільтром за проєктом / датою. |

## Infrastructure

### Models

- `ReportModel` — uuid, scan_id, format, payload (JSON), created_at.
- `ReportStatisticsModel` — report_id, total_count, low_count, medium_count, high_count, critical_count.

### Cache

- Експортовані звіти (JSON/HTML) кешуються на 1 годину за ключем `report:{uuid}:{format}`.