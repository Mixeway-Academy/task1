package com.example.thymeleaf.service;

import com.example.thymeleaf.entity.Address;
import com.example.thymeleaf.entity.Student;
import com.example.thymeleaf.repository.AddressRepository;
import com.example.thymeleaf.repository.StudentRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import static org.junit.jupiter.api.Assertions.*;
@ExtendWith(MockitoExtension.class)
class StudentServiceTest {

    @InjectMocks
    private StudentService studentService;
    @Mock
    private AddressRepository addressRepository;
    @Mock
    private StudentRepository studentRepository;

    @Test
    void save() {
        Address address = new Address();
        address.setId("120");
        address.setZipCode("11111-111");
        address.setStreet("Testowa");
        address.setNumber("1");
        address.setComplement("a");
        address.setDistrict("Testowy");
        address.setCity("Testowe");
        address.setState("Testowy");
        Student student = new Student();
        student.setAddress(address);
        student.setId("1");
        student.setName("Testowy");
        student.setEmail("test@test.org");
        boolean res = studentService.save(student);
        assertTrue(res);
    }

    @Test
    void saveNameXSS() {
        Address address = new Address();
        address.setId("120");
        address.setZipCode("11111-111");
        address.setStreet("Testowa");
        address.setNumber("1");
        address.setComplement("a");
        address.setDistrict("Testowy");
        address.setCity("Testowe");
        address.setState("Testowy");
        Student student = new Student();
        student.setAddress(address);
        student.setId("1");
        student.setName("<script>alert('name')</script>");
        student.setEmail("test@test.org");
        boolean res = studentService.save(student);
        assertFalse(res);
    }
}
