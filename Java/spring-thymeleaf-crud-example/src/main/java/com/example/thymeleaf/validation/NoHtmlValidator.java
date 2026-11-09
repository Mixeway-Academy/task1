package com.example.thymeleaf.validation;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

/**
 * Implementation of {@link NoHtml}. Treats {@code null} as valid so that
 * presence is governed by other constraints (e.g. {@code @NotEmpty}); a value
 * is rejected only when it contains '<' or '>'.
 */
public class NoHtmlValidator implements ConstraintValidator<NoHtml, String> {

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null) {
            return true;
        }
        return value.indexOf('<') < 0 && value.indexOf('>') < 0;
    }
}
