<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List" %>
<%@ page import="com.ecommerce.ecommercefrontend.models.Product" %>
<%@ page import="com.ecommerce.ecommercefrontend.models.Pricing_Rule" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Product Catalog</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .product { border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
        .product img { max-width: 150px; display: block; margin-bottom: 10px; }
        .product h2 { margin: 0 0 10px; font-size: 1.2em; }
        .product p { margin: 5px 0; }
        .product-price { font-weight: bold; color: green; }
    </style>
</head>
<body>
    <h1>Product Catalog</h1>

    <%
        // Retrieve the products list from request attributes
        List<Product> products = (List<Product>) request.getAttribute("products");
        if (products != null && !products.isEmpty()) {
            for (Product p : products) {
    %>
                <div class="product">
                    <h2><%= p.get_product_name() %></h2>
                    <p class="product-price">$<%= p.get_unit_price() %></p>
                    <p><%= p.get_is_available()? "available" : "not available" %></p>
                    <%
                        List<Pricing_Rule> pricingRules = p.get_pricing_rules();
                        if (pricingRules != null) {
                            for (Pricing_Rule rule : pricingRules) {
                    %>
                                <p>Pricing Rule: if you buy <%= rule.get_min_quantity() %> or more you will get a <%= rule.get_discount_percentage()%>% discount!</p>
                    <%
                            }
                        }
                    %>
                </div>
    <%
            }
        } else {
    %>
            <p>No products available at the moment.</p>
    <%
        }
    %>
</body>
</html>
