# FUCinemaBookingSystem – Cinema Ticket Booking System using API Gateway

Hệ thống Cinema Ticket Booking System gồm 3 Microservices và 1 API Gateway theo kiến trúc Polyglot Persistence.

## 1. Cấu trúc hệ thống & Database

| Service | Port | Database | DBMS |
|---|---|---|---|
| `customer-service` | 8081 | `cinema_customer` | Microsoft SQL Server 2022 |
| `movie-service` | 8082 | `cinema_movie` | MongoDB 7.0.5 |
| `booking-service` | 8083 | `cinema_booking` | MySQL 8.3.0 |
| `api-gateway` | 9000 | - | Spring Cloud Gateway Web MVC (Port chính) |

## 2. Hướng dẫn khởi chạy

### Bước 1: Khởi động Hạ tầng Docker
```bash
cd Assignment1/fu-cinema
docker compose up -d
```
Đợi container `cinema-sqlserver` đạt trạng thái `healthy` (khoảng 20–30s).

### Bước 2: Khởi động các Microservices
Mở 4 terminal riêng biệt hoặc chạy qua Services tool window trong IntelliJ IDEA:
1. `customer-service` (port 8081): `mvn -f customer-service/pom.xml spring-boot:run`
2. `movie-service` (port 8082): `mvn -f movie-service/pom.xml spring-boot:run`
3. `booking-service` (port 8083): `mvn -f booking-service/pom.xml spring-boot:run`
4. `api-gateway` (port 9000): `mvn -f api-gateway/pom.xml spring-boot:run`

## 3. Tài khoản kiểm thử

| Vai trò | Email | Mật khẩu | Ghi chú |
|---|---|---|---|
| Admin | `admin@fucinema.com` | `@@abc123@@` | Cấu hình trong properties |
| Customer 1 | `an@gmail.com` | `123456` | ID = 1, ACTIVE |
| Customer 2 | `binh@gmail.com` | `123456` | ID = 2, ACTIVE |
| Customer 3 | `chi@gmail.com` | `123456` | ID = 3, INACTIVE (bị khóa) |

## 4. Kiểm thử Postman
Import file Environment `postman/FUCinema-Local.postman_environment.json` và Collection `postman/FUCinemaBookingSystem.postman_collection.json` vào Postman Desktop để chạy kiểm thử tự động.
