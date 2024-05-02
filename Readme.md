# Vendor Management System API

This API provides endpoints for managing vendors and purchase orders in a Vendor Management System.

## Endpoints

### Authentication

- **Generate Token**: `POST /api-token-auth/`
  - Generates a token based on username and password.
  - URL: "http://localhost:8000/api-token-auth/"
  - Method: "POST"
  - Example Request Body (JSON):
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - Example Response Body:
    ```json
    {
      "token": "your_access_token"
    }
    ```

### Vendor Endpoints

- **Create Vendor**: `POST /api/vendors/`
  - Creates a new vendor with provided details.
  - URL: "http://localhost:8000/api/vendors/"
  - Method: "POST"
  - Authorization: Token <your_access_token>
  - Example Request Body (JSON):
    ```json
    {
      "name": "Vendor Name",
      "contact_details": "Contact Details",
      "address": "Vendor Address",
      "vendor_code": "ABC123"
    }
    ```
- **List Vendors**: `GET /api/vendors/all/`
  - Method: "GET"
  - Authorization: Token <your_access_token>
  - Retrieves a list of all vendors.
  - Query Parameters:
    - `page`: (optional) Specifies the page number for pagination.

- **Get Vendor**: `GET /api/vendors/{vendor_id}/`
  - Method: "GET"
  - Authorization: Token <your_access_token>
  - Retrieves details of a specific vendor by ID.

- **Update Vendor**: `PUT /api/vendors/{vendor_id}/update/`
  - Method: "PUT"
  - Authorization: Token <your_access_token>
  - Updates details of a specific vendor by ID.
  - Example request body (JSON) (optional):
    ```json
    {
      "name": "Updated Vendor Name",
      "contact_details": "Updated Contact Details",
      "address": "Updated Vendor Address",
      "vendor_code": "XYZ456"
    }
    ```
- **Delete Vendor**: `DELETE /api/vendors/{vendor_id}/delete/`
  - Method: "DELETE"
  - Authorization: Token <your_access_token>
  - Deletes a specific vendor by ID.

- **Fetch Vendor Performance Metrics**: `GET /api/vendors/{vendor_id}/performance/`
  - Method: "GET"
  - Authorization: Token <your_access_token>
  - Retrieves performance metrics of a specific vendor by ID.

### Purchase Order Endpoints

- **Create PO**: `POST /api/purchase_orders/`
  - Creates a new purchase order with provided details.
  - URL: "http://localhost:8000/api/purchase_orders/"
  - Method: "POST"
  - Authorization: Token <your_access_token>
  - Example request body (JSON):
    ```json
    {
      "vendor_id": 1,
      "po_number": "PO123",
      "order_date": "2024-05-05T10:00:00",
      "delivery_date": "2024-05-10",
      "items": [{"name": "Item 1", "quantity": 10}, {"name": "Item 2", "quantity": 20}],
      "quantity": 20,
      "status": "pending",
      "quality_rating": 5,
      "issue_date": "2024-05-01",
      "acknowledgment_date": "2024-05-02"
    }
    ```
- **List PO**: `GET /api/purchase_orders/all/`
  - Method: "GET"
  - Authorization: Token <your_access_token>
  - Retrieves a list of all purchase orders.
  - Query Parameters:
    - `page`: (optional) Specifies the page number for pagination.

- **Get PO**: `GET /api/purchase_orders/{po_id}/`
  - Method: "GET"
  - Authorization: Token <your_access_token>
  - Retrieves details of a specific purchase order by ID.

- **Update PO**: `PUT /api/purchase_orders/{po_id}/update/`
  - Method: "PUT"
  - Authorization: Token <your_access_token>
  - Updates details of a specific purchase order by ID.
  - Example request body (JSON) (optional):
    ```json
    {
      "po_number": "PO123",
      "order_date": "2024-05-05T10:00:00",
      "delivery_date": "2024-05-10",
      "items": [{"name": "Item 1", "quantity": 10}, {"name": "Item 2", "quantity": 20}],
      "quantity": 20,
      "status": "pending",
      "quality_rating": 5,
      "issue_date": "2024-05-01",
      "acknowledgment_date": "2024-05-02"
    }
    ```
- **Delete PO**: `DELETE /api/purchase_orders/{po_id}/delete/`
  - Method: "DELETE"
  - Authorization: Token <your_access_token>
  - Deletes a specific purchase order by ID.

### Additional Endpoints

- **Acknowledge Purchase Order**: `POST /api/purchase_orders/{po_id}/acknowledge/`
  - Method: "POST"
  - URL: "http://localhost:8000/api/purchase_orders/{po_id}/acknowledge/"
  - Acknowledges a purchase order by updating its acknowledgment date.
  - Authorization: Token <your_access_token>
  - Example request body (JSON):
    ```json
    {
      "acknowledgment_date": "2024-05-02"
    }
    ```

## Usage

1. Open The Project.
2. Activate Virtual Env
3. Install requirements.txt 
4. Start the Django development server.
5. Obtain an access token by sending a POST request to the token endpoint with your username and password.
6. Use the access token in the Authorization header for subsequent requests to the API endpoints.
7. Use Postman or any API client to send requests to the API endpoints.
8. Make sure to include necessary request headers and data in the request body as per the API documentation.
