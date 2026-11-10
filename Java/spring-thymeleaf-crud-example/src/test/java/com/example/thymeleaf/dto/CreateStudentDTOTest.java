package com.example.thymeleaf.dto;

import org.junit.jupiter.api.Test;
import javax.validation.Validation;
import javax.validation.Validator;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

class CreateStudentDTOTest {

    private final Validator validator =
            Validation.buildDefaultValidatorFactory().getValidator();

    @Test
    void shouldAcceptValidData() {
        CreateStudentDTO dto = createValidStudent();

        assertTrue(validator.validate(dto).isEmpty());
    }

    @Test
    void shouldRejectXSS() {
        CreateStudentDTO dto = createValidStudent();

        String xss = "<script>alert(1)</script>";

        dto.setName(xss);
        dto.setEmail(xss);
        dto.setZipCode(xss);
        dto.setStreet(xss);
        dto.setNumber(xss);
        dto.setComplement(xss);
        dto.setDistrict(xss);
        dto.setCity(xss);
        dto.setState(xss);

        assertEquals(9, validator.validate(dto).stream()
                .map(v -> v.getPropertyPath().toString())
                .distinct()
                .count());
    }

    private CreateStudentDTO createValidStudent() {
        CreateStudentDTO dto = new CreateStudentDTO();

        dto.setName("Jan Kowalski");
        dto.setEmail("jan@example.com");
        dto.setBirthday(LocalDate.of(2000, 1, 1));
        dto.setZipCode("01310-100");
        dto.setStreet("Rua Paulista");
        dto.setNumber("123");
        dto.setComplement("Apto 12");
        dto.setDistrict("Centro");
        dto.setCity("Sao Paulo");
        dto.setState("SP");

        return dto;
    }
}