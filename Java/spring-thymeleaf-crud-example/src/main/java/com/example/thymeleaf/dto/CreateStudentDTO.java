package com.example.thymeleaf.dto;

import com.example.thymeleaf.validation.NoHtml;
import lombok.Getter;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import java.time.LocalDate;

@Getter
@Setter
public class CreateStudentDTO {

    @NotEmpty(message = "{NotEmpty.name}")
    @NoHtml
    private String name;

    @Email
    @NotEmpty(message = "{NotEmpty.email}")
    @NoHtml
    private String email;

    @NotNull(message = "{NotNull.birthday}")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private LocalDate birthday;

    @NotEmpty(message = "{NotEmpty.zipCode}")
    @NoHtml
    private String zipCode;

    @NotEmpty(message = "{NotEmpty.street}")
    @NoHtml
    private String street;

    @NotEmpty(message = "{NotEmpty.number}")
    @NoHtml
    private String number;

    @NoHtml
    private String complement;

    @NotEmpty(message = "{NotEmpty.district}")
    @NoHtml
    private String district;

    @NotEmpty(message = "{NotEmpty.city}")
    @NoHtml
    private String city;

    @NotEmpty(message = "{NotEmpty.state}")
    @NoHtml
    private String state;

}
