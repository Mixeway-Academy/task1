package com.example.thymeleaf.validation;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Unit tests for {@link NoHtmlValidator} in isolation, without a Spring or
 * Bean Validation runtime.
 */
class NoHtmlValidatorTest {

    private final NoHtmlValidator validator = new NoHtmlValidator();

    @Test
    void nullIsValid() {
        assertTrue(validator.isValid(null, null));
    }

    @ParameterizedTest
    @ValueSource(strings = {
            "",
            "John Doe",
            "john@example.com",
            "Main Street 10",
            "Warsaw",
            "a & b, 50% off"
    })
    void acceptsPlainText(String value) {
        assertTrue(validator.isValid(value, null));
    }

    @ParameterizedTest
    @ValueSource(strings = {
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "name <b>bold</b>",
            "open <tag",
            "close tag>"
    })
    void rejectsValuesContainingAngleBrackets(String value) {
        assertFalse(validator.isValid(value, null));
    }
}
