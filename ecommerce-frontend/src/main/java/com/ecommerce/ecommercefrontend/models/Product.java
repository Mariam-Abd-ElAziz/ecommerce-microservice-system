package com.ecommerce.ecommercefrontend.models;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Product {
    
    @JsonProperty("product_name")
    private String product_name;

    @JsonProperty("unit_price")
    private double unit_price;


    public Product() {}

    public Product(String product_name, double unit_price) {
        this.product_name = product_name;
        this.unit_price = unit_price;
    }


    public String get_product_name() {
        return product_name;
    }

    public double get_unit_price() {
        return unit_price;
    }


    public void set_product_name(String product_name) {
        this.product_name = product_name;
    }

    public void set_unit_price(double unit_price) {
        this.unit_price = unit_price;
    }
}
