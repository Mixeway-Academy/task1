package com.example.thymeleaf.dto;

import lombok.Getter;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;
// import org.springframework.web.util.HtmlUtils;
// import org.springframework.beans.factory.annotation.Required;
import org.hibernate.validator.constraints.SafeHtml;
// @Getter(AccessLevel.NONE)
// @Required
// public void setName(String name) {
//     this.name = HtmlUtils.htmlEscape(name);
// }
import javax.validation.constraints.Email;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import java.time.LocalDate;

@Getter
@Setter
public class CreateStudentDTO {

    @SafeHtml(WhiteListType.NONE, message = "HTML not allowed in input")
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

}
