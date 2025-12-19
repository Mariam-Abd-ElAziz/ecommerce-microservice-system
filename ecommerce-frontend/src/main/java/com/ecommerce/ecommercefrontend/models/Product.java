package com.ecommerce.ecommercefrontend.models;

import java.util.List;

public class Product {
    
    private final int product_id;
    private final String product_name;
    private final double unit_price;
    private final boolean is_available;
    private final List<Pricing_Rule> pricing_rules;


    public Product(int product_id, String product_name, double unit_price, boolean is_available, List<Pricing_Rule> pricing_rules) {
        this.product_id = product_id;
        this.product_name = product_name;
        this.unit_price = unit_price;
        this.is_available = is_available;
        this.pricing_rules = pricing_rules;
    }


    public int get_product_id() {
        return product_id;
    }

    public String get_product_name() {
        return product_name;
    }

    public double get_unit_price() {
        return unit_price;
    }

    public boolean get_is_available() {
        return is_available;
    }

    public List<Pricing_Rule> get_pricing_rules() {
        return pricing_rules;
    }

}
