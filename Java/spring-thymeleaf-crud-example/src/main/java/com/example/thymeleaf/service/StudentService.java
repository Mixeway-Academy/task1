package com.example.thymeleaf.service;

import com.example.thymeleaf.entity.Student;
import com.example.thymeleaf.repository.AddressRepository;
import com.example.thymeleaf.repository.StudentRepository;

import com.example.thymeleaf.util.SanitizerUtil;
import lombok.AllArgsConstructor;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;

import java.util.regex.Pattern;

@Service
@AllArgsConstructor
public class StudentService {

    private AddressRepository addressRepository;
    private StudentRepository studentRepository;

    public Student findById(String id) {
        return this.studentRepository.findById(id).orElseThrow();
    }

    public Student save(Student student) {
        // Sanitize and validate fields in Student and Address
        sanitizeAndValidateStudent(student);

        // Save sanitized student and address
        this.studentRepository.save(student);
        this.addressRepository.save(student.getAddress());
        return student;
    }

    public Student update(String id, Student student) {
        Student studentDatabase = this.findById(id);

        // Sanitize and validate fields in Student and Address
        sanitizeAndValidateStudent(student);

        // Copy sanitized and validated properties
        BeanUtils.copyProperties(student, studentDatabase, "id", "createdAt", "updatedAt", "address");
        BeanUtils.copyProperties(student.getAddress(), studentDatabase.getAddress(), "id", "createdAt", "updatedAt", "student");

        return this.studentRepository.save(studentDatabase);
    }

    public void deleteById(String id) {
        this.studentRepository.delete(this.findById(id));
    }

    // Method to sanitize and validate fields in Student and Address entities
    private void sanitizeAndValidateStudent(Student student) {
        if (student != null) {
            // Sanitize fields
            student.setName(SanitizerUtil.sanitize(student.getName()));
            student.setEmail(SanitizerUtil.sanitize(student.getEmail()));

            if (student.getAddress() != null) {
                student.getAddress().setStreet(SanitizerUtil.sanitize(student.getAddress().getStreet()));
                student.getAddress().setCity(SanitizerUtil.sanitize(student.getAddress().getCity()));
            }

            // Validate fields
            validateStudentFields(student);
        }
    }

    // Method to validate student fields using regex
    private void validateStudentFields(Student student) {
        // Validate Name: only alphabets and spaces allowed
        if (!Pattern.matches("^[a-zA-Z\\s]+$", student.getName())) {
            throw new IllegalArgumentException("Invalid name: only alphabets and spaces are allowed.");
        }

        // Validate Email: must follow standard email format
        if (!Pattern.matches("^[\\w.%+-]+@[\\w.-]+\\.[a-zA-Z]{2,6}$", student.getEmail())) {
            throw new IllegalArgumentException("Invalid email format.");
        }

        if (student.getAddress() != null) {
            // Validate Address Street: alphanumeric and spaces only
            if (!Pattern.matches("^[a-zA-Z0-9\\s,.-]+$", student.getAddress().getStreet())) {
                throw new IllegalArgumentException("Invalid address street: only alphanumeric characters and ,.- are allowed.");
            }

            // Validate Address City: only alphabets and spaces allowed
            if (!Pattern.matches("^[a-zA-Z\\s]+$", student.getAddress().getCity())) {
                throw new IllegalArgumentException("Invalid city name: only alphabets and spaces are allowed.");
            }
        }
    }
}
