package com.example.thymeleaf;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.validation.BeanPropertyBindingResult;
import org.springframework.validation.Errors;
import org.springframework.validation.Validator;

import com.example.thymeleaf.dto.CreateStudentDTO;

@SpringBootTest
class CreateStudentDtoTests {

    @Autowired
    private Validator validator;

    private String[] xss_input = {
        "';a=prompt,a()//",
        "'-eval(\"window['pro'%2B'mpt'](8)\")-'",
        "<image/src/onerror=prompt(8)>",
        "<svg onload=alert(1)>",
        "</script><svg onload=alert(1)>",
        "<rb onblur=alert(1) tabindex=1 id=x></rb><input autofocus>",
        "<dt onfocusout=alert(1) tabindex=1 id=x></dt><input autofocus>",
        "<div id=\"42\"><head><base href=\"javascript://\"/></head><body><a href=\"/. /,alert(42)//#\">XXX</a></body>//[\"'`-->]]>]</div>",
        "<style>@keyframes x{}</style><header style=\"animation-name:x\" onanimationstart=\"alert(1)\"></header>",
        "<nextid onmouseover=\"alert(1)\">test</nextid>",
        "<shadow onkeypress=\"alert(1)\" contenteditable>test</shadow>",
        "<tr onbeforepaste=\"alert(1)\" contenteditable>test</tr>",
        "<header onmousemove=\"alert(1)\">test</header>",
        "<nextid onmousemove=\"alert(1)\">test</nextid>",
        "<template onblur=alert(1) tabindex=1 id=x></template><input autofocus>",
        "<div draggable=\"true\" contenteditable>drag me</div><menu ondrop=alert(1) contenteditable>drop here</menu>",
        "<x contenteditable onkeyup=alert(1)>press any key! ",
        "<cite onkeyup=\"alert(1)\" contenteditable>test</cite>",
        "<area onclick=\"alert(1)\">test</area>",
        "<div draggable=\"true\" contenteditable>drag me</div><noscript ondragover=alert(1) contenteditable>drop here</noscript>",
        "<rp onmouseleave=\"alert(1)\">test</rp>",
        "<h1 id=x tabindex=1 onactivate=alert(1)></h1>",
        "<style>:target {color: red;}</style><area id=x style=\"transition:color 10s\" ontransitioncancel=alert(1)></area>",
        "<input onauxclick=alert(1)>",
        "<style>:target {color:red;}</style><area id=x style=\"transition:color 1s\" ontransitionend=alert(1)></area>",
    };

    private String[] full_names = {
        "Thomas Anderson",
        "Robert F. Kennedy Jr.",
        "Thomas Alva Edison"
        // "京房",
        // "東方",
        // "Günter Hermann"
    };
    private String[] emails = {
        "me@example.com",
        "thomas.anderson@metacortex.com",
        "name+tag@example.com",
        "\"spaces may be quoted\"@example.com"
    };
    private String[] zipCodes = {
        "00-621",
        "21384-200"
    };
    private String[] street_names = {
        "al. Jerzego Waszyngtona",
        "ul. Polna",
        "257th Ave"
    };
    private String[] building_numbers = {
        "21",
        "42B"
    };
    private String[] address_complements = {
        "Apartment 21",
        "Floor 10",
        "Next to the gas station"
    };
    private String[] districts = {
        // "Włochy",
        "Brooklyn",
        "Manhattan",
        "Friedrichshain-Kreuzberg"
    };
    private String[] cities = {
        "Berlin",
        "Warsaw",
        "New York"
        // "臺北"
    };
    private String[] states = {
        "New York",
        "Providence",
        "California",
        "Mazowieckie"
    };


    @Test
    void test_name_fails_xss() {
        for (String input : xss_input) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setName(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("name") > 0);
        }
    }

    @Test
    void test_email_fails_xss() {
        for (String input : xss_input) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setEmail(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("email") > 0);
        }
    }

    @Test
    void test_zipCode_fails_xss() {
        for (String input : xss_input) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setZipCode(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("zipCode") > 0);
        }
    }

    @Test
    void test_street_name_fails_xss() {
        for (String input : xss_input) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setStreet(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("street") > 0);
        }
    }

    @Test
    void test_building_number_fails_xss() {
        for (String input : xss_input) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setNumber(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("number") > 0);
        }
    }

    @Test
    void test_complement_fails_xss() {
        for (String input : xss_input) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setComplement(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("complement") > 0);
        }
    }

    @Test
    void test_district_fails_xss() {
        for (String input : xss_input) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setDistrict(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("district") > 0);
        }
    }

    @Test
    void test_city_fails_xss() {
        for (String input : xss_input) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setCity(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("city") > 0);
        }
    }

    @Test
    void test_state_fails_xss() {
        for (String input : xss_input) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setState(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("state") > 0);
        }
    }


    @Test
    void test_name_passes_valid_input() {
        for (String input : full_names) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setName(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("name") == 0, "Failed at '" + input + "'.");
        }
    }

    @Test
    void test_email_passes_valid_input() {
        for (String input : emails) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setEmail(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("email") == 0, "Failed at '" + input + "'.");
        }
    }

    @Test
    void test_zipCode_passes_valid_input() {
        for (String input : zipCodes) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setZipCode(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("zipCode") == 0, "Failed at '" + input + "'.");
        }
    }

    @Test
    void test_street_name_passes_valid_input() {
        for (String input : street_names) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setStreet(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("street") == 0, "Failed at '" + input + "'.");
        }
    }

    @Test
    void test_building_number_passes_valid_input() {
        for (String input : building_numbers) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setNumber(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("number") == 0, "Failed at '" + input + "'.");
        }
    }

    @Test
    void test_complement_passes_valid_input() {
        for (String input : address_complements) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setComplement(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("complement") == 0, "Failed at '" + input + "'.");
        }
    }

    @Test
    void test_district_passes_valid_input() {
        for (String input : districts) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setDistrict(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("district") == 0, "Failed at '" + input + "'.");
        }
    }

    @Test
    void test_city_passes_valid_input() {
        for (String input : cities) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setCity(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("city") == 0, "Failed at '" + input + "'.");
        }
    }

    @Test
    void test_state_passes_valid_input() {
        for (String input : states) {
            
            CreateStudentDTO dto = new CreateStudentDTO();
            Errors errors = new BeanPropertyBindingResult(dto, "dto");

            dto.setState(input);
            validator.validate(dto, errors);

            assertTrue(errors.getFieldErrorCount("state") == 0, "Failed at '" + input + "'.");
        }
    }
}
