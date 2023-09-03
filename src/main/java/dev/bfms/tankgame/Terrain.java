package dev.bfms.tankgame;


import javafx.scene.canvas.GraphicsContext;

public class Terrain implements Drawable{
    public int random(){
        int numero = (int)(Math.random()*(10+0+1)+0);
        return numero;
    }
    public int mountainRandom(int alto, int medio){
        int numero = (int)(Math.random()*((alto-10)+(medio+10)+1)+(medio+10));
        return numero;
    }

    public int[] rellenaArray(){
        int array[]=new int[11];
        int mountain1=random();
        int mountain2=random();
        while (mountain2==mountain1){
            mountain2=random();
        }
        for (int i=0;i<array.length;i++){
            if(mountain1==i){
                int posY=mountainRandom();
                array[i]=posY;
            }
            else{
                int posY=mountainRandom();
                array[i]=posY;
            }
        }
    }
    @Override
    public void draw(GraphicsContext gc) {

    }

    @Override
    public void erase(GraphicsContext gc) {

    }
}
