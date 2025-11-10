package com.example.thymeleaf.dto;

import ch.qos.logback.core.net.SyslogOutputStream;
import lombok.Getter;
import lombok.Setter;
import org.springframework.context.annotation.Bean;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.validation.BindingResult;

import javax.validation.constraints.AssertFalse;
import javax.validation.constraints.AssertTrue;
import javax.validation.constraints.Email;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import java.time.LocalDate;

@Getter
@Setter
public class CreateStudentDTO {

    @NotEmpty(message = "{NotEmpty.name}")
    private String name;

    @Email
    @NotEmpty(message = "{NotEmpty.email}")
    private String email;

    @NotNull(message = "{NotNull.birthday}")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private LocalDate birthday;

    @NotEmpty(message = "{NotEmpty.zipCode}")
    private String zipCode;

    @NotEmpty(message = "{NotEmpty.street}")
    private String street;

    @NotEmpty(message = "{NotEmpty.number}")
    private String number;

    private String complement;

    @NotEmpty(message = "{NotEmpty.district}")
    private String district;

    @NotEmpty(message = "{NotEmpty.city}")
    private String city;

    @NotEmpty(message = "{NotEmpty.state}")
    private String state;

    // VALIDATE INPUT
    @AssertFalse(message = "Input contains unsafe or invalid content.")
    public boolean isUnsafeInput() {
        return isUnsafe(name) ||
                isUnsafe(email) ||
                isUnsafe(zipCode) ||
                isUnsafe(street) ||
                isUnsafe(number) ||
                isUnsafe(complement) ||
                isUnsafe(district) ||
                isUnsafe(city) ||
                isUnsafe(state);
    }

    private boolean isUnsafe(String value) {
        if (value == null) { return false; }

        String lower = value.toLowerCase();
        if (lower.contains("<") || lower.contains(">") ||
                lower.contains("script") || lower.contains("onerror") ||
                lower.contains("onload") || lower.contains("javascript:")) {

            return true;
        } else {
            return false;
        }
    }

}
