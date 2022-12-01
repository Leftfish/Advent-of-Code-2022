package aoc;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;

public class Day01 {
public static void main(String[] args) throws IOException {
    String path = System.getProperty("user.dir");
    File file = new File(path + "\\src\\aoc\\input01");
    BufferedReader br = new BufferedReader(new FileReader(file));
    
    ArrayList<Integer> elves = new ArrayList<Integer>();
    int elf = 0;
    
    while (br.ready()) {
        String s = br.readLine();
        if (!s.isEmpty()) {
        int calories = Integer.parseInt(s);
        elf += calories;
        }
        else {
            elves.add(elf);
            elf = 0;
        }
    }
    Collections.sort(elves);
    Collections.reverse(elves);
    int topElves = 0;
    for (int i = 0; i < 3; i++) {
        topElves += elves.get(i);
    }
    System.out.println("Top elf: " + elves.get(0));
    System.out.println("Top 3 elves: " + topElves);
    }
}
