package fu.de190220.reservation.service;

import fu.de190220.reservation.dto.ApiResponseDTO;
import fu.de190220.reservation.dto.ReservationDTO;
import org.springframework.data.domain.Pageable;

public interface ReservationService {

    ApiResponseDTO createReservation(ReservationDTO dto);

    ApiResponseDTO updateReservation(Long reservationId, ReservationDTO dto);

    ApiResponseDTO getReservationById(Long reservationId);

    ApiResponseDTO cancelReservation(Long reservationId);

    ApiResponseDTO getReservationList(String guestName, String status, Pageable pageable);
}
