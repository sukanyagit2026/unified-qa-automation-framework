package api;

import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeAll;

abstract class BaseApiTest {

    @BeforeAll
    static void configure() {
        RestAssured.baseURI = "https://automationintesting.online";
    }
}