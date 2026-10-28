package fu.de190220.reservation;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients
public class DE190220ReservationServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(DE190220ReservationServiceApplication.class, args);
    }
}
