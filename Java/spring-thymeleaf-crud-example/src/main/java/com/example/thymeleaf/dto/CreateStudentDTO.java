package com.example.thymeleaf.dto;

import lombok.Getter;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import javax.validation.constraints.*;
import java.time.LocalDate;

@Getter
@Setter
public class CreateStudentDTO {

    @NotEmpty(message = "{NotEmpty.name}")
    @Pattern(
            regexp = "^[\\p{L} .'-]+$",
            message = "Invalid name format"
    )
    private String name;

    @Email
    @NotEmpty(message = "{NotEmpty.email}")
    private String email;

    @NotNull(message = "{NotNull.birthday}")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private LocalDate birthday;

    @NotEmpty(message = "{NotEmpty.zipCode}")
    @Pattern(
            regexp = "^\\d{5}-\\d{3}$",
            message = "Zip code must have format 00000-000"
    )
    private String zipCode;

    @NotEmpty(message = "{NotEmpty.street}")
    @Pattern(
            regexp = "^[\\p{L}\\p{N} .,'/\\-]+$",
            message = "Invalid street format"
    )
    private String street;

    @NotEmpty(message = "{NotEmpty.number}")
    @Pattern(
        regexp = "^[\\p{L}\\p{N}/-]+$",
        message = "Invalid building number"
    )
    private String number;

    @Pattern(
            regexp = "^[\\p{L}\\p{N} .,'/#\\-]*$",
            message = "Invalid complement format"
    )
    private String complement;

    @NotEmpty(message = "{NotEmpty.district}")
    @Pattern(
            regexp = "^[\\p{L}\\p{N} .'-]+$",
            message = "Invalid district format"
    )
    private String district;

    @NotEmpty(message = "{NotEmpty.city}")
    @Pattern(
            regexp = "^[\\p{L}\\p{N} .'-]+$",
            message = "Invalid city format"
    )
    private String city;

    @NotEmpty(message = "{NotEmpty.state}")
    @Pattern(
            regexp = "^(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)$",
            message = "Invalid Brazilian state code"
    )
    private String state;

}
