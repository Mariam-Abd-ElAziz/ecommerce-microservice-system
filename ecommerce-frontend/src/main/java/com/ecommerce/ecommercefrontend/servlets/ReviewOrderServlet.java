package com.ecommerce.ecommercefrontend.servlets;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/reviewOrder")
public class ReviewOrderServlet extends HttpServlet {

    private static final String REVIEW_API_URL = "http://localhost:5001/api/orders/review";
    private final HttpClient httpClient = HttpClient.newHttpClient();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

        String customerId = request.getParameter("customer_id");
        String[] productIds = request.getParameterValues("product_id");
        String[] quantities = request.getParameterValues("quantity");

        if(customerId == null || productIds==null || quantities==null){
            request.setAttribute("error", "Missing required fields.");
            request.getRequestDispatcher("/checkout.jsp").forward(request, response);
            return;
        }

        // Build products JSON
        List<String> productsList = new ArrayList<>();
        int len = Math.min(productIds.length, quantities.length);
        for(int i=0;i<len;i++){
            String pid = productIds[i];
            String qty = quantities[i];
            if(pid==null || pid.trim().isEmpty()) continue;
            if(qty==null || qty.trim().isEmpty()) continue;
            productsList.add(String.format("{\"product_id\":%s,\"quantity\":%s}", pid.trim(), qty.trim()));
        }

        if(productsList.isEmpty()){
            request.setAttribute("error", "At least one product required.");
            request.getRequestDispatcher("/checkout.jsp").forward(request, response);
            return;
        }

        String jsonPayload = String.format("{\"customer_id\":%s,\"products\":[%s]}", customerId, String.join(",", productsList));

        try{
            HttpRequest req = HttpRequest.newBuilder()
                    .uri(URI.create(REVIEW_API_URL))
                    .header("Content-Type","application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                    .build();

            HttpResponse<String> apiRes = httpClient.send(req, HttpResponse.BodyHandlers.ofString());

            if (apiRes.statusCode() != 200) {
                String errorMessage = "An unknown error occurred.";
                try {
                    com.fasterxml.jackson.databind.ObjectMapper mapper = new com.fasterxml.jackson.databind.ObjectMapper();
                    com.fasterxml.jackson.databind.JsonNode errorNode = mapper.readTree(apiRes.body());

                    // Extract the most helpful message
                    if (errorNode.has("message")) {
                        errorMessage = errorNode.get("message").asText();
                    } else if (errorNode.has("error")) {
                        errorMessage = errorNode.get("error").asText();
                    }
                } catch (Exception e) {
                    errorMessage = apiRes.body(); // Fallback to raw body
                }

                request.setAttribute("error", errorMessage);
                // Ensure this path matches where your checkout.jsp actually is
                request.getRequestDispatcher("/checkout.jsp").forward(request, response);
                return;
            }

            // Parse response JSON
            com.fasterxml.jackson.databind.ObjectMapper mapper = new com.fasterxml.jackson.databind.ObjectMapper();
            com.fasterxml.jackson.databind.JsonNode rootNode = mapper.readTree(apiRes.body());

            request.setAttribute("items", rootNode.get("items"));
            request.setAttribute("total_amount", rootNode.get("total_amount"));
            request.setAttribute("customer_id", customerId);

            // Also pass productIds & quantities to hidden inputs for final submission
            request.setAttribute("productIds", productIds);
            request.setAttribute("quantities", quantities);

            request.getRequestDispatcher("/review.jsp").forward(request, response);

        }catch(Exception e){
            request.setAttribute("error", "Failed to review order: "+e.getMessage());
            request.getRequestDispatcher("/checkout.jsp").forward(request, response);
        }
    }
}
