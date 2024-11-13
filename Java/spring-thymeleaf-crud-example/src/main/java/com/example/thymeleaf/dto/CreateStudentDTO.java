package com.example.thymeleaf.dto;

import java.time.LocalDate;
import javax.validation.constraints.Email;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

@Getter
@Setter
public class CreateStudentDTO {

    @NotNull
    @NotEmpty(message = "{NotEmpty.name}")
    @Size(min = 2, max = 50)
    @Pattern(
        regexp = "^[a-zA-Z\\s]{2,50}$",
        message = "Name must be 2-50 characters long and contain only letters"
    )
    private String name;

    @NotNull
    @NotEmpty(message = "{NotEmpty.email}")
    @Size(max = 100, message = "Email must not exceed 100 characters")
    @Email(regexp = "^[A-Za-z0-9+_.-]+@(.+)$", message = "Invalid email format")
    private String email;

    @NotNull(message = "{NotNull.birthday}")
    @Past(message = "Birthday must be in the past")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private LocalDate birthday;

    @NotNull
    @NotEmpty(message = "{NotEmpty.zipCode}")
    @Size(min = 8, max = 9)
    @Pattern(
        regexp = "^\\d{5}-?\\d{3}$",
        message = "ZIP code must be in format 12345-678"
    )
    private String zipCode;

    @NotNull
    @NotEmpty(message = "{NotEmpty.street}")
    @Size(
        min = 3,
        max = 100,
        message = "Street must be between 3 and 100 characters"
    )
    @Pattern(
        regexp = "^[a-zA-Z0-9\\s]{3,100}$",
        message = "Street must contain only letters, numbers and spaces"
    )
    private String street;

    @NotNull
    @NotEmpty(message = "{NotEmpty.number}")
    @Size(min = 1, max = 5)
    @Pattern(
        regexp = "^[0-9]{1,5}$",
        message = "House number must be between 1 and 5 digits"
    )
    private String number;

    @Size(max = 50, message = "Complement must not exceed 50 characters")
    private String complement;

    @NotNull
    @NotEmpty(message = "{NotEmpty.district}")
    @Size(
        min = 2,
        max = 50,
        message = "District must be between 2 and 50 characters"
    )
    @Pattern(
        regexp = "^[a-zA-Z0-9\\s]{2,50}$",
        message = "District must contain only letters, numbers and spaces"
    )
    private String district;

    @NotNull
    @NotEmpty(message = "{NotEmpty.city}")
    @Size(min = 2, max = 50)
    @Pattern(
        regexp = "^[a-zA-Z\\s]{2,50}$",
        message = "City must be 2-50 characters long and contain only letters"
    )
    private String city;

    @NotNull
    @NotEmpty(message = "{NotEmpty.state}")
    @Size(min = 2, max = 2)
    @Pattern(regexp = "^[A-Z]{2}$", message = "State must be 2 capital letters")
    private String state;
}
