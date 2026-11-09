package com.example.thymeleaf.validation;

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.ElementType.ANNOTATION_TYPE;
import static java.lang.annotation.ElementType.FIELD;
import static java.lang.annotation.ElementType.PARAMETER;
import static java.lang.annotation.RetentionPolicy.RUNTIME;

/**
 * Validates that a string contains no HTML meta-characters ('<' or '>').
 *
 * <p>These characters are required to open an HTML tag, so rejecting them at
 * the point where user input enters the application prevents stored XSS
 * payloads (e.g. {@code <script>alert('XSS')</script>}) from ever being
 * persisted.
 */
@Documented
@Constraint(validatedBy = NoHtmlValidator.class)
@Target({FIELD, PARAMETER, ANNOTATION_TYPE})
@Retention(RUNTIME)
public @interface NoHtml {

    String message() default "{Invalid.html}";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
