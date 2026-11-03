package com.example.thymeleaf.entity;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "address")
@EqualsAndHashCode(of = {"id"})
public class Address {

    @Id
    private String id;

    @Column(name = "zip_code")
    private String zipCode;

    private String street;
    private String number;
    private String complement;
    private String district;
    private String city;
    private String state;

    private String validateText(String value) {
        if (value != null && !value.trim().isEmpty()) {
            if (!value.matches("^[a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ\\s\\-'./]+$")) {
                throw new IllegalArgumentException("Nielegalne znaki");
            }
        }
        return value;
    }

    public void setStreet(String street) { this.street = validateText(street); }
    public void setNumber(String number) { this.number = validateText(number); }
    public void setComplement(String complement) { this.complement = validateText(complement); }
    public void setDistrict(String district) { this.district = validateText(district); }
    public void setCity(String city) { this.city = validateText(city); }
    public void setState(String state) { this.state = validateText(state); }


    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @OneToOne
    @JoinColumn(name = "fk_student")
    private Student student;

    @PrePersist
    private void prePersist() {
        this.id = UUID.randomUUID().toString();
        this.createdAt = LocalDateTime.now();
    }

    @PreUpdate
    private void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

}
