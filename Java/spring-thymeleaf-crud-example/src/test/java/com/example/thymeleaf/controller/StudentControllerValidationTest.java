package com.example.thymeleaf.controller;

import com.example.thymeleaf.repository.StudentRepository;
import com.example.thymeleaf.service.StudentService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.model;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

/**
 * Tests the /students/new endpoint together with the Bean Validation rules
 * on {@link com.example.thymeleaf.dto.CreateStudentDTO}, which reject the
 * HTML meta-characters used in XSS payloads.
 */
@WebMvcTest(StudentController.class)
class StudentControllerValidationTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private StudentService studentService;

    @MockBean
    private StudentRepository studentRepository;

    @Test
    void rejectsXssPayloadInNameAndDoesNotPersist() throws Exception {
        mockMvc.perform(post("/students/new")
                        .param("name", "<script>alert('XSS')</script>")
                        .param("email", "john@example.com")
                        .param("birthday", "2000-01-01")
                        .param("zipCode", "00000-000")
                        .param("street", "Main Street")
                        .param("number", "10")
                        .param("district", "Center")
                        .param("city", "Warsaw")
                        .param("state", "MZ"))
                // validation fails -> form is redisplayed, no redirect
                .andExpect(status().isOk())
                .andExpect(view().name("new-student"))
                .andExpect(model().attributeHasFieldErrors("student", "name"));

        // the malicious payload must never reach the persistence layer
        verify(studentService, never()).save(any());
    }

    @Test
    void acceptsCleanInputAndPersists() throws Exception {
        mockMvc.perform(post("/students/new")
                        .param("name", "John Doe")
                        .param("email", "john@example.com")
                        .param("birthday", "2000-01-01")
                        .param("zipCode", "00000-000")
                        .param("street", "Main Street")
                        .param("number", "10")
                        .param("district", "Center")
                        .param("city", "Warsaw")
                        .param("state", "MZ"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/students"));

        verify(studentService).save(any());
    }
}
