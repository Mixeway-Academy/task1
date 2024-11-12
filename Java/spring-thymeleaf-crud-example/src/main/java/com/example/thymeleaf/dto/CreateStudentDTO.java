package com.example.thymeleaf.dto;

import lombok.Getter;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;

import java.time.LocalDate;

@Getter
@Setter
public class CreateStudentDTO {

    @NotBlank(message = "{NotEmpty.name}")
    @Pattern(
        regexp = "[- .\\w\\d]+", 
        flags = { Pattern.Flag.UNICODE_CASE, Pattern.Flag.CASE_INSENSITIVE }, 
        message="{Pattern.name}"
    )
    @Size(min = 4, max = 60, message = "{Size.name}")
    private String name;

    @Email
    @NotBlank(message = "{NotEmpty.email}")
    @Size(min = 5, max = 100, message = "{Size.email}")
    private String email;

    @NotNull(message = "{NotNull.birthday}")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private LocalDate birthday;

    @NotBlank(message = "{NotEmpty.zipCode}")
    @Pattern(
        regexp = "[- A-Za-z\\d\\[\\]]+",
        flags = { Pattern.Flag.CASE_INSENSITIVE },
        message = "{Pattern.zipCode}"
    )
    @Size(min = 1, max = 10, message = "{Size.zipCode}")
    private String zipCode;

    @NotBlank(message = "{NotEmpty.street}")
    @Pattern(
        regexp = "[- \\w.]+",
        flags = { Pattern.Flag.UNICODE_CASE, Pattern.Flag.CASE_INSENSITIVE },
        message = "{Pattern.street}"
    )
    @Size(min = 1, max = 50, message = "{Size.street}")
    private String street;

    @NotBlank(message = "{NotEmpty.number}")
    @Pattern(
        regexp = "[\\da-zA-Z]+",
        flags = { Pattern.Flag.CASE_INSENSITIVE },
        message = "{Pattern.number}"
    )
    @Size(min = 1, max = 10, message = "{Size.number}")
    private String number;

    @Pattern(
        regexp = "[-. \\w]*",
        flags = { Pattern.Flag.CASE_INSENSITIVE },
        message = "{Pattern.complement}"
    )
    @Size(min = 0, max = 50, message = "{Size.complement}")
    private String complement;

    @NotBlank(message = "{NotEmpty.district}")
    @Pattern(
        regexp = "[-. \\w]*",
        flags = { Pattern.Flag.UNICODE_CASE, Pattern.Flag.CASE_INSENSITIVE },
        message = "{Pattern.district}"
    )
    @Size(min = 0, max = 50, message = "{Size.district}")
    private String district;

    @NotBlank(message = "{NotEmpty.city}")
    @Pattern(
        regexp = "[-. \\w]*",
        flags = { Pattern.Flag.UNICODE_CASE, Pattern.Flag.CASE_INSENSITIVE },
        message = "{Pattern.city}"
    )
    @Size(min = 0, max = 50, message = "{Size.city}")
    private String city;

    @NotBlank(message = "{NotEmpty.state}")
    @Pattern(
        regexp = "[-. \\w]*",
        flags = { Pattern.Flag.UNICODE_CASE, Pattern.Flag.CASE_INSENSITIVE },
        message = "{Pattern.state}"
    )
    @Size(min = 0, max = 50, message = "{Size.state}")
    private String state;
}
