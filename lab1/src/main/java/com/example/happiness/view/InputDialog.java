package com.example.happiness.view;

import com.example.happiness.model.HappinessData;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.KeyStroke;
import javax.swing.SwingConstants;
import javax.swing.Timer;
import javax.swing.text.AbstractDocument;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Frame;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;

public class InputDialog extends JDialog {

    private static final long serialVersionUID = 2L;

    private static final int WARNING_MILLIS = 2500;

    private final JTextField sleepField = new JTextField(4);
    private final JTextField coffeeField = new JTextField(4);
    private final JTextField socialField = new JTextField(4);
    private final JTextField workField = new JTextField(4);
    private final JTextField weekendField = new JTextField(4);

    private final JLabel hintLabel = new JLabel(" ", SwingConstants.CENTER);
    private final JLabel warnLabel = new JLabel(" ", SwingConstants.CENTER);
    private final Timer hideWarningTimer;

    private boolean confirmed = false;

    public InputDialog(Frame owner, HappinessData initial) {
        super(owner, "Ввод данных: сутки и выходные", true); // true = модальный диалог
        hideWarningTimer = new Timer(WARNING_MILLIS, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                hideWarning();
            }
        });
        hideWarningTimer.setRepeats(false);
        buildUi();
        if (initial != null) {
            restore(initial);
        }
    }

    private void buildUi() {
        setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        setLayout(new BorderLayout(8, 8));

        JPanel form = new JPanel(new GridLayout(0, 1, 0, 6));
        form.setBorder(BorderFactory.createEmptyBorder(12, 16, 4, 16));

        form.add(fieldPanel("Сон, часов в сутки (0–24, можно дробное):", sleepField, true,
                "Меньше 6 часов — 0 баллов, полный балл — с 8 часов и выше."));
        form.add(fieldPanel("Кофе, чашек в сутки (0–20, целое):", coffeeField, false,
                "1–2 чашки — максимум, 0 чашек — половина балла, с 5-й — 0."));
        form.add(fieldPanel("Приятное общение, минут в сутки (0–1440, целое):", socialField, false,
                "Только отдых с друзьями и близкими — рабочие разговоры не считаются."));
        form.add(fieldPanel("Работа, часов в сутки (0–24, можно дробное):", workField, true,
                "Полный балл — до 8 часов, с 8 до 12 — падает, после 12 — 0."));
        form.add(fieldPanel("Выходные, дней в неделю (0–7, целое):", weekendField, false,
                "В неделю: 0 дней — 0 баллов, 1 — половина, 2 — 75 %, 3+ — максимум."));
        add(form, BorderLayout.CENTER);

        JPanel south = new JPanel(new BorderLayout(0, 2));
        hintLabel.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 14));
        hintLabel.setForeground(new Color(90, 90, 90));
        hintLabel.setText("<html><center>Сон + работа + общение не могут превышать 24 часа в сутки — "
                + "иначе появится ошибка.<br>Буквы в полях запрещены, дробную часть пишите "
                + "через точку или запятую.</center></html>");
        warnLabel.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 14));
        warnLabel.setForeground(new Color(178, 34, 34, 0));
        south.add(hintLabel, BorderLayout.NORTH);
        south.add(warnLabel, BorderLayout.CENTER);

        JPanel buttons = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 8));
        JButton okButton = new JButton("OK");
        JButton cancelButton = new JButton("Отмена");
        okButton.addActionListener(e -> {
            confirmed = true;
            dispose();
        });
        cancelButton.addActionListener(e -> dispose());
        buttons.add(okButton);
        buttons.add(cancelButton);
        south.add(buttons, BorderLayout.SOUTH);
        add(south, BorderLayout.SOUTH);

        getRootPane().setDefaultButton(okButton);
        getRootPane().registerKeyboardAction(e -> dispose(),
                KeyStroke.getKeyStroke(KeyEvent.VK_ESCAPE, 0),
                JComponent.WHEN_IN_FOCUSED_WINDOW);

        setSize(700, 580);
        setLocationRelativeTo(getOwner());
    }

    private JPanel fieldPanel(String labelText, JTextField field,
                              boolean allowDecimal, String hintText) {
        attachNumericFilter(field, allowDecimal);
        field.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 15));

        JLabel label = new JLabel(labelText);
        label.setLabelFor(field);
        label.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 15));

        JLabel hint = new JLabel(hintText);
        hint.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 13));
        hint.setForeground(new Color(120, 120, 120));

        JPanel panel = new JPanel(new BorderLayout(0, 2));
        panel.add(label, BorderLayout.NORTH);
        panel.add(field, BorderLayout.CENTER);
        panel.add(hint, BorderLayout.SOUTH);
        return panel;
    }

    private void attachNumericFilter(JTextField field, boolean allowDecimal) {
        if (field.getDocument() instanceof AbstractDocument) {
            ((AbstractDocument) field.getDocument()).setDocumentFilter(
                    new NumericDocumentFilter(allowDecimal, this::showWarning));
        }
    }

    private void showWarning(String attemptedText) {
        String shown = attemptedText == null ? "" : attemptedText.trim();
        if (shown.length() > 20) {
            shown = shown.substring(0, 20) + "…";
        }
        String what = shown.isEmpty() ? "недопустимые символы" : "«" + shown + "»";
        warnLabel.setText("<html><center><b>Только цифры!</b> " + what
                + " — вводить нельзя.</center></html>");
        hideWarningTimer.restart();
    }

    private void hideWarning() {
        warnLabel.setText(" ");
    }

    public final void restore(HappinessData data) {
        sleepField.setText(formatDouble(data.getSleepHoursPerDay()));
        coffeeField.setText(String.valueOf(data.getCoffeeCupsPerDay()));
        socialField.setText(String.valueOf(data.getSocialMinutesPerDay()));
        workField.setText(formatDouble(data.getWorkHoursPerDay()));
        weekendField.setText(String.valueOf(data.getWeekendDaysPerWeek()));
    }

    public void restoreRaw(String sleep, String coffee, String social, String work, String weekend) {
        sleepField.setText(sleep);
        coffeeField.setText(coffee);
        socialField.setText(social);
        workField.setText(work);
        weekendField.setText(weekend);
    }

    public boolean isConfirmed() {
        return confirmed;
    }

    public String getSleepText() {
        return sleepField.getText();
    }

    public String getCoffeeText() {
        return coffeeField.getText();
    }

    public String getSocialText() {
        return socialField.getText();
    }

    public String getWorkText() {
        return workField.getText();
    }

    public String getWeekendText() {
        return weekendField.getText();
    }

    private static String formatDouble(double value) {
        if (value == Math.rint(value)) {
            return String.valueOf((long) value);
        }
        return String.valueOf(value);
    }

    public static InputDialog create(JFrame owner, HappinessData initial) {
        return new InputDialog(owner, initial);
    }
}
