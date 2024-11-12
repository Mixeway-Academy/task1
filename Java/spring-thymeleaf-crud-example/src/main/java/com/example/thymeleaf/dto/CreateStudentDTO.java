package com.example.thymeleaf.dto;

import lombok.Getter;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;
import java.time.LocalDate;

@Getter
@Setter
public class CreateStudentDTO {

    @NotEmpty(message = "{NotEmpty.name}")
    @Size(min = 1, max = 25, message = "{Size.name}")
    @Pattern(regexp = "^[A-Z][a-z]*$", message = "{Pattern.name}")
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
    @Pattern(regexp = "^[A-Za-z0-9]*$", message = "{Pattern.street}")
    private String street;

    @NotEmpty(message = "{NotEmpty.number}")
    @Pattern(regexp = "^[1-9][0-9]*$", message = "{Pattern.number}")
    private String number;

    @Pattern(regexp = "^[A-Za-z0-9]*$", message = "{Pattern.complement}")
    private String complement;

    @NotEmpty(message = "{NotEmpty.district}")
    @Pattern(regexp = "^[A-Za-z0-9]*$", message = "{Pattern.district}")
    private String district;

    @NotEmpty(message = "{NotEmpty.city}")
    @Pattern(regexp = "^[A-Za-z0-9]*$", message = "{Pattern.city}")
    private String city;

    @NotEmpty(message = "{NotEmpty.state}")
    @Pattern(regexp = "^[A-Za-z0-9]*$", message = "{Pattern.state}")
    private String state;

}
