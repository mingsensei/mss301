package fu.de190220.room;

import com.fasterxml.jackson.databind.ObjectMapper;
import fu.de190220.room.dto.RoomDTO;
import fu.de190220.room.entity.Room;
import fu.de190220.room.entity.RoomStatus;
import fu.de190220.room.entity.RoomType;
import fu.de190220.room.repository.RoomRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@TestPropertySource(locations = "classpath:application-test.properties")
public class DE190220RoomControllerTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private RoomRepository roomRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @BeforeEach
    void setUp() {
        roomRepository.deleteAll();
    }

    @Test
    void testCreateRoom_Success() throws Exception {
        RoomDTO dto = new RoomDTO();
        dto.setRoomNumber("A-101");
        dto.setRoomType("DOUBLE");
        dto.setPricePerNight(new BigDecimal("850000.00"));
        dto.setCapacity(2);
        dto.setFloor(1);

        mockMvc.perform(post("/api/rooms")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status", is(1)))
                .andExpect(jsonPath("$.data.roomNumber", is("A-101")))
                .andExpect(jsonPath("$.data.status", is("AVAILABLE")));
    }

    @Test
    void testCreateRoom_DuplicateRoomNumber() throws Exception {
        Room existing = new Room(null, "A-101", RoomType.DOUBLE, new BigDecimal("850000.00"), 2, 1, RoomStatus.AVAILABLE);
        roomRepository.save(existing);

        RoomDTO dto = new RoomDTO();
        dto.setRoomNumber("A-101");
        dto.setRoomType("SINGLE");
        dto.setPricePerNight(new BigDecimal("500000.00"));
        dto.setCapacity(1);
        dto.setFloor(1);

        mockMvc.perform(post("/api/rooms")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().is(226))
                .andExpect(jsonPath("$.status", is(3)))
                .andExpect(jsonPath("$.message", containsString("duplicated")));
    }

    @Test
    void testCreateRoom_ValidationFailed() throws Exception {
        RoomDTO dto = new RoomDTO();
        dto.setRoomNumber(""); // Invalid
        dto.setRoomType("INVALID_TYPE");
        dto.setPricePerNight(BigDecimal.ZERO); // Must be > 0
        dto.setCapacity(20); // Must be <= 10
        dto.setFloor(0); // Must be >= 1

        mockMvc.perform(post("/api/rooms")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isNotAcceptable())
                .andExpect(jsonPath("$.status", is(2)));
    }

    @Test
    void testUpdateRoom_Success() throws Exception {
        Room existing = roomRepository.save(new Room(null, "A-102", RoomType.SINGLE, new BigDecimal("500000.00"), 1, 1, RoomStatus.AVAILABLE));

        RoomDTO updateDto = new RoomDTO();
        updateDto.setPricePerNight(new BigDecimal("600000.00"));

        mockMvc.perform(put("/api/rooms/" + existing.getRoomId())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updateDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is(1)))
                .andExpect(jsonPath("$.data.pricePerNight", is(600000.0)))
                .andExpect(jsonPath("$.data.roomNumber", is("A-102")));
    }

    @Test
    void testUpdateRoom_NotFound() throws Exception {
        RoomDTO updateDto = new RoomDTO();
        updateDto.setRoomNumber("B-999");

        mockMvc.perform(put("/api/rooms/999999")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updateDto)))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status", is(4)));
    }

    @Test
    void testGetRoomById_Success() throws Exception {
        Room existing = roomRepository.save(new Room(null, "A-103", RoomType.SUITE, new BigDecimal("1200000.00"), 3, 2, RoomStatus.AVAILABLE));

        mockMvc.perform(get("/api/rooms/" + existing.getRoomId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is(1)))
                .andExpect(jsonPath("$.data.roomNumber", is("A-103")));
    }

    @Test
    void testGetRoomById_NotFound() throws Exception {
        mockMvc.perform(get("/api/rooms/999999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status", is(4)));
    }

    @Test
    void testSetRoomToMaintenance_Success() throws Exception {
        Room existing = roomRepository.save(new Room(null, "A-104", RoomType.DELUXE, new BigDecimal("1500000.00"), 4, 3, RoomStatus.AVAILABLE));

        mockMvc.perform(delete("/api/rooms/" + existing.getRoomId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is(1)))
                .andExpect(jsonPath("$.data").doesNotExist());

        // Verify status is changed to MAINTENANCE
        mockMvc.perform(get("/api/rooms/" + existing.getRoomId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.status", is("MAINTENANCE")));
    }

    @Test
    void testGetRoomList_Success() throws Exception {
        roomRepository.save(new Room(null, "A-201", RoomType.SINGLE, new BigDecimal("400000.00"), 1, 2, RoomStatus.AVAILABLE));
        roomRepository.save(new Room(null, "A-202", RoomType.DOUBLE, new BigDecimal("700000.00"), 2, 2, RoomStatus.AVAILABLE));

        mockMvc.perform(get("/api/rooms?page=0&size=10"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is(1)))
                .andExpect(jsonPath("$.data.totalElements", is(2)))
                .andExpect(jsonPath("$.data.content", hasSize(2)));
    }

    @Test
    void testGetRoomList_InvalidPagination() throws Exception {
        mockMvc.perform(get("/api/rooms?page=-1&size=10"))
                .andExpect(status().isNotAcceptable())
                .andExpect(jsonPath("$.status", is(2)));

        mockMvc.perform(get("/api/rooms?page=0&size=101"))
                .andExpect(status().isNotAcceptable())
                .andExpect(jsonPath("$.status", is(2)));
    }
}
