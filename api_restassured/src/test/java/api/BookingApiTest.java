package api;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

import io.restassured.http.ContentType;
import java.time.LocalDate;
import java.util.concurrent.ThreadLocalRandom;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class BookingApiTest extends BaseApiTest {

    private static String token;

    @BeforeAll
    static void login() {
        token = given()
            .contentType(ContentType.JSON)
            .body("{\"username\":\"admin\",\"password\":\"password\"}")
        .when()
            .post("/api/auth/login")
        .then()
            .statusCode(200)
            .extract().path("token");
    }

    @Test
    void bookingLifecycle_createReadDeleteAndConfirmGone() {
        LocalDate checkin = LocalDate.now().plusDays(60 + ThreadLocalRandom.current().nextInt(600));
        LocalDate checkout = checkin.plusDays(2);

        String body = "{"
            + "\"roomid\":1,"
            + "\"firstname\":\"Sukanya\","
            + "\"lastname\":\"Boopathirajan\","
            + "\"depositpaid\":false,"
            + "\"email\":\"sukanya.test@example.com\","
            + "\"phone\":\"89045678678\","
            + "\"bookingdates\":{\"checkin\":\"" + checkin + "\",\"checkout\":\"" + checkout + "\"}"
            + "}";

        int bookingId = given()
            .contentType(ContentType.JSON)
            .body(body)
        .when()
            .post("/api/booking")
        .then()
            .statusCode(201)
            .body("roomid", equalTo(1))
            .body("firstname", equalTo("Sukanya"))
            .body("bookingdates.checkin", equalTo(checkin.toString()))
            .body("bookingdates.checkout", equalTo(checkout.toString()))
            .extract().path("bookingid");

        given()
            .cookie("token", token)
        .when()
            .get("/api/booking/" + bookingId)
        .then()
            .statusCode(200)
            .body("bookingid", equalTo(bookingId))
            .body("lastname", equalTo("Boopathirajan"));

        given()
            .cookie("token", token)
        .when()
            .delete("/api/booking/" + bookingId)
        .then()
            .statusCode(202);

        given()
            .cookie("token", token)
        .when()
            .get("/api/booking/" + bookingId)
        .then()
            .statusCode(404);
    }
}