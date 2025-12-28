<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="com.fasterxml.jackson.databind.JsonNode" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Review Order</title>
</head>
<body>
<h1>Review Your Order</h1>

<% if(request.getAttribute("error") != null){ %>
<div style="color:red;"><%= request.getAttribute("error") %></div>
<% } %>

<table border="1" cellpadding="6">
    <thead>
    <tr>
        <th>Product ID</th>
        <th>Quantity</th>
        <th>Price</th>
    </tr>
    </thead>
    <tbody>
    <%
        JsonNode items = (JsonNode) request.getAttribute("items");
        for(JsonNode item : items){
    %>
    <tr>
        <td><%= item.get("product_id").asText() %></td>
        <td><%= item.get("quantity").asText() %></td>
        <td><%= item.get("unit_price").asText() %></td>
    </tr>
    <% } %>
    </tbody>
</table>

<p>Total Amount: <strong><%= request.getAttribute("total_amount") %> EGP</strong></p>

<form method="post" action="${pageContext.request.contextPath}/submitOrder">
    <input type="hidden" name="customer_id" value="<%= request.getAttribute("customer_id") %>" />
    <%
        String[] productIds = (String[]) request.getAttribute("productIds");
        String[] quantities = (String[]) request.getAttribute("quantities");
        for(int i=0;i<productIds.length;i++){
            if(productIds[i] != null && !productIds[i].trim().isEmpty()){
    %>
    <input type="hidden" name="product_id" value="<%= productIds[i] %>" />
    <input type="hidden" name="quantity" value="<%= quantities[i] %>" />
    <%
            }
        }
    %>
    <button type="submit">Proceed</button>
    <a href="${pageContext.request.contextPath}/index.jsp"><button type="button">Cancel</button></a>
</form>
</body>
</html>
