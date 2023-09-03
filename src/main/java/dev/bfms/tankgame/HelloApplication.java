package dev.bfms.tankgame;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

enum States {
    DONE,
    UNDONE,
    FAIL,
    DOING,
}

enum TypeOfCollision {
    SOIL,
    AIR,
    HIT,
}

public class HelloApplication extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(HelloApplication.class.getResource("hello-view.fxml"));
        Scene scene = new Scene(fxmlLoader.load(), 320, 240);
        stage.setTitle("Hello!");

    
        stage.show();
    }

    public static void main(String[] args) {
        var actualState = States.DONE;



        launch();
    }
}
