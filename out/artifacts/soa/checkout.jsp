<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Checkout</title>
    <% if(request.getAttribute("error") != null) { %>
    <div style="color: white; background-color: #ff4d4d; padding: 10px; margin-bottom: 20px; border-radius: 5px;">
        <strong>Error:</strong> <%= request.getAttribute("error") %>
    </div>
    <% } %>
    <%-- END OF BLOCK --%>

    <form method="post" action="${pageContext.request.contextPath}/reviewOrder">
    <style>
        body { font-family: Arial; margin: 20px; }
        .form-row { margin-bottom: 10px; }
        label { display:block; margin-bottom:4px; }
        input { padding:6px; width:300px; }
        table { border-collapse: collapse; width:100%; margin-top:15px; }
        th, td { border:1px solid #ddd; padding:8px; }
        th { background:#f7f7f7; }
    </style>
</head>
<body>
<h1>Checkout</h1>

<form method="post" action="${pageContext.request.contextPath}/reviewOrder">
    <div class="form-row">
        <label for="customer_id">Customer ID</label>
        <input type="text" id="customer_id" name="customer_id" required/>
    </div>

    <h2>Products (up to 5)</h2>
    <table>
        <thead>
        <tr>
            <th>Product ID</th>
            <th>Quantity</th>
        </tr>
        </thead>
        <tbody>
        <%-- 5 rows for products --%>
        <% for(int i=0;i<5;i++){ %>
        <tr>
            <td><input type="number" name="product_id" min="1" <% if(i==0){%>required<%}%> /></td>
            <td><input type="number" name="quantity" min="1" <% if(i==0){%>required<%}%> /></td>
        </tr>
        <% } %>
        </tbody>
    </table>

    <div style="margin-top:15px;">
        <button type="submit">Review Order</button>
    </div>
</form>
</body>
</html>
