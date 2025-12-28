package com.ecommerce.ecommercefrontend.servlets;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/checkout")
public class CheckoutServlet extends HttpServlet {

    private final HttpClient client = HttpClient.newHttpClient();
    private final ObjectMapper mapper = new ObjectMapper();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        /* ----------------------------------------------------
           1️⃣ Read selected products from request
        ---------------------------------------------------- */
        Map<Integer, Integer> selectedProducts = new HashMap<>();

        request.getParameterMap().forEach((key, value) -> {
            if (key.startsWith("quantity_")) {
                int productId = Integer.parseInt(key.split("_")[1]);
                int qty = Integer.parseInt(value[0]);
                if (qty > 0) {
                    selectedProducts.put(productId, qty);
                }
            }
        });

        if (selectedProducts.isEmpty()) {
            request.setAttribute("error", "No products selected");
            request.getRequestDispatcher("/WEB-INF/index.jsp").forward(request, response);
            return;
        }

        /* ----------------------------------------------------
           2️⃣ Check stock using Inventory Service
        ---------------------------------------------------- */
        for (Map.Entry<Integer, Integer> entry : selectedProducts.entrySet()) {
            int productId = entry.getKey();
            int requestedQty = entry.getValue();

            HttpRequest inventoryReq = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5002/api/inventory/check/" + productId))
                    .GET()
                    .build();

            HttpResponse<String> inventoryRes;
            try {
                inventoryRes = client.send(
                        inventoryReq,
                        HttpResponse.BodyHandlers.ofString()
                );
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt(); // VERY IMPORTANT
                throw new ServletException("Inventory service interrupted", e);
            }

            JsonNode inventoryJson = mapper.readTree(inventoryRes.body());
            int availableQty = inventoryJson.get("available_quantity").asInt();

            if (requestedQty > availableQty) {
                request.setAttribute(
                        "error",
                        "Not enough stock for product ID " + productId
                );
                request.getRequestDispatcher("/WEB-INF/index.jsp")
                        .forward(request, response);
                return;
            }
        }

        /* ----------------------------------------------------
           3️⃣ Call Pricing Service to calculate total
        ---------------------------------------------------- */
        String pricingPayload = buildPricingPayload(selectedProducts);

        HttpRequest pricingReq = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5003/api/pricing/calculate"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(pricingPayload))
                .build();

        HttpResponse<String> pricingRes;
        try {
            pricingRes = client.send(
                    pricingReq,
                    HttpResponse.BodyHandlers.ofString()
            );
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new ServletException("Pricing service interrupted", e);
        }

        JsonNode pricingJson = mapper.readTree(pricingRes.body());
        double totalAmount = pricingJson.get("total_price").asDouble();

        /* ----------------------------------------------------
           4️⃣ Forward to checkout.jsp
        ---------------------------------------------------- */
        request.setAttribute("selectedProducts", selectedProducts);
        request.setAttribute("totalAmount", totalAmount);

        request.getRequestDispatcher("/WEB-INF/checkout.jsp")
                .forward(request, response);
    }

    /* ----------------------------------------------------
       Helper method: build pricing JSON
    ---------------------------------------------------- */
    private String buildPricingPayload(Map<Integer, Integer> products) {
        StringBuilder sb = new StringBuilder();
        sb.append("{\"items\":[");

        boolean first = true;
        for (Map.Entry<Integer, Integer> entry : products.entrySet()) {
            if (!first) sb.append(",");
            sb.append(String.format(
                    "{\"product_id\":%d,\"quantity\":%d}",
                    entry.getKey(),
                    entry.getValue()
            ));
            first = false;
        }

        sb.append("]}");
        return sb.toString();
    }
}
