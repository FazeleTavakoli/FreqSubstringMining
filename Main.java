package com.company;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        // write your code here
        Corpus.FileCleaner();
        String filePath = "/Users/fazeletavakoli/IdeaProjects/DataMiningFirstProject/sequential-data.txt";
        int windowSize = 4;
        String mySubstring = "";
        FrequentSubStringMining frequentSubStringMining = new FrequentSubStringMining();
        try {
            String line = "";
            BufferedReader br = null;
            InputStream inputStream = new FileInputStream(filePath);
            br = new BufferedReader(new InputStreamReader(inputStream, "UTF-8"));
            while ((line = br.readLine()) != null) {
                String myInput = line.trim();
                for (int i=1; i<57; i++){
                    for(int j=0; j<myInput.length()-i; j++){
                        mySubstring = myInput.substring(j,j+i);

                        frequentSubStringMining.createFirstHash(mySubstring);
                        //Corpus.writeInFile(mySubstring);
                    }
                }
            }
        } catch (Exception e) {

        }
        frequentSubStringMining.getSubstringFreqHash();
        int userFreq = 0;
        System.out.println("Enter your desired frequency");
        Scanner scanner = new Scanner (System.in);
        userFreq = scanner.nextInt();
        frequentSubStringMining.substringFreqHashItrator(userFreq);
    }
}
