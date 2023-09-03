package dev.bfms.tankgame;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.HBox;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import java.io.IOException;


public class GameMain extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        AnchorPane root = new AnchorPane();
        Scene scene = new Scene(root, Constants.WINDOWS_WIDTH, Constants.WINDOWS_HEIGHT);

        Canvas canvas = new Canvas(Constants.WINDOWS_WIDTH, Constants.WINDOWS_HEIGHT);

        Context.getInstance().setGraphicsContext(canvas.getGraphicsContext2D());

        var ctx = canvas.getGraphicsContext2D();
        ctx.setFill(Color.LAVENDER);
        ctx.fillRect(20, 20,Constants.WINDOWS_WIDTH-20, Constants.WINDOWS_HEIGHT-20);


        root.getChildren().add(canvas);
        scene.setRoot(root);
        stage.setScene(scene);
        stage.setResizable(false);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
