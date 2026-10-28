# MSS301 - Practical Exam (Summer 2026) - Hotel Management System

**Student Name:** Duong Hong Minh  
**Student ID:** DE190220  
**Subject:** MSS301 - Microservices with Spring Cloud  

---

## 1. Architecture Overview

The system consists of three microservices and one API Gateway implementing a layered enterprise architecture:

```
                      +-----------------------------+
                      |   Client / Postman / Web    |
                      +--------------+--------------+
                                     |
                                     v
                 +---------------------------------------+
                 |    Hotel Gateway (:8080)              |
                 |    Spring Cloud Gateway (WebFlux)     |
                 |    Swagger Aggregation + CORS         |
                 +----------+-----------------+----------+
                            |                 |
            /api/rooms/**   |                 |   /api/reservations/**
                            v                 v
            +--------------------+       +----------------------------+
            |  Room Service      |       |  Reservation Service       |
            |  Port: 8081        | <==== |  Port: 8082                |
            |  Spring MVC + JPA  | Open- |  Spring MVC + JPA          |
            |  MSSQL Server      | Feign |  OpenFeign Client          |
            +--------------------+       +----------------------------+
                      |                                 |
                      v                                 v
            +---------------------------------------------------------+
            |               MS SQL Server 2016+ (MSS301_2026_PE)      |
            |         Tables: [rooms], [reservations]                 |
            +---------------------------------------------------------+
```

---

## 2. Microservices Breakdown

### 2.1 DE190220RoomService (`port: 8081`)
- **Package:** `fu.de190220.room`
- **Database:** MS SQL Server (`rooms` table in `MSS301_2026_PE`)
- **Features:**
  - `POST /api/rooms`: Create room (returns `201` with `status: 1`, default status `AVAILABLE`; `226` if duplicate room number; `406` if validation fails).
  - `PUT /api/rooms/{roomId}`: Partially update room (`200` with `status: 1`; `226` if duplicate room number; `404` if not found; `406` if validation fails).
  - `GET /api/rooms/{roomId}`: Get room details (`200` with `status: 1`; `404` if not found).
  - `DELETE /api/rooms/{roomId}`: Set room status to `MAINTENANCE` (`200` with `status: 1`, data is `null`; `404` if not found).
  - `GET /api/rooms`: Paginated query with filters (`page`, `size` [1..100], `roomType`, `status`). Returns `PageDTO` (`200` with `status: 1`; `406` if pagination params invalid).
- **CORS:** Configured with `CorsFilter` allowing `*` pattern for Swagger UI aggregation.
- **Swagger Docs:** `http://localhost:8081/swagger-ui.html`

### 2.2 DE190220ReservationService (`port: 8082`)
- **Package:** `fu.de190220.reservation`
- **Database:** MS SQL Server (`reservations` table in `MSS301_2026_PE`)
- **OpenFeign Integration:** Calls `RoomService` at `http://localhost:8081/api/rooms/{roomId}` via `RoomClient`.
- **Features:**
  - `POST /api/reservations`: Create reservation.
    - Validates `checkOutDate > checkInDate` (`406` / `status: 2`).
    - Validates Room existence via Feign (`404` / `status: 4`).
    - Validates Room status is `AVAILABLE` (`400` / `status: 5`).
    - Validates `numberOfGuests <= room.capacity` (`406` / `status: 2`).
    - Computes `totalAmount = pricePerNight * nights`. Default status: `CONFIRMED`. Returns `201` / `status: 1`.
  - `PUT /api/reservations/{reservationId}`: Partially update reservation (`200` / `status: 1`; `404` if not found; `406` if dates invalid; recomputes `totalAmount`).
  - `GET /api/reservations/{reservationId}`: Get reservation details with embedded `RoomDTO` (`200` / `status: 1`; `404` if not found).
  - `DELETE /api/reservations/{reservationId}`: Cancel reservation, sets status to `CANCELLED` (`200` / `status: 1`, data: `null`; `404` if not found).
  - `GET /api/reservations`: Paginated list of reservations with embedded `RoomDTO` for each entry. Filters: `page`, `size`, `guestName`, `status`.
- **Swagger Docs:** `http://localhost:8082/swagger-ui.html`

### 2.3 DE190220HotelGateway (`port: 8080`)
- **Package:** `fu.de190220.gateway`
- **Engine:** Spring Cloud Gateway Server WebFlux (reactive non-blocking).
- **Routes:**
  - `/api/rooms/**` -> `http://localhost:8081`
  - `/api/reservations/**` -> `http://localhost:8082`
- **Swagger UI Aggregation:**
  - Accessible at `http://localhost:8080/swagger-ui.html`
  - Dropdown selector allows switching between `room-service` and `reservation-service`.
- **CORS:** Configured with reactive `CorsWebFilter` accepting all hosts.

---

## 3. Database Setup

Run SQL Server scripts in order:
```sql
CREATE DATABASE MSS301_2026_PE;
GO
USE MSS301_2026_PE;
GO
-- 1. Execute create_rooms_sql.txt
-- 2. Execute create_reservations_sql.txt
```

Seed initial sample rooms:
```sql
USE MSS301_2026_PE;
GO
INSERT INTO rooms (room_number, room_type, price_per_night, capacity, floor, status) VALUES
('R-101', 'DOUBLE', 850000.00, 2, 1, 'AVAILABLE'),
('R-102', 'SINGLE', 500000.00, 1, 1, 'AVAILABLE'),
('R-201', 'SUITE', 1500000.00, 4, 2, 'AVAILABLE'),
('R-301', 'DELUXE', 2500000.00, 6, 3, 'OCCUPIED');
GO
```

---

## 4. How to Run & Verify

### Build all 3 projects:
```bash
cd Slot16/DE190220RoomService && mvn clean test
cd ../DE190220ReservationService && mvn clean test
cd ../DE190220HotelGateway && mvn clean test
```

### Start services:
1. `DE190220RoomService`:
   ```bash
   cd Slot16/DE190220RoomService && mvn spring-boot:run
   ```
2. `DE190220ReservationService`:
   ```bash
   cd Slot16/DE190220ReservationService && mvn spring-boot:run
   ```
3. `DE190220HotelGateway`:
   ```bash
   cd Slot16/DE190220HotelGateway && mvn spring-boot:run
   ```

### Verify Endpoints:
- Gateway Swagger UI: `http://localhost:8080/swagger-ui.html`
- Postman Collection: import `Slot16/Hotel_Postman_Collection.json`

---

## 5. PE Submission Checklist

- [x] All 3 projects created strictly following naming convention (`DE190220RoomService`, `DE190220ReservationService`, `DE190220HotelGateway`)
- [x] Controller names follow specification (`DE190220RoomController`, `DE190220ReservationController`)
- [x] Package structure follows `fu.de190220.<servicename>.*`
- [x] All required response codes implemented (`201`, `200`, `226`, `406`, `404`, `400`, `500`)
- [x] OpenFeign client implemented with error handling (`FeignException.NotFound` -> `404`)
- [x] Target directories cleaned with `mvn clean` before submission
- [x] Packaged zip file ready for EOS / PEA submission
