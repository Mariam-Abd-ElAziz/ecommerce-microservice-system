package controller;
import com.ecommerce.ecommercefrontend.util.ServiceClient;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/initiateOrder")
public class OrderInitiationServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String productId = request.getParameter("productId");
        int quantity = Integer.parseInt(request.getParameter("quantity"));

        try {
            // 1. Check Inventory [cite: 14, 18]
            String inventoryStatus = ServiceClient.sendRequest("http://localhost:8081/api/inventory/check/" + productId, "GET", null);

            // 2. Calculate Pricing [cite: 14, 21]
            String priceJson = "{\"productId\":\"" + productId + "\", \"quantity\":" + quantity + "}";
            String totalAmount = ServiceClient.sendRequest("http://localhost:8082/api/pricing/calculate", "POST", priceJson);

            // 3. Pass to Checkout JSP [cite: 22, 23]
            request.setAttribute("totalAmount", totalAmount);
            request.getRequestDispatcher("checkout.jsp").forward(request, response);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}