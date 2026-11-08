package com.example.thymeleaf.validation;

import javax.validation.Constraint;
import javax.validation.Payload;
import javax.validation.ReportAsSingleViolation;
import javax.validation.constraints.Pattern;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.ElementType.FIELD;
import static java.lang.annotation.RetentionPolicy.RUNTIME;

@Target(FIELD)
@Retention(RUNTIME)
@Constraint(validatedBy = {})
@Pattern(regexp = "\\p{L}+")
@ReportAsSingleViolation
public @interface OnlyLetters {
    String message() default "{Pattern.letters}";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
