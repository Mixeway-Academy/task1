package com.example.thymeleaf.dto;

import javax.validation.Constraint;
import javax.validation.OverridesAttribute;
import javax.validation.Payload;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@NotBlank(message = "{NotBlank.name}")
@Size(message = "{Size.name}")
@Pattern(regexp = ".*", message = "{Pattern.name}")
@Target({ElementType.FIELD, ElementType.PARAMETER, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = {})
public @interface MyCustomValidation {

    String message() default "{MyCustomValidation.default}";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};

    @OverridesAttribute(constraint = Size.class, name = "min")
    int min() default 0;

    @OverridesAttribute(constraint = Size.class, name = "max")
    int max() default 100;

    @OverridesAttribute(constraint = Pattern.class, name = "regexp")
    String regexp() default ".*";
}
