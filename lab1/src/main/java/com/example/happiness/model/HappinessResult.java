package com.example.happiness.model;

import java.io.Serializable;

public final class HappinessResult implements Serializable {

    private static final long serialVersionUID = 2L;

    private final double index;          // 0..100, округлён до 1 знака
    private final String recommendation;
    private final double sleepScore;
    private final double coffeeScore;
    private final double socialScore;
    private final double workScore;
    private final double weekendScore;

    public HappinessResult(double index, String recommendation,
                           double sleepScore, double coffeeScore,
                           double socialScore, double workScore,
                           double weekendScore) {
        this.index = index;
        this.recommendation = recommendation;
        this.sleepScore = sleepScore;
        this.coffeeScore = coffeeScore;
        this.socialScore = socialScore;
        this.workScore = workScore;
        this.weekendScore = weekendScore;
    }

    public double getIndex() {
        return index;
    }

    public String getRecommendation() {
        return recommendation;
    }

    public double getSleepScore() {
        return sleepScore;
    }

    public double getCoffeeScore() {
        return coffeeScore;
    }

    public double getSocialScore() {
        return socialScore;
    }

    public double getWorkScore() {
        return workScore;
    }

    public double getWeekendScore() {
        return weekendScore;
    }

    @Override
    public String toString() {
        return "HappinessResult{"
                + "индекс=" + index
                + ", рекомендация='" + recommendation + '\''
                + '}';
    }
}
