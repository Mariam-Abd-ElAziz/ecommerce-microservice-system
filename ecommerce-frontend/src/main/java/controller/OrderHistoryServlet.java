package controller;
import com.ecommerce.ecommercefrontend.util.ServiceClient;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/viewHistory")
public class OrderHistoryServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String customerId = "123"; // Retrieve from session

        try {
            // 1. Get History IDs [cite: 60, 65]
            String orderIds = ServiceClient.sendRequest("http://localhost:8084/api/customers/" + customerId + "/orders", "GET", null);

            // 2. Get Details for each ID (Logic simplified) [cite: 60, 68]
            // Note: In a real app, you'd loop through IDs and call Order Service for each

            request.setAttribute("history", orderIds);
            request.getRequestDispatcher("View_orders_history.jsp").forward(request, response); // [cite: 61, 70]
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}