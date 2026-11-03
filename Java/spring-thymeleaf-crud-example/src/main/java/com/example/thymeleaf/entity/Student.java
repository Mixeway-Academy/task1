package com.example.thymeleaf.entity;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "student")
@EqualsAndHashCode(of = {"id"})
public class Student {

    @Id
    private String id;

    private String name;
    private String email;
    private LocalDate birthday;

    public void setName(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Pole nie może być puste");
        }
        if (!name.matches("^[a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ\\s\\-']+$")) {
            throw new IllegalArgumentException("Nielegalne znaki");
        }
        this.name = name;
    }

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @OneToOne(mappedBy = "student", cascade = CascadeType.ALL, orphanRemoval = true)
    private Address address;

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
