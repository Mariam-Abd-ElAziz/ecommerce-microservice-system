<%@ page contentType="text/html;charset=UTF-8" %>
<%@ page import="com.fasterxml.jackson.databind.JsonNode" %>

<html>
<head>
    <title>Orders History</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 15px; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background: #f2f2f2; }
    </style>
</head>
<body>

<h1>📦 Orders History</h1>

<%
    String error = (String) request.getAttribute("error");
    JsonNode orders = (JsonNode) request.getAttribute("orders");
%>

<% if (error != null) { %>
<p style="color:red;"><%= error %></p>
<% } %>

<% if (orders != null && orders.isArray() && orders.size() > 0) { %>
<table>
    <tr>
        <th>Order ID</th>
        <th>Total Amount</th>
        <th>Products</th>
    </tr>

    <%
        for (JsonNode orderWrapper : orders) {
            JsonNode order = orderWrapper.get("order");
            JsonNode products = orderWrapper.get("products");
    %>
    <tr>
        <td><%= order.get("order_id").asText() %></td>
        <td><%= order.get("total_amount").asText() %></td>
        <td>
            <ul>
                <%
                    for (JsonNode product : products) {
                %>
                <li>
                    Product ID: <%= product.get("product_id").asText() %>,
                    Qty: <%= product.get("quantity").asText() %>
                </li>
                <%
                    }
                %>
            </ul>
        </td>
    </tr>
    <%
        }
    %>
</table>

<% } else if (error == null) { %>
<p>No previous orders found.</p>
<% } %>

<br>
<a href="<%= request.getContextPath() %>/">⬅ Back to Home</a>

</body>
</html>
