package aoc;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;

public class Day02 {
    public static void main(String[] args) throws IOException {
        String path = System.getProperty("user.dir");
        File file = new File(path + "\\src\\aoc\\input02");
        BufferedReader br = new BufferedReader(new FileReader(file));

        HashMap<String, Integer> scoringRound1 = new HashMap<String, Integer>();
        scoringRound1.put("A X", 4);
        scoringRound1.put("A Y", 8);
        scoringRound1.put("A Z", 3);
        scoringRound1.put("B X", 1);
        scoringRound1.put("B Y", 5);
        scoringRound1.put("B Z", 9);
        scoringRound1.put("C X", 7);
        scoringRound1.put("C Y", 2);
        scoringRound1.put("C Z", 6);
        
        HashMap<String, Integer> scoringRound2 = new HashMap<String, Integer>();
        scoringRound2.put("A X", 3);
        scoringRound2.put("A Y", 4);
        scoringRound2.put("A Z", 8);
        scoringRound2.put("B X", 1);
        scoringRound2.put("B Y", 5);
        scoringRound2.put("B Z", 9);
        scoringRound2.put("C X", 2);
        scoringRound2.put("C Y", 6);
        scoringRound2.put("C Z", 7);
        
        int scoreRound1 = 0;
        int scoreRound2 = 0;
        
        while (br.ready()) {
            String line = br.readLine();
            scoreRound1 += scoringRound1.get(line);
            scoreRound2 += scoringRound2.get(line);
            }
        System.out.printf("Round one: %d Round two: %d", scoreRound1, scoreRound2);
        }
    }
