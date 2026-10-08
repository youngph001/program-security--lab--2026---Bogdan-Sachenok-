# ====== Scan BUSINESS LOGIC ======

> Опис стабільного концептуального змісту модуля `Scan`: призначення, межі, доменні елементи та інваріанти. Завжди відображає поточний стан модуля.

## Purpose

`Scan` володіє:
- життєвим циклом сканування (від створення до завершення/скасування/помилки);
- прийомом вихідного коду (архів або Git-URL);
- запуском статичного аналізу (SAST) через відповідні сервіси;
- агрегацією знайдених вразливостей у межах одного сканування.

**NOT here:**
- формування та збереження звітів — `Report`;
- каталог правил безпеки — `Rule`;
- управління користувачами — поза межами проєкту;
- автоматичне виправлення коду — свідомо не реалізується.

## Entities

| Entity | Basic Fields | Description | Invariants |
|---|---|---|---|
| `AScan` *(abstract)* | uuid, status, sourceType, createdAt, startedAt, finishedAt | Абстрактна база сканування. Містить ідентичність, статус та часові мітки. | - `uuid` іммутабельний.<br>- Статус змінюється лише за політиками переходів (див. «Status Lifecycle»).<br>- Новостворене сканування завжди стартує в статусі `PENDING`. |
| `ArchiveScan` *(extends AScan)* | + archivePath | Сканування завантаженого архіву. | - Успадковує інваріанти `AScan`.<br>- `archivePath` не порожній.<br>- Розмір архіву ≤ 100 МБ. |
| `GitScan` *(extends AScan)* | + repositoryUrl, branch | Сканування Git-репозиторію. | - Успадковує інваріанти `AScan`.<br>- `repositoryUrl` валідний URL.<br>- `branch` за замовчуванням `main`. |
| `Vulnerability` *(internal Entity)* | uuid, type, severity, file, line, message | Знайдена вразливість у межах сканування. | - `uuid` іммутабельний.<br>- `type` — одне зі значень енума `VulnerabilityType`.<br>- `severity` — одне зі значень енума `Severity`.<br>- `line > 0`. |

## Status Lifecycle

- Нове сканування створюється в статусі `PENDING`.

Дозволені переходи:

| From | Self-initiated | System/admin-initiated |
|---|---|---|
| `PENDING` | → `CANCELLED` | → `RUNNING` |
| `RUNNING` | → `CANCELLED` | → `COMPLETED`, `FAILED` |
| `COMPLETED` | — (terminal) | — (terminal) |
| `FAILED` | — (terminal) | — (terminal) |
| `CANCELLED` | — (terminal) | — (terminal) |

- **Self-initiated:** ініціює клієнт через `CancelScanAC` (тільки для `PENDING`, `RUNNING`).
- **System/admin-initiated:** ініціює воркер або адміністратор.
- Прямий перехід `PENDING → COMPLETED` заборонений — спочатку треба пройти `RUNNING`.

## Key Flow

*Сценарій: запуск сканування*

1. Клієнт надсилає запит з архівом або Git-URL.
2. `StartScanUC` створює `ArchiveScan` або `GitScan` у статусі `PENDING`.
3. Сканування зберігається; емиться `ScanStartedDE`.
4. Асинхронний воркер бере сканування зі статусом `PENDING`.
5. `RunScanService` переводить у `RUNNING`; викликає `CodeParserService` через `IParser` (OutsourceContract).
6. Для кожного правила з BC `Rule` виконується перевірка; знайдені вразливості додаються до сканування.
7. Після завершення аналізу статус → `COMPLETED`; емиться `ScanCompletedDE`.
8. BC `Report` створює звіт на основі результату.

**Boundary:** усе, що стосується життєвого циклу та агрегації вразливостей — тут. Формування звіту — `Report`. Каталог правил — `Rule`.

## Value Objects

| Value Object | Description | Invariants |
|---|---|---|
| `ScanUuidVO` | Типізований UUID сканування. Розширює `AEntityUuidVO`. | - Іммутабельний.<br>- Валідність UUID гарантується базовим класом. |
| `ScanStatusVO` | Обгортка енума `ScanStatus`. | - Іммутабельний.<br>- Значення валідне через енум. |
| `VulnerabilityTypeVO` | Обгортка енума `VulnerabilityType`. | - Іммутабельний. |
| `SeverityVO` | Обгортка енума `Severity`. | - Іммутабельний. |
| `FileReferenceVO` | Шлях до файлу в проєкті + номер рядка. | - Іммутабельний.<br>- `path` не порожній.<br>- `line > 0`. |
| `SourceTypeVO` | Обгортка енума `SourceType` (`ARCHIVE` / `GIT`). | - Іммутабельний. |

## Domain Policies

| Domain Policy | Description |
|---|---|
| `StartPendingScanDPolicy` | Дозволяє `PENDING → RUNNING`. Перевіряє, що сканування не скасовано і не завершено. |
| `CancelScanDPolicy` | Дозволяє `PENDING → CANCELLED` і `RUNNING → CANCELLED`. Блокує скасування `COMPLETED`, `FAILED`, `CANCELLED`. |
| `CompleteRunningScanDPolicy` | Дозволяє `RUNNING → COMPLETED` або `FAILED`. |
| `AddVulnerabilityDPolicy` | Дозволяє додавати вразливість лише у статусі `RUNNING`. |

## Domain Services

| Domain Service | Operation |
|---|---|
| `ScanFactoryService` | Створює `ArchiveScan` або `GitScan` з валідованих вхідних даних; емить `ScanStartedDE`. |
| `RunScanService` | Переводить сканування в `RUNNING`, викликає парсер і правила, агрегує результати, переводить у `COMPLETED`/`FAILED`; емить `ScanCompletedDE` або `ScanFailedDE`. |
| `CancelScanService` | Скасовує сканування за політикою; емить `ScanCancelledDE`. |
| `AddVulnerabilityService` *(internal — no UC)* | Внутрішній сервіс: додає знайдену вразливість до сканування. Викликається з `RunScanService`. |

## Domain Events

Тригеряться лише на значущі зміни. Чутливі дані не потрапляють у пейлоади.

| Event | Carries | Notes |
|---|---|---|
| `ScanStartedDE` | scan uuid, sourceType | |
| `ScanCompletedDE` | scan uuid, vulnerabilitiesCount | |
| `ScanFailedDE` | scan uuid, reason | |
| `ScanCancelledDE` | scan uuid, reason | |
| `VulnerabilityFoundDE` | scan uuid, vulnerability uuid, type, severity | Окремий івент для підписки у `Report` |

## Application Commands & Queries

**Commands (`AC`):**

| Area | Commands |
|---|---|
| Scan | `StartScanAC`, `CancelScanAC`, `RetryScanAC` |

**Queries (`AQ`):**

| Query | Purpose |
|---|---|
| `GetScanAQ` | Повертає деталі сканування за `scanId`. |
| `ListScansAQ` | Список сканувань із фільтром за статусом. Свідомо НЕ віддає повний вміст вихідного коду. |

## Infrastructure

### Models

- `ScanModel` — uuid, status, source_type, source_url, archive_path, created_at, started_at, finished_at, user_ref.
- `VulnerabilityModel` — uuid, scan_id, type, severity, file_path, line, message.

### Async

- Сканування виконується асинхронно через чергу (`Queue`). Після створення `PENDING`-сканування публікується job `RunScanJob`, який викликає `RunScanService`.