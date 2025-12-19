package com.ecommerce.ecommercefrontend.models;

public class Product {
    
    private final int product_id;
    private final String product_name;
    private final double unit_price;
    private final boolean is_available;
    private final Pricing_Rule[] pricing_rules;


    public Product(int product_id, String product_name, double unit_price, boolean is_available, Pricing_Rule[] pricing_rules) {
        this.product_id = product_id;
        this.product_name = product_name;
        this.unit_price = unit_price;
        this.is_available = is_available;
        this.pricing_rules = pricing_rules;
    }
}
