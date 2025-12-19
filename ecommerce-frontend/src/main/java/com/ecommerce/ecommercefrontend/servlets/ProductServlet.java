package com.ecommerce.ecommercefrontend.servlets;

import com.ecommerce.ecommercefrontend.models.Product;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;

@WebServlet("/products")
public class ProductServlet extends HttpServlet {

    // to be adjusted based on actual Flask service location
    private static final String INVENTORY_SERVICE_URL = "http://localhost:5002/api/inventory";
    private final HttpClient httpClient = HttpClient.newHttpClient();
    private final ObjectMapper objectMapper = new ObjectMapper();


    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        try {
            // 1. Build request to Flask service
            HttpRequest inventoryFlaskRequest = HttpRequest.newBuilder()
                    .uri(URI.create(INVENTORY_SERVICE_URL))
                    .header("Accept", "application/json")
                    .GET()
                    .build();

            // 2. Call Flask service
            HttpResponse<String> inventoryFlaskResponse =
                    httpClient.send(inventoryFlaskRequest, HttpResponse.BodyHandlers.ofString());

            // 3. Parse JSON into a list of Product objects
            List<Product> products = objectMapper.readValue(
                    inventoryFlaskResponse.body(),
                    new TypeReference<List<Product>>() {}
            );

            // 4. Pass data to JSP
            request.setAttribute("products", products);

            // 5. Forward to JSP (hidden from direct access)
            request.getRequestDispatcher("/WEB-INF/index.jsp")
                   .forward(request, response);

        } catch (InterruptedException e) {
            // Thread.currentThread().interrupt();
            response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }
}
