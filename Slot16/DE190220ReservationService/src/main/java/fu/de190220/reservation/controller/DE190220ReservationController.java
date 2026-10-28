package fu.de190220.reservation.controller;

import fu.de190220.reservation.dto.ApiResponseDTO;
import fu.de190220.reservation.dto.ReservationDTO;
import fu.de190220.reservation.service.ReservationService;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/reservations")
public class DE190220ReservationController {

    private final ReservationService reservationService;

    public DE190220ReservationController(ReservationService reservationService) {
        this.reservationService = reservationService;
    }

    @PostMapping
    public ResponseEntity<ApiResponseDTO> createReservation(@Valid @RequestBody ReservationDTO dto) {
        ApiResponseDTO res = reservationService.createReservation(dto);
        if (res.getStatus() == 1) {
            return ResponseEntity.status(HttpStatus.CREATED).body(res); // 201
        } else if (res.getStatus() == 2) {
            return ResponseEntity.status(HttpStatus.NOT_ACCEPTABLE).body(res); // 406
        } else if (res.getStatus() == 4) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(res); // 404
        } else if (res.getStatus() == 5) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(res); // 400
        }
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(res); // 500
    }

    @PutMapping("/{reservationId}")
    public ResponseEntity<ApiResponseDTO> updateReservation(@PathVariable("reservationId") Long reservationId,
                                                           @RequestBody ReservationDTO dto) {
        ApiResponseDTO res = reservationService.updateReservation(reservationId, dto);
        if (res.getStatus() == 1) {
            return ResponseEntity.status(HttpStatus.OK).body(res); // 200
        } else if (res.getStatus() == 2) {
            return ResponseEntity.status(HttpStatus.NOT_ACCEPTABLE).body(res); // 406
        } else if (res.getStatus() == 4) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(res); // 404
        }
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(res); // 500
    }

    @GetMapping("/{reservationId}")
    public ResponseEntity<ApiResponseDTO> getReservationById(@PathVariable("reservationId") Long reservationId) {
        ApiResponseDTO res = reservationService.getReservationById(reservationId);
        if (res.getStatus() == 1) {
            return ResponseEntity.status(HttpStatus.OK).body(res); // 200
        } else if (res.getStatus() == 4) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(res); // 404
        }
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(res); // 500
    }

    @DeleteMapping("/{reservationId}")
    public ResponseEntity<ApiResponseDTO> cancelReservation(@PathVariable("reservationId") Long reservationId) {
        ApiResponseDTO res = reservationService.cancelReservation(reservationId);
        if (res.getStatus() == 1) {
            return ResponseEntity.status(HttpStatus.OK).body(res); // 200
        } else if (res.getStatus() == 4) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(res); // 404
        }
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(res); // 500
    }

    @GetMapping
    public ResponseEntity<ApiResponseDTO> getReservationList(
            @RequestParam(name = "page", required = false, defaultValue = "0") Integer page,
            @RequestParam(name = "size", required = false, defaultValue = "10") Integer size,
            @RequestParam(name = "guestName", required = false) String guestName,
            @RequestParam(name = "status", required = false) String status) {

        if (page == null || page < 0 || size == null || size <= 0 || size > 100) {
            return ResponseEntity.status(HttpStatus.NOT_ACCEPTABLE)
                    .body(ApiResponseDTO.error(2, "Data validation failed (page must be >= 0, size must be between 1 and 100)"));
        }

        Pageable pageable = PageRequest.of(page, size);
        ApiResponseDTO res = reservationService.getReservationList(guestName, status, pageable);
        return ResponseEntity.status(HttpStatus.OK).body(res); // 200
    }
}
