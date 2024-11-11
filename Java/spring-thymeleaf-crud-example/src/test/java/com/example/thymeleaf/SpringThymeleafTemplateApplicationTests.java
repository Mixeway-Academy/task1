package com.example.thymeleaf;

import com.example.thymeleaf.dto.CreateStudentDTO;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.LocalDate;
import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;
import javax.validation.ValidatorFactory;
import java.time.format.DateTimeFormatter;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
class SpringThymeleafTemplateApplicationTests {

	@Test
	void contextLoads() {
	}

	@Test
	void should_not_create_student_when_name_is_invalid() {
		ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
		var validator = factory.getValidator();
		LocalDate date = LocalDate.of(2022, 1, 1);
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");

		CreateStudentDTO student =  new CreateStudentDTO();
				student.setBirthday(LocalDate.of(2022,1,21));
				student.setName("<script/>");
				student.setEmail("a@gmail.com");
				student.setCity("city");
				student.setNumber("123");
				student.setState("state");
				student.setZipCode("123456");

		validator.validate(student);

		Set<ConstraintViolation<CreateStudentDTO>> violations = validator.validate(student);

		assertFalse(violations.isEmpty());
	}

}
