package com.example.happiness.controller;

import com.example.happiness.model.HappinessData;
import com.example.happiness.model.HappinessModel;
import com.example.happiness.view.InputDialog;
import com.example.happiness.view.MainFrame;

import javax.swing.JOptionPane;

public class HappinessController {

    private final HappinessModel model;
    private final MainFrame mainFrame;

    public HappinessController(HappinessModel model, MainFrame mainFrame) {
        if (model == null || mainFrame == null) {
            throw new IllegalArgumentException("Модель и главное окно должны быть заданы.");
        }
        this.model = model;
        this.mainFrame = mainFrame;
    }

    public void onInputButtonClicked() {
        HappinessData initial = model.hasData() ? model.getData() : HappinessModel.defaultData();

        String rawSleep = null, rawCoffee = null, rawSocial = null, rawWork = null, rawWeekend = null;
        boolean firstOpen = true;

        while (true) {
            InputDialog dialog = InputDialog.create(mainFrame, firstOpen ? initial : null);
            if (!firstOpen) {
                dialog.restoreRaw(rawSleep, rawCoffee, rawSocial, rawWork, rawWeekend);
            }
            firstOpen = false;
            dialog.setVisible(true);

            if (!dialog.isConfirmed()) {
                return;
            }

            rawSleep = dialog.getSleepText();
            rawCoffee = dialog.getCoffeeText();
            rawSocial = dialog.getSocialText();
            rawWork = dialog.getWorkText();
            rawWeekend = dialog.getWeekendText();

            try {
                HappinessData data = parseInput(rawSleep, rawCoffee, rawSocial, rawWork, rawWeekend);
                model.setData(data);
                return;
            } catch (IllegalArgumentException e) {
                showError(e.getMessage());
            }
        }
    }

    /** Показать сообщение об ошибке ввода. */
    private void showError(String message) {
        JOptionPane.showMessageDialog(mainFrame, message,
                "Ошибка ввода", JOptionPane.ERROR_MESSAGE);
    }


    public static HappinessData parseInput(String sleepText, String coffeeText,
                                          String socialText, String workText,
                                          String weekendText) {
        double sleep = parseDoubleField(sleepText, "Сон",
                HappinessData.MIN_SLEEP_HOURS, HappinessData.MAX_SLEEP_HOURS, "часов в сутки");
        int coffee = parseIntField(coffeeText, "Кофе",
                HappinessData.MIN_COFFEE_CUPS, HappinessData.MAX_COFFEE_CUPS, "чашек в сутки");
        int social = parseIntField(socialText, "Общение",
                HappinessData.MIN_SOCIAL_MINUTES, HappinessData.MAX_SOCIAL_MINUTES,
                "минут в сутки");
        double work = parseDoubleField(workText, "Работа",
                HappinessData.MIN_WORK_HOURS, HappinessData.MAX_WORK_HOURS, "часов в сутки");
        int weekend = parseIntField(weekendText, "Выходные",
                HappinessData.MIN_WEEKEND_DAYS, HappinessData.MAX_WEEKEND_DAYS, "дней в неделю");

        HappinessData.checkDayFits(sleep, work, social);

        return new HappinessData(sleep, coffee, social, work, weekend);
    }

    static double parseDoubleField(String text, String fieldName,
                                   double min, double max, String unit) {
        String trimmed = requireText(text, fieldName, min, max, unit, false);
        String normalized = trimmed.replace(',', '.');
        if (!normalized.matches("\\d+(\\.\\d+)?")) {
            throw lettersError(trimmed, fieldName, min, max, unit, false);
        }
        double value;
        try {
            value = Double.parseDouble(normalized);
        } catch (NumberFormatException e) {
            throw lettersError(trimmed, fieldName, min, max, unit, false);
        }
        return checkRange(value, fieldName, min, max, unit);
    }

    static int parseIntField(String text, String fieldName,
                             int min, int max, String unit) {
        String trimmed = requireText(text, fieldName, min, max, unit, true);
        if (!trimmed.matches("\\d+")) {
            throw lettersError(trimmed, fieldName, min, max, unit, true);
        }
        int value;
        try {
            value = Integer.parseInt(trimmed);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException(
                    "Поле «" + fieldName + "»: «" + trimmed + "» — слишком большое число. "
                            + "Введите целое число от " + min + " до " + max + " (" + unit + ").");
        }
        return (int) checkRange(value, fieldName, min, max, unit);
    }

    private static String requireText(String text, String fieldName,
                                      double min, double max, String unit,
                                      boolean integerOnly) {
        if (text == null || text.trim().isEmpty()) {
            throw new IllegalArgumentException(
                    "Поле «" + fieldName + "» не заполнено. Введите "
                            + (integerOnly ? "целое " : "") + "число от "
                            + formatBound(min) + " до " + formatBound(max)
                            + " (" + unit + ").");
        }
        return text.trim();
    }

    private static IllegalArgumentException lettersError(String trimmed, String fieldName,
                                                         double min, double max, String unit,
                                                         boolean integerOnly) {
        boolean hasLetters = false;
        for (int i = 0; i < trimmed.length(); i++) {
            if (Character.isLetter(trimmed.charAt(i))) {
                hasLetters = true;
                break;
            }
        }
        StringBuilder message = new StringBuilder("Поле «").append(fieldName).append("»: «")
                .append(trimmed).append("» — ");
        if (hasLetters) {
            message.append("содержит буквы. Вводить можно только цифры");
        } else {
            message.append("не число. Введите число");
        }
        if (integerOnly) {
            message.append(" — целое, без дробной части");
        } else {
            message.append(" — дробную часть отделяйте точкой или запятой");
        }
        message.append(". Допустимые значения: от ").append(formatBound(min))
                .append(" до ").append(formatBound(max)).append(" (").append(unit).append(").");
        return new IllegalArgumentException(message.toString());
    }

    private static double checkRange(double value, String fieldName,
                                     double min, double max, String unit) {
        if (Double.isNaN(value) || Double.isInfinite(value) || value < min || value > max) {
            throw new IllegalArgumentException(
                    "Поле «" + fieldName + "»: значение должно быть от "
                            + formatBound(min) + " до " + formatBound(max)
                            + " (" + unit + ").");
        }
        return value;
    }

    private static String formatBound(double bound) {
        if (bound == Math.rint(bound)) {
            return String.valueOf((long) bound);
        }
        return String.valueOf(bound);
    }
}
