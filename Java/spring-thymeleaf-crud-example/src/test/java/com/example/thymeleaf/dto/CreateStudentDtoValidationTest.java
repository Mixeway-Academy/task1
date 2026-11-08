package com.example.thymeleaf.dto;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.springframework.context.support.ResourceBundleMessageSource;
import org.springframework.validation.beanvalidation.LocalValidatorFactoryBean;

import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;

class CreateStudentDtoValidationTest {

    private static LocalValidatorFactoryBean validator;

    @BeforeAll
    static void setUp() {
        ResourceBundleMessageSource messages = new ResourceBundleMessageSource();
        messages.setBasename("messages");
        validator = new LocalValidatorFactoryBean();
        validator.setValidationMessageSource(messages);
        validator.afterPropertiesSet();
    }

    @AfterAll
    static void tearDown() {
        validator.close();
    }

    @Test
    void shouldAcceptValidStudent() {
        // given
        CreateStudentDTO dto = validStudentBuilder().build();

        // when
        var violations = validator.validate(dto);

        // then
        assertThat(violations).isEmpty();
    }

    @Test
    void shouldRejectScriptPayloadInName() {
        // given
        CreateStudentDTO dto = validStudentBuilder()
                .name("<script>alert('XSS wykonany')</script>")
                .build();

        // when
        var violations = validator.validate(dto);

        // then
        assertThat(violations).singleElement().satisfies(violation -> {
            assertThat(violation.getPropertyPath()).hasToString("name");
            assertThat(violation.getMessage()).isEqualTo("Must contain only letters");
        });
    }

    @Test
    void shouldRejectImgPayloadInStreet() {
        // given
        CreateStudentDTO dto = validStudentBuilder()
                .street("<img src=\"https://i.imgur.com/wBIGztj.png\" onload=\"alert('Mike Wazowski')\">")
                .build();

        // when
        var violations = validator.validate(dto);

        // then
        assertThat(violations).singleElement().satisfies(violation -> {
            assertThat(violation.getPropertyPath()).hasToString("street");
            assertThat(violation.getMessage()).isEqualTo("Must not contain <, > or control characters");
        });
    }

    @ParameterizedTest
    @ValueSource(strings = {
            "<script>alert('XSS wykonany')</script>",
            "<img src=\"https://i.imgur.com/wBIGztj.png\" onload=\"alert('Mike Wazowski')\">"
    })
    void shouldRejectXssInAllTextFields(String payload) {
        // given
        CreateStudentDTO dto = validStudentBuilder()
                .name(payload)
                .email(payload)
                .zipCode(payload)
                .street(payload)
                .number(payload)
                .complement(payload)
                .district(payload)
                .city(payload)
                .state(payload)
                .build();

        // when
        var violations = validator.validate(dto);

        // then
        assertThat(violations)
                .extracting(violation -> violation.getPropertyPath().toString())
                .containsExactlyInAnyOrder("name", "email", "zipCode", "street", "number",
                        "complement", "district", "city", "state");
    }

    @Test
    void shouldRejectLettersInNumber() {
        // given
        CreateStudentDTO dto = validStudentBuilder().number("12A").build();

        // when
        var violations = validator.validate(dto);

        // then
        assertThat(violations).singleElement().satisfies(violation -> {
            assertThat(violation.getPropertyPath()).hasToString("number");
            assertThat(violation.getMessage()).isEqualTo("Must contain only digits (0-9)");
        });
    }

    @Test
    void shouldRejectTooLongStreetWithResolvedMessage() {
        // given
        CreateStudentDTO dto = validStudentBuilder().street("a".repeat(256)).build();

        // when
        var violations = validator.validate(dto);

        // then
        assertThat(violations).singleElement().satisfies(violation -> {
            assertThat(violation.getPropertyPath()).hasToString("street");
            assertThat(violation.getMessage()).isEqualTo("Must contain at most 255 characters");
        });
    }

    private CreateStudentDTO.CreateStudentDTOBuilder validStudentBuilder() {
        return CreateStudentDTO.builder()
                .name("Łukasz")
                .email("jan@example.com")
                .birthday(LocalDate.of(2000, 1, 1))
                .zipCode("12345-678")
                .street("ul. Świętego Jana 12/3")
                .number("12")
                .complement("")
                .district("Centro")
                .city("Kraków")
                .state("SP");
    }
}
