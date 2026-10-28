package fu.de190220.room.controller;

import fu.de190220.room.dto.ApiResponseDTO;
import fu.de190220.room.dto.RoomDTO;
import fu.de190220.room.service.RoomService;
import jakarta.validation.Valid;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/rooms")
public class DE190220RoomController {

    private final RoomService roomService;

    public DE190220RoomController(RoomService roomService) {
        this.roomService = roomService;
    }

    @PostMapping
    public ResponseEntity<ApiResponseDTO> createRoom(@Valid @RequestBody RoomDTO dto) {
        ApiResponseDTO res = roomService.createRoom(dto);
        if (res.getStatus() == 1) {
            return ResponseEntity.status(HttpStatus.CREATED).body(res); // 201
        } else if (res.getStatus() == 3) {
            return ResponseEntity.status(HttpStatus.IM_USED).body(res); // 226
        } else if (res.getStatus() == 2) {
            return ResponseEntity.status(HttpStatus.NOT_ACCEPTABLE).body(res); // 406
        }
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(res); // 500
    }

    @PutMapping("/{roomId}")
    public ResponseEntity<ApiResponseDTO> updateRoom(@PathVariable("roomId") Long roomId,
                                                     @RequestBody RoomDTO dto) {
        ApiResponseDTO res = roomService.updateRoom(roomId, dto);
        if (res.getStatus() == 1) {
            return ResponseEntity.status(HttpStatus.OK).body(res); // 200
        } else if (res.getStatus() == 3) {
            return ResponseEntity.status(HttpStatus.IM_USED).body(res); // 226
        } else if (res.getStatus() == 4) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(res); // 404
        } else if (res.getStatus() == 2) {
            return ResponseEntity.status(HttpStatus.NOT_ACCEPTABLE).body(res); // 406
        }
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(res); // 500
    }

    @GetMapping("/{roomId}")
    public ResponseEntity<ApiResponseDTO> getRoomById(@PathVariable("roomId") Long roomId) {
        ApiResponseDTO res = roomService.getRoomById(roomId);
        if (res.getStatus() == 1) {
            return ResponseEntity.status(HttpStatus.OK).body(res); // 200
        } else if (res.getStatus() == 4) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(res); // 404
        }
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(res); // 500
    }

    @DeleteMapping("/{roomId}")
    public ResponseEntity<ApiResponseDTO> setRoomToMaintenance(@PathVariable("roomId") Long roomId) {
        ApiResponseDTO res = roomService.setRoomToMaintenance(roomId);
        if (res.getStatus() == 1) {
            return ResponseEntity.status(HttpStatus.OK).body(res); // 200
        } else if (res.getStatus() == 4) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(res); // 404
        }
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(res); // 500
    }

    @GetMapping
    public ResponseEntity<ApiResponseDTO> getRoomList(
            @RequestParam(name = "page", required = false, defaultValue = "0") Integer page,
            @RequestParam(name = "size", required = false, defaultValue = "10") Integer size,
            @RequestParam(name = "roomType", required = false) String roomType,
            @RequestParam(name = "status", required = false) String status) {

        if (page == null || page < 0 || size == null || size <= 0 || size > 100) {
            return ResponseEntity.status(HttpStatus.NOT_ACCEPTABLE)
                    .body(ApiResponseDTO.error(2, "Data validation failed (page must be >= 0, size must be between 1 and 100)"));
        }

        Pageable pageable = PageRequest.of(page, size);
        ApiResponseDTO res = roomService.getRoomList(roomType, status, pageable);
        return ResponseEntity.status(HttpStatus.OK).body(res); // 200
    }
}
