package com.example.thymeleaf;

import static javax.validation.Validation.buildDefaultValidatorFactory;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.Set;
import javax.validation.*;

import com.example.thymeleaf.dto.CreateStudentDTO;

public class StudentTests {

    private Validator validator;

    @BeforeEach
    void setup() {
        ValidatorFactory factory = buildDefaultValidatorFactory();
        validator = factory.getValidator();
    }

    @Test
    void testUnsafeName() {
        CreateStudentDTO dto = new CreateStudentDTO();
        dto.setName("><img src=x onerror=\"alert(' hacking ')\"><a hre=\"a");
        dto.setEmail("abc@example.com");
        dto.setBirthday(LocalDate.of(2000, 1, 1));
        dto.setZipCode("00-001");
        dto.setStreet("Main Street");
        dto.setNumber("10");
        dto.setDistrict("District");
        dto.setCity("Warszawa");
        dto.setState("Mazowieckie");

        Set<ConstraintViolation<CreateStudentDTO>> violations = validator.validate(dto);
        System.out.println(violations);

        assertFalse(violations.isEmpty());
    }

    @Test
    void testSafeName() {
        CreateStudentDTO dto = new CreateStudentDTO();
        dto.setName("Monika");
        dto.setEmail("abc@example.com");
        dto.setBirthday(LocalDate.of(2000, 1, 1));
        dto.setZipCode("00-001");
        dto.setStreet("Main Street");
        dto.setNumber("10");
        dto.setDistrict("District");
        dto.setCity("Warszawa");
        dto.setState("Mazowieckie");

        Set<ConstraintViolation<CreateStudentDTO>> violations = validator.validate(dto);

        assertTrue(violations.isEmpty());
    }

    @Test
    void testUnsafeStreet() {
        CreateStudentDTO dto = new CreateStudentDTO();
        dto.setName("monika");
        dto.setEmail("abc@example.com");
        dto.setStreet("javascript:alert('xss')");
        dto.setBirthday(LocalDate.of(2000, 1, 1));
        dto.setZipCode("00-001");
        dto.setNumber("10");
        dto.setDistrict("District");
        dto.setCity("Warszawa");
        dto.setState("Mazowieckie");
        Set<ConstraintViolation<CreateStudentDTO>> violations = validator.validate(dto);

        assertFalse(violations.isEmpty());
    }

}
