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
@Pattern(regexp = "[0-9]+")
@ReportAsSingleViolation
public @interface OnlyDigits {
    String message() default "{Pattern.number}";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
