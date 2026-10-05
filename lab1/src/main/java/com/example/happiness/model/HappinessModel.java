package com.example.happiness.model;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;

public class HappinessModel {

    public static final String PROP_DATA = "data";
    public static final String PROP_RESULT = "result";
    public static final double MAX_SLEEP_SCORE = 30.0;
    public static final double SLEEP_ZERO_HOURS = 6.0;
    public static final double SLEEP_FULL_HOURS = 8.0;
    public static final double MAX_COFFEE_SCORE = 10.0;
    public static final int COFFEE_OPTIMAL_MIN = 1;
    public static final int COFFEE_OPTIMAL_MAX = 2;
    public static final int COFFEE_ZERO_CUPS = 5;
    public static final double COFFEE_NO_CUP_RATIO = 0.5;

    public static final double MAX_SOCIAL_SCORE = 20.0;
    public static final double ENOUGH_SOCIAL_MINUTES = 120.0;

    public static final double MAX_WORK_SCORE = 20.0;
    public static final double NORMAL_WORK_HOURS = 8.0;
    public static final double HARD_WORK_HOURS = 12.0;
    public static final double IDLE_WORK_RATIO = 0.7;
    public static final double IDLE_WORK_HOURS = 2.0;

    public static final double MAX_WEEKEND_SCORE = 20.0;
    public static final double ENOUGH_WEEKEND_DAYS = 3.0;
    public static final double ONE_WEEKEND_RATIO = 0.5;
    public static final double TWO_WEEKEND_RATIO = 0.75;

    public static final double SLEEP_DEBT_THRESHOLD = 6.0;
    public static final double OVERWORK_THRESHOLD = 10.0;
    public static final int COFFEE_OVERDOSE_THRESHOLD = 3;

    private final PropertyChangeSupport support = new PropertyChangeSupport(this);

    private HappinessData data;
    private HappinessResult result;

    public static HappinessData defaultData() {
        return new HappinessData(8, 2, 60, 8, 2);
    }

    public void addPropertyChangeListener(PropertyChangeListener listener) {
        support.addPropertyChangeListener(listener);
    }

    public void addPropertyChangeListener(String propertyName, PropertyChangeListener listener) {
        support.addPropertyChangeListener(propertyName, listener);
    }

    public void removePropertyChangeListener(PropertyChangeListener listener) {
        support.removePropertyChangeListener(listener);
    }


    public synchronized void setData(HappinessData newData) {
        if (newData == null) {
            throw new IllegalArgumentException("Данные не заданы.");
        }
        newData.validate();

        HappinessData oldData = this.data;
        HappinessResult oldResult = this.result;

        this.data = newData;
        this.result = calculate(newData);

        support.firePropertyChange(PROP_DATA, oldData, this.data);
        support.firePropertyChange(PROP_RESULT, oldResult, this.result);
    }

    public synchronized HappinessData getData() {
        return data;
    }

    public synchronized HappinessResult getResult() {
        return result;
    }

    public synchronized boolean hasData() {
        return data != null;
    }


    public static HappinessResult calculate(HappinessData d) {
        double sleepScore = sleepScore(d.getSleepHoursPerDay());
        double coffeeScore = coffeeScore(d.getCoffeeCupsPerDay());
        double socialScore = socialScore(d.getSocialMinutesPerDay());
        double workScore = workScore(d.getWorkHoursPerDay());
        double weekendScore = weekendScore(d.getWeekendDaysPerWeek());

        double index = round1(sleepScore + coffeeScore + socialScore + workScore + weekendScore);
        String recommendation = recommend(index, d);
        return new HappinessResult(index, recommendation,
                round1(sleepScore), round1(coffeeScore), round1(socialScore),
                round1(workScore), round1(weekendScore));
    }

    public static double sleepScore(double hoursPerDay) {
        if (hoursPerDay >= SLEEP_FULL_HOURS) {
            return MAX_SLEEP_SCORE;
        }
        if (hoursPerDay <= SLEEP_ZERO_HOURS) {
            return 0.0;
        }
        double ratio = (hoursPerDay - SLEEP_ZERO_HOURS) / (SLEEP_FULL_HOURS - SLEEP_ZERO_HOURS);
        return MAX_SLEEP_SCORE * Math.max(0.0, ratio);
    }

    public static double coffeeScore(int cupsPerDay) {
        if (cupsPerDay < COFFEE_OPTIMAL_MIN) {
            return MAX_COFFEE_SCORE * COFFEE_NO_CUP_RATIO;
        }
        if (cupsPerDay <= COFFEE_OPTIMAL_MAX) {
            return MAX_COFFEE_SCORE;
        }
        if (cupsPerDay >= COFFEE_ZERO_CUPS) {
            return 0.0;
        }
        double ratio = (COFFEE_ZERO_CUPS - cupsPerDay) / (double) (COFFEE_ZERO_CUPS - COFFEE_OPTIMAL_MAX);
        return MAX_COFFEE_SCORE * Math.max(0.0, ratio);
    }

    public static double socialScore(double minutesPerDay) {
        return MAX_SOCIAL_SCORE * Math.min(1.0, minutesPerDay / ENOUGH_SOCIAL_MINUTES);
    }

    public static double workScore(double hoursPerDay) {
        if (hoursPerDay > HARD_WORK_HOURS) {
            return 0.0;
        }
        if (hoursPerDay <= NORMAL_WORK_HOURS) {
            if (hoursPerDay < IDLE_WORK_HOURS) {
                return MAX_WORK_SCORE * IDLE_WORK_RATIO;
            }
            return MAX_WORK_SCORE;
        }
        double left = 1.0 - (hoursPerDay - NORMAL_WORK_HOURS) / (HARD_WORK_HOURS - NORMAL_WORK_HOURS);
        return MAX_WORK_SCORE * Math.max(0.0, left);
    }

    public static double weekendScore(double daysPerWeek) {
        if (daysPerWeek >= ENOUGH_WEEKEND_DAYS) {
            return MAX_WEEKEND_SCORE;
        }
        if (daysPerWeek >= 2.0) {
            return MAX_WEEKEND_SCORE * TWO_WEEKEND_RATIO;
        }
        if (daysPerWeek >= 1.0) {
            return MAX_WEEKEND_SCORE * ONE_WEEKEND_RATIO;
        }
        return 0.0;
    }


    public static String recommend(double index, HappinessData d) {
        double sleep = d.getSleepHoursPerDay();
        double work = d.getWorkHoursPerDay();

        if (sleep < SLEEP_DEBT_THRESHOLD) {
            return String.format(
                    "Поспать! Вы спите %.1f ч в сутки — это меньше нормы (6–8 часов). "
                            + "Недосып — главный враг счастья.", sleep);
        }
        if (work > OVERWORK_THRESHOLD) {
            return String.format(
                    "Уволиться! %.1f ч работы в сутки — это переработка (предел 12 часов, "
                            + "а лучше не больше 8). Возьмите отпуск или смените работу.", work);
        }
        if (d.getWeekendDaysPerWeek() < 1) {
            return "Купить пиццу — и договориться хотя бы об одном выходном! "
                    + "Работать семь дней в неделю нельзя.";
        }
        if (d.getCoffeeCupsPerDay() > COFFEE_OVERDOSE_THRESHOLD) {
            return String.format(
                    "Купить пиццу и заменить часть кофе водой: %d чашек в день — перебор "
                            + "(норма 1–2).", d.getCoffeeCupsPerDay());
        }
        if (index >= 70) {
            return "Купить пиццу и наслаждаться жизнью! У вас отличный баланс.";
        }
        if (index >= 40) {
            return "Купить пиццу — всё неплохо, а с пиццей станет ещё лучше!";
        }
        return "Купить пиццу! И срочно себя порадовать: больше сна, отдыха и приятного общения.";
    }

    private static double round1(double value) {
        return Math.round(value * 10.0) / 10.0;
    }
}
