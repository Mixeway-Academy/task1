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
    @Pattern(regexp = "[a-zA-Z0-9]+", message = "Enter alphanumerical for name")
    @Size(max = 127, message = "Enter less than 127 signs")
    private String name;

    @Email
    @NotEmpty(message = "{NotEmpty.email}")
    @Size(max = 127, message = "Enter less than 127 signs")
    private String email;

    @NotNull(message = "{NotNull.birthday}")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private LocalDate birthday;

    @NotEmpty(message = "{NotEmpty.zipCode}")
    @Size(max = 127, message = "Enter less than 127 signs")
    @Pattern(regexp = "[0-9]+", message = "Enter correct zip code number")
    private String zipCode;

    @NotEmpty(message = "{NotEmpty.street}")
    @Size(max = 127, message = "Enter less than 127 signs")
    @Pattern(regexp = "[a-zA-Z0-9]+", message = "Enter alphanumerical for street")
    private String street;

    @NotEmpty(message = "{NotEmpty.number}")
    @Size(max = 127, message = "Enter less than 127 signs")
    @Pattern(regexp = "[0-9]+", message = "Enter correct number")
    private String number;

    @Pattern(regexp = "[a-zA-Z0-9]*", message = "Enter alphanumerical for complement")
    @Size(max = 127, message = "Enter less than 127 signs")
    private String complement;

    @NotEmpty(message = "{NotEmpty.district}")
    @Pattern(regexp = "[a-zA-Z0-9]+", message = "Enter alphanumerical for district")
    @Size(max = 127, message = "Enter less than 127 signs")
    private String district;

    @NotEmpty(message = "{NotEmpty.city}")
    @Pattern(regexp = "[a-zA-Z0-9]+", message = "Enter alphanumerical for city")
    @Size(max = 127, message = "Enter less than 127 signs")
    private String city;

    @NotEmpty(message = "{NotEmpty.state}")
    @Pattern(regexp = "[a-zA-Z0-9]+", message = "Enter alphanumerical for state")
    @Size(max = 127, message = "Enter less than 127 signs")
    private String state;

}
