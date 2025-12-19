<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Order Confirmation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .box { border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
        pre { background:#f6f6f6; padding:10px; }
    </style>
    </head>
<body>
    <h1>Order Confirmation</h1>

    <div class="box">
        <h3>Order response (server)</h3>
        <%
            Object respObj = request.getAttribute("orderResponse");
            if (respObj != null) {
        %>
            <pre><%= respObj.toString() %></pre>
        <%
            } else {
        %>
            <p>No server-side order response found. If you navigated here directly, please view orders via the Order Service.</p>
        <%
            }
        %>
    </div>

</body>
</html>
