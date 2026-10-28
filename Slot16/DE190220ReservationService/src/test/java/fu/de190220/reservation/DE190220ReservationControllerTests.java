package fu.de190220.reservation;

import com.fasterxml.jackson.databind.ObjectMapper;
import fu.de190220.reservation.client.RoomClient;
import fu.de190220.reservation.dto.ApiResponseDTO;
import fu.de190220.reservation.dto.ReservationDTO;
import fu.de190220.reservation.dto.RoomDTO;
import fu.de190220.reservation.entity.Reservation;
import fu.de190220.reservation.entity.ReservationStatus;
import fu.de190220.reservation.repository.ReservationRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.text.SimpleDateFormat;
import java.util.Date;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@TestPropertySource(locations = "classpath:application-test.properties")
public class DE190220ReservationControllerTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ReservationRepository reservationRepository;

    @MockitoBean
    private RoomClient roomClient;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy");

    @BeforeEach
    void setUp() {
        reservationRepository.deleteAll();
    }

    @Test
    void testCreateReservation_Success() throws Exception {
        RoomDTO mockRoom = new RoomDTO(1L, "A-101", "DOUBLE", new BigDecimal("850000.00"), 2, 1, "AVAILABLE");
        when(roomClient.getRoomById(eq(1L))).thenReturn(ApiResponseDTO.ok("Successful", mockRoom));

        ReservationDTO dto = new ReservationDTO();
        dto.setGuestName("Nguyen Van A");
        dto.setGuestEmail("a@example.com");
        dto.setGuestPhone("0901234567");
        dto.setCheckInDate(dateFormat.parse("25/07/2026"));
        dto.setCheckOutDate(dateFormat.parse("28/07/2026"));
        dto.setNumberOfGuests(2);
        dto.setRoomId(1L);

        mockMvc.perform(post("/api/reservations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status", is(1)))
                .andExpect(jsonPath("$.data.status", is("CONFIRMED")))
                .andExpect(jsonPath("$.data.totalAmount", is(2550000.0)));
    }

    @Test
    void testCreateReservation_InvalidDates() throws Exception {
        ReservationDTO dto = new ReservationDTO();
        dto.setGuestName("Nguyen Van A");
        dto.setGuestEmail("a@example.com");
        dto.setGuestPhone("0901234567");
        dto.setCheckInDate(dateFormat.parse("28/07/2026"));
        dto.setCheckOutDate(dateFormat.parse("25/07/2026")); // checkOut before checkIn
        dto.setNumberOfGuests(2);
        dto.setRoomId(1L);

        mockMvc.perform(post("/api/reservations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isNotAcceptable())
                .andExpect(jsonPath("$.status", is(2)));
    }

    @Test
    void testCreateReservation_RoomNotFound() throws Exception {
        when(roomClient.getRoomById(eq(999L))).thenReturn(ApiResponseDTO.error(4, "Room is not found"));

        ReservationDTO dto = new ReservationDTO();
        dto.setGuestName("Nguyen Van A");
        dto.setGuestEmail("a@example.com");
        dto.setGuestPhone("0901234567");
        dto.setCheckInDate(dateFormat.parse("25/07/2026"));
        dto.setCheckOutDate(dateFormat.parse("28/07/2026"));
        dto.setNumberOfGuests(2);
        dto.setRoomId(999L);

        mockMvc.perform(post("/api/reservations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status", is(4)));
    }

    @Test
    void testCreateReservation_RoomNotAvailable() throws Exception {
        RoomDTO mockRoom = new RoomDTO(2L, "A-102", "DOUBLE", new BigDecimal("850000.00"), 2, 1, "OCCUPIED");
        when(roomClient.getRoomById(eq(2L))).thenReturn(ApiResponseDTO.ok("Successful", mockRoom));

        ReservationDTO dto = new ReservationDTO();
        dto.setGuestName("Nguyen Van A");
        dto.setGuestEmail("a@example.com");
        dto.setGuestPhone("0901234567");
        dto.setCheckInDate(dateFormat.parse("25/07/2026"));
        dto.setCheckOutDate(dateFormat.parse("28/07/2026"));
        dto.setNumberOfGuests(2);
        dto.setRoomId(2L);

        mockMvc.perform(post("/api/reservations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status", is(5)));
    }

    @Test
    void testCreateReservation_CapacityExceeded() throws Exception {
        RoomDTO mockRoom = new RoomDTO(3L, "A-103", "SINGLE", new BigDecimal("500000.00"), 1, 1, "AVAILABLE");
        when(roomClient.getRoomById(eq(3L))).thenReturn(ApiResponseDTO.ok("Successful", mockRoom));

        ReservationDTO dto = new ReservationDTO();
        dto.setGuestName("Nguyen Van A");
        dto.setGuestEmail("a@example.com");
        dto.setGuestPhone("0901234567");
        dto.setCheckInDate(dateFormat.parse("25/07/2026"));
        dto.setCheckOutDate(dateFormat.parse("28/07/2026"));
        dto.setNumberOfGuests(3); // Exceeds capacity 1
        dto.setRoomId(3L);

        mockMvc.perform(post("/api/reservations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isNotAcceptable())
                .andExpect(jsonPath("$.status", is(2)));
    }

    @Test
    void testUpdateReservation_Success() throws Exception {
        RoomDTO mockRoom = new RoomDTO(1L, "A-101", "DOUBLE", new BigDecimal("850000.00"), 2, 1, "AVAILABLE");
        when(roomClient.getRoomById(eq(1L))).thenReturn(ApiResponseDTO.ok("Successful", mockRoom));

        Date in = dateFormat.parse("25/07/2026");
        Date out = dateFormat.parse("28/07/2026");
        Reservation existing = reservationRepository.save(new Reservation(null, "Old Name", "old@ex.com", "0900000000", in, out, 2, new BigDecimal("2550000.00"), ReservationStatus.CONFIRMED, 1L));

        ReservationDTO updateDto = new ReservationDTO();
        updateDto.setGuestName("New Name");

        mockMvc.perform(put("/api/reservations/" + existing.getReservationId())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updateDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is(1)))
                .andExpect(jsonPath("$.data.guestName", is("New Name")));
    }

    @Test
    void testGetReservationById_Success() throws Exception {
        RoomDTO mockRoom = new RoomDTO(1L, "A-101", "DOUBLE", new BigDecimal("850000.00"), 2, 1, "AVAILABLE");
        when(roomClient.getRoomById(eq(1L))).thenReturn(ApiResponseDTO.ok("Successful", mockRoom));

        Date in = dateFormat.parse("25/07/2026");
        Date out = dateFormat.parse("28/07/2026");
        Reservation existing = reservationRepository.save(new Reservation(null, "Guest 1", "g1@ex.com", "0900000001", in, out, 2, new BigDecimal("2550000.00"), ReservationStatus.CONFIRMED, 1L));

        mockMvc.perform(get("/api/reservations/" + existing.getReservationId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is(1)))
                .andExpect(jsonPath("$.data.guestName", is("Guest 1")))
                .andExpect(jsonPath("$.data.room.roomNumber", is("A-101")));
    }

    @Test
    void testCancelReservation_Success() throws Exception {
        Date in = dateFormat.parse("25/07/2026");
        Date out = dateFormat.parse("28/07/2026");
        Reservation existing = reservationRepository.save(new Reservation(null, "Guest 2", "g2@ex.com", "0900000002", in, out, 2, new BigDecimal("2550000.00"), ReservationStatus.CONFIRMED, 1L));

        mockMvc.perform(delete("/api/reservations/" + existing.getReservationId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is(1)))
                .andExpect(jsonPath("$.data").doesNotExist());

        // Verify status changed to CANCELLED
        Reservation cancelled = reservationRepository.findById(existing.getReservationId()).orElseThrow();
        org.junit.jupiter.api.Assertions.assertEquals(ReservationStatus.CANCELLED, cancelled.getStatus());
    }

    @Test
    void testGetReservationList_Success() throws Exception {
        RoomDTO mockRoom = new RoomDTO(1L, "A-101", "DOUBLE", new BigDecimal("850000.00"), 2, 1, "AVAILABLE");
        when(roomClient.getRoomById(eq(1L))).thenReturn(ApiResponseDTO.ok("Successful", mockRoom));

        Date in = dateFormat.parse("25/07/2026");
        Date out = dateFormat.parse("28/07/2026");
        reservationRepository.save(new Reservation(null, "Alice", "alice@ex.com", "0900000001", in, out, 2, new BigDecimal("2550000.00"), ReservationStatus.CONFIRMED, 1L));
        reservationRepository.save(new Reservation(null, "Bob", "bob@ex.com", "0900000002", in, out, 1, new BigDecimal("2550000.00"), ReservationStatus.CONFIRMED, 1L));

        mockMvc.perform(get("/api/reservations?page=0&size=10"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is(1)))
                .andExpect(jsonPath("$.data.totalElements", is(2)))
                .andExpect(jsonPath("$.data.content", hasSize(2)));
    }

    @Test
    void testGetReservationList_InvalidPagination() throws Exception {
        mockMvc.perform(get("/api/reservations?page=-1&size=10"))
                .andExpect(status().isNotAcceptable())
                .andExpect(jsonPath("$.status", is(2)));

        mockMvc.perform(get("/api/reservations?page=0&size=101"))
                .andExpect(status().isNotAcceptable())
                .andExpect(jsonPath("$.status", is(2)));
    }
}
