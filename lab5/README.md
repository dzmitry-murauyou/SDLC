# Лабораторная работа №5 — UML-моделирование Guardian

Материалы лабораторной работы подготовлены на основе SRS, SDD и ADR проекта Guardian и структуры отчёта-примера по ЛР №5.

## Основные результаты

- [`report.docx`](report.docx) — отчёт для сдачи; содержит четыре UML-диаграммы и ответы на контрольные вопросы.
- [`report.md`](report.md) — текстовая версия отчёта.
- [`glossary.md`](glossary.md) — глоссарий проекта в отдельном файле.
- [`specs/additional-specifications.md`](specs/additional-specifications.md) — дополнительные спецификации и границы модели.
- [`specs/use-cases.md`](specs/use-cases.md) — актёры и подробные спецификации прецедентов.
- [`diagrams/`](diagrams/) — редактируемые исходники PlantUML и готовые SVG/PNG: use case, activity, state machine и sequence.
- SDD дополнен ссылками на поведенческие представления; добавлен ADR-0004 о моделировании поведения.

## Область модели

Основная модель описывает базовый Guardian 1.0 по SRS: локальный Windows-клиент, хранилище, FIDO2, записи, wallet-data, автозаполнение, резервное копирование и блокировка. Change-01 (регистрация запасного FIDO2-ключа) сохранён в поясняющих материалах как сценарий ЛР №4, но не изображается на базовых диаграммах и не считается изменением SRS.

## Пересборка материалов

Из корня репозитория:

```bash
python3 -m pip install -r lab5/scripts/requirements.txt
python3 lab5/scripts/render_diagrams.py
npm install --prefix lab5/scripts
npm run --prefix lab5/scripts render
python3 lab5/scripts/build_report.py
```

Команды создают SVG/PNG из описания диаграмм и собирают DOCX из `report.md`. PlantUML-файлы можно открыть в любой среде с поддержкой PlantUML; готовые PNG уже вставлены в DOCX, SVG предназначены для просмотра в браузере и масштабирования без потери качества.
