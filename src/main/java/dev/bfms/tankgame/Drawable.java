package dev.bfms.tankgame;

import javafx.scene.canvas.GraphicsContext;

public interface Drawable {
    void draw(GraphicsContext gc);
    void erase(GraphicsContext gc);
}
