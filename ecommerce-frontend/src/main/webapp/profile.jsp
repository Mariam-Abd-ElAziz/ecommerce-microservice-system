<%@ page contentType="text/html;charset=UTF-8" language="java" %>

<!DOCTYPE html>
<html>
<head>
    <title>Customer Profile</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 0;
        }
        .profile-container {
            max-width: 600px;
            margin: 60px auto;
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h2 {
            text-align: center;
            margin-bottom: 20px;
        }
        .profile-item {
            margin-bottom: 16px;
        }
        .label {
            font-weight: bold;
            color: #555;
        }
        .value {
            display: block;
            margin-top: 4px;
            font-size: 1.05rem;
        }
        .points {
            color: #2a7a2e;
            font-weight: bold;
        }
    </style>
</head>

<body>
<div class="profile-container">
    <h2>Customer Profile</h2>

    <div class="profile-item">
        <span class="label">Name</span>
        <span class="value">${customerName}</span>
    </div>

    <div class="profile-item">
        <span class="label">Email</span>
        <span class="value">${email}</span>
    </div>

    <div class="profile-item">
        <span class="label">Phone Number</span>
        <span class="value">${phone}</span>
    </div>

    <div class="profile-item">
        <span class="label">Loyalty Points</span>
        <span class="value points">${loyaltyPoints}</span>
    </div>
</div>
</body>
</html>
