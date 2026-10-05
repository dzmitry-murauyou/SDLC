package com.example.happiness.view;

import com.example.happiness.controller.HappinessController;
import com.example.happiness.model.HappinessData;
import com.example.happiness.model.HappinessModel;
import com.example.happiness.model.HappinessResult;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;
import java.awt.BorderLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;

public class MainFrame extends JFrame implements PropertyChangeListener {

    private static final long serialVersionUID = 1L;

    private final JLabel titleLabel = new JLabel("Калькулятор счастья", SwingConstants.CENTER);
    private final JLabel dataLabel = new JLabel("", SwingConstants.CENTER);
    private final JLabel indexLabel = new JLabel("", SwingConstants.CENTER);
    private final JLabel recommendationLabel = new JLabel("", SwingConstants.CENTER);
    private final JLabel breakdownLabel = new JLabel("", SwingConstants.CENTER);
    private final JButton inputButton = new JButton("Ввести данные");

    private HappinessController controller;

    public MainFrame() {
        super("Калькулятор счастья");
        buildUi();
    }

    public void setController(HappinessController controller) {
        this.controller = controller;
    }

    private void buildUi() {
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(700, 500);
        setLocationRelativeTo(null); // по центру экрана
        setLayout(new BorderLayout(10, 10));

        titleLabel.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 24));
        titleLabel.setBorder(BorderFactory.createEmptyBorder(15, 10, 5, 10));
        add(titleLabel, BorderLayout.NORTH);

        JPanel center = new JPanel(new GridLayout(4, 1, 5, 5));
        center.setBorder(BorderFactory.createEmptyBorder(10, 20, 10, 20));

        dataLabel.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 16));
        indexLabel.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 22));
        recommendationLabel.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 16));
        breakdownLabel.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 14));

        center.add(dataLabel);
        center.add(indexLabel);
        center.add(recommendationLabel);
        center.add(breakdownLabel);
        add(center, BorderLayout.CENTER);

        JPanel bottom = new JPanel();
        bottom.setBorder(BorderFactory.createEmptyBorder(0, 10, 15, 10));
        inputButton.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 17));
        inputButton.addActionListener(e -> {
            if (controller != null) {
                controller.onInputButtonClicked();
            }
        });
        bottom.add(inputButton);
        add(bottom, BorderLayout.SOUTH);

        showPlaceholder();
    }

    private void showPlaceholder() {
        dataLabel.setText("Нажмите «Ввести данные» и расскажите о своих сутках.");
        indexLabel.setText("Индекс счастья: —");
        recommendationLabel.setText("Рекомендация появится здесь.");
        breakdownLabel.setText("");
    }

    @Override
    public void propertyChange(PropertyChangeEvent evt) {
        if (HappinessModel.PROP_RESULT.equals(evt.getPropertyName())) {
            HappinessResult result = (HappinessResult) evt.getNewValue();
            HappinessData data = null;
            if (evt.getSource() instanceof HappinessModel) {
                data = ((HappinessModel) evt.getSource()).getData();
            }
            updateResult(data, result);
        }
    }

    private void updateResult(HappinessData data, HappinessResult result) {
        if (data == null || result == null) {
            showPlaceholder();
            return;
        }
        dataLabel.setText(String.format(
                "<html><center>Сон: %s ч/сутки &nbsp;•&nbsp; Кофе: %d чашек/сутки "
                        + "&nbsp;•&nbsp; Приятное общение: %d мин/сутки<br>"
                        + "Работа: %s ч/сутки &nbsp;•&nbsp; Выходные: %d дн/неделю</center></html>",
                formatDouble(data.getSleepHoursPerDay()),
                data.getCoffeeCupsPerDay(),
                data.getSocialMinutesPerDay(),
                formatDouble(data.getWorkHoursPerDay()),
                data.getWeekendDaysPerWeek()));

        indexLabel.setText(String.format("Индекс счастья: %.1f из 100", result.getIndex()));
        recommendationLabel.setText(
                "<html><center><b>Рекомендация:</b> " + result.getRecommendation() + "</center></html>");
        breakdownLabel.setText(String.format(
                "<html><center>Баллы: сон %.1f/30 • кофе %.1f/10 • общение %.1f/20 "
                        + "• работа %.1f/20 • выходные %.1f/20</center></html>",
                result.getSleepScore(), result.getCoffeeScore(), result.getSocialScore(),
                result.getWorkScore(), result.getWeekendScore()));
    }

    private static String formatDouble(double value) {
        if (value == Math.rint(value)) {
            return String.valueOf((long) value);
        }
        return String.valueOf(value);
    }
}
