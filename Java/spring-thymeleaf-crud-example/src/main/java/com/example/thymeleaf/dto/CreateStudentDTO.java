package com.example.thymeleaf.dto;

import com.example.thymeleaf.validation.OnlyDigits;
import com.example.thymeleaf.validation.ValidName;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;
import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@Builder(access = AccessLevel.PACKAGE)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class CreateStudentDTO {

    @ValidName
    @Size(max = 255, message = "{Size.maxText}")
    @NotBlank(message = "{NotEmpty.name}")
    private String name;

    @Email
    @Size(max = 255, message = "{Size.maxText}")
    @NotBlank(message = "{NotEmpty.email}")
    private String email;

    @NotNull(message = "{NotNull.birthday}")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private LocalDate birthday;

    @Pattern(regexp = "[0-9]{5}-[0-9]{3}", message = "{Pattern.zipCode}")
    @NotBlank(message = "{NotEmpty.zipCode}")
    private String zipCode;

    @Pattern(regexp = "[^<>\\p{Cc}]*", message = "{Pattern.address}")
    @Size(max = 255, message = "{Size.maxText}")
    @NotBlank(message = "{NotEmpty.street}")
    private String street;

    @OnlyDigits
    @Size(max = 255, message = "{Size.maxText}")
    @NotBlank(message = "{NotEmpty.number}")
    private String number;

    @Pattern(regexp = "[^<>\\p{Cc}]*", message = "{Pattern.address}")
    @Size(max = 255, message = "{Size.maxText}")
    private String complement;

    @Pattern(regexp = "[^<>\\p{Cc}]*", message = "{Pattern.address}")
    @Size(max = 255, message = "{Size.maxText}")
    @NotBlank(message = "{NotEmpty.district}")
    private String district;

    @ValidName
    @Size(max = 255, message = "{Size.maxText}")
    @NotBlank(message = "{NotEmpty.city}")
    private String city;

    @Pattern(regexp = "[A-Z]{2}", message = "{Pattern.state}")
    @NotBlank(message = "{NotEmpty.state}")
    private String state;

}
