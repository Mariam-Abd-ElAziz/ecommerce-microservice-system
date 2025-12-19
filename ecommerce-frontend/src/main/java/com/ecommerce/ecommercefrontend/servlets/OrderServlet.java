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
        String productId = request.getParameter("product_id");
        String quantity = request.getParameter("quantity");

        // Build JSON payload
        String jsonPayload = String.format( "{\"customer_id\":%s,\"products\":[{\"product_id\":%s,\"quantity\":%s}]}", customerId, productId, quantity );
        
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
            
            // Forward to confirmation page
            request.setAttribute("orderResponse", orderFlaskResponse.body());
            request.getRequestDispatcher("confirmation.jsp").forward(request, response);
        
        } catch (InterruptedException e) {
            response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }
}