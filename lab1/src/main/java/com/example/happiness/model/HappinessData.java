package com.example.happiness.model;

import java.io.Serializable;
import java.util.Objects;

public final class HappinessData implements Serializable {

    private static final long serialVersionUID = 2L;

    public static final double MAX_HOURS_PER_DAY = 24.0;
    public static final int MAX_MINUTES_PER_DAY = 1440; // 24 * 60

    public static final double MIN_SLEEP_HOURS = 0.0;
    public static final double MAX_SLEEP_HOURS = 24.0;
    public static final int MIN_COFFEE_CUPS = 0;
    public static final int MAX_COFFEE_CUPS = 20;
    public static final int MIN_SOCIAL_MINUTES = 0;
    public static final int MAX_SOCIAL_MINUTES = MAX_MINUTES_PER_DAY;
    public static final double MIN_WORK_HOURS = 0.0;
    public static final double MAX_WORK_HOURS = 24.0;
    public static final int MIN_WEEKEND_DAYS = 0;
    public static final int MAX_WEEKEND_DAYS = 7;

    private final double sleepHoursPerDay;
    private final int coffeeCupsPerDay;
    private final int socialMinutesPerDay;
    private final double workHoursPerDay;
    private final int weekendDaysPerWeek;

    public HappinessData(double sleepHoursPerDay,
                         int coffeeCupsPerDay,
                         int socialMinutesPerDay,
                         double workHoursPerDay,
                         int weekendDaysPerWeek) {
        this.sleepHoursPerDay = sleepHoursPerDay;
        this.coffeeCupsPerDay = coffeeCupsPerDay;
        this.socialMinutesPerDay = socialMinutesPerDay;
        this.workHoursPerDay = workHoursPerDay;
        this.weekendDaysPerWeek = weekendDaysPerWeek;
        validate();
    }

    public double getSleepHoursPerDay() {
        return sleepHoursPerDay;
    }

    public int getCoffeeCupsPerDay() {
        return coffeeCupsPerDay;
    }

    public int getSocialMinutesPerDay() {
        return socialMinutesPerDay;
    }

    public double getWorkHoursPerDay() {
        return workHoursPerDay;
    }

    public int getWeekendDaysPerWeek() {
        return weekendDaysPerWeek;
    }

    public double getBusyHoursPerDay() {
        return sleepHoursPerDay + workHoursPerDay + socialMinutesPerDay / 60.0;
    }

    public void validate() {
        if (!isFinite(sleepHoursPerDay)
                || sleepHoursPerDay < MIN_SLEEP_HOURS
                || sleepHoursPerDay > MAX_SLEEP_HOURS) {
            throw new IllegalArgumentException(
                    "Некорректный сон: введите число от 0 до 24 часов в сутки.");
        }
        if (coffeeCupsPerDay < MIN_COFFEE_CUPS || coffeeCupsPerDay > MAX_COFFEE_CUPS) {
            throw new IllegalArgumentException(
                    "Некорректное кофе: введите целое число от 0 до 20 чашек в сутки.");
        }
        if (socialMinutesPerDay < MIN_SOCIAL_MINUTES || socialMinutesPerDay > MAX_SOCIAL_MINUTES) {
            throw new IllegalArgumentException(
                    "Некорректное общение: введите целое число от 0 до 1440 минут в сутки.");
        }
        if (!isFinite(workHoursPerDay)
                || workHoursPerDay < MIN_WORK_HOURS
                || workHoursPerDay > MAX_WORK_HOURS) {
            throw new IllegalArgumentException(
                    "Некорректная работа: введите число от 0 до 24 часов в сутки.");
        }
        if (weekendDaysPerWeek < MIN_WEEKEND_DAYS || weekendDaysPerWeek > MAX_WEEKEND_DAYS) {
            throw new IllegalArgumentException(
                    "Некорректные выходные: введите целое число от 0 до 7 дней в неделю.");
        }
        checkDayFits(sleepHoursPerDay, workHoursPerDay, socialMinutesPerDay);
    }

    public static void checkDayFits(double sleepHoursPerDay,
                                    double workHoursPerDay,
                                    int socialMinutesPerDay) {
        double busy = sleepHoursPerDay + workHoursPerDay + socialMinutesPerDay / 60.0;
        if (busy > MAX_HOURS_PER_DAY + 0.005) {
            throw new IllegalArgumentException(String.format(
                    "В сутках всего 24 часа, а у вас получилось %.1f ч: сон %.1f ч + работа %.1f ч"
                            + " + общение %d мин (%.1f ч). Уменьшите одно из значений.",
                    busy, sleepHoursPerDay, workHoursPerDay,
                    socialMinutesPerDay, socialMinutesPerDay / 60.0));
        }
    }

    private static boolean isFinite(double value) {
        return !Double.isNaN(value) && !Double.isInfinite(value);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof HappinessData)) {
            return false;
        }
        HappinessData that = (HappinessData) o;
        return Double.compare(that.sleepHoursPerDay, sleepHoursPerDay) == 0
                && coffeeCupsPerDay == that.coffeeCupsPerDay
                && socialMinutesPerDay == that.socialMinutesPerDay
                && Double.compare(that.workHoursPerDay, workHoursPerDay) == 0
                && weekendDaysPerWeek == that.weekendDaysPerWeek;
    }

    @Override
    public int hashCode() {
        return Objects.hash(sleepHoursPerDay, coffeeCupsPerDay,
                socialMinutesPerDay, workHoursPerDay, weekendDaysPerWeek);
    }

    @Override
    public String toString() {
        return "HappinessData{"
                + "сон=" + sleepHoursPerDay + " ч/день"
                + ", кофе=" + coffeeCupsPerDay + " чашек/день"
                + ", общение=" + socialMinutesPerDay + " мин/день"
                + ", работа=" + workHoursPerDay + " ч/день"
                + ", выходные=" + weekendDaysPerWeek + " дн/нед"
                + '}';
    }
}
