package com.example.thymeleaf.dto;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;
import javax.validation.ValidatorFactory;
import javax.validation.constraints.*;
import java.time.LocalDate;
import java.util.Set;

import static org.assertj.core.api.Assertions.assertThat;

class CreateStudentDTOValidationTest {

    private static Validator validator;
    private CreateStudentDTO dto;

    @BeforeAll
    static void initValidator() {
        try (ValidatorFactory factory = Validation.buildDefaultValidatorFactory()) {
            validator = factory.getValidator();
        } catch (Exception ex) {
            System.err.println(ex.getMessage());
        }
    }

    @BeforeEach
    void setUp() {
        dto = new CreateStudentDTO();
        dto.setName("Jan Kowalski");
        dto.setEmail("jan@example.com");
        dto.setBirthday(LocalDate.of(1990, 1, 1));
        dto.setZipCode("00000-000");
        dto.setStreet("Main Street 10");
        dto.setNumber("12");
        dto.setComplement("m. 5");
        dto.setDistrict("Downtown");
        dto.setCity("Warsaw");
        dto.setState("Mazowieckie");
    }

    private static boolean failedOn(
            Set<ConstraintViolation<CreateStudentDTO>> vs,
            String field, Class<?> innerConstraint) {
        return vs.stream().anyMatch(v ->
                v.getPropertyPath().toString().equals(field)
                        && v.getConstraintDescriptor().getAnnotation()
                        .annotationType().equals(innerConstraint));
    }

    private static long countOn(
            Set<ConstraintViolation<CreateStudentDTO>> vs, String field) {
        return vs.stream()
                .filter(v -> v.getPropertyPath().toString().equals(field))
                .count();
    }

    @Test
    void baselineDto_isFullyValid() {
        assertThat(validator.validate(dto)).isEmpty();
    }

    @Nested
    class NameValidation {

        @Test
        void blank_failsNotBlankOnly() {
            dto.setName("");
            var vs = validator.validate(dto);
            assertThat(failedOn(vs, "name", NotBlank.class)).isTrue();
            assertThat(failedOn(vs, "name", Size.class)).isTrue();
            assertThat(failedOn(vs, "name", Pattern.class)).isTrue();
            assertThat(countOn(vs, "name")).isEqualTo(3);
        }

        @Test
        void tooShort_failsSizeOnly() {
            dto.setName("J");
            var vs = validator.validate(dto);
            assertThat(failedOn(vs, "name", NotBlank.class)).isFalse();
            assertThat(failedOn(vs, "name", Size.class)).isTrue();
            assertThat(failedOn(vs, "name", Pattern.class)).isTrue();
            assertThat(countOn(vs, "name")).isEqualTo(2);
        }

        @Test
        void withDigits_failsPatternOnly() {
            dto.setName("Jan123");
            var vs = validator.validate(dto);
            assertThat(failedOn(vs, "name", Pattern.class)).isTrue();
            assertThat(failedOn(vs, "name", Size.class)).isFalse();
            assertThat(failedOn(vs, "name", NotBlank.class)).isFalse();
            assertThat(countOn(vs, "name")).isEqualTo(1);
        }

        @Test
        void tooLong_failsSizeOnly() {
            dto.setName("A".repeat(51));
            var vs = validator.validate(dto);
            assertThat(failedOn(vs, "name", Size.class)).isTrue();
            assertThat(countOn(vs, "name")).isEqualTo(2);
        }

        @Test
        void null_failsNotBlankOnly() {
            dto.setName(null);
            var vs = validator.validate(dto);
            assertThat(failedOn(vs, "name", NotBlank.class)).isTrue();
            assertThat(countOn(vs, "name")).isEqualTo(1);
        }

        @ParameterizedTest
        @ValueSource(strings = {"Jan Kowalski", "O'Brien", "Smith-Jones", "Anna Maria"})
        void validFormats_pass(String name) {
            dto.setName(name);
            assertThat(countOn(validator.validate(dto), "name")).isZero();
        }
    }

    @Nested
    class EmailValidation {

        @Test
        void email_null_failsNotEmpty() {
            dto.setEmail(null);
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "email", NotEmpty.class)).isTrue();
            assertThat(countOn(vs, "email")).isEqualTo(1);
        }

        @Test
        void email_empty_failsNotEmpty() {
            dto.setEmail("");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "email", NotEmpty.class)).isTrue();
            assertThat(countOn(vs, "email")).isEqualTo(1);
        }

        @ParameterizedTest
        @ValueSource(strings = {
                "not-an-email",
                "foo@",
                "@bar.com",
                "foo bar@baz.com",
                "foo@@bar.com"
        })
        void email_invalidFormat_failsEmail(String email) {
            dto.setEmail(email);
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "email", Email.class)).isTrue();
        }

        @ParameterizedTest
        @ValueSource(strings = {
                "jan@example.com",
                "jan.kowalski@example.co.uk",
                "jan+test@example.org"
        })
        void email_validFormats_pass(String email) {
            dto.setEmail(email);
            assertThat(countOn(validator.validate(dto), "email")).isZero();
        }
    }

    @Nested
    class BirthdayValidation {

        @Test
        void null_failsNotNull() {
            dto.setBirthday(null);
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "birthday", NotNull.class)).isTrue();
            assertThat(countOn(vs, "birthday")).isEqualTo(1);
        }

        @Test
        void anyDate_passes() {
            dto.setBirthday(LocalDate.of(2000, 12, 31));
            assertThat(countOn(validator.validate(dto), "birthday")).isZero();
        }

        @Test
        void futureDate_fails() {
            dto.setBirthday(LocalDate.now().plusDays(1));
            assertThat(countOn(validator.validate(dto), "birthday")).isOne();
        }
    }

    @Nested
    class ZipCodeValidation {

        @Test
        void zipCode_null_failsNotBlank() {
            dto.setZipCode(null);
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "zipCode", NotBlank.class)).isTrue();
            assertThat(countOn(vs, "zipCode")).isEqualTo(1);
        }

        @Test
        void zipCode_empty_failsNotBlankSizePattern() {
            dto.setZipCode("");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "zipCode", NotBlank.class)).isTrue();
            assertThat(failedOn(vs, "zipCode", Size.class)).isTrue();
            assertThat(failedOn(vs, "zipCode", Pattern.class)).isTrue();
            assertThat(countOn(vs, "zipCode")).isEqualTo(3);
        }

        @Test
        void zipCode_validFormat_passes() {
            dto.setZipCode("12345-678");
            assertThat(countOn(validator.validate(dto), "zipCode")).isZero();
        }

        @Test
        void zipCode_tooShort_failsSizeOnly() {
            dto.setZipCode("1234-678");
            var vs = validator.validate(dto);
            assertThat(failedOn(vs, "zipCode", Size.class)).isTrue();
            assertThat(failedOn(vs, "zipCode", Pattern.class)).isTrue();
            assertThat(countOn(vs, "zipCode")).isEqualTo(2);
        }

        @Test
        void zipCode_tooLong_failsSizeAndPattern() {
            dto.setZipCode("12345-6789");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "zipCode", Size.class)).isTrue();
            assertThat(failedOn(vs, "zipCode", Pattern.class)).isTrue();
            assertThat(countOn(vs, "zipCode")).isEqualTo(2);
        }

        @Test
        void zipCode_correctLengthWrongFormat_failsPatternOnly() {
            dto.setZipCode("abcde-fgh");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "zipCode", Pattern.class)).isTrue();
            assertThat(failedOn(vs, "zipCode", Size.class)).isFalse();
            assertThat(countOn(vs, "zipCode")).isEqualTo(1);
        }
    }

    @Nested
    class StreetValidation {

        @ParameterizedTest
        @ValueSource(strings = {
                "Main Street 10",
                "123",
                "ul. Kowalska 10",
                "O'Brien 5",
                "Aleja 3 Maja"
        })
        void street_validFormats_pass(String street) {
            dto.setStreet(street);
            assertThat(countOn(validator.validate(dto), "street")).isZero();
        }

        @Test
        void street_null_failsNotBlank() {
            dto.setStreet(null);
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "street", NotBlank.class)).isTrue();
            assertThat(countOn(vs, "street")).isEqualTo(1);
        }

        @Test
        void street_tooShort_failsSizeAndPattern() {
            dto.setStreet("Ab");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "street", Size.class)).isTrue();
            assertThat(failedOn(vs, "street", Pattern.class)).isTrue();
            assertThat(countOn(vs, "street")).isEqualTo(2);
        }

        @Test
        void street_tooLong_failsSizeAndPattern() {
            dto.setStreet("A".repeat(81));
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "street", Size.class)).isTrue();
            assertThat(failedOn(vs, "street", Pattern.class)).isTrue();
        }

        @Test
        void street_withIllegalCharacter_failsPatternOnly() {
            dto.setStreet("Main St#");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "street", Pattern.class)).isTrue();
            assertThat(failedOn(vs, "street", Size.class)).isFalse();
            assertThat(countOn(vs, "street")).isEqualTo(1);
        }
    }

    @Nested
    class NumberValidation {

        @ParameterizedTest
        @ValueSource(strings = {"12", "12A", "12/34", "12-34", "1234", "1234A", "1234-5"})
        void number_validFormats_pass(String number) {
            dto.setNumber(number);
            assertThat(countOn(validator.validate(dto), "number")).isZero();
        }

        @Test
        void number_null_failsNotBlank() {
            dto.setNumber(null);
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "number", NotBlank.class)).isTrue();
            assertThat(countOn(vs, "number")).isEqualTo(1);
        }

        @Test
        void number_tooLong_failsSizeOnly() {
            dto.setNumber("1234567");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "number", Size.class)).isTrue();
            assertThat(failedOn(vs, "number", Pattern.class)).isTrue();
            assertThat(countOn(vs, "number")).isEqualTo(2);
        }

        @Test
        void number_correctLengthWrongFormat_failsPatternOnly() {
            dto.setNumber("12..34");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "number", Pattern.class)).isTrue();
            assertThat(failedOn(vs, "number", Size.class)).isFalse();
            assertThat(countOn(vs, "number")).isEqualTo(1);
        }

        @ParameterizedTest
        @ValueSource(strings = {"ABC", "12//34", "12--34"})
        void number_invalidFormats_failPattern(String number) {
            dto.setNumber(number);
            assertThat(failedOn(validator.validate(dto), "number", Pattern.class)).isTrue();
        }
    }

    @Nested
    class ComplementValidation {

        @ParameterizedTest
        @ValueSource(strings = {"12", "12A", "m. 5", "mieszk. 12", "apt 3", "lokal 12A"})
        void complement_validFormats_pass(String complement) {
            dto.setComplement(complement);
            assertThat(countOn(validator.validate(dto), "complement")).isZero();
        }

        @Test
        void complement_null_failsNotBlank() {
            dto.setComplement(null);
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "complement", NotBlank.class)).isTrue();
            assertThat(countOn(vs, "complement")).isEqualTo(1);
        }

        @Test
        void complement_withoutNumber_failsPatternOnly() {
            dto.setComplement("m.");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "complement", Pattern.class)).isTrue();
            assertThat(failedOn(vs, "complement", Size.class)).isFalse();
            assertThat(countOn(vs, "complement")).isEqualTo(1);
        }

        @Test
        void complement_tooLong_failsSizeAndPattern() {
            dto.setComplement("m. " + "1".repeat(25));
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "complement", Size.class)).isTrue();
            assertThat(failedOn(vs, "complement", Pattern.class)).isTrue();
            assertThat(countOn(vs, "complement")).isEqualTo(2);
        }
    }

    @Nested
    class DistrictValidation {

        @ParameterizedTest
        @ValueSource(strings = {"Downtown", "Old Town", "O'Brien", "Sródmieście"})
        void district_validFormats_pass(String district) {
            dto.setDistrict(district);
            assertThat(countOn(validator.validate(dto), "district")).isZero();
        }

        @Test
        void district_null_failsNotBlank() {
            dto.setDistrict(null);
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "district", NotBlank.class)).isTrue();
            assertThat(countOn(vs, "district")).isEqualTo(1);
        }

        @Test
        void district_tooShort_failsSizeAndPattern() {
            dto.setDistrict("A");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "district", Size.class)).isTrue();
            assertThat(failedOn(vs, "district", Pattern.class)).isTrue();
            assertThat(countOn(vs, "district")).isEqualTo(2);
        }

        @Test
        void district_tooLong_failsSizeAndPattern() {
            dto.setDistrict("A".repeat(61));
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "district", Size.class)).isTrue();
            assertThat(failedOn(vs, "district", Pattern.class)).isTrue();
            assertThat(countOn(vs, "district")).isEqualTo(2);
        }

        @Test
        void district_withDigit_failsPatternOnly() {
            dto.setDistrict("Downtown1");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "district", Pattern.class)).isTrue();
            assertThat(failedOn(vs, "district", Size.class)).isFalse();
            assertThat(countOn(vs, "district")).isEqualTo(1);
        }
    }

    @Nested
    class CityValidation {

        @ParameterizedTest
        @ValueSource(strings = {"Warsaw", "Nowy Sącz", "St. Louis", "Winston-Salem"})
        void city_validFormats_pass(String city) {
            dto.setCity(city);
            assertThat(countOn(validator.validate(dto), "city")).isZero();
        }

        @Test
        void city_empty_failsNotBlankAndPattern() {
            dto.setCity("");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "city", NotBlank.class)).isTrue();
            assertThat(failedOn(vs, "city", Pattern.class)).isTrue();
            assertThat(failedOn(vs, "city", Size.class)).isFalse();
            assertThat(countOn(vs, "city")).isEqualTo(2);
        }

        @Test
        void city_null_failsNotBlank() {
            dto.setCity(null);
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "city", NotBlank.class)).isTrue();
            assertThat(countOn(vs, "city")).isEqualTo(1);
        }

        @Test
        void city_withDigit_failsPatternOnly() {
            dto.setCity("Warsaw1");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "city", Pattern.class)).isTrue();
            assertThat(countOn(vs, "city")).isEqualTo(1);
        }

        @Test
        void city_tooLong_failsSizeAndPattern() {
            dto.setCity("A".repeat(101));
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "city", Size.class)).isTrue();
            assertThat(failedOn(vs, "city", Pattern.class)).isTrue();
            assertThat(countOn(vs, "city")).isEqualTo(2);
        }
    }

    @Nested
    class StateValidation {

        @ParameterizedTest
        @ValueSource(strings = {
                "Mazowieckie",
                "Greater Poland",
                "województwo mazowieckie"
        })
        void state_validFormats_pass(String state) {
            dto.setState(state);
            assertThat(countOn(validator.validate(dto), "state")).isZero();
        }

        @Test
        void state_null_failsNotBlank() {
            dto.setState(null);
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "state", NotBlank.class)).isTrue();
            assertThat(countOn(vs, "state")).isEqualTo(1);
        }

        @Test
        void state_tooShort_failsSizeAndPattern() {
            dto.setState("Ma");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "state", Size.class)).isTrue();
            assertThat(failedOn(vs, "state", Pattern.class)).isTrue();
            assertThat(countOn(vs, "state")).isEqualTo(2);
        }

        @Test
        void state_between41And60Chars_failsPatternOnly() {
            dto.setState("A".repeat(50));
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "state", Size.class)).isFalse();
            assertThat(failedOn(vs, "state", Pattern.class)).isTrue();
            assertThat(countOn(vs, "state")).isEqualTo(1);
        }

        @Test
        void state_tooLong_failsSizeAndPattern() {
            dto.setState("A".repeat(61));
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "state", Size.class)).isTrue();
            assertThat(failedOn(vs, "state", Pattern.class)).isTrue();
            assertThat(countOn(vs, "state")).isEqualTo(2);
        }

        @Test
        void state_withDigit_failsPatternOnly() {
            dto.setState("Mazowieckie1");
            var vs = validator.validate(dto);

            assertThat(failedOn(vs, "state", Pattern.class)).isTrue();
            assertThat(failedOn(vs, "state", Size.class)).isFalse();
            assertThat(countOn(vs, "state")).isEqualTo(1);
        }
    }
}
