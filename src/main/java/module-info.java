module dev.bfms.tankgame {
    requires javafx.controls;
    requires javafx.fxml;


    opens dev.bfms.tankgame to javafx.fxml;
    exports dev.bfms.tankgame;
}