package api;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

import io.restassured.http.ContentType;
import org.junit.jupiter.api.Test;

class AuthApiTest extends BaseApiTest {

    private static final String VALID_LOGIN = "{\"username\":\"admin\",\"password\":\"password\"}";
    private static final String WRONG_PASSWORD = "{\"username\":\"admin\",\"password\":\"wrongpassword\"}";

    @Test
    void loginWithValidCredentialsReturnsToken() {
        given()
            .contentType(ContentType.JSON)
            .body(VALID_LOGIN)
        .when()
            .post("/api/auth/login")
        .then()
            .statusCode(200)
            .body("token", not(emptyOrNullString()));
    }

    @Test
    void loginWithWrongPasswordIsRejected() {
        given()
            .contentType(ContentType.JSON)
            .body(WRONG_PASSWORD)
        .when()
            .post("/api/auth/login")
        .then()
            .statusCode(401)
            .body("error", equalTo("Invalid credentials"))
            .body("token", nullValue());
    }

    @Test
    void freshTokenIsAcceptedByValidateEndpoint() {
        String token = given()
            .contentType(ContentType.JSON)
            .body(VALID_LOGIN)
        .when()
            .post("/api/auth/login")
        .then()
            .statusCode(200)
            .extract().path("token");

        given()
            .contentType(ContentType.JSON)
            .body("{\"token\":\"" + token + "\"}")
        .when()
            .post("/api/auth/validate")
        .then()
            .statusCode(200);
    }
}