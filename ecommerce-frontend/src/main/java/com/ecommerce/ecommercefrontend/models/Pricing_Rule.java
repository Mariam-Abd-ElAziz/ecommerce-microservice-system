package com.ecommerce.ecommercefrontend.models;

public class Pricing_Rule {
    private final int min_quantity;
    private final float discount_percentage;


    public Pricing_Rule(int min_quantity, float discount_percentage) {
        this.min_quantity = min_quantity;
        this.discount_percentage = discount_percentage;
    }
}
