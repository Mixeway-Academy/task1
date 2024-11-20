package com.example.thymeleaf.util;

import org.owasp.html.HtmlPolicyBuilder;
import org.owasp.html.PolicyFactory;

public class SanitizerUtil {
    // Define allowed HTML elements (e.g., allowing basic formatting elements)
    private static final PolicyFactory POLICY = new HtmlPolicyBuilder()
            .allowElements("b", "i", "u", "p") // specify allowed HTML elements
            .toFactory();

    public static String sanitize(String input) {
        return input == null ? null : POLICY.sanitize(input);
    }
}
