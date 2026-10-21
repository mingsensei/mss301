# Kết Quả Kiểm Thử Saga Orchestration (Slot 13)

- **Thời gian chạy**: 2026-10-21
- **Công cụ kiểm thử**: Postman / Newman CLI
- **Môi trường**: Docker Compose (MySQL 8.4, SQL Server 2022, MongoDB 8.0, order-service, inventory-service, payment-service)
- **Tổng số assertions**: 70/70 PASSED (0 FAILED)

---

## 1. Kết quả chạy tự động (Collection Runner / Newman)

```
newman

MSS301 - Saga Demo (Spring Boot 4.1.1)

❏ 0 - Kiểm tra service
↳ 1. Danh sách sản phẩm
  GET http://localhost:8082/api/inventory/products [200 OK, 262B, 76ms]
  ✓  HTTP 200
  ✓  Có sản phẩm P1, P2
↳ 2. Danh sách ví
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 94ms]
  ✓  HTTP 200
  ✓  Có ví C1, C2
↳ 3. Danh sách đơn hàng
  GET http://localhost:8081/api/orders [200 OK, 157B, 73ms]
  ✓  HTTP 200

❏ KB1 - Happy path
↳ [KB1] 1. Snapshot kho & ví
  GET http://localhost:8082/api/inventory/products [200 OK, 262B, 8ms]
  ✓  HTTP 200
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 11ms]
  ✓  Đọc được số dư ví
↳ [KB1] 2. Đặt hàng
  POST http://localhost:8081/api/orders [200 OK, 296B, 967ms]
  ✓  HTTP 200
  ✓  Order status = CONFIRMED
  ✓  Saga status = COMPLETED
  ✓  Không có failureReason
↳ [KB1] 3. Kiểm tra kho & ví
  GET http://localhost:8082/api/inventory/products [200 OK, 261B, 8ms]
  ✓  HTTP 200
  ✓  Tồn kho P1: 10 -> 8
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 10ms]
  ✓  Số dư C1: 5000 -> 3000
↳ [KB1] 4. Saga logs
  GET http://localhost:8081/api/orders/1/saga-logs [200 OK, 667B, 288ms]
  ✓  HTTP 200
  ✓  Thứ tự bước Saga đúng

❏ KB2 - Thanh toán thất bại (402)
↳ [KB2] 1. Snapshot kho & ví
  GET http://localhost:8082/api/inventory/products [200 OK, 261B, 7ms]
  ✓  HTTP 200
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 14ms]
  ✓  Đọc được số dư ví
↳ [KB2] 2. Đặt hàng
  POST http://localhost:8081/api/orders [200 OK, 349B, 157ms]
  ✓  HTTP 200
  ✓  Order status = CANCELLED
  ✓  Saga status = COMPENSATED
  ✓  failureReason bắt đầu bằng 402
↳ [KB2] 3. Kiểm tra kho & ví
  GET http://localhost:8082/api/inventory/products [200 OK, 261B, 5ms]
  ✓  HTTP 200
  ✓  Tồn kho P1: 8 -> 8
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 10ms]
  ✓  Số dư C2: 100 -> 100
↳ [KB2] 4. Kiểm tra reservation RELEASED
  GET http://localhost:8082/api/inventory/reservations [200 OK, 286B, 6ms]
  ✓  HTTP 200
  ✓  Reservation status = RELEASED
↳ [KB2] 5. Saga logs
  GET http://localhost:8081/api/orders/2/saga-logs [200 OK, 818B, 6ms]
  ✓  HTTP 200
  ✓  Thứ tự bước Saga đúng

❏ KB3 - Hết hàng (409)
↳ [KB3] 1. Snapshot kho & ví
  GET http://localhost:8082/api/inventory/products [200 OK, 261B, 5ms]
  ✓  HTTP 200
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 10ms]
  ✓  Đọc được số dư ví
↳ [KB3] 2. Đặt hàng
  POST http://localhost:8081/api/orders [200 OK, 341B, 56ms]
  ✓  HTTP 200
  ✓  Order status = CANCELLED
  ✓  Saga status = COMPENSATED
  ✓  failureReason bắt đầu bằng 409
↳ [KB3] 3. Kiểm tra kho & ví
  GET http://localhost:8082/api/inventory/products [200 OK, 261B, 9ms]
  ✓  HTTP 200
  ✓  Tồn kho P2: 5 -> 5
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 10ms]
  ✓  Số dư C1: 3000 -> 3000
↳ [KB3] 4. Saga logs
  GET http://localhost:8081/api/orders/3/saga-logs [200 OK, 557B, 6ms]
  ✓  HTTP 200
  ✓  Thứ tự bước Saga đúng

❏ KB4 - Sản phẩm không tồn tại (404 inventory)
↳ [KB4] 1. Snapshot kho & ví
  GET http://localhost:8082/api/inventory/products [200 OK, 261B, 6ms]
  ✓  HTTP 200
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 12ms]
  ✓  Đọc được số dư ví
↳ [KB4] 2. Đặt hàng
  POST http://localhost:8081/api/orders [200 OK, 334B, 47ms]
  ✓  HTTP 200
  ✓  Order status = CANCELLED
  ✓  Saga status = COMPENSATED
  ✓  failureReason bắt đầu bằng 404
↳ [KB4] 3. Kiểm tra kho & ví
  GET http://localhost:8082/api/inventory/products [200 OK, 261B, 6ms]
  ✓  HTTP 200
  ✓  Tồn kho P1: 8 -> 8
  ✓  Tồn kho P2: 5 -> 5
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 8ms]
  ✓  Số dư C1: 3000 -> 3000
↳ [KB4] 4. Saga logs
  GET http://localhost:8081/api/orders/4/saga-logs [200 OK, 554B, 8ms]
  ✓  HTTP 200
  ✓  Thứ tự bước Saga đúng

❏ KB5 - Ví không tồn tại (404 payment)
↳ [KB5] 1. Snapshot kho & ví
  GET http://localhost:8082/api/inventory/products [200 OK, 261B, 6ms]
  ✓  HTTP 200
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 8ms]
  ✓  Đọc được số dư ví
↳ [KB5] 2. Đặt hàng
  POST http://localhost:8081/api/orders [200 OK, 331B, 81ms]
  ✓  HTTP 200
  ✓  Order status = CANCELLED
  ✓  Saga status = COMPENSATED
  ✓  failureReason bắt đầu bằng 404
↳ [KB5] 3. Kiểm tra kho & ví
  GET http://localhost:8082/api/inventory/products [200 OK, 261B, 8ms]
  ✓  HTTP 200
  ✓  Tồn kho P2: 5 -> 5
  GET http://localhost:8083/api/payments/wallets [200 OK, 230B, 11ms]
↳ [KB5] 4. Saga logs
  GET http://localhost:8081/api/orders/5/saga-logs [200 OK, 807B, 7ms]
  ✓  HTTP 200
  ✓  Thứ tự bước Saga đúng

❏ KB7 - Idempotent (gọi lặp lại)
↳ [KB7] 1. Release lặp lại
  POST http://localhost:8082/api/inventory/release/2 [200 OK, 171B, 7ms]
  ✓  HTTP 200
  ✓  Response body = RELEASED
↳ [KB7] 2. Reserve lặp lại
  POST http://localhost:8082/api/inventory/reserve [200 OK, 219B, 9ms]
  ✓  HTTP 200
  ✓  Status = RESERVED
↳ [KB7] 3. Pay lặp lại
  POST http://localhost:8083/api/payments/pay [200 OK, 219B, 11ms]
  ✓  HTTP 200
  ✓  Status = PAID
↳ [KB7] 4. Refund đơn chưa trả
  POST http://localhost:8083/api/payments/refund/2 [200 OK, 171B, 12ms]
  ✓  HTTP 200
  ✓  Response body = REFUNDED

┌─────────────────────────┬───────────────────┬───────────────────┐
│                         │          executed │            failed │
├─────────────────────────┼───────────────────┼───────────────────┤
│              iterations │                 1 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│                requests │                38 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│            test-scripts │                28 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│      prerequest-scripts │                 0 │                 0 │
├─────────────────────────┼───────────────────┼───────────────────┤
│              assertions │                70 │                 0 │
└─────────────────────────┴───────────────────┴───────────────────┘
```

---

## 2. Kết quả chạy thủ công KB6 (Network failure - payment-service tắt)

- **Hành động**: `docker compose stop payment-service` rồi gửi `POST /api/orders` đặt hàng sản phẩm `P2`.
- **Response**:
```json
{
  "id": 6,
  "customerId": "C1",
  "productId": "P2",
  "quantity": 1,
  "amount": 20.0,
  "status": "CANCELLED",
  "sagaStatus": "COMPENSATED",
  "failureReason": "Service không phản hồi: I/O error on POST request for \"http://payment-service:8083/api/payments/pay\": HTTP connect timed out"
}
```
- **Saga Logs**:
```json
[
  {"orderId": 6, "step": "CREATE_ORDER", "result": "SUCCESS", "message": "Order PENDING"},
  {"orderId": 6, "step": "RESERVE_INVENTORY", "result": "SUCCESS", "message": "Đã giữ 1 P2"},
  {"orderId": 6, "step": "SAGA", "result": "FAILED", "message": "Service không phản hồi: I/O error on POST request for \"http://payment-service:8083/api/payments/pay\": HTTP connect timed out"},
  {"orderId": 6, "step": "COMPENSATION", "result": "SUCCESS", "message": "Lần thử 1"},
  {"orderId": 6, "step": "CANCEL_ORDER", "result": "SUCCESS", "message": "Saga COMPENSATED"}
]
```
- **Trạng thái kho sau khi hoàn tác**: Tồn kho `P2` vẫn nguyên vẹn là 5 (được reserve rồi compensate release an toàn).
