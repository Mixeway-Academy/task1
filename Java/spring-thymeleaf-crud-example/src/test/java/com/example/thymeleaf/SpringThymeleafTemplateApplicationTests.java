package com.example.thymeleaf;

import com.example.thymeleaf.dto.CreateStudentDTO;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.LocalDate;
import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;
import javax.validation.ValidatorFactory;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
class SpringThymeleafTemplateApplicationTests {


	@Test
	void contextLoads() {
	}

	@Test
	void test_xss(){
		
		Validator validator =  ValidatorFactory.validation.buildDefaultValidatorFactory().getValidator();

		CreateStudentDTO student = CreateStudentDTO.builder();
			.Name("<script>alert('test')</script>")//xss
			.Email("test@test.com")
			.Birthday(LocalDate.now())
			.Street("test")
			.Number("11111")
			.District("test")
			.City("Warsaw")
			.ZipCode("11111")
			.State("PL")
			.build();

		validator.validate(student);

		Set<ConstraintViolation<CreateStudentDTO>> violations = validator.validate(student);

		assertFalse(violations.isEmpty(), violations); //prints violations
	}

	@Test
	void test_ok(){
		
		Validator validator =  ValidatorFactory.validation.buildDefaultValidatorFactory().getValidator();

		CreateStudentDTO student = CreateStudentDTO.builder();
			.Name("Alice")
			.Email("test@test.com")
			.Birthday(LocalDate.now())
			.Street("test")
			.Number("11111")
			.District("test")
			.City("Warsaw")
			.ZipCode("11111")
			.State("PL")
			.build();

		validator.validate(student);

		Set<ConstraintViolation<CreateStudentDTO>> violations = validator.validate(student);

		assertTrue(violations.isEmpty(), violations); //no errors
	}

}