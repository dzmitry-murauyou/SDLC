// ============================================================================
//  use-case-context.sysml — контекстная диаграмма и диаграмма вариантов
//  использования приложения «Ларец» (SysML v2 → PNG)
//  Лабораторная работа №3, кафедра ЭВМ, БГУИР
//
//  Диаграммы описывают границы системы: что входит в «Ларец», а что является
//  внешней сущностью (пользователь, браузер с расширением, приложение-
//  аутентификатор, файл сейфа, буфер обмена).
// ============================================================================

package Larets::UI::Diagrams {
    private import Larets::UI::*;

    // ========================================================================
    //  Диаграмма 7. Контекст системы (System Context)
    //  Ссылка в SRS: раздел 2.1 «Перспектива продукта»
    // ========================================================================
    part def SystemContextDiagram {
        attribute kind = "screen";
        attribute title = "System context";
        attribute file = "07-system-context.png";
        attribute canvasWidth = 1000;
        attribute canvasHeight = 640;

        // --- связи (рисуются первыми, чтобы линии были под блоками) ---------
        part c1 : Connector {
            attribute x = 180; attribute y = 300; attribute x2 = 370; attribute y2 = 320;
            attribute text = "мастер-пароль + код 2FA"; attribute labelAt = 0.45;
        }
        part c2 : Connector {
            attribute x = 630; attribute y = 290; attribute x2 = 700; attribute y2 = 170;
            attribute text = "Native Messaging"; attribute labelAt = 0.62;
        }
        part c3 : Connector {
            attribute x = 630; attribute y = 350; attribute x2 = 700; attribute y2 = 372;
            attribute text = "TOTP-код"; attribute labelAt = 0.35;
        }
        part c4 : Connector {
            attribute x = 390; attribute y = 430; attribute x2 = 200; attribute y2 = 480;
            attribute text = "AES-256-GCM"; attribute labelAt = 0.55;
        }
        part c5 : Connector {
            attribute x = 500; attribute y = 430; attribute x2 = 500; attribute y2 = 470;
            attribute text = "копия сейфа"; attribute labelAt = 0.9;
        }
        part c6 : Connector {
            attribute x = 500; attribute y = 250; attribute x2 = 500; attribute y2 = 152;
            attribute text = "копирование"; attribute labelAt = 0.45;
        }
        part c7 : Connector {
            attribute x = 630; attribute y = 420; attribute x2 = 700; attribute y2 = 490;
            attribute text = "k-анонимный запрос"; attribute labelAt = 0.4;
            attribute dashed = true;
        }

        // --- акторы и внешние системы --------------------------------------
        part user : Actor {
            attribute x = 60; attribute y = 250; attribute w = 120; attribute h = 90;
            attribute text = "Пользователь";
        }
        part clipboard : Boundary {
            attribute x = 370; attribute y = 80; attribute w = 260; attribute h = 72;
            attribute text = "Буфер обмена ОС";
        }
        part clipboardNote : Label {
            attribute x = 384; attribute y = 116; attribute w = 232; attribute h = 16;
            attribute text = "очистка через 20 секунд"; attribute size = 11;
            attribute color = "muted"; attribute align = "center";
        }
        part browser : Boundary {
            attribute x = 700; attribute y = 100; attribute w = 240; attribute h = 92;
            attribute text = "Браузер + расширение";
        }
        part browserNote : Label {
            attribute x = 712; attribute y = 136; attribute w = 216; attribute h = 40;
            attribute text = "компаньон «Ларец для браузера»";
            attribute size = 11; attribute color = "muted"; attribute align = "center";
            attribute wrap = true;
        }
        part authenticator : Boundary {
            attribute x = 700; attribute y = 300; attribute w = 240; attribute h = 92;
            attribute text = "Приложение-аутентификатор";
        }
        part authenticatorNote : Label {
            attribute x = 712; attribute y = 336; attribute w = 216; attribute h = 40;
            attribute text = "Google Authenticator / Aegis / «Ключ»";
            attribute size = 11; attribute color = "muted"; attribute align = "center";
            attribute wrap = true;
        }
        part vault : Boundary {
            attribute x = 70; attribute y = 470; attribute w = 230; attribute h = 92;
            attribute text = "Файл сейфа vault.db";
        }
        part vaultNote : Label {
            attribute x = 82; attribute y = 506; attribute w = 206; attribute h = 40;
            attribute text = "SQLite + AES-256-GCM, локальный диск";
            attribute size = 11; attribute color = "muted"; attribute align = "center";
            attribute wrap = true;
        }
        part backups : Boundary {
            attribute x = 370; attribute y = 470; attribute w = 240; attribute h = 92;
            attribute text = "Каталог резервных копий";
        }
        part backupsNote : Label {
            attribute x = 382; attribute y = 506; attribute w = 216; attribute h = 40;
            attribute text = "ротация: 7 последних копий";
            attribute size = 11; attribute color = "muted"; attribute align = "center";
            attribute wrap = true;
        }
        part leaks : Boundary {
            attribute x = 700; attribute y = 470; attribute w = 240; attribute h = 92;
            attribute text = "Сервис проверки утечек";
        }
        part leaksNote : Label {
            attribute x = 712; attribute y = 506; attribute w = 216; attribute h = 40;
            attribute text = "Have I Been Pwned (опционально)";
            attribute size = 11; attribute color = "muted"; attribute align = "center";
            attribute wrap = true;
        }

        // --- сама система ---------------------------------------------------
        part system : Boundary {
            attribute x = 370; attribute y = 250; attribute w = 260; attribute h = 180;
            attribute text = "«Ларец» 0.1.0";
        }
        part systemSub : Label {
            attribute x = 384; attribute y = 286; attribute w = 232; attribute h = 16;
            attribute text = "Desktop · Java 21 / JavaFX 21"; attribute size = 11;
            attribute color = "faint"; attribute align = "center";
        }
        part sysItem1 : Label {
            attribute x = 392; attribute y = 312; attribute w = 220; attribute h = 18;
            attribute text = "— локальный сейф"; attribute size = 12; attribute color = "text";
        }
        part sysItem2 : Label {
            attribute x = 392; attribute y = 334; attribute w = 220; attribute h = 18;
            attribute text = "— генератор паролей"; attribute size = 12; attribute color = "text";
        }
        part sysItem3 : Label {
            attribute x = 392; attribute y = 356; attribute w = 220; attribute h = 18;
            attribute text = "— 2FA (TOTP)"; attribute size = 12; attribute color = "text";
        }
        part sysItem4 : Label {
            attribute x = 392; attribute y = 378; attribute w = 220; attribute h = 18;
            attribute text = "— категории и заметки"; attribute size = 12; attribute color = "text";
        }
        part sysItem5 : Label {
            attribute x = 392; attribute y = 400; attribute w = 220; attribute h = 18;
            attribute text = "— мост автозаполнения"; attribute size = 12; attribute color = "text";
        }

        part statusBar : StatusBar {
            attribute x = 0; attribute y = 600; attribute w = 1000; attribute h = 40;
            attribute text = "Границы системы: всё, что внутри «Ларец», реализуется командой проекта";
            attribute trailing = "SysML v2 · system context";
        }
    }

    // ========================================================================
    //  Диаграмма 8. Варианты использования (Use Case)
    //  Ссылка в SRS: раздел 2.2 «Функции продукта»
    // ========================================================================
    part def UseCaseDiagram {
        attribute kind = "screen";
        attribute title = "Use cases";
        attribute file = "08-use-cases.png";
        attribute canvasWidth = 1000;
        attribute canvasHeight = 640;


        // связи рисуются поверх рамки диаграммы, чтобы подписи читались
        part c1 : Connector {
            attribute x = 180; attribute y = 285; attribute x2 = 250; attribute y2 = 285;
        }
        part c2 : Connector {
            attribute x = 770; attribute y = 190; attribute x2 = 830; attribute y2 = 320;
            attribute dashed = true;
        }
        part c3 : Connector {
            attribute x = 770; attribute y = 470; attribute x2 = 830; attribute y2 = 340;
        }

        part actorUser : Actor {
            attribute x = 60; attribute y = 240; attribute w = 120; attribute h = 90;
            attribute text = "Пользователь";
        }
        part actorExt : Actor {
            attribute x = 830; attribute y = 290; attribute w = 130; attribute h = 90;
            attribute text = "Расширение браузера";
        }

        part caseBox : Boundary {
            attribute x = 250; attribute y = 60; attribute w = 520; attribute h = 500;
            attribute text = "«Ларец» 0.1.0 — варианты использования";
        }

        part uc1 : UseCase {
            attribute x = 278; attribute y = 100; attribute w = 210; attribute h = 52;
            attribute text = "Разблокировать сейф";
        }
        part uc2 : UseCase {
            attribute x = 278; attribute y = 176; attribute w = 210; attribute h = 52;
            attribute text = "Управлять записями";
        }
        part uc3 : UseCase {
            attribute x = 278; attribute y = 252; attribute w = 210; attribute h = 52;
            attribute text = "Генерировать пароль";
        }
        part uc4 : UseCase {
            attribute x = 278; attribute y = 328; attribute w = 210; attribute h = 52;
            attribute text = "Настроить 2FA";
        }
        part uc5 : UseCase {
            attribute x = 278; attribute y = 404; attribute w = 210; attribute h = 52;
            attribute text = "Искать и фильтровать";
        }
        part uc6 : UseCase {
            attribute x = 528; attribute y = 100; attribute w = 210; attribute h = 52;
            attribute text = "Копировать с автоочисткой";
        }
        part uc7 : UseCase {
            attribute x = 528; attribute y = 176; attribute w = 210; attribute h = 52;
            attribute text = "Категории и избранное";
        }
        part uc8 : UseCase {
            attribute x = 528; attribute y = 252; attribute w = 210; attribute h = 52;
            attribute text = "Резервное копирование";
        }
        part uc9 : UseCase {
            attribute x = 528; attribute y = 328; attribute w = 210; attribute h = 52;
            attribute text = "Проверить утечки";
        }
        part uc10 : UseCase {
            attribute x = 528; attribute y = 404; attribute w = 210; attribute h = 52;
            attribute text = "Автозаполнить форму";
        }

        part note : Panel {
            attribute x = 290; attribute y = 474; attribute w = 440; attribute h = 76;
            attribute r = 10; attribute fill = "surface-alt";
        }
        part noteLabel : Label {
            attribute x = 306; attribute y = 486; attribute w = 408; attribute h = 54;
            attribute text = "Расширение браузера запрашивает автозаполнение только по действию пользователя и не получает доступ к мастер-паролю.";
            attribute size = 11; attribute color = "muted"; attribute align = "center";
            attribute wrap = true;
        }

        part statusBar : StatusBar {
            attribute x = 0; attribute y = 600; attribute w = 1000; attribute h = 40;
            attribute text = "Трассировка: каждый вариант использования связан с REQ-FUNC-* в SRS";
            attribute trailing = "SysML v2 · use case";
        }
    }
}
