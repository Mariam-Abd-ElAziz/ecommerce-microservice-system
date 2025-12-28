<%@ page contentType="text/html;charset=UTF-8" %>
<%@ page import="com.fasterxml.jackson.databind.JsonNode" %>

<html>
<head>
    <title>Customer Profile</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .label { font-weight: bold; }
    </style>
</head>
<body>

<h1>Customer Profile</h1>

<%
    String error = (String) request.getAttribute("error");
    JsonNode customer = (JsonNode) request.getAttribute("customer");
%>

<% if (error != null) { %>
<p style="color:red;"><%= error %></p>
<% } %>

<% if (customer != null) { %>
<p><span class="label">Customer ID:</span> <%= customer.get("customer_id").asText() %></p>
<p><span class="label">Name:</span> <%= customer.get("name").asText() %></p>
<p><span class="label">Email:</span> <%= customer.get("email").asText() %></p>
<p><span class="label">Phone:</span> <%= customer.get("phone").asText() %></p>
<p><span class="label">Loyalty Points:</span> <%= customer.get("loyalty_points").asText() %></p>
<% } %>

<br>
<a href="<%= request.getContextPath() %>/">⬅ Back to Home</a>

</body>
</html>
