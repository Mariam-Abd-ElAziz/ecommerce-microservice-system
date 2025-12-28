package controller;
import com.ecommerce.ecommercefrontend.util.ServiceClient;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/confirmOrder")
public class PlaceOrderServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String customerId = request.getParameter("customerId"); // [cite: 31]
        String amount = request.getParameter("totalAmount"); // [cite: 33]

        try {
            // 1. Create Order [cite: 34, 39]
            ServiceClient.sendRequest("http://localhost:8083/api/orders/create", "POST", "{...order data...}");

            // 2. Update Loyalty [cite: 35, 42]
            ServiceClient.sendRequest("http://localhost:8084/api/customers/" + customerId + "/loyalty", "PUT", null);

            // 3. Send Notification [cite: 43, 45]
            ServiceClient.sendRequest("http://localhost:8085/api/notifications/send", "POST", "{\"customerId\":\""+customerId+"\"}");

            response.sendRedirect("confirmation.jsp"); // [cite: 47]
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}