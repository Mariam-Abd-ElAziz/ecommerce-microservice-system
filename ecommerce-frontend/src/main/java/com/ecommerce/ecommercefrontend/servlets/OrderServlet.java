package com.ecommerce.ecommercefrontend.servlets;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/submitOrder")
public class OrderServlet extends HttpServlet {
    
    // to be adjusted based on actual Flask service location
    private static final String ORDER_SERVICE_URL = "http://localhost:5001/api/orders/create";
    private final HttpClient httpClient = HttpClient.newHttpClient();

    
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {

        // Get form parameters
        String customerId = request.getParameter("customer_id");
        String[] productIds = request.getParameterValues("product_id");
        String[] quantities = request.getParameterValues("quantity");

        if (customerId == null || productIds == null || quantities == null) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "Missing required fields");
            return;
        }

        // Build products array from parallel parameter arrays; ignore empty rows
        StringBuilder productsJson = new StringBuilder();
        productsJson.append("[");
        boolean first = true;
        int len = Math.min(productIds.length, quantities.length);
        for (int i = 0; i < len; i++) {
            String pid = productIds[i];
            String qty = quantities[i];
            if (pid == null || pid.trim().isEmpty()) continue;
            if (qty == null || qty.trim().isEmpty()) continue;
            if (!first) productsJson.append(",");
            productsJson.append(String.format("{\"product_id\":%s,\"quantity\":%s}", pid.trim(), qty.trim()));
            first = false;
        }
        productsJson.append("]");

        String jsonPayload = String.format("{\"customer_id\":%s,\"products\":%s}", customerId, productsJson.toString());
        
        // Build request to Flask service
        HttpRequest orderFlaskRequest = HttpRequest.newBuilder()
                                    .uri(URI.create(ORDER_SERVICE_URL))
                                    .header("Content-Type", "application/json")
                                    .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                                    .build();
        
        try {
            // Call Flask service
            HttpResponse<String> orderFlaskResponse =
            httpClient.send(orderFlaskRequest, HttpResponse.BodyHandlers.ofString());
            
            // Forward to confirmation page with server-side order response
            request.setAttribute("orderResponse", orderFlaskResponse.body());
            request.getRequestDispatcher("confirmation.jsp").forward(request, response);
        
        } catch (InterruptedException e) {
            response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }
}