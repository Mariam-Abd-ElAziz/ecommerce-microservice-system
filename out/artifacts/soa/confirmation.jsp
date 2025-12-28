<%@ page contentType="text/html;charset=UTF-8" %>
<%@ page import="com.fasterxml.jackson.databind.JsonNode" %>

<html>
<head>
    <title>Order Confirmation</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 15px; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background: #f4f4f4; }
    </style>
</head>
<body>

<h1>✅ Order Confirmed</h1>

<%
    Integer orderId = (Integer) session.getAttribute("order_id");
    Double totalAmount = (Double) session.getAttribute("total_amount");
    String customerId = (String) session.getAttribute("customer_id");
    JsonNode items = (JsonNode) session.getAttribute("items");
%>

<p><strong>Order ID:</strong> <%= orderId %></p>
<p><strong>Customer ID:</strong> <%= customerId %></p>
<p><strong>Total Amount:</strong> <%= totalAmount %></p>

<h2>Order Items</h2>

<table>
    <tr>
        <th>Product ID</th>
        <th>Quantity</th>
        <th>Price</th>
    </tr>

    <%
        if(items != null && items.isArray()){
            for(JsonNode item : items){
    %>
    <tr>
        <td><%= item.get("product_id").asText() %></td>
        <td><%= item.get("quantity").asText() %></td>
        <td><%= item.has("total_price") ? item.get("total_price").asText() : "-" %></td>
    </tr>
    <%
        }
    } else {
    %>
    <tr><td colspan="3">No item details available</td></tr>
    <%
        }
    %>

</table>

<br>
<a href="<%= request.getContextPath() %>/">⬅ Back to Home</a>

</body>
</html>
