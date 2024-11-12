package com.example.thymeleaf.service;

import com.example.thymeleaf.entity.Address;
import com.example.thymeleaf.entity.Student;
import com.example.thymeleaf.repository.AddressRepository;
import com.example.thymeleaf.repository.StudentRepository;
import lombok.AllArgsConstructor;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import org.apache.commons.lang3.BooleanUtils;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
@AllArgsConstructor
public class StudentService {

    private AddressRepository addressRepository;
    private StudentRepository studentRepository;

    // 1. Name: Allows letters (including Polish letters), spaces, apostrophes, and hyphens.
    public static final String NAME_REGEX = "^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ'\\-\\s]{1,50}$";
    // 2. Email: Basic email pattern
    public static final String EMAIL_REGEX = "^((?!\\.)[\\w-_.]*[^.])(@\\w+)(\\.\\w+(\\.\\w+)?[^.\\W])$";
    // 3. Street: Allows letters (including Polish letters), numbers, spaces length between 1 and 100
    public static final String STREET_REGEX = "^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9'\\-\\s]{1,100}$";
    // 4. Number: Allows numeric values with optional letters.
    public static final String NUMBER_REGEX = "^[0-9]{1,5}[A-Za-z0-9\\-]{0,5}$";

    // 5. Complement: Optional field that allows letters, numbers, spaces, apostrophes, and hyphens.
    public static final String COMPLEMENT_REGEX = "^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9'\\-\\s]{0,50}$";

    // 6. District: Allows letters (including Polish letters), numbers, spaces, and punctuation, length between 1 and 50
    public static final String DISTRICT_REGEX = "^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9'\\-\\s]{1,50}$";

    // 7. City: Allows letters (including Polish letters) and spaces, length between 1 and 50
    public static final String CITY_REGEX = "^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\\s]{1,50}$";

    // 8. State : Matches full names of voivodeships/states (case-insensitive).
    public static final String STATE_REGEX = "^[a-zA-Z\\s\\-\\.,']{1,100}$";
    // 9. ZIP Code: Matches multiple international ZIP code formats.
    // - (\\d{2}-?\\d{3}) matches Polish ZIP codes like "12-345" or "12345".
    public static final String ZIP_CODE_REGEX = "^(\\d{5}-?\\d{3})$";

    public Student findById(String id) {
        return this.studentRepository.findById(id).orElseThrow();
    }

    public boolean save(Student student) {
        if (validateStudent(student)) {
            this.studentRepository.save(student);
            this.addressRepository.save(student.getAddress());
            return true;
        }
        return false;
    }

    public boolean update(String id, Student student) {
        if (validateStudent(student)) {
            Student studentDatabase = this.findById(id);
            BeanUtils.copyProperties(student, studentDatabase, "id", "createdAt", "updatedAt", "address");
            BeanUtils.copyProperties(student.getAddress(), studentDatabase.getAddress(), "id", "createdAt", "updatedAt", "student");
            this.studentRepository.save(studentDatabase);
            return true;
        }
        return false;
    }
    public boolean validateAddress(Address address) {

        boolean isZipCodeSafe = isInputSafe(address.getZipCode()) && validateInput(address.getZipCode(), ZIP_CODE_REGEX);
        boolean isStreetSafe = isInputSafe(address.getStreet()) && validateInput(address.getStreet(), STREET_REGEX);
        boolean isNumberSafe = isInputSafe(address.getNumber()) && validateInput(address.getNumber(), NUMBER_REGEX);
        boolean isComplementSafe = isInputSafe(address.getComplement()) && validateInput(address.getComplement(), COMPLEMENT_REGEX);
        boolean isDistrictSafe = isInputSafe(address.getDistrict()) && validateInput(address.getDistrict(), DISTRICT_REGEX);
        boolean isCitySafe = isInputSafe(address.getCity()) && validateInput(address.getCity(), CITY_REGEX);
        boolean isStateSafe = isInputSafe(address.getState()) && validateInput(address.getState(), STATE_REGEX);
        return BooleanUtils.and(new boolean[] {isZipCodeSafe, isStreetSafe, isNumberSafe, isComplementSafe,
                isDistrictSafe, isCitySafe, isStateSafe});
    }
    public boolean validateStudent(Student student) {
        boolean isNameSafe = isInputSafe(student.getName()) && validateInput(student.getName(), NAME_REGEX);
        boolean isEmailSafe = isInputSafe(student.getEmail()) && validateInput(student.getEmail(), EMAIL_REGEX);
        boolean isAddressSafe = validateAddress(student.getAddress());
        return BooleanUtils.and(new boolean[] {isNameSafe, isEmailSafe, isAddressSafe});
    }
    public boolean validateInput(String input, String pattern) {
        Pattern compiledPattern = Pattern.compile(pattern);
        Matcher matcher = compiledPattern.matcher(input);

        return matcher.matches();
    }
    public static boolean isInputSafe(String input) {
        if (input == null) {
            return true;
        }
        String[] xssPatterns = {
                "<script>", "</script>", "javascript:", "onload=", "onerror=", "<img", "<iframe"
        };
        String lowerCaseInput = input.toLowerCase();
        for (String pattern : xssPatterns) {
            if (lowerCaseInput.contains(pattern)) {
                return false;
            }
        }
        return true;
    }
    public void deleteById(String id) {
        this.studentRepository.delete(this.findById(id));
    }

}
