package com.ecommerce.ecommercefrontend.models;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Product {
    @JsonProperty("product_id")
    private int productId;

    @JsonProperty("product_name")
    private String product_name;

    @JsonProperty("unit_price")
    private double unit_price;

    @JsonProperty("quantity_available")
    private int quantity_available;


    public Product() {}

    public Product(String product_name, double unit_price, int quantity_available) {
        this.product_name = product_name;
        this.unit_price = unit_price;
        this.quantity_available = quantity_available;
    }

    public int getProductId() {
        return productId;
    }

    public String get_product_name() {
        return product_name;
    }

    public double get_unit_price() {
        return unit_price;
    }

    public int getQuantity() {
        return quantity_available;
    }
    public void setProductId(int productId) {
        this.productId = productId;
    }

    public void set_product_name(String product_name) {
        this.product_name = product_name;
    }

    public void set_unit_price(double unit_price) {
        this.unit_price = unit_price;
    }

    public void setQuantity(int quantity) {
        this.quantity_available = quantity;
    }
}
