package com.example.thymeleaf.dto;

import lombok.Getter;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import javax.validation.constraints.*;
import java.time.LocalDate;

@Getter
@Setter
public class CreateStudentDTO {

    @MyCustomValidation(
            min = 2,
            max = 50,
            regexp = "^(?=.{2,50}$)[A-Za-z]+(?:[ '\\-][A-Za-z]+)*$"
    )
    private String name;

    @Email
    @NotEmpty(message = "{NotEmpty.email}")
    private String email;

    @NotNull(message = "{NotNull.birthday}")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    @PastOrPresent
    private LocalDate birthday;

    @MyCustomValidation(
            min = 9,
            max = 9,
            regexp = "^[0-9]{5}-[0-9]{3}$"
    )
    private String zipCode;

    @MyCustomValidation(
            min = 3,
            max = 80,
            regexp = "^(?=.{3,80}$)(?:\\p{L}+(?:['’]\\p{L}+)*\\.?|\\p{N}+)(?:[ -](?:\\p{L}+(?:['’]\\p{L}+)*\\.?|\\p{N}+))*$"
    )
    private String street;

    @MyCustomValidation(
            min = 1,
            max = 6,
            regexp = "^\\d{1,4}[A-Za-z]?(?:[/\\-]\\d{1,4}[A-Za-z]?)?$"
    )
    private String number;

    @MyCustomValidation(
            min = 1,
            max = 20,
            regexp = "^(?:(?:m|mieszk|mieszkanie|lok|lokal|apt|apartament)\\.?\\s*)?\\d{1,4}[A-Za-z]?$"
    )
    private String complement;

    @MyCustomValidation(
            min = 2,
            max = 60,
            regexp = "^(?=.{2,60}$)\\p{L}+(?:[ '\\-]\\p{L}+)*$"
    )
    private String district;

    @MyCustomValidation(regexp = "^(?=.{1,100}$)\\p{L}+(?:[ '\\-.]+\\p{L}+)*\\.?$")
    private String city;

    @MyCustomValidation(
            min = 3,
            max = 60,
            regexp = "^(?:województwo\\s+)?(?=.{3,40}$)\\p{L}+(?:[ \\-]\\p{L}+)*$"
    )
    private String state;

}
