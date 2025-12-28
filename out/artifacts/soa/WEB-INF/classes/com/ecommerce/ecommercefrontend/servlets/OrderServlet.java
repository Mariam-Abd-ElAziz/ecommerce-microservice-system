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
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        // Show checkout page
        request.getRequestDispatcher("/WEB-INF/checkout.jsp")
                .forward(request, response);
    }

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
            HttpResponse<String> orderFlaskResponse =
                    httpClient.send(orderFlaskRequest, HttpResponse.BodyHandlers.ofString());

            int statusCode = orderFlaskResponse.statusCode();
            String responseBody = orderFlaskResponse.body();

            if (statusCode != 201) {
                // Parse JSON and show only the "message" field
                String userMessage = responseBody; // default
                try {
                    com.fasterxml.jackson.databind.ObjectMapper mapper = new com.fasterxml.jackson.databind.ObjectMapper();
                    com.fasterxml.jackson.databind.JsonNode jsonNode = mapper.readTree(responseBody);
                    if (jsonNode.has("message")) {
                        userMessage = jsonNode.get("message").asText();
                    } else if (jsonNode.has("error")) {
                        userMessage = jsonNode.get("error").asText();
                    }
                } catch (Exception ex) {
                    // if parsing fails, fallback to full response
                }

                request.setAttribute("error", userMessage);
                request.getRequestDispatcher("/WEB-INF/checkout.jsp").forward(request, response);
                return;
            }

            // Success: store order info in session and redirect to confirmation
            request.getSession().setAttribute("orderResponse", responseBody);
            response.sendRedirect("confirmation.jsp");
            request.getSession().setAttribute("statusCode", orderFlaskResponse.statusCode());

        } catch (InterruptedException e) {
            request.setAttribute("error", "Internal server error: " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/checkout.jsp").forward(request, response);
            Thread.currentThread().interrupt();
        }
    }
}