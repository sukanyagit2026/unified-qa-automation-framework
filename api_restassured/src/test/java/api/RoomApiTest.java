package api;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

import org.junit.jupiter.api.Test;

class RoomApiTest extends BaseApiTest {

    @Test
    void getAllRoomsReturnsNonEmptyList() {
        given()
        .when()
            .get("/api/room")
        .then()
            .statusCode(200)
            .time(lessThan(5000L))
            .body("rooms", not(empty()))
            .body("rooms.roomid", everyItem(notNullValue()))
            .body("rooms.roomPrice", everyItem(greaterThan(0)));
    }

    @Test
    void getRoomByIdReturnsRoom() {
        given()
        .when()
            .get("/api/room/1")
        .then()
            .statusCode(200)
            .body("roomid", equalTo(1))
            .body("roomName", notNullValue())
            .body("roomPrice", greaterThan(0));
    }
}