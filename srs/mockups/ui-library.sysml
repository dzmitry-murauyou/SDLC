// ============================================================================
//  ui-library.sysml — библиотека элементов пользовательского интерфейса
//  Проект: «Ларец» — менеджер паролей (Desktop, Java)
//  Лабораторная работа №3, кафедра ЭВМ, БГУИР
//
//  Пакет описывает словарь GUI-прототипирования на языке SysML v2:
//  каждый элемент интерфейса — это part def с типизированными атрибутами
//  (позиция, размер, состояние, подпись, оформление). Модель экранов
//  (ui-mockups.sysml) использует эти определения, а скрипт render_mockups.py
//  отрисовывает её в PNG. Так требования к UI становятся проверяемой моделью,
//  а не набором картинок.
// ============================================================================

package Larets::UI {

    // ------------------------------------------------------------------
    //  Общие перечисления предметной области мокапов
    // ------------------------------------------------------------------
    enum def ControlStyle {
        enum primary;      // основное действие экрана
        enum secondary;    // второстепенное действие
        enum ghost;        // действие-ссылка
        enum danger;       // деструктивное действие
        enum danger-solid;
        enum on-dark;      // кнопка на тёмной панели
    }

    enum def FieldState {
        enum normal;
        enum focused;
        enum error;
        enum disabled;
    }

    enum def StrengthLevel {
        enum weak;         // < 60 бит энтропии
        enum medium;       // 60–90 бит
        enum strong;       // 90–120 бит
        enum excellent;    // > 120 бит
    }

    // ------------------------------------------------------------------
    //  Контейнеры и оформление
    // ------------------------------------------------------------------

    // Заголовок окна приложения (desktop title bar)
    part def TitleBar {
        attribute text : String;        // заголовок окна
        attribute trailing : String;    // подпись справа (версия, счётчик)
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer;
        attribute fill : String = "dark";
    }

    // Плоская область (панель, сайдбар, полоса)
    part def Panel {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer;
        attribute r : Integer = 0;      // радиус скругления
        attribute fill : String;
        attribute stroke : String;      // цвет рамки (опционально)
    }

    // Карточка контента с тенью и рамкой
    part def Card {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer;
        attribute r : Integer = 14;
        attribute fill : String = "surface";
        attribute stroke : String = "border-soft";
    }

    part def Divider {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer = 1;
        attribute fill : String = "border-soft";
    }

    // ------------------------------------------------------------------
    //  Текст и данные
    // ------------------------------------------------------------------

    // Текстовая подпись; align = left | center | right
    part def Label {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer = 0;
        attribute text : String;
        attribute size : Integer = 14;
        attribute style : String = "regular";   // regular | bold | mono | mono-bold
        attribute color : String = "text";
        attribute align : String = "left";
        attribute wrap : Boolean = false;
    }

    // Однострочное поле ввода; mask = true скрывает значение точками
    part def Field {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer = 42;
        attribute value : String;       // отображаемое значение
        attribute placeholder : String;
        attribute mask : Boolean = false;
        attribute mono : Boolean = false;
        attribute disabled : Boolean = false;
        attribute trailing : String;    // суффикс (например, «▾» у списка)
        attribute size : Integer = 15;
        attribute dots : Integer = 14;   // число точек при mask = true
        attribute fill : String;
        attribute stroke : String = "border";
    }

    // Многострочное поле заметок
    part def TextArea {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer;
        attribute value : String;
        attribute placeholder : String;
        attribute size : Integer = 14;
        attribute fill : String = "surface";
        attribute stroke : String = "border";
    }

    // ------------------------------------------------------------------
    //  Действия и управляющие элементы
    // ------------------------------------------------------------------

    part def Button {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer = 40;
        attribute text : String;
        attribute style : ControlStyle = ControlStyle::primary;
        attribute size : Integer = 14;
        attribute r : Integer = 9;
    }

    // Квадратная кнопка-иконка (меню, обновление, настройки)
    part def IconButton {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer = 40;
        attribute h : Integer = 40;
        attribute glyph : String;
        attribute style : String = "secondary";
        attribute size : Integer = 15;
    }

    part def CheckBox {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer = 22;
        attribute text : String;
        attribute checked : Boolean = false;
        attribute size : Integer = 14;
        attribute color : String = "text";
    }

    // Переключатель (toggle switch)
    part def Toggle {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer = 44;
        attribute h : Integer = 24;
        attribute on : Boolean = true;
    }

    // Индикатор заполненности: шкала надёжности, срок действия TOTP
    part def Bar {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer = 8;
        attribute value : Real;         // 0.0 … 1.0
        attribute fill : String = "success";
        attribute background : String = "border-soft";
        attribute caption : String;
    }

    part def Slider {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer = 20;
        attribute value : Real;         // 0.0 … 1.0
    }

    // ------------------------------------------------------------------
    //  Навигация и списки
    // ------------------------------------------------------------------

    // Строка списка записей сейфа
    part def ListRow {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer = 64;
        attribute text : String;
        attribute subtitle : String;
        attribute badge : String;
        attribute selected : Boolean = false;
        attribute icon : String = "border-soft";
    }

    // Строка боковой навигации
    part def SidebarRow {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer = 32;
        attribute text : String;
        attribute badge : String;
        attribute active : Boolean = false;
    }

    part def Tab {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer = 150;
        attribute h : Integer = 40;
        attribute text : String;
        attribute active : Boolean = false;
    }

    part def StatusBar {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer = 40;
        attribute text : String;
        attribute trailing : String;
    }

    // ------------------------------------------------------------------
    //  Специализированные элементы предметной области
    // ------------------------------------------------------------------

    // Шаг мастера (нумерация в сценарии 2FA)
    part def Step {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer = 200;
        attribute h : Integer = 24;
        attribute number : String;
        attribute text : String;
        attribute active : Boolean = true;
    }

    // Ячейка ввода одноразового кода
    part def CodeCell {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer = 44;
        attribute h : Integer = 52;
        attribute text : String;
    }

    // QR-код для сопряжения с аутентификатором
    part def Qr {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer = 180;
        attribute h : Integer = 180;
        attribute text : String;        // otpauth://-ссылка, из неё строится узор
    }

    // Логотип приложения
    part def Logo {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer = 64;
        attribute h : Integer = 64;
        attribute r : Integer = 18;
        attribute fill : String = "primary";
    }

    // ------------------------------------------------------------------
    //  Элементы контекстной (use case) диаграммы
    // ------------------------------------------------------------------
    part def Boundary {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer;
        attribute h : Integer;
        attribute text : String;
    }

    part def Actor {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer = 120;
        attribute h : Integer = 90;
        attribute text : String;
    }

    part def UseCase {
        attribute x : Integer;
        attribute y : Integer;
        attribute w : Integer = 160;
        attribute h : Integer = 56;
        attribute text : String;
        attribute size : Integer = 12;
    }

    // Линия связи между элементами диаграммы
    part def Connector {
        attribute x : Integer;
        attribute y : Integer;
        attribute x2 : Integer;
        attribute y2 : Integer;
        attribute dashed : Boolean = false;
        attribute text : String;
        attribute fill : String = "muted";
    }
}
