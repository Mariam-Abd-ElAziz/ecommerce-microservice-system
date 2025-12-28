<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List" %>
<%@ page import="com.ecommerce.ecommercefrontend.models.Product" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Product Catalog</title>

    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }

        .top-links {
            margin-bottom: 20px;
        }

        .top-links a {
            margin-right: 15px;
            padding: 10px 18px;
            background: #4a6cf7;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
        }

        .top-links a:hover {
            background: #354ed8;
        }

        .product {
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
        }

        .product h2 {
            margin: 0 0 10px;
            font-size: 1.2em;
        }

        .product-price {
            font-weight: bold;
            color: green;
        }
    </style>
</head>

<body>

<h1>Product Catalog</h1>

<!-- REQUIRED LINKS -->
<div class="top-links">
    <a href="${pageContext.request.contextPath}/customerProfile?customer_id=1">
        View Profile
    </a>

    <a href="${pageContext.request.contextPath}/ordersHistory?customer_id=2">
        View Orders History
    </a>

</div>

<!-- FORM STARTS SCENARIO-1 -->
<form action="${pageContext.request.contextPath}/checkout.jsp" method="post">

    <%
        List<Product> products = (List<Product>) request.getAttribute("products");

        if (products != null && !products.isEmpty()) {
            for (Product p : products) {
    %>
    <div class="product">
        <h2><%= p.get_product_name() %></h2>
        <p class="product-price">$<%= p.get_unit_price() %></p>
        <p>Available: <%= p.getQuantity() %></p>

        <!-- IMPORTANT: required for checkout -->
        <input type="hidden" name="product_id" value="<%= p.getProductId() %>" />

    </div>
    <%
        }
    } else {
    %>
    <p>No products available at the moment.</p>
    <%
        }
    %>

    <br>
    <button type="submit">Make Order</button>
</form>

</body>
</html>
