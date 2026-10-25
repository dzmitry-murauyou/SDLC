// ============================================================================
//  ui-mockups.sysml — модель GUI-прототипов приложения «Ларец»
//  Проект: «Ларец» — локальный менеджер паролей (Desktop, Java 21 / JavaFX)
//  Лабораторная работа №3, кафедра ЭВМ, БГУИР
//
//  Каждый экран — это part def с attribute kind = "screen". Скрипт
//  render_mockups.py разбирает модель и сохраняет PNG в каталог rendering/.
//  Единица координат — пиксель виртуального холста 1000 × 640.
// ============================================================================

package Larets::UI::Mockups {

    // ========================================================================
    //  ЭКРАН 1. Разблокировка хранилища (стартовый экран)
    //  Трассировка: REQ-FUNC-001, REQ-SEC-001, REQ-SEC-005, REQ-INT-001
    // ========================================================================
    part def UnlockScreen {
        attribute kind = "screen";
        attribute title = "Unlock screen";
        attribute file = "01-unlock-screen.png";
        attribute canvasWidth = 1000;
        attribute canvasHeight = 640;

        part titleBar : TitleBar {
            attribute x = 0; attribute y = 0; attribute w = 1000; attribute h = 40;
            attribute text = "Ларец — Разблокировка хранилища";
            attribute trailing = "v0.1.0 · локальный режим";
        }

        // Левая брендовая панель
        part brandPanel : Panel {
            attribute x = 0; attribute y = 40; attribute w = 390; attribute h = 600;
            attribute fill = "dark";
        }
        part brandLogo : Logo {
            attribute x = 163; attribute y = 96; attribute w = 64; attribute h = 64;
        }
        part brandName : Label {
            attribute x = 0; attribute y = 174; attribute w = 390; attribute h = 36;
            attribute text = "Ларец"; attribute size = 28; attribute style = "bold";
            attribute color = "dark-text"; attribute align = "center";
        }
        part brandTagline : Label {
            attribute x = 0; attribute y = 214; attribute w = 390; attribute h = 20;
            attribute text = "Ваши пароли остаются у вас";
            attribute size = 13; attribute color = "dark-muted"; attribute align = "center";
        }
        part brandFeaturesTitle : Label {
            attribute x = 44; attribute y = 288; attribute w = 300; attribute h = 16;
            attribute text = "ВОЗМОЖНОСТИ"; attribute size = 11; attribute style = "bold";
            attribute color = "dark-muted";
        }
        part feature1 : Label {
            attribute x = 44; attribute y = 318; attribute w = 310; attribute h = 20;
            attribute text = "— генерация паролей по политике";
            attribute size = 13; attribute color = "sidebar-text";
        }
        part feature2 : Label {
            attribute x = 44; attribute y = 350; attribute w = 310; attribute h = 20;
            attribute text = "— категории, теги и заметки";
            attribute size = 13; attribute color = "sidebar-text";
        }
        part feature3 : Label {
            attribute x = 44; attribute y = 382; attribute w = 310; attribute h = 20;
            attribute text = "— двухфакторная аутентификация";
            attribute size = 13; attribute color = "sidebar-text";
        }
        part feature4 : Label {
            attribute x = 44; attribute y = 414; attribute w = 310; attribute h = 20;
            attribute text = "— автозаполнение в браузере";
            attribute size = 13; attribute color = "sidebar-text";
        }
        part brandFooter : Label {
            attribute x = 0; attribute y = 560; attribute w = 390; attribute h = 20;
            attribute text = "AES-256-GCM · PBKDF2 · офлайн-хранилище";
            attribute size = 11; attribute color = "dark-muted"; attribute align = "center";
        }

        // Карточка разблокировки
        part unlockCard : Card {
            attribute x = 430; attribute y = 96; attribute w = 510; attribute h = 454;
        }
        part unlockTitle : Label {
            attribute x = 470; attribute y = 132; attribute w = 430; attribute h = 30;
            attribute text = "Разблокировать хранилище";
            attribute size = 22; attribute style = "bold";
        }
        part unlockSubtitle : Label {
            attribute x = 470; attribute y = 168; attribute w = 430; attribute h = 20;
            attribute text = "Введите мастер-пароль для доступа к сейфу";
            attribute size = 13; attribute color = "muted";
        }
        part masterCaption : Label {
            attribute x = 470; attribute y = 212; attribute w = 300; attribute h = 18;
            attribute text = "МАСТЕР-ПАРОЛЬ"; attribute size = 11; attribute style = "bold";
            attribute color = "muted";
        }
        part masterField : Field {
            attribute x = 470; attribute y = 234; attribute w = 300; attribute h = 44;
            attribute value = "hidden"; attribute mask = true; attribute dots = 12;
        }
        part showPassword : Button {
            attribute x = 780; attribute y = 234; attribute w = 120; attribute h = 44;
            attribute text = "Показать"; attribute style = "secondary"; attribute size = 13;
        }
        part rememberSession : CheckBox {
            attribute x = 470; attribute y = 294; attribute w = 300; attribute h = 22;
            attribute text = "Запомнить на 30 минут"; attribute checked = false;
        }
        part unlockButton : Button {
            attribute x = 470; attribute y = 332; attribute w = 430; attribute h = 46;
            attribute text = "Разблокировать"; attribute style = "primary"; attribute size = 15;
        }
        part forgotLink : Label {
            attribute x = 470; attribute y = 388; attribute w = 430; attribute h = 20;
            attribute text = "Забыли мастер-пароль?"; attribute size = 13;
            attribute color = "primary"; attribute align = "center";
        }
        part unlockDivider : Divider {
            attribute x = 470; attribute y = 424; attribute w = 430; attribute h = 1;
        }
        part orLabel : Label {
            attribute x = 470; attribute y = 436; attribute w = 430; attribute h = 18;
            attribute text = "или"; attribute size = 12; attribute color = "faint";
            attribute align = "center";
        }
        part totpLogin : Button {
            attribute x = 470; attribute y = 462; attribute w = 430; attribute h = 44;
            attribute text = "Войти по одноразовому коду (2FA)";
            attribute style = "secondary"; attribute size = 14;
        }
        part hintLockout : Label {
            attribute x = 470; attribute y = 516; attribute w = 430; attribute h = 18;
            attribute text = "5 неудачных попыток — пауза 60 секунд";
            attribute size = 11; attribute color = "faint"; attribute align = "center";
        }

        part statusBar : StatusBar {
            attribute x = 0; attribute y = 600; attribute w = 1000; attribute h = 40;
            attribute text = "Хранилище: ~/.larets/vault.db";
            attribute trailing = "Офлайн-режим · сеть не используется";
        }
    }

    // ========================================================================
    //  ЭКРАН 2. Основное окно — список записей и карточка записи
    //  Трассировка: REQ-FUNC-002, REQ-FUNC-003, REQ-FUNC-004, REQ-INT-002
    // ========================================================================
    part def VaultScreen {
        attribute kind = "screen";
        attribute title = "Vault screen";
        attribute file = "02-vault-screen.png";
        attribute canvasWidth = 1000;
        attribute canvasHeight = 640;

        part titleBar : TitleBar {
            attribute x = 0; attribute y = 0; attribute w = 1000; attribute h = 40;
            attribute text = "Ларец — Хранилище";
            attribute trailing = "42 записи · сейф открыт";
        }

        // Боковая навигация
        part sidebar : Panel {
            attribute x = 0; attribute y = 40; attribute w = 250; attribute h = 560;
            attribute fill = "dark";
        }
        part sidebarLogo : Logo {
            attribute x = 18; attribute y = 60; attribute w = 34; attribute h = 34;
            attribute r = 10;
        }
        part sidebarName : Label {
            attribute x = 62; attribute y = 56; attribute w = 150; attribute h = 20;
            attribute text = "Ларец"; attribute size = 16; attribute style = "bold";
            attribute color = "dark-text";
        }
        part sidebarVersion : Label {
            attribute x = 62; attribute y = 76; attribute w = 150; attribute h = 16;
            attribute text = "v0.1.0 · beta"; attribute size = 10; attribute color = "dark-muted";
        }
        part navAll : SidebarRow {
            attribute x = 10; attribute y = 118; attribute w = 230; attribute h = 34;
            attribute text = "Все записи"; attribute badge = "42"; attribute active = true;
        }
        part navFavorites : SidebarRow {
            attribute x = 10; attribute y = 158; attribute w = 230; attribute h = 34;
            attribute text = "Избранное"; attribute badge = "7";
        }
        part navRecent : SidebarRow {
            attribute x = 10; attribute y = 198; attribute w = 230; attribute h = 34;
            attribute text = "Недавние";
        }
        part categoriesTitle : Label {
            attribute x = 20; attribute y = 254; attribute w = 210; attribute h = 16;
            attribute text = "КАТЕГОРИИ"; attribute size = 10; attribute style = "bold";
            attribute color = "dark-muted";
        }
        part catWork : SidebarRow {
            attribute x = 10; attribute y = 276; attribute w = 230; attribute h = 30;
            attribute text = "Работа"; attribute badge = "18";
        }
        part catPersonal : SidebarRow {
            attribute x = 10; attribute y = 310; attribute w = 230; attribute h = 30;
            attribute text = "Личное"; attribute badge = "12";
        }
        part catFinance : SidebarRow {
            attribute x = 10; attribute y = 344; attribute w = 230; attribute h = 30;
            attribute text = "Финансы"; attribute badge = "7";
        }
        part catDev : SidebarRow {
            attribute x = 10; attribute y = 378; attribute w = 230; attribute h = 30;
            attribute text = "Разработка"; attribute badge = "5";
        }
        part toolsTitle : Label {
            attribute x = 20; attribute y = 426; attribute w = 210; attribute h = 16;
            attribute text = "ИНСТРУМЕНТЫ"; attribute size = 10; attribute style = "bold";
            attribute color = "dark-muted";
        }
        part toolGenerator : SidebarRow {
            attribute x = 10; attribute y = 448; attribute w = 230; attribute h = 30;
            attribute text = "Генератор паролей";
        }
        part toolLeaks : SidebarRow {
            attribute x = 10; attribute y = 482; attribute w = 230; attribute h = 30;
            attribute text = "Проверка утечек";
        }
        part navSettings : SidebarRow {
            attribute x = 10; attribute y = 528; attribute w = 230; attribute h = 30;
            attribute text = "Настройки";
        }
        part navLock : SidebarRow {
            attribute x = 10; attribute y = 562; attribute w = 230; attribute h = 30;
            attribute text = "Заблокировать сейф";
        }

        // Верхняя полоса: поиск и основное действие
        part topBar : Panel {
            attribute x = 250; attribute y = 40; attribute w = 750; attribute h = 64;
            attribute fill = "surface";
        }
        part topBarDivider : Divider {
            attribute x = 250; attribute y = 104; attribute w = 750; attribute h = 1;
        }
        part searchField : Field {
            attribute x = 268; attribute y = 52; attribute w = 360; attribute h = 40;
            attribute value = ""; attribute placeholder = "Поиск: название, логин или тег";
            attribute size = 13; attribute fill = "surface-alt";
        }
        part newEntryButton : Button {
            attribute x = 646; attribute y = 52; attribute w = 190; attribute h = 40;
            attribute text = "+ Новая запись"; attribute size = 13;
        }
        part overflowButton : IconButton {
            attribute x = 848; attribute y = 52; attribute w = 40; attribute h = 40;
            attribute glyph = "…";
        }
        part syncButton : IconButton {
            attribute x = 896; attribute y = 52; attribute w = 40; attribute h = 40;
            attribute glyph = "↻";
        }

        // Список записей
        part listPanel : Panel {
            attribute x = 250; attribute y = 104; attribute w = 330; attribute h = 496;
            attribute fill = "surface"; attribute stroke = "border-soft";
        }
        part listHeader : Label {
            attribute x = 270; attribute y = 118; attribute w = 200; attribute h = 18;
            attribute text = "Все записи (42)"; attribute size = 12; attribute style = "bold";
            attribute color = "muted";
        }
        part rowGithub : ListRow {
            attribute x = 250; attribute y = 148; attribute w = 330; attribute h = 64;
            attribute text = "GitHub"; attribute subtitle = "d.murauyou@example.com";
            attribute selected = true;
        }
        part rowGoogle : ListRow {
            attribute x = 250; attribute y = 212; attribute w = 330; attribute h = 64;
            attribute text = "Google"; attribute subtitle = "d.murauyou@gmail.com";
        }
        part rowBank : ListRow {
            attribute x = 250; attribute y = 276; attribute w = 330; attribute h = 64;
            attribute text = "Сбербанк-онлайн"; attribute subtitle = "Личный кабинет";
        }
        part rowJira : ListRow {
            attribute x = 250; attribute y = 340; attribute w = 330; attribute h = 64;
            attribute text = "Jira"; attribute subtitle = "work.bguir.by"; attribute badge = "2FA";
        }
        part rowTelegram : ListRow {
            attribute x = 250; attribute y = 404; attribute w = 330; attribute h = 64;
            attribute text = "Telegram"; attribute subtitle = "+375 29 ••• 41 07";
        }
        part rowSteam : ListRow {
            attribute x = 250; attribute y = 468; attribute w = 330; attribute h = 64;
            attribute text = "Steam"; attribute subtitle = "game_nick_2019";
        }
        part rowNotion : ListRow {
            attribute x = 250; attribute y = 532; attribute w = 330; attribute h = 64;
            attribute text = "Notion"; attribute subtitle = "Учебные конспекты";
        }

        // Карточка выбранной записи
        part detailPanel : Panel {
            attribute x = 580; attribute y = 104; attribute w = 420; attribute h = 496;
            attribute fill = "surface"; attribute stroke = "border-soft";
        }
        part detailTitle : Label {
            attribute x = 606; attribute y = 122; attribute w = 200; attribute h = 28;
            attribute text = "GitHub"; attribute size = 20; attribute style = "bold";
        }
        part detailMeta : Label {
            attribute x = 606; attribute y = 154; attribute w = 260; attribute h = 18;
            attribute text = "Категория: Работа · обновлено сегодня";
            attribute size = 12; attribute color = "muted";
        }
        part editButton : Button {
            attribute x = 828; attribute y = 122; attribute w = 76; attribute h = 30;
            attribute text = "Правка"; attribute style = "secondary"; attribute size = 12;
        }
        part deleteButton : Button {
            attribute x = 912; attribute y = 122; attribute w = 62; attribute h = 30;
            attribute text = "Удалить"; attribute style = "danger"; attribute size = 11;
        }
        part detailDivider : Divider {
            attribute x = 606; attribute y = 182; attribute w = 368; attribute h = 1;
        }
        part loginCaption : Label {
            attribute x = 606; attribute y = 196; attribute w = 200; attribute h = 16;
            attribute text = "ЛОГИН"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part loginField : Field {
            attribute x = 606; attribute y = 214; attribute w = 262; attribute h = 40;
            attribute value = "d.murauyou@example.com"; attribute size = 13;
        }
        part copyLogin : Button {
            attribute x = 876; attribute y = 214; attribute w = 98; attribute h = 40;
            attribute text = "Копировать"; attribute style = "ghost"; attribute size = 12;
        }
        part passwordCaption : Label {
            attribute x = 606; attribute y = 268; attribute w = 200; attribute h = 16;
            attribute text = "ПАРОЛЬ"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part passwordField : Field {
            attribute x = 606; attribute y = 286; attribute w = 262; attribute h = 40;
            attribute mask = true; attribute dots = 14;
        }
        part revealPassword : Button {
            attribute x = 876; attribute y = 286; attribute w = 98; attribute h = 40;
            attribute text = "Показать"; attribute style = "ghost"; attribute size = 12;
        }
        part urlCaption : Label {
            attribute x = 606; attribute y = 340; attribute w = 200; attribute h = 16;
            attribute text = "АДРЕС САЙТА"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part urlField : Field {
            attribute x = 606; attribute y = 358; attribute w = 368; attribute h = 40;
            attribute value = "https://github.com/login"; attribute size = 13;
        }
        part notesCaption : Label {
            attribute x = 606; attribute y = 412; attribute w = 200; attribute h = 16;
            attribute text = "ЗАМЕТКИ"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part notesArea : TextArea {
            attribute x = 606; attribute y = 430; attribute w = 368; attribute h = 62;
            attribute value = "2FA включена. Резервные коды — в сейфе.";
            attribute size = 12;
        }
        part totpCard : Card {
            attribute x = 606; attribute y = 508; attribute w = 368; attribute h = 74;
            attribute r = 10;
        }
        part totpCaption : Label {
            attribute x = 620; attribute y = 518; attribute w = 240; attribute h = 14;
            attribute text = "ОДНОРАЗОВЫЙ КОД (TOTP)"; attribute size = 10;
            attribute style = "bold"; attribute color = "muted";
        }
        part totpCode : Label {
            attribute x = 620; attribute y = 534; attribute w = 140; attribute h = 28;
            attribute text = "492 301"; attribute size = 21; attribute style = "mono-bold";
        }
        part totpBar : Bar {
            attribute x = 730; attribute y = 546; attribute w = 150; attribute h = 8;
            attribute value = 0.55; attribute fill = "primary";
        }
        part totpTimer : Label {
            attribute x = 890; attribute y = 538; attribute w = 70; attribute h = 16;
            attribute text = "11 с"; attribute size = 11; attribute color = "muted";
        }

        part statusBar : StatusBar {
            attribute x = 250; attribute y = 600; attribute w = 750; attribute h = 40;
            attribute text = "Буфер обмена очистится через 20 с";
            attribute trailing = "Синхронизация: выключена";
        }
    }

    // ========================================================================
    //  ЭКРАН 3. Создание / редактирование записи
    //  Трассировка: REQ-FUNC-003, REQ-FUNC-005, REQ-FUNC-006
    // ========================================================================
    part def EntryEditorScreen {
        attribute kind = "screen";
        attribute title = "Entry editor";
        attribute file = "03-entry-editor.png";
        attribute canvasWidth = 1000;
        attribute canvasHeight = 640;

        part titleBar : TitleBar {
            attribute x = 0; attribute y = 0; attribute w = 1000; attribute h = 40;
            attribute text = "Ларец — Новая запись";
            attribute trailing = "категория: Работа";
        }
        part editorCard : Card {
            attribute x = 110; attribute y = 70; attribute w = 780; attribute h = 520;
        }
        part editorTitle : Label {
            attribute x = 146; attribute y = 96; attribute w = 400; attribute h = 28;
            attribute text = "Новая запись"; attribute size = 20; attribute style = "bold";
        }
        part editorSubtitle : Label {
            attribute x = 146; attribute y = 128; attribute w = 640; attribute h = 18;
            attribute text = "Поля со звёздочкой обязательны. Пароль сохраняется только в зашифрованном виде.";
            attribute size = 12; attribute color = "muted";
        }
        part titleCaption : Label {
            attribute x = 146; attribute y = 162; attribute w = 300; attribute h = 16;
            attribute text = "ЗАГОЛОВОК *"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part titleField : Field {
            attribute x = 146; attribute y = 182; attribute w = 330; attribute h = 42;
            attribute value = "GitLab"; attribute size = 14;
        }
        part categoryCaption : Label {
            attribute x = 500; attribute y = 162; attribute w = 300; attribute h = 16;
            attribute text = "КАТЕГОРИЯ"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part categoryField : Field {
            attribute x = 500; attribute y = 182; attribute w = 330; attribute h = 42;
            attribute value = "Работа"; attribute trailing = "▾"; attribute size = 14;
        }
        part loginCaption : Label {
            attribute x = 146; attribute y = 242; attribute w = 300; attribute h = 16;
            attribute text = "ЛОГИН"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part loginField : Field {
            attribute x = 146; attribute y = 262; attribute w = 330; attribute h = 42;
            attribute value = "d.murauyou"; attribute size = 14;
        }
        part urlCaption : Label {
            attribute x = 500; attribute y = 242; attribute w = 300; attribute h = 16;
            attribute text = "АДРЕС САЙТА"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part urlField : Field {
            attribute x = 500; attribute y = 262; attribute w = 330; attribute h = 42;
            attribute value = "https://gitlab.example.by"; attribute size = 13;
        }
        part passwordCaption : Label {
            attribute x = 146; attribute y = 322; attribute w = 300; attribute h = 16;
            attribute text = "ПАРОЛЬ *"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part passwordField : Field {
            attribute x = 146; attribute y = 342; attribute w = 230; attribute h = 42;
            attribute mask = true; attribute dots = 12;
        }
        part generateButton : Button {
            attribute x = 386; attribute y = 342; attribute w = 110; attribute h = 42;
            attribute text = "Сгенерировать"; attribute style = "secondary"; attribute size = 11;
        }
        part strengthBar : Bar {
            attribute x = 146; attribute y = 394; attribute w = 230; attribute h = 6;
            attribute value = 0.86; attribute fill = "success";
        }
        part strengthLabel : Label {
            attribute x = 386; attribute y = 386; attribute w = 110; attribute h = 16;
            attribute text = "Надёжный"; attribute size = 11; attribute color = "success";
        }
        part totpCaption : Label {
            attribute x = 500; attribute y = 322; attribute w = 330; attribute h = 16;
            attribute text = "СЕКРЕТ TOTP (НЕОБЯЗАТЕЛЬНО)"; attribute size = 10;
            attribute style = "bold"; attribute color = "muted";
        }
        part totpField : Field {
            attribute x = 500; attribute y = 342; attribute w = 330; attribute h = 42;
            attribute value = ""; attribute placeholder = "JBSW Y3DP EHPK 3PXP";
            attribute mono = true; attribute size = 13;
        }
        part notesCaption : Label {
            attribute x = 146; attribute y = 418; attribute w = 300; attribute h = 16;
            attribute text = "ЗАМЕТКИ"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part notesArea : TextArea {
            attribute x = 146; attribute y = 438; attribute w = 684; attribute h = 62;
            attribute placeholder = "Например: доступ только из офисной сети, 2FA обязательна";
            attribute size = 12;
        }
        part totpCheck : CheckBox {
            attribute x = 146; attribute y = 514; attribute w = 420; attribute h = 22;
            attribute text = "Требовать двухфакторную аутентификацию для записи";
            attribute checked = true;
        }
        part cancelButton : Button {
            attribute x = 520; attribute y = 542; attribute w = 130; attribute h = 36;
            attribute text = "Отмена"; attribute style = "secondary"; attribute size = 13;
        }
        part saveButton : Button {
            attribute x = 662; attribute y = 542; attribute w = 168; attribute h = 36;
            attribute text = "Сохранить запись"; attribute size = 13;
        }
        part statusBar : StatusBar {
            attribute x = 0; attribute y = 600; attribute w = 1000; attribute h = 40;
            attribute text = "Черновик сохраняется локально каждые 30 секунд";
            attribute trailing = "AES-256-GCM";
        }
    }

    // ========================================================================
    //  ЭКРАН 4. Генератор паролей
    //  Трассировка: REQ-FUNC-005, REQ-SEC-004, REQ-PERF-001
    // ========================================================================
    part def GeneratorScreen {
        attribute kind = "screen";
        attribute title = "Password generator";
        attribute file = "04-generator.png";
        attribute canvasWidth = 1000;
        attribute canvasHeight = 640;

        part titleBar : TitleBar {
            attribute x = 0; attribute y = 0; attribute w = 1000; attribute h = 40;
            attribute text = "Ларец — Генератор паролей";
            attribute trailing = "SecureRandom";
        }
        part outputCard : Card {
            attribute x = 80; attribute y = 70; attribute w = 840; attribute h = 180;
        }
        part outputCaption : Label {
            attribute x = 110; attribute y = 92; attribute w = 500; attribute h = 16;
            attribute text = "СГЕНЕРИРОВАННЫЙ ПАРОЛЬ"; attribute size = 10;
            attribute style = "bold"; attribute color = "muted";
        }
        part outputField : Field {
            attribute x = 110; attribute y = 116; attribute w = 540; attribute h = 52;
            attribute value = "tR7#vQ2!mZx9Lp@Kw8e"; attribute mono = true; attribute size = 20;
        }
        part copyButton : Button {
            attribute x = 664; attribute y = 116; attribute w = 110; attribute h = 52;
            attribute text = "Копировать"; attribute style = "secondary"; attribute size = 12;
        }
        part refreshButton : Button {
            attribute x = 782; attribute y = 116; attribute w = 110; attribute h = 52;
            attribute text = "Обновить"; attribute style = "secondary"; attribute size = 12;
        }
        part outputStrengthLabel : Label {
            attribute x = 110; attribute y = 182; attribute w = 500; attribute h = 18;
            attribute text = "Надёжность: высокая · энтропия 118 бит";
            attribute size = 12; attribute color = "muted";
        }
        part outputStrengthBar : Bar {
            attribute x = 110; attribute y = 206; attribute w = 540; attribute h = 8;
            attribute value = 0.88; attribute fill = "success";
        }
        part crackTime : Label {
            attribute x = 664; attribute y = 182; attribute w = 228; attribute h = 18;
            attribute text = "Подбор: > 1000 лет"; attribute size = 12; attribute color = "success";
        }

        // Настройки генерации
        part settingsCard : Card {
            attribute x = 80; attribute y = 272; attribute w = 470; attribute h = 298;
        }
        part settingsTitle : Label {
            attribute x = 110; attribute y = 296; attribute w = 200; attribute h = 18;
            attribute text = "ПАРАМЕТРЫ ГЕНЕРАЦИИ"; attribute size = 10;
            attribute style = "bold"; attribute color = "muted";
        }
        part lengthCaption : Label {
            attribute x = 110; attribute y = 324; attribute w = 200; attribute h = 20;
            attribute text = "Длина пароля"; attribute size = 14;
        }
        part lengthValue : Label {
            attribute x = 300; attribute y = 324; attribute w = 220; attribute h = 20;
            attribute text = "20 символов"; attribute size = 14; attribute style = "bold";
            attribute align = "right";
        }
        part lengthSlider : Slider {
            attribute x = 110; attribute y = 352; attribute w = 380; attribute h = 20;
            attribute value = 0.55;
        }
        part charsetUpper : CheckBox {
            attribute x = 110; attribute y = 392; attribute w = 190; attribute h = 22;
            attribute text = "Заглавные (A–Z)"; attribute checked = true;
        }
        part charsetLower : CheckBox {
            attribute x = 310; attribute y = 392; attribute w = 190; attribute h = 22;
            attribute text = "Строчные (a–z)"; attribute checked = true;
        }
        part charsetDigits : CheckBox {
            attribute x = 110; attribute y = 424; attribute w = 190; attribute h = 22;
            attribute text = "Цифры (0–9)"; attribute checked = true;
        }
        part charsetSymbols : CheckBox {
            attribute x = 310; attribute y = 424; attribute w = 190; attribute h = 22;
            attribute text = "Символы (!@#$%)"; attribute checked = true;
        }
        part excludeSimilar : CheckBox {
            attribute x = 110; attribute y = 456; attribute w = 200; attribute h = 22;
            attribute text = "Исключить похожие"; attribute checked = true;
        }
        part noAmbiguous : CheckBox {
            attribute x = 110; attribute y = 488; attribute w = 380; attribute h = 22;
            attribute text = "Только символы, которые легко продиктовать";
            attribute checked = false; attribute size = 13;
        }
        part settingsDivider : Divider {
            attribute x = 110; attribute y = 524; attribute w = 380; attribute h = 1;
        }
        part presetsLabel : Label {
            attribute x = 110; attribute y = 536; attribute w = 380; attribute h = 18;
            attribute text = "Пресеты: PIN · Для сайта · Максимальный";
            attribute size = 11; attribute color = "muted";
        }

        // Оценка надёжности
        part strengthCard : Card {
            attribute x = 570; attribute y = 272; attribute w = 350; attribute h = 298;
        }
        part strengthTitle : Label {
            attribute x = 600; attribute y = 296; attribute w = 290; attribute h = 18;
            attribute text = "ОЦЕНКА НАДЁЖНОСТИ"; attribute size = 10;
            attribute style = "bold"; attribute color = "muted";
        }
        part strengthWord : Label {
            attribute x = 600; attribute y = 318; attribute w = 290; attribute h = 30;
            attribute text = "Высокая"; attribute size = 22; attribute style = "bold";
            attribute color = "success";
        }
        part strengthBar : Bar {
            attribute x = 600; attribute y = 358; attribute w = 290; attribute h = 10;
            attribute value = 0.88; attribute fill = "success";
        }
        part entropyLabel : Label {
            attribute x = 600; attribute y = 384; attribute w = 290; attribute h = 18;
            attribute text = "Энтропия: 118 бит"; attribute size = 12; attribute color = "muted";
        }
        part combosLabel : Label {
            attribute x = 600; attribute y = 406; attribute w = 290; attribute h = 18;
            attribute text = "Комбинаций: 6,5 × 10³⁰"; attribute size = 12; attribute color = "muted";
        }
        part strengthDivider : Divider {
            attribute x = 600; attribute y = 436; attribute w = 290; attribute h = 1;
        }
        part localNote : Label {
            attribute x = 600; attribute y = 448; attribute w = 290; attribute h = 40;
            attribute text = "Пароль проверяется локально и не отправляется в сеть.";
            attribute size = 12; attribute color = "muted"; attribute wrap = true;
        }
        part historyButton : Button {
            attribute x = 600; attribute y = 510; attribute w = 290; attribute h = 34;
            attribute text = "История генератора (7)"; attribute style = "secondary";
            attribute size = 12;
        }
        part statusBar : StatusBar {
            attribute x = 0; attribute y = 600; attribute w = 1000; attribute h = 40;
            attribute text = "Источник случайности: java.security.SecureRandom";
            attribute trailing = "Только локально";
        }
    }

    // ========================================================================
    //  ЭКРАН 5. Подключение двухфакторной аутентификации (TOTP)
    //  Трассировка: REQ-FUNC-007, REQ-SEC-003
    // ========================================================================
    part def TwoFactorScreen {
        attribute kind = "screen";
        attribute title = "Two-factor setup";
        attribute file = "05-two-factor.png";
        attribute canvasWidth = 1000;
        attribute canvasHeight = 640;

        part titleBar : TitleBar {
            attribute x = 0; attribute y = 0; attribute w = 1000; attribute h = 40;
            attribute text = "Ларец — Двухфакторная аутентификация";
            attribute trailing = "TOTP · SHA-1 · 30 с";
        }
        part setupCard : Card {
            attribute x = 80; attribute y = 70; attribute w = 840; attribute h = 500;
        }
        part setupTitle : Label {
            attribute x = 110; attribute y = 94; attribute w = 500; attribute h = 28;
            attribute text = "Подключение 2FA (TOTP)"; attribute size = 20;
            attribute style = "bold";
        }
        part setupSubtitle : Label {
            attribute x = 110; attribute y = 126; attribute w = 760; attribute h = 18;
            attribute text = "Одноразовые коды защитят сейф, даже если мастер-пароль стал известен.";
            attribute size = 12; attribute color = "muted";
        }
        part step1 : Step {
            attribute x = 110; attribute y = 162; attribute w = 230; attribute h = 24;
            attribute number = "1"; attribute text = "Отсканируйте QR-код";
        }
        part step2 : Step {
            attribute x = 360; attribute y = 162; attribute w = 230; attribute h = 24;
            attribute number = "2"; attribute text = "Введите код из приложения";
        }
        part step3 : Step {
            attribute x = 620; attribute y = 162; attribute w = 280; attribute h = 24;
            attribute number = "3"; attribute text = "Сохраните резервные коды";
        }
        part setupQr : Qr {
            attribute x = 110; attribute y = 206; attribute w = 180; attribute h = 180;
            attribute text = "otpauth://totp/Larets:d.murauyou?secret=JBSWY3DPEHPK3PXP&issuer=Larets";
        }
        part secretCaption : Label {
            attribute x = 320; attribute y = 206; attribute w = 240; attribute h = 16;
            attribute text = "СЕКРЕТНЫЙ КЛЮЧ"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part secretField : Field {
            attribute x = 320; attribute y = 226; attribute w = 290; attribute h = 40;
            attribute value = "JBSW Y3DP EHPK 3PXP"; attribute mono = true; attribute size = 13;
        }
        part copySecret : Button {
            attribute x = 620; attribute y = 226; attribute w = 100; attribute h = 40;
            attribute text = "Копировать"; attribute style = "ghost"; attribute size = 11;
        }
        part appsHint : Label {
            attribute x = 320; attribute y = 278; attribute w = 430; attribute h = 34;
            attribute text = "Подойдут Google Authenticator, Aegis, 1Password или «Ключ».";
            attribute size = 12; attribute color = "muted"; attribute wrap = true;
        }
        part codeCaption : Label {
            attribute x = 320; attribute y = 320; attribute w = 240; attribute h = 16;
            attribute text = "КОД ИЗ ПРИЛОЖЕНИЯ"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part cell1 : CodeCell {
            attribute x = 320; attribute y = 340; attribute w = 44; attribute h = 52;
            attribute text = "4";
        }
        part cell2 : CodeCell {
            attribute x = 372; attribute y = 340; attribute w = 44; attribute h = 52;
            attribute text = "9";
        }
        part cell3 : CodeCell {
            attribute x = 424; attribute y = 340; attribute w = 44; attribute h = 52;
            attribute text = "2";
        }
        part cell4 : CodeCell {
            attribute x = 476; attribute y = 340; attribute w = 44; attribute h = 52;
            attribute text = "";
        }
        part cell5 : CodeCell {
            attribute x = 528; attribute y = 340; attribute w = 44; attribute h = 52;
            attribute text = "";
        }
        part cell6 : CodeCell {
            attribute x = 580; attribute y = 340; attribute w = 44; attribute h = 52;
            attribute text = "";
        }
        part confirmButton : Button {
            attribute x = 320; attribute y = 410; attribute w = 304; attribute h = 42;
            attribute text = "Проверить и включить"; attribute size = 13;
        }
        part errorHint : Label {
            attribute x = 320; attribute y = 462; attribute w = 340; attribute h = 18;
            attribute text = "Неверный код. Осталось попыток: 4.";
            attribute size = 12; attribute color = "danger";
        }
        part backupCaption : Label {
            attribute x = 756; attribute y = 206; attribute w = 180; attribute h = 16;
            attribute text = "РЕЗЕРВНЫЕ КОДЫ"; attribute size = 10; attribute style = "bold";
            attribute color = "muted";
        }
        part backupCodes : Label {
            attribute x = 756; attribute y = 228; attribute w = 180; attribute h = 110;
            attribute text = "7F3A-91C2\nB2D4-6E80\nC1A9-4F57\n9E3B-72D1\n5D8C-0A64\nA4F7-3C29";
            attribute size = 12; attribute style = "mono"; attribute color = "text";
        }
        part downloadCodes : Button {
            attribute x = 746; attribute y = 362; attribute w = 190; attribute h = 32;
            attribute text = "Скачать .txt"; attribute style = "secondary"; attribute size = 12;
        }
        part backupHint : Label {
            attribute x = 746; attribute y = 402; attribute w = 190; attribute h = 60;
            attribute text = "Каждый код одноразовый. Храните распечатку отдельно от компьютера.";
            attribute size = 11; attribute color = "muted"; attribute wrap = true;
        }
        part setupDivider : Divider {
            attribute x = 110; attribute y = 496; attribute w = 780; attribute h = 1;
        }
        part setupFooter : Label {
            attribute x = 110; attribute y = 508; attribute w = 780; attribute h = 18;
            attribute text = "2FA запрашивается при каждом открытии сейфа и через 30 минут бездействия.";
            attribute size = 11; attribute color = "muted";
        }
        part statusBar : StatusBar {
            attribute x = 0; attribute y = 600; attribute w = 1000; attribute h = 40;
            attribute text = "Настройка 2FA для записи GitHub";
            attribute trailing = "Секрет хранится в зашифрованном виде";
        }
    }

    // ========================================================================
    //  ЭКРАН 6. Настройки приложения
    //  Трассировка: REQ-FUNC-008, REQ-FUNC-009, REQ-SEC-002, REQ-SEC-006
    // ========================================================================
    part def SettingsScreen {
        attribute kind = "screen";
        attribute title = "Settings";
        attribute file = "06-settings.png";
        attribute canvasWidth = 1000;
        attribute canvasHeight = 640;

        part titleBar : TitleBar {
            attribute x = 0; attribute y = 0; attribute w = 1000; attribute h = 40;
            attribute text = "Ларец — Настройки";
            attribute trailing = "профиль: локальный";
        }
        part tabsBar : Panel {
            attribute x = 0; attribute y = 40; attribute w = 1000; attribute h = 56;
            attribute fill = "surface";
        }
        part tabGeneral : Tab {
            attribute x = 40; attribute y = 48; attribute w = 150; attribute h = 40;
            attribute text = "Общие"; attribute active = true;
        }
        part tabSecurity : Tab {
            attribute x = 190; attribute y = 48; attribute w = 150; attribute h = 40;
            attribute text = "Безопасность";
        }
        part tabAutofill : Tab {
            attribute x = 340; attribute y = 48; attribute w = 170; attribute h = 40;
            attribute text = "Автозаполнение";
        }
        part tabBackup : Tab {
            attribute x = 510; attribute y = 48; attribute w = 175; attribute h = 40;
            attribute text = "Резервные копии";
        }
        part tabAbout : Tab {
            attribute x = 685; attribute y = 48; attribute w = 150; attribute h = 40;
            attribute text = "О программе";
        }
        part tabsDivider : Divider {
            attribute x = 0; attribute y = 96; attribute w = 1000; attribute h = 1;
        }
        part settingsCard : Card {
            attribute x = 60; attribute y = 118; attribute w = 880; attribute h = 432;
        }
        part settingsHeader : Label {
            attribute x = 96; attribute y = 142; attribute w = 500; attribute h = 24;
            attribute text = "Общие настройки"; attribute size = 17; attribute style = "bold";
        }

        part autofillTitle : Label {
            attribute x = 96; attribute y = 184; attribute w = 620; attribute h = 20;
            attribute text = "Автозаполнение в браузере"; attribute size = 14; attribute style = "bold";
        }
        part autofillDesc : Label {
            attribute x = 96; attribute y = 204; attribute w = 620; attribute h = 16;
            attribute text = "Компаньон-расширение подставляет пароли только по явному запросу";
            attribute size = 11; attribute color = "muted";
        }
        part autofillToggle : Toggle {
            attribute x = 872; attribute y = 188; attribute w = 44; attribute h = 24;
            attribute on = true;
        }
        part divider1 : Divider {
            attribute x = 96; attribute y = 230; attribute w = 820; attribute h = 1;
        }

        part lockTitle : Label {
            attribute x = 96; attribute y = 238; attribute w = 620; attribute h = 20;
            attribute text = "Автоблокировка при бездействии"; attribute size = 14;
            attribute style = "bold";
        }
        part lockDesc : Label {
            attribute x = 96; attribute y = 258; attribute w = 620; attribute h = 16;
            attribute text = "Сейф закрывается автоматически после указанного интервала";
            attribute size = 11; attribute color = "muted";
        }
        part lockSelect : Field {
            attribute x = 742; attribute y = 244; attribute w = 174; attribute h = 36;
            attribute value = "5 минут"; attribute trailing = "▾"; attribute size = 13;
        }
        part divider2 : Divider {
            attribute x = 96; attribute y = 288; attribute w = 820; attribute h = 1;
        }

        part minimizeTitle : Label {
            attribute x = 96; attribute y = 296; attribute w = 620; attribute h = 20;
            attribute text = "Блокировать при сворачивании окна"; attribute size = 14;
            attribute style = "bold";
        }
        part minimizeDesc : Label {
            attribute x = 96; attribute y = 316; attribute w = 620; attribute h = 16;
            attribute text = "Дополнительный барьер, когда вы отходите от компьютера";
            attribute size = 11; attribute color = "muted";
        }
        part minimizeToggle : Toggle {
            attribute x = 872; attribute y = 300; attribute w = 44; attribute h = 24;
            attribute on = false;
        }
        part divider3 : Divider {
            attribute x = 96; attribute y = 342; attribute w = 820; attribute h = 1;
        }

        part breachTitle : Label {
            attribute x = 96; attribute y = 350; attribute w = 620; attribute h = 20;
            attribute text = "Проверка паролей по базе утечек"; attribute size = 14;
            attribute style = "bold";
        }
        part breachDesc : Label {
            attribute x = 96; attribute y = 370; attribute w = 620; attribute h = 16;
            attribute text = "k-анонимный запрос: наружу уходят только 5 символов хеша SHA-1";
            attribute size = 11; attribute color = "muted";
        }
        part breachToggle : Toggle {
            attribute x = 872; attribute y = 354; attribute w = 44; attribute h = 24;
            attribute on = true;
        }
        part divider4 : Divider {
            attribute x = 96; attribute y = 396; attribute w = 820; attribute h = 1;
        }

        part intervalTitle : Label {
            attribute x = 96; attribute y = 404; attribute w = 620; attribute h = 20;
            attribute text = "Интервал фоновой проверки"; attribute size = 14;
            attribute style = "bold";
        }
        part intervalDesc : Label {
            attribute x = 96; attribute y = 424; attribute w = 620; attribute h = 16;
            attribute text = "Как часто перепроверять сохранённые пароли";
            attribute size = 11; attribute color = "muted";
        }
        part intervalSelect : Field {
            attribute x = 742; attribute y = 410; attribute w = 174; attribute h = 36;
            attribute value = "1 раз в 7 дней"; attribute trailing = "▾"; attribute size = 13;
        }
        part divider5 : Divider {
            attribute x = 96; attribute y = 454; attribute w = 820; attribute h = 1;
        }

        part backupTitle : Label {
            attribute x = 96; attribute y = 462; attribute w = 620; attribute h = 20;
            attribute text = "Папка резервных копий"; attribute size = 14; attribute style = "bold";
        }
        part backupDesc : Label {
            attribute x = 96; attribute y = 482; attribute w = 620; attribute h = 16;
            attribute text = "Зашифрованные копии сейфа создаются автоматически";
            attribute size = 11; attribute color = "muted";
        }
        part backupField : Field {
            attribute x = 662; attribute y = 468; attribute w = 254; attribute h = 36;
            attribute value = "~/Larets/backups"; attribute size = 12; attribute mono = true;
        }
        part cardFooter : Label {
            attribute x = 96; attribute y = 514; attribute w = 820; attribute h = 18;
            attribute text = "Тема: светлая · Язык: русский · Версия 0.1.0";
            attribute size = 11; attribute color = "muted";
        }

        part resetButton : Button {
            attribute x = 700; attribute y = 562; attribute w = 120; attribute h = 34;
            attribute text = "Сбросить"; attribute style = "secondary"; attribute size = 13;
        }
        part saveButton : Button {
            attribute x = 832; attribute y = 562; attribute w = 108; attribute h = 34;
            attribute text = "Сохранить"; attribute size = 13;
        }
        part statusBar : StatusBar {
            attribute x = 0; attribute y = 604; attribute w = 1000; attribute h = 36;
            attribute text = "Изменения применяются сразу после сохранения";
            attribute trailing = "Настройки хранятся локально";
        }
    }
}
