package com.example.thymeleaf;

import com.example.thymeleaf.dto.CreateStudentDTO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;
import javax.validation.ValidatorFactory;
import java.time.LocalDate;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
class SpringThymeleafTemplateApplicationTests {
	private Validator validator;

	@Test
	void contextLoads() {
	}

	@BeforeEach
	public void setUp() {
		ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
		validator = factory.getValidator();
	}

	@Test
	void testCreateStudentDTOValidation_correctInput(){
		String name = "Alice";
		CreateStudentDTO student = new CreateStudentDTO();
		student.setName(name);
		student.setEmail("alice@example.com");
		student.setBirthday(LocalDate.of(2000, 1, 1));
		student.setZipCode("12345");
		student.setStreet("Main St");
		student.setNumber("123");
		student.setDistrict("Downtown");
		student.setCity("Springfield");
		student.setState("SP");

		validator.validate(student);

		Set<ConstraintViolation<CreateStudentDTO>> violations = validator.validate(student);
		assertTrue(violations.isEmpty(), "Object's data violates set rules: " + violations);
	}

	@Test
	void testCreateStudentDTOValidation_tryXSSOnNameInput() {
		String name = "<script>alert('xss!');</script>";
		CreateStudentDTO student = new CreateStudentDTO();
		student.setName(name);
		student.setEmail("alice@example.com");
		student.setBirthday(LocalDate.of(2000, 1, 1));
		student.setZipCode("12345");
		student.setStreet("Main St");
		student.setNumber("123");
		student.setDistrict("Downtown");
		student.setCity("Springfield");
		student.setState("SP");

		validator.validate(student);

		Set<ConstraintViolation<CreateStudentDTO>> violations = validator.validate(student);
		assertFalse(violations.isEmpty(), "Object's data violates set rules: " + violations);
	}

}
