<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List" %>
<%@ page import="com.ecommerce.ecommercefrontend.models.Product" %>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Checkout</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .form-row { margin-bottom: 10px; }
            label { display: block; margin-bottom: 4px; }
            input[type="text"], select { width: 300px; padding: 6px; }
            table { border-collapse: collapse; width: 100%; margin-top: 15px; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background: #f7f7f7; }
            .actions { margin-top: 12px; }
        </style>
    </head>
    <body>
        <h1>Checkout</h1>

        <!-- Must write this "${pageContext.request.contextPath}" part in order for the form to redirect correctly when deployed under a .war file -->
        <form id="orderForm" method="post" action="${pageContext.request.contextPath}/submitOrder">
            <div class="form-row">
                <label for="customer_id">Customer ID</label>
                <input type="text" id="customer_id" name="customer_id" required />
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
                    <tr>
                        <td><input type="number" name="product_id" min="1" required /></td>
                        <td><input type="number" name="quantity" min="1" value="1" required /></td>
                    </tr>
                    <tr>
                        <td><input type="number" name="product_id" min="1" /></td>
                        <td><input type="number" name="quantity" min="1" /></td>
                    </tr>
                    <tr>
                        <td><input type="number" name="product_id" min="1" /></td>
                        <td><input type="number" name="quantity" min="1" /></td>
                    </tr>
                    <tr>
                        <td><input type="number" name="product_id" min="1" /></td>
                        <td><input type="number" name="quantity" min="1" /></td>
                    </tr>
                    <tr>
                        <td><input type="number" name="product_id" min="1" /></td>
                        <td><input type="number" name="quantity" min="1" /></td>
                    </tr>
                </tbody>
            </table>

            <div class="actions">
                <button type="submit">Place Order</button>
            </div>
        </form>

    </body>
</html>
