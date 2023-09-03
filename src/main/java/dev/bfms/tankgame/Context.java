package dev.bfms.tankgame;

import javafx.scene.canvas.GraphicsContext;

public class Context {
    private static Context instance = null;

    private GraphicsContext gc;

    private Context() {}

    public static Context getInstance() {
        if (instance == null) {
            instance = new Context();
        }
        return instance;
    }

    public GraphicsContext getGraphicContext() {
        return gc;
    }

    public void setGraphicsContext(GraphicsContext gc) {
        this.gc = gc;
    }
}
