package com.ecommerce.ecommercefrontend.util;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class ServiceClient {

    /**
     * Common method to call Microservice APIs
     * @param urlString The endpoint (e.g., http://localhost:8081/api/inventory/products)
     * @param method GET, POST, or PUT
     * @param jsonBody The JSON payload (for POST/PUT) or null for GET
     */
    public static String sendRequest(String urlString, String method, String jsonBody) throws Exception {
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod(method);
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setRequestProperty("Accept", "application/json");

        // Attach body if it's a POST or PUT request [cite: 21, 39, 42, 45]
        if (jsonBody != null && !jsonBody.isEmpty()) {
            conn.setDoOutput(true);
            try (OutputStream os = conn.getOutputStream()) {
                byte[] input = jsonBody.getBytes("utf-8");
                os.write(input, 0, input.length);
            }
        }

        // Read the response from the service
        try (Scanner scanner = new Scanner(conn.getInputStream(), "UTF-8")) {
            scanner.useDelimiter("\\A");
            return scanner.hasNext() ? scanner.next() : "";
        } finally {
            conn.disconnect();
        }
    }
}