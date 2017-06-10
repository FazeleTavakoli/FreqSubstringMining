package com.company;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.*;
import java.io.*;
import java.lang.*;
import java.util.concurrent.locks.ReentrantLock;
import java.util.regex.Pattern;


public class Corpus  {


    private static File file = new File("/Users/fazeletavakoli/IdeaProjects/DataMiningFirstProject/Output.txt");
    public static void writeInFile(String fileInput) {
        BufferedWriter bw = null;
        try {
            FileWriter fw = new FileWriter(file, true);
            bw = new BufferedWriter(fw);
            bw.write(fileInput);
            bw.write("\r\n");
            System.out.println("File written Successfully");

        } catch (IOException ioe) {
            ioe.printStackTrace();
        } finally {
            try {
                if (bw != null)
                    bw.close();
            } catch (Exception ex) {
                System.out.println("Error in closing the BufferedWriter" + ex);
            }

        }
    }

    /*public  void writeInFile(String fileInput) {
        BufferedWriter bw = null;
        try {
            FileWriter fw = new FileWriter(file, true);
            bw = new BufferedWriter(fw);
            if (printedCounter == 0 && !fileInput.isEmpty()) {
                bw.write("$" + fileInput);
            }
            else if (printedCounter != 0 && !fileInput.isEmpty() && !fileInput.equals("\r\n") && !fileInput.equals("") )
                bw.write("*" + fileInput);
            else if (fileInput.equals("\r\n"))
                bw.write(fileInput);
            printedCounter += 1;
            //bw.write("\r\n");
            System.out.println("File written Successfully");

        } catch (IOException ioe) {
            ioe.printStackTrace();
        } finally {
            try {
                if (bw != null)
                    bw.close();
            } catch (Exception ex) {
                System.out.println("Error in closing the BufferedWriter" + ex);
            }

        }
    }*/




    public static void FileCleaner(){
        // empty the current content
        try {
            FileWriter fw = new FileWriter(file);
            fw.write("");
            fw.close();
        }catch(IOException ioe){
            ioe.printStackTrace();
        }
    }



}

