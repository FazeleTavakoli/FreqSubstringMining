package com.company;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Created by fazeletavakoli on 6/10/17.
 */
public class FrequentSubStringMining {
    private static ConcurrentHashMap<String,Integer> substringFreqHash = new ConcurrentHashMap<>();
    private Map<Integer,Set<String>> substringFreqHash_fixed = new HashMap<>();
    private int maxFreq = 0;

    public void createFirstHash(String s){
        //Map<String,Integer> substringFreqHash = new HashMap<>();

        if (!substringFreqHash.containsKey(s)) {
            substringFreqHash.put(s,1);
        }
        else{
            int i1 = substringFreqHash.get(s);
            substringFreqHash.put(s,i1+1);
        }
        int i2 = substringFreqHash.get(s);
        if (i2  > maxFreq)
            maxFreq = i2;
    }

    public Map<String,Integer> getSubstringFreqHash(){

        return substringFreqHash;
    }

    /*public void createSecondHash(){
        for (String s: substringFreqHash.keySet()){
            int frequency = substringFreqHash.get(s);
            for (String s1 : substringFreqHash.keySet()){
                if (substringFreqHash.get(s1).equals(frequency)){
                    if (substringFreqHash_fixed.containsKey(s1)){
                        int i1 = substringFreqHash_fixed.get(s1);
                        substringFreqHash_fixed.put()
                    }
                }
            }

        }
    }*/

    public void substringFreqHashItrator(int i){
        for(String s: substringFreqHash.keySet()){
            if (substringFreqHash.get(s).equals(i) || substringFreqHash.get(s) > i){
                Corpus.writeInFile(s);
            }
        }
    }

}
