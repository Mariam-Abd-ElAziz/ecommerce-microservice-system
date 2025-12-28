package com.ecommerce.ecommercefrontend.servlets;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/ordersHistory")
public class ViewOrdersHistoryServlet extends HttpServlet {

    private static final String CUSTOMER_SERVICE_URL =
            "http://localhost:5004/api/customers/";

    private final HttpClient httpClient = HttpClient.newHttpClient();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String customerId = request.getParameter("customer_id");

        if (customerId == null || customerId.isBlank()) {
            request.setAttribute("error", "Customer ID is required");
            request.getRequestDispatcher("/view_orders_history.jsp")
                    .forward(request, response);
            return;
        }

        try {
            // Call Customer Service
            HttpRequest apiRequest = HttpRequest.newBuilder()
                    .uri(URI.create(CUSTOMER_SERVICE_URL + customerId + "/orders"))
                    .GET()
                    .build();

            HttpResponse<String> apiResponse =
                    httpClient.send(apiRequest, HttpResponse.BodyHandlers.ofString());

            if (apiResponse.statusCode() != 200) {
                request.setAttribute("error", "Failed to load order history");
                request.getRequestDispatcher("/view_orders_history.jsp")
                        .forward(request, response);
                return;
            }

            ObjectMapper mapper = new ObjectMapper();
            JsonNode ordersJson = mapper.readTree(apiResponse.body());

            // Pass data to JSP
            request.setAttribute("orders", ordersJson);

            request.getRequestDispatcher("/view_orders_history.jsp")
                    .forward(request, response);

        } catch (Exception e) {
            request.setAttribute("error", "Order history service unavailable");
            request.getRequestDispatcher("/view_orders_history.jsp")
                    .forward(request, response);
        }
    }
}
